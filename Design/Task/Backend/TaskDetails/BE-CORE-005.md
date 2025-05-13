**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-05 | Chiến Trần Văn | Định nghĩa chi tiết task File Storage Utilities | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển các tiện ích quản lý lưu trữ file cho backend system. Các tiện ích này sẽ cung cấp phương thức thống nhất để lưu trữ, truy xuất và quản lý tập tin trong hệ thống.

# Chi tiết Task: BE-CORE-005 - File Storage Utilities

## Thông tin chung

**Task ID:** BE-CORE-005  
**Task Name:** Phát triển File Storage Utilities  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-CORE-001, BE-INF-001  
**Các task phụ thuộc vào task này:** BE-API-CTR-010, BE-API-CTR-011, BE-API-HRM-007, BE-API-OPP-006

## Mô tả

Task này bao gồm việc phát triển các tiện ích để quản lý file trong hệ thống, chủ yếu tập trung vào việc tích hợp AWS S3 để lưu trữ tập tin. Các tiện ích này sẽ cung cấp API đơn giản và thống nhất để upload, download, quản lý và bảo mật các tập tin trong hệ thống. Các tính năng sẽ được sử dụng trong nhiều module của ứng dụng, như đính kèm file hợp đồng, import dữ liệu nhân viên, lưu trữ tài liệu cơ hội, và nhiều tình huống khác.

## Chi tiết công việc

### Thiết kế Storage Provider Interface

- [ ] Xây dựng interface chung cho storage providers:
  - Thiết kế `StorageProvider` interface class
  - Định nghĩa các method chuẩn: upload, download, delete, list, get_url
  - Xác định các abstractions cho metadata, permissions, và lifecycle policies

### Triển khai S3StorageProvider

- [ ] Phát triển implementation cho AWS S3:
  - Tạo `S3StorageProvider` class implement `StorageProvider` interface
  - Tích hợp với boto3 S3 client
  - Xử lý cấu hình cho các bucket khác nhau
  - Triển khai error handling cụ thể cho S3
  - Cài đặt các tính năng nâng cao như multipart upload

### Xây dựng File Operations Utilities

- [ ] Phát triển các utility function cho thao tác file:
  - Hàm xử lý MIME type detection
  - Utilities để validate file extensions
  - Xử lý file name normalization và sanitization
  - Chunk handling cho large files
  - Utilities để tạo ra unique file names

### Phát triển File Security Utilities

- [ ] Triển khai các tính năng bảo mật file:
  - Lớp FilePermissionManager để quản lý quyền truy cập
  - Tích hợp với IAM roles và S3 bucket policies
  - Cơ chế tạo pre-signed URL với thời gian hạn chế
  - Server-side encryption khi lưu trữ file
  - Scanning file trước khi upload (nếu cần)

### Xây dựng File Metadata Management

- [ ] Phát triển hệ thống quản lý metadata:
  - Lớp `FileMetadata` để đại diện cho metadata của file
  - Lưu trữ metadata trong DynamoDB (tích hợp với các model đã có)
  - Đồng bộ metadata với S3 object tags
  - Tìm kiếm file dựa trên metadata
  - Versioning của file và metadata tracking

### Triển khai File Upload/Download UI Support

- [ ] Phát triển các tính năng hỗ trợ UI:
  - Tạo pre-signed URL cho direct upload từ client
  - Cấu hình CORS policy cho S3 buckets
  - Hỗ trợ progress tracking cho large uploads
  - Tạo thumbnail và preview generation cho images
  - Resume upload functionality (nếu cần)

### Xây dựng File Type Handlers

- [ ] Phát triển xử lý đặc biệt cho các loại file:
  - Xử lý đặc biệt cho file hình ảnh (resize, optimizing)
  - Xử lý cho file PDF (thumbnail, text extraction)
  - Xử lý cho file Office (Excel, Word, Powerpoint) 
  - Xử lý cho file CSV (parsing, validation)
  - Xử lý cho file ZIP (extraction, scanning)

### Phát triển File Import/Export Utilities

- [ ] Triển khai các tiện ích xử lý import/export:
  - Utilities để import data từ CSV/Excel
  - Export data ra file CSV/Excel/PDF
  - Template generation cho import files
  - Batch processing cho large datasets
  - Validation của import data

### Triển khai Storage Lifecycle Management

- [ ] Xây dựng cơ chế quản lý lifecycle:
  - Cấu hình S3 lifecycle rules
  - File archiving & backup strategy
  - File cleanup và purging cũ
  - Version control và retention policy
  - Storage cost optimization

### Viết Unit Tests

- [ ] Phát triển test suites cho storage utilities:
  - Tests cho StorageProvider interface
  - Tests cho S3StorageProvider implementation
  - Tests cho file operations utilities
  - Tests cho metadata management
  - Tests cho file security features
  - Integration tests với AWS services (mocks và real)

### Xây dựng Documentation và Examples

- [ ] Tạo tài liệu hướng dẫn sử dụng File Storage Utilities:
  - API documentation cho tất cả các classes và methods
  - Usage examples cho các trường hợp phổ biến
  - Security best practices
  - Kiến trúc và design decisions
  - Troubleshooting guide

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách mong muốn sử dụng File Storage Utilities khi hoàn thành:

### Uploading a file

