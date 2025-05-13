**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý file đính kèm | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý file đính kèm cho hợp đồng, phục vụ cho việc upload, lưu trữ và quản lý tệp tin liên quan đến hợp đồng.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-CTR-003  
**Task Name:** Triển khai Lambda functions quản lý file đính kèm  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-INF-006 (Cấu hình S3 buckets)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-CTR-001 (Triển khai Lambda functions quản lý hợp đồng)

**Các task phụ thuộc vào task này:** 
- Không có

**Các API:**
- POST /api/v1/contracts/{contractId}/attachments (API-CTR-009)
- GET /api/v1/contracts/{contractId}/attachments (API-CTR-010)
- GET /api/v1/attachments/{attachmentId}/download (API-CTR-011)
- DELETE /api/v1/attachments/{attachmentId} (API-CTR-012)

## Mô tả

Triển khai các Lambda functions để quản lý file đính kèm cho hợp đồng, bao gồm các chức năng:
- Upload file đính kèm cho hợp đồng (như file scan hợp đồng, phụ lục, hóa đơn, v.v.)
- Lấy danh sách file đính kèm của một hợp đồng
- Tải xuống file đính kèm
- Xóa file đính kèm

Hệ thống cần hỗ trợ nhiều loại file phổ biến (PDF, Word, Excel, hình ảnh) và đảm bảo an toàn dữ liệu với các chính sách phân quyền phù hợp. File sẽ được lưu trữ trong S3 bucket với cơ chế mã hóa và thông tin metadata được lưu trong DynamoDB.

## Chi tiết công việc

### Phát triển Lambda function upload file đính kèm

- [ ] Triển khai Lambda function xử lý POST /api/v1/contracts/{contractId}/attachments:
  - Location: src/functions/attachments/upload_attachment.py
  - Triển khai logic upload file đính kèm:
    - Xác thực và phân quyền người dùng
    - Kiểm tra hợp đồng tồn tại
    - Xử lý file upload từ multipart/form-data request
    - Validate file:
      - Kiểm tra loại file (MIME type)
      - Kiểm tra kích thước file (giới hạn tối đa 20MB hoặc theo cấu hình)
      - Kiểm tra tên file và extension
      - Quét virus/malware (tùy chọn/tương lai)
    - Tạo ID duy nhất cho file
    - Lưu file vào S3 bucket với các thông số bảo mật phù hợp
    - Lưu metadata của file vào DynamoDB (ATTACHMENT entity):
      - ID, tên file, loại file, kích thước, contract_id
      - Hash file (để xác minh tính toàn vẹn)
      - Người upload, thời gian upload
      - Type của attachment (contract, invoice, amendment, other)
      - Description (nếu có)
    - Cập nhật thông tin attachment vào hợp đồng (nếu cần)
  - Triển khai xử lý lỗi và logging chi tiết
  - Xử lý các trường hợp upload thất bại, timeout, network issues

### Phát triển Lambda function lấy danh sách file đính kèm

- [ ] Triển khai Lambda function xử lý GET /api/v1/contracts/{contractId}/attachments:
  - Location: src/functions/attachments/list_attachments.py
  - Triển khai logic lấy danh sách file đính kèm:
    - Xác thực và phân quyền người dùng
    - Kiểm tra hợp đồng tồn tại
    - Truy vấn DynamoDB để lấy danh sách metadata của các file đính kèm
    - Hỗ trợ các tham số filter:
      - type: Lọc theo loại file đính kèm (contract, invoice, amendment, other)
      - uploaded_by: Lọc theo người upload
      - upload_date_from/upload_date_to: Lọc theo khoảng thời gian
    - Hỗ trợ tìm kiếm theo tên file
    - Hỗ trợ phân trang
    - Hỗ trợ sắp xếp theo thời gian upload, tên file, kích thước
    - Tạo pre-signed URL tạm thời cho việc xem trước file (nếu loại file hỗ trợ)
    - Nhóm file theo loại (tùy chọn)
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function tải xuống file đính kèm

