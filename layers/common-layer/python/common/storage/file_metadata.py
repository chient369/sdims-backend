"""
File Metadata Model

This module defines the FileMetadata model used to store metadata
about files in the application.
"""

import os
import datetime
import mimetypes
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field

from common.models.base import BaseModel


@dataclass
class FileMetadata(BaseModel):
    """
    Model class for file metadata
    
    This class represents metadata about a file stored in the system.
    It is used to track file information in DynamoDB.
    """
    # Required fields
    id: str                         # Unique identifier for the file
    original_filename: str          # Original name of the file
    file_path: str                  # Storage path/key
    
    # Optional fields with defaults
    file_type: str = ""             # MIME type
    file_size: int = 0              # Size in bytes 
    entity_type: str = ""           # Type of entity this file is related to (e.g., contract, employee)
    entity_id: str = ""             # ID of the related entity
    description: str = ""           # Description of the file
    uploaded_by_id: str = ""        # ID of the user who uploaded the file
    upload_date: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    is_public: bool = False         # Whether the file is publicly accessible
    is_active: bool = True          # Whether the file is active
    version: int = 1                # File version
    tags: List[str] = field(default_factory=list)  # Tags for the file
    custom_metadata: Dict[str, Any] = field(default_factory=dict)  # Additional custom metadata

    @classmethod
    def create_from_upload(cls, 
                         file_id: str, 
                         filename: str, 
                         file_path: str, 
                         file_size: int,
                         entity_type: str = "", 
                         entity_id: str = "",
                         description: str = "",
                         uploaded_by_id: str = "",
                         is_public: bool = False,
                         tags: Optional[List[str]] = None,
                         custom_metadata: Optional[Dict[str, Any]] = None) -> 'FileMetadata':
        """
        Create a FileMetadata instance from an uploaded file
        
        Args:
            file_id: Unique identifier for the file
            filename: Original filename
            file_path: Storage path/key
            file_size: Size in bytes
            entity_type: Type of entity this file is related to
            entity_id: ID of the related entity
            description: Description of the file
            uploaded_by_id: ID of the user who uploaded the file
            is_public: Whether the file is publicly accessible
            tags: Tags for the file
            custom_metadata: Additional custom metadata
            
        Returns:
            FileMetadata instance
        """
        # Determine MIME type from filename
        file_type, _ = mimetypes.guess_type(filename)
        if not file_type:
            # Default to binary if type cannot be determined
            file_type = "application/octet-stream"
            
        return cls(
            id=file_id,
            original_filename=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            uploaded_by_id=uploaded_by_id,
            is_public=is_public,
            tags=tags or [],
            custom_metadata=custom_metadata or {}
        )
    
    @property
    def extension(self) -> str:
        """Get the file extension"""
        _, ext = os.path.splitext(self.original_filename)
        return ext.lower()
    
    @property
    def filename_without_extension(self) -> str:
        """Get the filename without extension"""
        base, _ = os.path.splitext(self.original_filename)
        return base
    
    @property
    def is_image(self) -> bool:
        """Check if the file is an image"""
        return self.file_type and self.file_type.startswith('image/')
    
    @property
    def is_document(self) -> bool:
        """Check if the file is a document"""
        doc_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'text/plain'
        ]
        return self.file_type in doc_types
    
    def to_storage_metadata(self) -> Dict[str, str]:
        """
        Convert to storage metadata format
        
        Returns a dictionary suitable for storage as metadata in S3 or similar
        
        Returns:
            Dictionary of metadata
        """
        # S3 and similar services only support string metadata
        metadata = {
            'file_id': self.id,
            'original_filename': self.original_filename,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'description': self.description,
            'uploaded_by': self.uploaded_by_id,
            'upload_date': self.upload_date,
            'is_public': str(self.is_public).lower(),
            'version': str(self.version)
        }
        
        # Include tags if any
        if self.tags:
            metadata['tags'] = ','.join(self.tags)
            
        # Add custom metadata (only string values)
        for key, value in self.custom_metadata.items():
            if isinstance(value, (str, int, float, bool)):
                metadata[f'custom_{key}'] = str(value)
                
        return metadata
    
    @classmethod
    def from_storage_metadata(cls, 
                            file_id: str, 
                            file_path: str, 
                            file_size: int,
                            file_type: str,
                            metadata: Dict[str, str]) -> 'FileMetadata':
        """
        Create FileMetadata from storage metadata
        
        Args:
            file_id: File ID
            file_path: Storage path/key
            file_size: File size in bytes
            file_type: MIME type
            metadata: Metadata from storage
            
        Returns:
            FileMetadata instance
        """
        # Extract basic metadata
        original_filename = metadata.get('original_filename', os.path.basename(file_path))
        entity_type = metadata.get('entity_type', '')
        entity_id = metadata.get('entity_id', '')
        description = metadata.get('description', '')
        uploaded_by_id = metadata.get('uploaded_by', '')
        upload_date = metadata.get('upload_date', datetime.datetime.now().isoformat())
        is_public = metadata.get('is_public', 'false').lower() == 'true'
        version = int(metadata.get('version', '1'))
        
        # Extract tags
        tags = []
        if 'tags' in metadata:
            tags = metadata['tags'].split(',')
            
        # Extract custom metadata
        custom_metadata = {}
        for key, value in metadata.items():
            if key.startswith('custom_'):
                custom_key = key[7:]  # Remove 'custom_' prefix
                custom_metadata[custom_key] = value
                
        return cls(
            id=file_id,
            original_filename=original_filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            uploaded_by_id=uploaded_by_id,
            upload_date=upload_date,
            is_public=is_public,
            version=version,
            tags=tags,
            custom_metadata=custom_metadata
        ) 