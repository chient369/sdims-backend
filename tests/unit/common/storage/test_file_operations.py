"""
Unit tests for FileOperations class
"""

import os
import uuid
import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock

from common.storage.file_operations import FileOperations
from common.storage.exceptions import StorageFileTypeError, StorageFileSizeError


class TestFileOperations:
    """Tests for FileOperations class"""
    
    def test_sanitize_filename(self):
        """Test sanitize_filename method"""
        # Test with spaces and special characters
        filename = "My File (1).txt"
        sanitized = FileOperations.sanitize_filename(filename)
        assert sanitized == "My_File_1.txt"
        
        # Test with path components
        filename = "/path/to/file.txt"
        sanitized = FileOperations.sanitize_filename(filename)
        assert sanitized == "file.txt"
        
        # Test with problematic characters
        filename = "file<>:\"\\|?*.txt"
        sanitized = FileOperations.sanitize_filename(filename)
        assert sanitized == "file_.txt"
        
        # Test with empty string
        filename = ""
        sanitized = FileOperations.sanitize_filename(filename)
        assert sanitized == "unnamed_file"
        
    def test_generate_unique_filename(self):
        """Test generate_unique_filename method"""
        # Test with UUID
        filename = "test.txt"
        unique = FileOperations.generate_unique_filename(filename, add_uuid=True)
        
        # Should be sanitized and have a UUID
        assert unique.endswith(".txt")
        assert unique.startswith("test_")
        assert len(unique) > len(filename) + 5  # At least some UUID chars added
        
        # Test with timestamp
        filename = "test.txt"
        unique = FileOperations.generate_unique_filename(filename, add_uuid=False)
        
        # Should be sanitized and have a timestamp
        assert unique.endswith(".txt")
        assert unique.startswith("test_")
        assert len(unique) > len(filename) + 5  # Timestamp added
    
    @patch('magic.from_buffer')
    def test_detect_mime_type_bytes(self, mock_from_buffer):
        """Test detect_mime_type with bytes input"""
        # Mock magic.from_buffer to return a predetermined MIME type
        mock_from_buffer.return_value = 'text/plain'
        
        # Test with bytes
        file_data = b"test content"
        mime_type = FileOperations.detect_mime_type(file_data)
        
        assert mime_type == 'text/plain'
        mock_from_buffer.assert_called_once()
    
    @patch('magic.from_buffer')
    def test_detect_mime_type_file_object(self, mock_from_buffer):
        """Test detect_mime_type with file-like object"""
        # Mock magic.from_buffer to return a predetermined MIME type
        mock_from_buffer.return_value = 'application/octet-stream'
        
        # Test with file-like object
        file_data = BytesIO(b"test content")
        mime_type = FileOperations.detect_mime_type(file_data, "test.pdf")
        
        # Should fall back to mimetypes if magic returns octet-stream
        assert mime_type == 'application/pdf'
        mock_from_buffer.assert_called_once()
    
    def test_validate_file_type_valid(self):
        """Test validate_file_type with valid file type"""
        # Patch detect_mime_type to return a valid MIME type
        with patch.object(FileOperations, 'detect_mime_type', return_value='image/jpeg'):
            file_data = b"test content"
            
            # Use default allowed types
            mime_type = FileOperations.validate_file_type(file_data, "test.jpg")
            
            assert mime_type == 'image/jpeg'
    
    def test_validate_file_type_invalid_mime(self):
        """Test validate_file_type with invalid MIME type"""
        # Patch detect_mime_type to return an invalid MIME type
        with patch.object(FileOperations, 'detect_mime_type', return_value='application/x-invalid'):
            file_data = b"test content"
            
            # Should raise exception for invalid MIME type
            with pytest.raises(StorageFileTypeError):
                FileOperations.validate_file_type(file_data, "test.xyz")
    
    def test_validate_file_type_invalid_extension(self):
        """Test validate_file_type with invalid extension"""
        # Patch detect_mime_type to return a valid MIME type
        with patch.object(FileOperations, 'detect_mime_type', return_value='image/jpeg'):
            file_data = b"test content"
            
            # Should raise exception for invalid extension
            with pytest.raises(StorageFileTypeError):
                FileOperations.validate_file_type(file_data, "test.xyz")
    
    def test_validate_file_size_valid(self):
        """Test validate_file_size with valid file size"""
        # Create a small file
        file_data = b"test content"
        
        # Use default max size
        file_size = FileOperations.validate_file_size(file_data)
        
        assert file_size == len(file_data)
        
        # Test with file-like object
        file_obj = BytesIO(file_data)
        file_size = FileOperations.validate_file_size(file_obj)
        
        assert file_size == len(file_data)
    
    def test_validate_file_size_invalid(self):
        """Test validate_file_size with invalid file size"""
        # Create a file larger than max size
        file_data = b"a" * 100
        max_size = 50
        
        # Should raise exception for file too large
        with pytest.raises(StorageFileSizeError):
            FileOperations.validate_file_size(file_data, max_size)
    
    def test_get_file_hash(self):
        """Test get_file_hash method"""
        # Test with bytes
        file_data = b"test content"
        hash_sha256 = FileOperations.get_file_hash(file_data, "sha256")
        hash_md5 = FileOperations.get_file_hash(file_data, "md5")
        
        # Verify hashes (precomputed)
        assert hash_sha256 == "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"
        
        # Test with file-like object
        file_obj = BytesIO(file_data)
        hash_obj = FileOperations.get_file_hash(file_obj)
        
        assert hash_obj == hash_sha256
        
    @patch('PIL.Image.open')
    def test_process_image(self, mock_open):
        """Test process_image method"""
        # Mock PIL Image
        mock_img = MagicMock()
        mock_img.size = (100, 100)
        mock_img.mode = 'RGB'
        mock_open.return_value = mock_img
        
        # Test with bytes
        file_data = b"test image data"
        output = FileOperations.process_image(file_data, max_width=50, max_height=50)
        
        # Verify image was processed
        assert mock_img.resize.called
        assert mock_img.save.called
        assert isinstance(output, BytesIO)
        
    @patch('PIL.Image.open')
    def test_create_thumbnail(self, mock_open):
        """Test create_thumbnail method"""
        # Mock PIL Image
        mock_img = MagicMock()
        mock_open.return_value = mock_img
        
        # Test with bytes
        file_data = b"test image data"
        output = FileOperations.create_thumbnail(file_data, width=100, height=100)
        
        # Verify thumbnail was created
        assert mock_img.thumbnail.called
        assert mock_img.save.called
        assert isinstance(output, BytesIO) 