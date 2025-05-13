"""
Storage Provider Interface

This module defines the interface for storage providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, BinaryIO, Tuple


class StorageProvider(ABC):
    """
    Abstract class defining the interface for storage providers.
    All storage implementations should implement this interface.
    """

    @abstractmethod
    def upload(self, 
               file_data: Union[bytes, BinaryIO], 
               key: str, 
               content_type: Optional[str] = None,
               metadata: Optional[Dict[str, str]] = None) -> str:
        """
        Upload file data to storage
        
        Args:
            file_data: The file data as bytes or file-like object
            key: The storage key/path where the file will be stored
            content_type: The content type (MIME type) of the file
            metadata: Additional metadata to associate with the file
            
        Returns:
            The storage key where the file was stored
            
        Raises:
            StorageUploadError: If upload fails
            StoragePermissionError: If permission is denied
            StorageFileSizeError: If file size exceeds limits
            StorageFileTypeError: If file type is not allowed
        """
        pass
    
    @abstractmethod
    def download(self, key: str) -> bytes:
        """
        Download file from storage
        
        Args:
            key: The storage key/path of the file
            
        Returns:
            The file data as bytes
            
        Raises:
            StorageDownloadError: If download fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Delete file from storage
        
        Args:
            key: The storage key/path of the file
            
        Returns:
            True if file was deleted, False otherwise
            
        Raises:
            StorageDeleteError: If deletion fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        pass
    
    @abstractmethod
    def list(self, prefix: str = "", delimiter: str = "", max_keys: int = 1000) -> List[Dict[str, Any]]:
        """
        List files in storage
        
        Args:
            prefix: Prefix to filter files
            delimiter: Delimiter for hierarchical listing
            max_keys: Maximum number of keys to return
            
        Returns:
            List of file information dictionaries
            
        Raises:
            StorageError: If listing fails
            StoragePermissionError: If permission is denied
        """
        pass
    
    @abstractmethod
    def get_metadata(self, key: str) -> Dict[str, Any]:
        """
        Get metadata for a file
        
        Args:
            key: The storage key/path of the file
            
        Returns:
            Dictionary of metadata
            
        Raises:
            StorageError: If operation fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        pass
    
    @abstractmethod
    def update_metadata(self, key: str, metadata: Dict[str, str]) -> Dict[str, Any]:
        """
        Update metadata for a file
        
        Args:
            key: The storage key/path of the file
            metadata: Metadata to update
            
        Returns:
            Updated metadata dictionary
            
        Raises:
            StorageError: If operation fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        pass
    
    @abstractmethod
    def get_presigned_url(self, 
                          key: str, 
                          expires_in: int = 3600, 
                          response_content_type: Optional[str] = None,
                          response_content_disposition: Optional[str] = None) -> str:
        """
        Generate a pre-signed URL for direct access to a file
        
        Args:
            key: The storage key/path of the file
            expires_in: Expiration time in seconds
            response_content_type: Override content type in response
            response_content_disposition: Override content disposition in response
            
        Returns:
            Pre-signed URL for direct access
            
        Raises:
            StorageError: If generation fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        pass
    
    @abstractmethod
    def get_upload_url(self, 
                       key: str, 
                       expires_in: int = 3600,
                       content_type: Optional[str] = None,
                       metadata: Optional[Dict[str, str]] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a pre-signed URL for direct upload
        
        Args:
            key: The storage key/path where the file will be stored
            expires_in: Expiration time in seconds
            content_type: Content type of the file to be uploaded
            metadata: Additional metadata for the file
            
        Returns:
            Tuple of (pre-signed URL, additional fields required for upload)
            
        Raises:
            StorageError: If generation fails
            StoragePermissionError: If permission is denied
        """
        pass
    
    @staticmethod
    @abstractmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename to be safe for storage
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        pass
    
    @abstractmethod
    def file_exists(self, key: str) -> bool:
        """
        Check if a file exists in storage
        
        Args:
            key: The storage key/path of the file
            
        Returns:
            True if file exists, False otherwise
        """
        pass
    
    @abstractmethod
    def copy(self, source_key: str, destination_key: str, metadata: Optional[Dict[str, str]] = None) -> str:
        """
        Copy a file within the storage
        
        Args:
            source_key: Source storage key/path
            destination_key: Destination storage key/path
            metadata: Optional new metadata to apply
            
        Returns:
            The destination key
            
        Raises:
            StorageError: If copy fails
            StorageFileNotFoundError: If source file is not found
            StoragePermissionError: If permission is denied
        """
        pass 