- [ ] Triển khai Lambda function xử lý GET /api/v1/attachments/{attachmentId}/download:
  - Location: src/functions/attachments/download_attachment.py
  - Triển khai logic tải xuống file đính kèm:
    - Xác thực và phân quyền người dùng
    - Kiểm tra file tồn tại
    - Xác minh người dùng có quyền truy cập file này (thông qua liên kết với hợp đồng)
    - Tạo pre-signed URL cho file trong S3 với thời gian hết hạn ngắn (5-15 phút)
    - Tùy chọn: Ghi log hoạt động tải xuống
  - Triển khai xử lý lỗi
  - Hỗ trợ tùy chọn tải trực tiếp từ Lambda (phù hợp cho file nhỏ) hoặc redirect đến pre-signed URL

### Phát triển Lambda function xóa file đính kèm

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/attachments/{attachmentId}:
  - Location: src/functions/attachments/delete_attachment.py
  - Triển khai logic xóa file đính kèm:
    - Xác thực và phân quyền người dùng (chỉ Admin, người tạo hợp đồng và một số vai trò đặc biệt)
    - Kiểm tra file tồn tại
    - Xác minh người dùng có quyền xóa file này
    - Xóa file từ S3 bucket
    - Xóa metadata từ DynamoDB hoặc đánh dấu đã xóa (soft delete)
    - Cập nhật thông tin hợp đồng liên quan (nếu cần)
    - Ghi log hoạt động xóa
  - Triển khai xử lý lỗi và rollback nếu cần

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho file đính kèm:
  - Location: src/models/attachment.py
  - Định nghĩa model cho file đính kèm:
    - Các trường cơ bản: id, contract_id, file_name, file_type, file_size, content_type, hash
    - Các trường S3: bucket_name, object_key
    - Các trường phân loại: type (contract, invoice, amendment, other), description
    - Các trường theo dõi: uploaded_by, uploaded_at, updated_at, is_deleted, deleted_at, deleted_by
  - Triển khai các method truy vấn DynamoDB:
    - create_attachment(attachment_data)
    - get_attachment(attachment_id)
    - get_attachments_by_contract(contract_id, filters, pagination)
    - update_attachment(attachment_id, attachment_data)
    - delete_attachment(attachment_id)
    - get_attachments_by_type(contract_id, type)

### Phát triển Service Layer

- [ ] Xây dựng service layer cho xử lý file và tương tác với S3:
  - Location: src/services/attachment_service.py
  - Implement các phương thức:
    - validate_file(file_object, allowed_types, max_size): Kiểm tra file hợp lệ
    - upload_to_s3(file_object, bucket, key, metadata): Upload file lên S3
    - generate_download_url(bucket, key, expiry=900): Tạo pre-signed URL tạm thời
    - delete_from_s3(bucket, key): Xóa file từ S3
    - calculate_file_hash(file_object): Tính toán hash của file
    - validate_user_permission(user_id, contract_id, action): Kiểm tra quyền của người dùng

### Cấu hình S3 Bucket và IAM Policies

