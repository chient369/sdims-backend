"""
Unit tests for FileMetadata class
"""

import os
import uuid
import datetime
import pytest
from unittest.mock import patch

from common.storage.file_metadata import FileMetadata


class TestFileMetadata:
    """Tests for FileMetadata class"""
    
    def test_create_basic_metadata(self):
        """Test basic metadata creation"""
        # Create basic metadata
        file_id = str(uuid.uuid4())
        file_metadata = FileMetadata(
            id=file_id,
            original_filename="test.txt",
            file_path="uploads/test.txt"
        )
        
        # Check basic properties
        assert file_metadata.id == file_id
        assert file_metadata.original_filename == "test.txt"
        assert file_metadata.file_path == "uploads/test.txt"
        assert file_metadata.file_type == ""  # Default value
        assert file_metadata.file_size == 0   # Default value
        assert file_metadata.is_public is False  # Default value
        assert file_metadata.is_active is True   # Default value
        assert file_metadata.version == 1        # Default value
        
    def test_create_from_upload(self):
        """Test create_from_upload factory method"""
        # Create metadata from upload
        file_id = str(uuid.uuid4())
        file_metadata = FileMetadata.create_from_upload(
            file_id=file_id,
            filename="document.pdf",
            file_path="contracts/123/document.pdf",
            file_size=1024,
            entity_type="contract",
            entity_id="123",
            description="Contract document",
            uploaded_by_id="user123",
            is_public=False
        )
        
        # Check properties
        assert file_metadata.id == file_id
        assert file_metadata.original_filename == "document.pdf"
        assert file_metadata.file_path == "contracts/123/document.pdf"
        assert file_metadata.file_type == "application/pdf"  # Detected from filename
        assert file_metadata.file_size == 1024
        assert file_metadata.entity_type == "contract"
        assert file_metadata.entity_id == "123"
        assert file_metadata.description == "Contract document"
        assert file_metadata.uploaded_by_id == "user123"
        assert file_metadata.is_public is False
        
    def test_extension_property(self):
        """Test extension property"""
        # Create metadata with various extensions
        meta1 = FileMetadata(id="1", original_filename="file.txt", file_path="file.txt")
        meta2 = FileMetadata(id="2", original_filename="file.PDF", file_path="file.PDF")
        meta3 = FileMetadata(id="3", original_filename="file", file_path="file")
        
        # Check extensions
        assert meta1.extension == ".txt"
        assert meta2.extension == ".pdf"  # Should be lowercase
        assert meta3.extension == ""      # No extension
        
    def test_filename_without_extension_property(self):
        """Test filename_without_extension property"""
        # Create metadata with various filenames
        meta1 = FileMetadata(id="1", original_filename="file.txt", file_path="file.txt")
        meta2 = FileMetadata(id="2", original_filename="report.2023.pdf", file_path="report.2023.pdf")
        meta3 = FileMetadata(id="3", original_filename="image", file_path="image")
        
        # Check filenames without extension
        assert meta1.filename_without_extension == "file"
        assert meta2.filename_without_extension == "report.2023"
        assert meta3.filename_without_extension == "image"
        
    def test_is_image_property(self):
        """Test is_image property"""
        # Create metadata for different file types
        image_meta = FileMetadata(
            id="1",
            original_filename="photo.jpg",
            file_path="photo.jpg",
            file_type="image/jpeg"
        )
        
        doc_meta = FileMetadata(
            id="2",
            original_filename="document.pdf",
            file_path="document.pdf",
            file_type="application/pdf"
        )
        
        # Check is_image property
        assert image_meta.is_image is True
        assert doc_meta.is_image is False
        
    def test_is_document_property(self):
        """Test is_document property"""
        # Create metadata for different file types
        doc_meta = FileMetadata(
            id="1",
            original_filename="document.pdf",
            file_path="document.pdf",
            file_type="application/pdf"
        )
        
        image_meta = FileMetadata(
            id="2",
            original_filename="photo.jpg",
            file_path="photo.jpg",
            file_type="image/jpeg"
        )
        
        # Check is_document property
        assert doc_meta.is_document is True
        assert image_meta.is_document is False
        
    def test_to_storage_metadata(self):
        """Test to_storage_metadata method"""
        # Create metadata with various properties
        file_id = str(uuid.uuid4())
        file_metadata = FileMetadata(
            id=file_id,
            original_filename="report.xlsx",
            file_path="reports/q3/report.xlsx",
            file_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            file_size=2048,
            entity_type="report",
            entity_id="q3-2023",
            description="Q3 Financial Report",
            uploaded_by_id="user456",
            is_public=True,
            version=2,
            tags=["financial", "quarterly"],
            custom_metadata={"department": "finance", "year": 2023, "status": "final"}
        )
        
        # Convert to storage metadata
        storage_metadata = file_metadata.to_storage_metadata()
        
        # Check metadata
        assert storage_metadata["file_id"] == file_id
        assert storage_metadata["original_filename"] == "report.xlsx"
        assert storage_metadata["entity_type"] == "report"
        assert storage_metadata["entity_id"] == "q3-2023"
        assert storage_metadata["description"] == "Q3 Financial Report"
        assert storage_metadata["uploaded_by"] == "user456"
        assert storage_metadata["is_public"] == "true"
        assert storage_metadata["version"] == "2"
        assert storage_metadata["tags"] == "financial,quarterly"
        
        # Check custom metadata (as strings)
        assert storage_metadata["custom_department"] == "finance"
        assert storage_metadata["custom_year"] == "2023"
        assert storage_metadata["custom_status"] == "final"
        
    def test_from_storage_metadata(self):
        """Test from_storage_metadata method"""
        # Create storage metadata
        file_id = str(uuid.uuid4())
        storage_metadata = {
            "original_filename": "image.png",
            "entity_type": "opportunity",
            "entity_id": "opp-789",
            "description": "Screenshot of prototype",
            "uploaded_by": "user789",
            "upload_date": "2023-08-01T10:15:30",
            "is_public": "false",
            "version": "1",
            "tags": "screenshot,prototype,design",
            "custom_client": "ABC Corp",
            "custom_reviewed": "true"
        }
        
        # Create FileMetadata from storage metadata
        file_metadata = FileMetadata.from_storage_metadata(
            file_id=file_id,
            file_path="opportunities/opp-789/image.png",
            file_size=5000,
            file_type="image/png",
            metadata=storage_metadata
        )
        
        # Check properties
        assert file_metadata.id == file_id
        assert file_metadata.original_filename == "image.png"
        assert file_metadata.file_path == "opportunities/opp-789/image.png"
        assert file_metadata.file_size == 5000
        assert file_metadata.file_type == "image/png"
        assert file_metadata.entity_type == "opportunity"
        assert file_metadata.entity_id == "opp-789"
        assert file_metadata.description == "Screenshot of prototype"
        assert file_metadata.uploaded_by_id == "user789"
        assert file_metadata.upload_date == "2023-08-01T10:15:30"
        assert file_metadata.is_public is False
        assert file_metadata.version == 1
        
        # Check tags
        assert file_metadata.tags == ["screenshot", "prototype", "design"]
        
        # Check custom metadata
        assert file_metadata.custom_metadata["client"] == "ABC Corp"
        assert file_metadata.custom_metadata["reviewed"] == "true" 