# File Storage Utilities

This module provides comprehensive utilities for file storage, management, and processing in the SDIMS application.

## Features

- File storage abstraction with consistent interface
- AWS S3 implementation with robust error handling
- File metadata management
- File security and access control
- File operations (validation, sanitization, transformation)
- File import/export utilities

## Components

### StorageProvider Interface

Abstract interface defining the contract for all storage providers:

```python
from common.storage import StorageProvider

# Example abstract method
def upload(file_data, key, content_type=None, metadata=None) -> str:
    """Upload file data to storage"""
    pass
```

### S3StorageProvider

AWS S3 implementation of the StorageProvider interface:

```python
from common.storage import S3StorageProvider

# Initialize with bucket name (or use environment variable)
storage = S3StorageProvider(bucket_name="my-bucket")

# Upload a file
file_path = storage.upload(
    file_data=my_file_data,
    key="path/to/file.pdf",
    content_type="application/pdf",
    metadata={"entity_type": "contract", "entity_id": "123"}
)

# Generate pre-signed URL for download
url = storage.get_presigned_url(
    key="path/to/file.pdf",
    expires_in=3600,
    response_content_disposition='attachment; filename="contract.pdf"'
)
```

### FileMetadata

Model for storing and managing file metadata:

```python
from common.storage import FileMetadata

# Create metadata for a file
metadata = FileMetadata.create_from_upload(
    file_id="unique-id",
    filename="contract.pdf",
    file_path="contracts/123/contract.pdf",
    file_size=1024,
    entity_type="contract",
    entity_id="123",
    description="Contract document",
    uploaded_by_id="user-id"
)

# Store in DynamoDB
metadata.save()

# Get AWS S3 compatible metadata
s3_metadata = metadata.to_storage_metadata()
```

### FileOperations

Utilities for file operations:

```python
from common.storage import FileOperations

# Validate a file
mime_type = FileOperations.validate_file_type(
    file_data=my_file_data,
    filename="document.pdf",
    allowed_mime_types={"application/pdf"}
)

# Sanitize a filename
safe_name = FileOperations.sanitize_filename("my file (1).pdf")  # "my_file_1.pdf"

# Process an image
processed_image = FileOperations.process_image(
    image_data=my_image_data,
    max_width=800,
    max_height=600
)

# Create a thumbnail
thumbnail = FileOperations.create_thumbnail(my_image_data, width=200, height=200)
```

### FilePermissionManager

Security and access control for files:

```python
from common.storage import FilePermissionManager

# Check if user has permission to access a file
permission_manager = FilePermissionManager()
has_access = permission_manager.check_file_access(
    entity_type="contract",
    entity_id="123",
    required_permission="contract:read"
)
```

### Import/Export Utilities

Utilities for importing and exporting data from files:

```python
from common.storage.import_export import ExcelParser, CSVExporter, EmployeeDataValidator

# Parse Excel file
parser = ExcelParser(file_data=my_excel_data)
data = parser.parse_sheet("Employees")

# Validate data
validator = EmployeeDataValidator()
results = validator.validate_bulk(data)

# Export data to CSV
exporter = CSVExporter()
csv_bytes = exporter.export(data)
```

## Error Handling

The module provides a comprehensive set of exceptions for proper error handling:

```python
from common.storage.exceptions import (
    StorageError,
    StorageFileNotFoundError,
    StoragePermissionError,
    StorageFileTypeError,
    StorageFileSizeError
)

try:
    storage.download(key="path/to/file.pdf")
except StorageFileNotFoundError:
    # Handle not found
except StoragePermissionError:
    # Handle permission denied
except StorageError as e:
    # Handle general storage error
```

## Best Practices

1. **Always validate files** before uploading to ensure they meet size and type requirements
2. **Use sanitized filenames** to prevent path traversal and other security issues
3. **Check permissions** before allowing file access
4. **Use pre-signed URLs** for secure direct downloads
5. **Include appropriate metadata** for better file organization and searching
6. **Handle errors gracefully** using the specific exception types

## Dependencies

- boto3 - For AWS S3 integration
- python-magic - For MIME type detection
- Pillow - For image processing
- pandas/openpyxl - For Excel file handling 