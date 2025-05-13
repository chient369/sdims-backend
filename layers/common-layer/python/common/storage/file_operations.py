"""
File Operations Utilities

This module provides utilities for file operations like
MIME type detection, file validation, name sanitization, etc.
"""

import os
import re
import uuid
import mimetypes
import hashlib
from typing import Dict, List, Set, Tuple, Optional, BinaryIO, Union
from io import BytesIO
import magic
from PIL import Image

from common.storage.exceptions import StorageFileTypeError, StorageFileSizeError


class FileOperations:
    """
    Utility class for file operations
    """
    
    # Default allowed MIME types
    DEFAULT_ALLOWED_MIME_TYPES = {
        # Images
        'image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/webp',
        # Documents
        'application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'text/plain', 'text/csv',
        # Archives
        'application/zip', 'application/x-rar-compressed',
        # Others
        'application/json', 'text/xml', 'application/xml'
    }
    
    # Default allowed file extensions
    DEFAULT_ALLOWED_EXTENSIONS = {
        # Images
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
        # Documents
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv',
        # Archives
        '.zip', '.rar',
        # Others
        '.json', '.xml'
    }
    
    # Default maximum file size (10MB)
    DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def detect_mime_type(file_data: Union[bytes, BinaryIO], filename: Optional[str] = None) -> str:
        """
        Detect MIME type of a file using python-magic and mimetypes
        
        Args:
            file_data: The file data as bytes or file-like object
            filename: Optional filename to help with detection
                
        Returns:
            MIME type string
        """
        # Ensure we have a bytes buffer
        if hasattr(file_data, 'read'):
            # Reset file position if it supports seeking
            if hasattr(file_data, 'seek'):
                current_pos = file_data.tell()
                file_data.seek(0)
                
            # Read a chunk for magic detection
            data_chunk = file_data.read(2048)
            
            # Reset file position if it supports seeking
            if hasattr(file_data, 'seek'):
                file_data.seek(current_pos)
        else:
            # Use the first 2048 bytes for detection
            data_chunk = file_data[:2048] if len(file_data) > 2048 else file_data
            
        # Use magic to detect MIME type from content
        mime_type = magic.from_buffer(data_chunk, mime=True)
        
        # If magic returns a generic type and filename is provided, try mimetypes
        if mime_type == 'application/octet-stream' and filename:
            guessed_type, _ = mimetypes.guess_type(filename)
            if guessed_type:
                mime_type = guessed_type
                
        return mime_type
    
    @staticmethod
    def validate_file_type(file_data: Union[bytes, BinaryIO], 
                         filename: Optional[str] = None, 
                         allowed_mime_types: Optional[Set[str]] = None,
                         allowed_extensions: Optional[Set[str]] = None) -> str:
        """
        Validate file type against allowed types
        
        Args:
            file_data: The file data as bytes or file-like object
            filename: Optional filename to help with detection
            allowed_mime_types: Set of allowed MIME types
            allowed_extensions: Set of allowed file extensions
                
        Returns:
            Detected MIME type if valid
                
        Raises:
            StorageFileTypeError: If file type is not allowed
        """
        # Use defaults if not provided
        allowed_mime_types = allowed_mime_types or FileOperations.DEFAULT_ALLOWED_MIME_TYPES
        allowed_extensions = allowed_extensions or FileOperations.DEFAULT_ALLOWED_EXTENSIONS
        
        # Get detected MIME type
        mime_type = FileOperations.detect_mime_type(file_data, filename)
        
        # Check MIME type
        if mime_type not in allowed_mime_types:
            raise StorageFileTypeError(f"File type '{mime_type}' is not allowed")
            
        # Check extension if filename is provided
        if filename:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            if ext not in allowed_extensions:
                raise StorageFileTypeError(f"File extension '{ext}' is not allowed")
                
        return mime_type
    
    @staticmethod
    def validate_file_size(file_data: Union[bytes, BinaryIO], max_size: Optional[int] = None) -> int:
        """
        Validate file size against maximum allowed size
        
        Args:
            file_data: The file data as bytes or file-like object
            max_size: Maximum allowed size in bytes
                
        Returns:
            File size in bytes if valid
                
        Raises:
            StorageFileSizeError: If file size exceeds maximum
        """
        # Use default if not provided
        max_size = max_size or FileOperations.DEFAULT_MAX_FILE_SIZE
        
        # Get file size
        if hasattr(file_data, 'seek') and hasattr(file_data, 'tell'):
            # For file-like objects that support seeking
            current_pos = file_data.tell()
            file_data.seek(0, os.SEEK_END)
            file_size = file_data.tell()
            file_data.seek(current_pos)
        elif hasattr(file_data, 'getbuffer'):
            # For BytesIO
            file_size = len(file_data.getbuffer())
        else:
            # For bytes
            file_size = len(file_data)
            
        # Check size
        if file_size > max_size:
            raise StorageFileSizeError(
                f"File size {file_size} bytes exceeds maximum allowed size {max_size} bytes"
            )
            
        return file_size
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename to be safe for storage
        
        Args:
            filename: Original filename
                
        Returns:
            Sanitized filename
        """
        # Remove any path components
        filename = os.path.basename(filename)
        
        # Replace problematic characters
        filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Replace multiple consecutive underscores with a single one
        filename = re.sub(r'_+', '_', filename)
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        # Ensure it's not empty
        if not filename:
            filename = 'unnamed_file'
            
        # Limit length (max 255 characters)
        if len(filename) > 255:
            base, ext = os.path.splitext(filename)
            filename = base[:255 - len(ext)] + ext
            
        return filename
    
    @staticmethod
    def generate_unique_filename(original_filename: str, add_uuid: bool = True) -> str:
        """
        Generate a unique filename
        
        Args:
            original_filename: Original filename
            add_uuid: Whether to add a UUID to the filename
                
        Returns:
            Unique sanitized filename
        """
        # First sanitize the filename
        safe_filename = FileOperations.sanitize_filename(original_filename)
        
        if add_uuid:
            # Split filename and extension
            base, ext = os.path.splitext(safe_filename)
            
            # Add UUID
            uuid_str = str(uuid.uuid4())
            unique_filename = f"{base}_{uuid_str[:8]}{ext}"
        else:
            # Add timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Split filename and extension
            base, ext = os.path.splitext(safe_filename)
            
            unique_filename = f"{base}_{timestamp}{ext}"
            
        return unique_filename
    
    @staticmethod
    def get_file_hash(file_data: Union[bytes, BinaryIO], algorithm: str = 'sha256') -> str:
        """
        Calculate hash of file data
        
        Args:
            file_data: The file data as bytes or file-like object
            algorithm: Hash algorithm to use
                
        Returns:
            Hex digest of hash
        """
        # Choose hash algorithm
        if algorithm.lower() == 'md5':
            hash_obj = hashlib.md5()
        elif algorithm.lower() == 'sha1':
            hash_obj = hashlib.sha1()
        elif algorithm.lower() == 'sha256':
            hash_obj = hashlib.sha256()
        elif algorithm.lower() == 'sha512':
            hash_obj = hashlib.sha512()
        else:
            hash_obj = hashlib.sha256()
            
        # Update hash with file data
        if hasattr(file_data, 'read'):
            # For file-like objects
            if hasattr(file_data, 'seek'):
                current_pos = file_data.tell()
                file_data.seek(0)
                
            chunk = file_data.read(8192)
            while chunk:
                hash_obj.update(chunk)
                chunk = file_data.read(8192)
                
            if hasattr(file_data, 'seek'):
                file_data.seek(current_pos)
        else:
            # For bytes
            hash_obj.update(file_data)
            
        return hash_obj.hexdigest()
    
    @staticmethod
    def process_image(image_data: Union[bytes, BinaryIO], 
                    max_width: Optional[int] = None,
                    max_height: Optional[int] = None,
                    quality: int = 85,
                    output_format: str = 'JPEG') -> BytesIO:
        """
        Process an image (resize, optimize)
        
        Args:
            image_data: The image data as bytes or file-like object
            max_width: Maximum width of the image
            max_height: Maximum height of the image
            quality: Output quality (0-100, for JPEG)
            output_format: Output format ('JPEG', 'PNG', etc.)
                
        Returns:
            BytesIO object containing the processed image
                
        Raises:
            ValueError: If image cannot be processed
        """
        try:
            # Ensure we're working with a BytesIO object
            if isinstance(image_data, bytes):
                image_file = BytesIO(image_data)
            else:
                # Create a copy of the file-like object
                if hasattr(image_data, 'seek'):
                    current_pos = image_data.tell()
                    image_data.seek(0)
                    
                image_file = BytesIO(image_data.read())
                
                if hasattr(image_data, 'seek'):
                    image_data.seek(current_pos)
                    
            # Open the image
            img = Image.open(image_file)
            
            # Resize if needed
            if max_width or max_height:
                original_width, original_height = img.size
                
                # Calculate new dimensions
                if max_width and max_height:
                    # Both dimensions specified, maintain aspect ratio within limits
                    width_ratio = max_width / original_width
                    height_ratio = max_height / original_height
                    ratio = min(width_ratio, height_ratio)
                    new_width = int(original_width * ratio)
                    new_height = int(original_height * ratio)
                elif max_width:
                    # Only width specified
                    ratio = max_width / original_width
                    new_width = max_width
                    new_height = int(original_height * ratio)
                else:
                    # Only height specified
                    ratio = max_height / original_height
                    new_width = int(original_width * ratio)
                    new_height = max_height
                    
                # Resize only if necessary
                if new_width < original_width or new_height < original_height:
                    img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Save to BytesIO
            output = BytesIO()
            
            # Handle different formats
            if output_format.upper() == 'JPEG':
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output, format='JPEG', quality=quality, optimize=True)
            elif output_format.upper() == 'PNG':
                img.save(output, format='PNG', optimize=True)
            elif output_format.upper() == 'WEBP':
                img.save(output, format='WEBP', quality=quality)
            else:
                img.save(output, format=output_format)
                
            # Reset BytesIO position
            output.seek(0)
            
            return output
        except Exception as e:
            raise ValueError(f"Image processing failed: {str(e)}")
    
    @staticmethod
    def create_thumbnail(image_data: Union[bytes, BinaryIO], 
                       width: int = 200,
                       height: int = 200,
                       format: str = 'JPEG') -> BytesIO:
        """
        Create a thumbnail from an image
        
        Args:
            image_data: The image data as bytes or file-like object
            width: Thumbnail width
            height: Thumbnail height
            format: Output format
                
        Returns:
            BytesIO object containing the thumbnail
                
        Raises:
            ValueError: If thumbnail cannot be created
        """
        try:
            # Ensure we're working with a BytesIO object
            if isinstance(image_data, bytes):
                image_file = BytesIO(image_data)
            else:
                # Create a copy of the file-like object
                if hasattr(image_data, 'seek'):
                    current_pos = image_data.tell()
                    image_data.seek(0)
                    
                image_file = BytesIO(image_data.read())
                
                if hasattr(image_data, 'seek'):
                    image_data.seek(current_pos)
                    
            # Open the image
            img = Image.open(image_file)
            
            # Create thumbnail
            img.thumbnail((width, height), Image.LANCZOS)
            
            # Save to BytesIO
            output = BytesIO()
            
            # Handle different formats
            if format.upper() == 'JPEG':
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output, format='JPEG', quality=85, optimize=True)
            elif format.upper() == 'PNG':
                img.save(output, format='PNG', optimize=True)
            elif format.upper() == 'WEBP':
                img.save(output, format='WEBP', quality=85)
            else:
                img.save(output, format=format)
                
            # Reset BytesIO position
            output.seek(0)
            
            return output
        except Exception as e:
            raise ValueError(f"Thumbnail creation failed: {str(e)}") 