- [ ] Cấu hình S3 bucket cho lưu trữ file:
  - Location: template.yaml (trong phần Resources)
  - Thiết lập S3 bucket với các cấu hình:
    - Tên bucket: ${ProjectName}-attachments-${Stage}
    - Mã hóa: AES-256 hoặc KMS
    - Lifecycle policies: Archival rules (tùy chọn)
    - CORS configuration: Cho phép upload từ frontend
    - Logging: Bật S3 access logging
  - IAM Policy cho Lambda function có quyền:
    - s3:PutObject, s3:GetObject, s3:DeleteObject
    - s3:ListBucket, s3:HeadObject
  - Thiết lập IAM roles với principle of least privilege

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route POST /api/v1/contracts/{contractId}/attachments:
    - Method: POST
    - Path parameter: contractId
    - Content-Type: multipart/form-data
    - Binary support: Cấu hình API Gateway để xử lý nội dung binary
    - Liên kết với Lambda function upload_attachment
    - Phân quyền: Authenticated Users với quyền upload
    - Cấu hình timeout đủ dài cho file lớn
  - Cấu hình route GET /api/v1/contracts/{contractId}/attachments:
    - Method: GET
    - Path parameter: contractId
    - Các tham số query: type, uploaded_by, upload_date_from, upload_date_to, search, page, size, sortBy, sortDirection
    - Liên kết với Lambda function list_attachments
    - Phân quyền: Authenticated Users với quyền xem hợp đồng
  - Cấu hình route GET /api/v1/attachments/{attachmentId}/download:
    - Method: GET
    - Path parameter: attachmentId
    - Liên kết với Lambda function download_attachment
    - Phân quyền: Authenticated Users với quyền xem hợp đồng
  - Cấu hình route DELETE /api/v1/attachments/{attachmentId}:
    - Method: DELETE
    - Path parameter: attachmentId
    - Liên kết với Lambda function delete_attachment
    - Phân quyền: Admin, Contract Owner và các vai trò đặc biệt
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/attachments/
  - Test case cho upload_attachment.py:
    - Test upload file thành công
    - Test upload với file không hợp lệ (loại file, kích thước)
    - Test upload với hợp đồng không tồn tại
    - Test phân quyền
  - Test case cho list_attachments.py:
    - Test lấy danh sách file đính kèm
    - Test filter và search
    - Test phân trang và sắp xếp
    - Test phân quyền
  - Test case cho download_attachment.py:
    - Test tải xuống file thành công
    - Test với file không tồn tại
    - Test phân quyền
  - Test case cho delete_attachment.py:
    - Test xóa file thành công
    - Test với file không tồn tại
    - Test phân quyền
  - Test case cho các method trong attachment_service.py:
    - Test validate_file
    - Test generate_download_url
    - Test validate_user_permission
    - Test upload_to_s3 và delete_from_s3 (có thể dùng mock S3)

### Tích hợp Security Scanning

- [ ] Tích hợp kiểm tra bảo mật:
  - Cấu hình virus scanning cho file upload (có thể sử dụng ClamAV hoặc dịch vụ bên thứ ba)
  - File type verification để ngăn chặn file độc hại
  - File content validation cho các file quan trọng

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - POST /api/v1/contracts/{contractId}/attachments
    - GET /api/v1/contracts/{contractId}/attachments
    - GET /api/v1/attachments/{attachmentId}/download
    - DELETE /api/v1/attachments/{attachmentId}
  - Tài liệu quyền truy cập và sử dụng API
  - Tài liệu mô tả cấu trúc dữ liệu và quy trình quản lý file đính kèm
  - Hướng dẫn tích hợp cho frontend

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách upload file đính kèm:

```python
# Upload file đính kèm cho hợp đồng
import requests

def upload_attachment(api_base_url, token, contract_id, file_path, attachment_type, description=None):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    files = {
        'file': open(file_path, 'rb')
    }
    
    data = {
        'type': attachment_type,  # contract, invoice, amendment, other
    }
    
    if description:
        data['description'] = description
    
    response = requests.post(
        f"{api_base_url}/api/v1/contracts/{contract_id}/attachments",
        headers=headers,
        files=files,
        data=data
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 201,
#   "message": "File đã được upload thành công",
#   "data": {
#     "id": "att123",
#     "file_name": "contract_signed.pdf",
#     "file_type": "pdf",
#     "file_size": 1024000,
#     "content_type": "application/pdf",
#     "type": "contract",
#     "description": "Hợp đồng đã ký",
#     "uploaded_by": "user456",
#     "uploaded_at": "2025-05-13T10:30:00Z",
#     "contract_id": "contract123"
#   }
# }
```