```python
from common.storage import S3StorageProvider, FileMetadata
import uuid

def upload_contract_file(contract_id, file_data, filename, file_type, description):
    """
    Upload a contract file to storage
    
    Args:
        contract_id: The ID of the contract
        file_data: The binary file data
        filename: Original filename
        file_type: MIME type or file type
        description: File description
    
    Returns:
        dict: The file metadata
    """
    # Initialize storage provider
    storage = S3StorageProvider(bucket_name="sdims-contract-files")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    safe_filename = storage.sanitize_filename(filename)
    storage_key = f"contracts/{contract_id}/{file_id}-{safe_filename}"
    
    # Prepare metadata
    metadata = FileMetadata(
        id=file_id,
        original_filename=filename,
        file_path=storage_key,
        file_type=file_type,
        file_size=len(file_data),
        entity_type="contract",
        entity_id=contract_id,
        description=description,
        uploaded_by_id="current-user-id",
        is_public=False
    )
    
    # Upload file to S3
    storage.upload(
        file_data=file_data,
        key=storage_key,
        content_type=file_type,
        metadata={
            "entity_type": "contract",
            "entity_id": contract_id,
            "file_id": file_id
        }
    )
    
    # Save metadata to DynamoDB (using DynamoDB Repository from BE-CORE-001)
    from common.dynamodb import DynamoDBRepository
    db_repo = DynamoDBRepository()
    db_repo.save_model(metadata)
    
    return metadata.to_dict()
```

### Generating a download URL

```python
from common.storage import S3StorageProvider
from common.errors import NotFoundError

def get_file_download_url(file_id, expires_in=3600):
    """
    Generate a pre-signed URL to download a file
    
    Args:
        file_id: The ID of the file
        expires_in: URL expiration time in seconds
    
    Returns:
        str: The pre-signed download URL
    """
    # Get file metadata from DynamoDB
    from common.dynamodb import DynamoDBRepository
    from common.models import FileAttachment
    
    db_repo = DynamoDBRepository()
    file_metadata = db_repo.get_model(FileAttachment, file_id=file_id)
    
    if not file_metadata:
        raise NotFoundError(f"File with ID {file_id} not found")
    
    # Check permissions based on entity type and user role
    from common.auth import current_user
    if not file_metadata.is_public:
        if file_metadata.entity_type == "contract":
            if not current_user.has_permission("contract:read", file_metadata.entity_id):
                raise ForbiddenError("You don't have permission to access this file")
    
    # Initialize storage provider based on file location
    storage = S3StorageProvider(bucket_name="sdims-contract-files")
    
    # Generate pre-signed URL
    url = storage.get_presigned_url(
        key=file_metadata.file_path,
        expires_in=expires_in,
        response_content_disposition=f'attachment; filename="{file_metadata.original_filename}"',
        response_content_type=file_metadata.file_type
    )
    
    return url
```

### Import từ file Excel

```python
from common.storage import S3StorageProvider
from common.import_export import ExcelParser, EmployeeDataValidator

def import_employees_from_excel(file_data, filename):
    """
    Import employees from Excel file
    
    Args:
        file_data: The binary file data
        filename: Original filename
    
    Returns:
        dict: Import summary
    """
    # Temporarily store the file
    storage = S3StorageProvider(bucket_name="sdims-imports")
    temp_key = f"temp/employees/{str(uuid.uuid4())}-{filename}"
    storage.upload(file_data=file_data, key=temp_key)
    
    # Get file URL for processing
    file_url = storage.get_file_url(temp_key)
    
    # Parse Excel file
    parser = ExcelParser(url=file_url)
    data = parser.parse_sheet("Employees")
    
    # Validate data
    validator = EmployeeDataValidator()
    validation_results = validator.validate_bulk(data)
    
    if not validation_results.is_valid:
        # Return validation errors
        return {
            "success": False,
            "errors": validation_results.errors,
            "total": len(data),
            "valid": validation_results.valid_count,
            "invalid": validation_results.invalid_count
        }
    
    # Process valid data
    from common.dynamodb import DynamoDBRepository
    from common.models import Employee
    
    db_repo = DynamoDBRepository()
    imported_count = 0
    errors = []
    
    for item in validation_results.valid_items:
        try:
            employee = Employee(
                first_name=item["first_name"],
                last_name=item["last_name"],
                employee_code=item["employee_code"],
                email=item["email"],
                position=item["position"],
                hire_date=item["hire_date"]
                # other fields...
            )
            db_repo.save_model(employee)
            imported_count += 1
        except Exception as e:
            errors.append({"row": item["_row_number"], "error": str(e)})
    
    # Clean up temporary file
    storage.delete(temp_key)
    
    return {
        "success": True,
        "total": len(data),
        "imported": imported_count,
        "errors": errors
    }
```

## Tiêu chí hoàn thành

- StorageProvider interface và S3StorageProvider implementation được hoàn thành
- File metadata management được triển khai
- File upload/download và generation of pre-signed URL hoạt động tốt
- Security và permissions được triển khai đầy đủ
- Các tiện ích import/export được triển khai
- Xử lý từng loại file đặc biệt được hoàn thành
- Tất cả các tính năng được unit test đầy đủ
- Documentation và examples được tạo

## Ước tính thời gian

- 4-5 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý tới security và permissions khi truy cập file
- File upload phải có validation kỹ lưỡng về file size, type và content
- Cần triển khai error handling toàn diện cho các vấn đề phổ biến như network issues, permission errors
- Nên thiết kế để dễ dàng chuyển đổi giữa các storage providers (S3, local filesystem, etc.)
- Cân nhắc các vấn đề về hiệu suất như caching, lazy loading cho large files
- Nên tối ưu hóa chi phí lưu trữ thông qua lifecycle policies và compression options 