Ví dụ về cách lấy danh sách file đính kèm:

```python
# Lấy danh sách file đính kèm của một hợp đồng
import requests

def get_attachments(api_base_url, token, contract_id, attachment_type=None, page=1, size=10):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page': page,
        'size': size
    }
    
    if attachment_type:
        params['type'] = attachment_type
    
    response = requests.get(
        f"{api_base_url}/api/v1/contracts/{contract_id}/attachments",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "attachments": [
#       {
#         "id": "att123",
#         "file_name": "contract_signed.pdf",
#         "file_type": "pdf",
#         "file_size": 1024000,
#         "content_type": "application/pdf",
#         "type": "contract",
#         "description": "Hợp đồng đã ký",
#         "uploaded_by": {
#           "id": "user456",
#           "full_name": "Nguyễn Văn A"
#         },
#         "uploaded_at": "2025-05-13T10:30:00Z",
#         "preview_url": "https://example.com/preview/att123?token=abc123",
#         "download_url": "/api/v1/attachments/att123/download"
#       },
#       {
#         "id": "att456",
#         "file_name": "invoice_001.pdf",
#         "file_type": "pdf",
#         "file_size": 512000,
#         "content_type": "application/pdf",
#         "type": "invoice",
#         "description": "Hóa đơn tạm ứng",
#         "uploaded_by": {
#           "id": "user789",
#           "full_name": "Trần Thị B"
#         },
#         "uploaded_at": "2025-05-13T11:15:00Z",
#         "preview_url": "https://example.com/preview/att456?token=def456",
#         "download_url": "/api/v1/attachments/att456/download"
#       }
#       // ... more attachments
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 10,
#       "total_items": 5,
#       "total_pages": 1
#     }
#   }
# }
```

Ví dụ về cách tải xuống file đính kèm:

```python
# Tải xuống file đính kèm
import requests

def download_attachment(api_base_url, token, attachment_id):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(
        f"{api_base_url}/api/v1/attachments/{attachment_id}/download",
        headers=headers,
        allow_redirects=False  # Để xem redirect URL
    )
    
    if response.status_code == 302:
        # Redirect to pre-signed URL
        download_url = response.headers['Location']
        return download_url
    else:
        # Direct download or error
        return response.json()

# Kết quả mong đợi (nếu sử dụng pre-signed URL):
# Status code 302 với Location header chứa pre-signed URL
# hoặc
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "download_url": "https://your-bucket.s3.amazonaws.com/path/to/file?AWSAccessKeyId=xxx&Signature=xxx&Expires=xxx"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function upload file đính kèm hoạt động chính xác với validation đầy đủ
2. Lambda function lấy danh sách file đính kèm hoạt động chính xác với khả năng filter và phân trang
3. Lambda function tải xuống file đính kèm hoạt động chính xác
4. Lambda function xóa file đính kèm hoạt động chính xác
5. S3 bucket được cấu hình đúng với các chính sách bảo mật phù hợp
6. API Gateway được cấu hình đúng để xử lý binary content và các request lớn
7. IAM Policies tuân thủ principle of least privilege
8. Unit tests đạt coverage > 80%
9. Tài liệu API và quy trình quản lý file đính kèm đầy đủ, chính xác

## Ước tính thời gian

- 4-5 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý đến vấn đề bảo mật khi xử lý file upload, bao gồm kiểm tra loại file, kích thước, và quét virus nếu có thể
- Cần tối ưu việc xử lý file lớn, tránh load toàn bộ file vào memory của Lambda
- Có thể cân nhắc sử dụng S3 multi-part upload cho file lớn
- Cần đảm bảo phân quyền chặt chẽ để người dùng chỉ có thể truy cập file của hợp đồng mà họ có quyền
- Có thể cân nhắc tích hợp với các dịch vụ xem trước file (như AWS Textract cho PDF) để tăng trải nghiệm người dùng 