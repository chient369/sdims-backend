**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda functions import/export danh sách nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions cho phép import và export danh sách nhân viên, giúp quản lý dữ liệu nhân sự hiệu quả và tích hợp với các hệ thống khác.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-009  
**Task Name:** Phát triển Lambda functions import/export danh sách nhân viên  
**Độ ưu tiên:** Thấp  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)

**Các task phụ thuộc vào task này:** 
- Không có

**Các API:**
- POST /api/v1/employees/import (API-HRM-022)
- GET /api/v1/employees/export (API-HRM-023)

## Mô tả

Phát triển Lambda functions cho phép import và export danh sách nhân viên trong các định dạng phổ biến như CSV, Excel (XLSX), và JSON. Chức năng này sẽ giúp:
- Nhập dữ liệu nhân viên hàng loạt từ các file
- Xuất dữ liệu nhân viên để sử dụng trong các ứng dụng khác
- Tạo báo cáo định kỳ về danh sách nhân viên
- Đồng bộ dữ liệu với các hệ thống HR khác

Cả hai chức năng import và export đều cần xử lý lượng dữ liệu lớn một cách hiệu quả, hỗ trợ nhiều định dạng file, và có khả năng xác thực dữ liệu để đảm bảo tính toàn vẹn.

## Chi tiết công việc

### Phát triển Lambda function import danh sách nhân viên

- [ ] Triển khai Lambda function xử lý POST /api/v1/employees/import:
  - Location: src/functions/employee_import_export/import_employees.py
  - Triển khai logic import:
    - Xác thực người dùng và phân quyền (Admin, HR Manager)
    - Xử lý upload file từ request
    - Hỗ trợ các định dạng: CSV, XLSX, JSON
    - Validate dữ liệu đầu vào:
      - Kiểm tra định dạng file
      - Kiểm tra cấu trúc cột và dữ liệu bắt buộc
      - Kiểm tra dữ liệu trùng lặp hoặc mâu thuẫn
    - Tạo quy trình import theo batch:
      - Đọc và phân tích dữ liệu theo từng batch
      - Validate từng record
      - Xử lý insert/update vào DynamoDB
      - Theo dõi trạng thái xử lý
    - Tạo báo cáo kết quả import:
      - Số lượng records thành công/thất bại
      - Chi tiết lỗi cho từng record
      - Log toàn bộ quá trình
    - Hỗ trợ import nhiều loại dữ liệu:
      - Thông tin cơ bản nhân viên
      - Skills và proficiency
      - Thông tin liên hệ và vị trí
  - Triển khai cơ chế xử lý bất đồng bộ cho file lớn:
    - Lưu file vào S3
    - Tạo background job để xử lý
    - Cung cấp API kiểm tra tiến độ

### Phát triển Lambda function export danh sách nhân viên

- [ ] Triển khai Lambda function xử lý GET /api/v1/employees/export:
  - Location: src/functions/employee_import_export/export_employees.py
  - Triển khai logic export:
    - Xác thực người dùng và phân quyền (Admin, HR Manager, Division Manager, Team Leader)
    - Xử lý các tham số filter:
      - status: Lọc theo trạng thái
      - teamId: Lọc theo team
      - department: Lọc theo phòng ban
      - position: Lọc theo vị trí
      - includeDetails: Mức độ chi tiết (basic, full, custom)
      - fields: Danh sách các trường cần export (tùy chọn)
    - Hỗ trợ các định dạng xuất: CSV, XLSX, JSON
    - Xử lý tạo file export:
      - Truy vấn dữ liệu từ DynamoDB theo filter
      - Định dạng và chuyển đổi dữ liệu
      - Tạo file theo định dạng yêu cầu
      - Lưu file vào S3 và tạo signed URL để download
    - Hỗ trợ export dữ liệu tùy chỉnh:
      - Chọn các trường cụ thể để export
      - Tùy chỉnh tên cột/header
      - Định dạng dữ liệu theo yêu cầu
  - Triển khai cơ chế xử lý bất đồng bộ cho dataset lớn:
    - Tạo background job để xử lý export
    - Gửi email thông báo khi export hoàn tất
    - Cung cấp link download có thời hạn

### Phát triển Utilities cho Import/Export

- [ ] Xây dựng các utility classes cho xử lý import/export:
  - Location: src/utils/import_export/
  - Triển khai các utility:
    - file_parser.py: Xử lý đọc và phân tích các định dạng file
    - data_validator.py: Kiểm tra tính hợp lệ của dữ liệu
    - format_converter.py: Chuyển đổi giữa các định dạng dữ liệu
    - batch_processor.py: Xử lý dữ liệu theo batch
    - error_handler.py: Xử lý và báo cáo lỗi
    - template_generator.py: Tạo các template file để import

### Phát triển Background Processing Service

- [ ] Triển khai service xử lý background job:
  - Location: src/services/background_processor.py
  - Triển khai các hàm:
    - create_import_job(file_url, options): Tạo job import
    - create_export_job(filters, format, options): Tạo job export
    - process_import_job(job_id): Xử lý job import
    - process_export_job(job_id): Xử lý job export
    - get_job_status(job_id): Lấy trạng thái job
    - notify_job_completion(job_id, result): Thông báo khi job hoàn thành
  - Tích hợp với SQS hoặc Step Functions để quản lý queue và xử lý job

### Cấu hình API Gateway và S3

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route POST /api/v1/employees/import:
    - Method: POST
    - Content-Type: multipart/form-data
    - Request body: file và các options
    - Liên kết với Lambda function import_employees
    - Phân quyền: Admin, HR Manager
  - Cấu hình route GET /api/v1/employees/export:
    - Method: GET
    - Các tham số query: format, status, teamId, department, position, includeDetails, fields
    - Liên kết với Lambda function export_employees
    - Phân quyền: Admin, HR Manager, Division Manager, Team Leader
  - Cấu hình route GET /api/v1/import-export/job/{jobId}:
    - Method: GET
    - Path parameter: jobId
    - Liên kết với Lambda function get_job_status

- [ ] Cấu hình S3 bucket:
  - Location: template.yaml (trong phần Resources)
  - Tạo S3 bucket cho lưu trữ file import/export
  - Cấu hình các policy bảo mật
  - Cấu hình lifecycle policy để tự động xóa file cũ

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/employee_import_export/
  - Test case cho import_employees.py:
    - Test import từ các định dạng file khác nhau
    - Test validate dữ liệu
    - Test xử lý lỗi
    - Test phân quyền
  - Test case cho export_employees.py:
    - Test export ra các định dạng khác nhau
    - Test filter dữ liệu
    - Test custom fields
    - Test phân quyền
  - Test case cho các utility classes

### Tạo Documentation và Templates

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - POST /api/v1/employees/import
    - GET /api/v1/employees/export
  - Tài liệu hướng dẫn cách sử dụng tính năng import/export
  - Tài liệu mô tả cấu trúc file template và quy tắc validate

- [ ] Tạo các template file:
  - Template CSV cho import nhân viên
  - Template Excel cho import nhân viên
  - Mẫu JSON structure

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách import danh sách nhân viên:

```python
# Import danh sách nhân viên
import requests

def import_employees(api_base_url, token, file_path, import_options=None):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    files = {
        'file': open(file_path, 'rb')
    }
    
    data = {}
    if import_options:
        for key, value in import_options.items():
            data[key] = value
    
    response = requests.post(
        f"{api_base_url}/api/v1/employees/import",
        headers=headers,
        files=files,
        data=data
    )
    
    return response.json()

# Ví dụ gọi hàm:
# import_options = {
#     'updateExisting': 'true',  # Cập nhật nếu nhân viên đã tồn tại
#     'validateOnly': 'false',   # Không chỉ validate mà còn import luôn
#     'notifyOnCompletion': 'true'  # Gửi email thông báo khi hoàn tất
# }
# 
# result = import_employees(
#     api_base_url="https://api.example.com",
#     token="your_auth_token",
#     file_path="employees_list.xlsx",
#     import_options=import_options
# )

# Kết quả mong đợi cho import đồng bộ (file nhỏ):
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "import_id": "imp-20250513-001",
#     "summary": {
#       "total_records": 25,
#       "processed": 25,
#       "successful": 23,
#       "failed": 2,
#       "updated": 10,
#       "created": 13
#     },
#     "errors": [
#       {
#         "row": 5,
#         "employee_code": "E005",
#         "error": "Email format is invalid"
#       },
#       {
#         "row": 18,
#         "employee_code": "E018",
#         "error": "Missing required field: position"
#       }
#     ],
#     "import_time": "2025-05-13T10:15:30Z",
#     "initiated_by": {
#       "id": "user123",
#       "name": "Nguyễn Văn A"
#     }
#   }
# }

# Kết quả mong đợi cho import bất đồng bộ (file lớn):
# {
#   "status": "success",
#   "code": 202,
#   "data": {
#     "job_id": "job-20250513-002",
#     "status": "processing",
#     "message": "Import job started. You will be notified when complete.",
#     "check_status_url": "https://api.example.com/api/v1/import-export/job/job-20250513-002"
#   }
# }
```

Ví dụ về cách export danh sách nhân viên:

```python
# Export danh sách nhân viên
import requests

def export_employees(api_base_url, token, export_format='xlsx', filters=None, include_details='basic', fields=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'format': export_format,
        'includeDetails': include_details
    }
    
    if filters:
        for key, value in filters.items():
            params[key] = value
    
    if fields:
        params['fields'] = ','.join(fields)
    
    response = requests.get(
        f"{api_base_url}/api/v1/employees/export",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ gọi hàm:
# filters = {
#     'status': 'Active',
#     'department': 'Engineering',
#     'position': 'Developer'
# }
# 
# fields = [
#     'employee_code', 'full_name', 'email', 'phone', 'position', 
#     'department', 'join_date', 'skills', 'team'
# ]
# 
# result = export_employees(
#     api_base_url="https://api.example.com",
#     token="your_auth_token",
#     export_format='xlsx',
#     filters=filters,
#     include_details='full',
#     fields=fields
# )

# Kết quả mong đợi cho export nhỏ (đồng bộ):
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "export_id": "exp-20250513-001",
#     "file_url": "https://s3.amazonaws.com/bucket-name/exports/employees_20250513_101530.xlsx?signature=...",
#     "expiry_time": "2025-05-14T10:15:30Z",  # URL có hiệu lực trong 24 giờ
#     "record_count": 15,
#     "file_size": 45678,
#     "format": "xlsx",
#     "export_time": "2025-05-13T10:15:30Z",
#     "filters_applied": {
#       "status": "Active",
#       "department": "Engineering",
#       "position": "Developer"
#     }
#   }
# }

# Kết quả mong đợi cho export lớn (bất đồng bộ):
# {
#   "status": "success",
#   "code": 202,
#   "data": {
#     "job_id": "job-20250513-003",
#     "status": "processing",
#     "message": "Export job started. You will be notified when complete.",
#     "check_status_url": "https://api.example.com/api/v1/import-export/job/job-20250513-003"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function import nhân viên hoạt động chính xác, hỗ trợ nhiều định dạng file
2. Lambda function export nhân viên hoạt động chính xác với các tùy chọn filter và format
3. Validate dữ liệu import chính xác và cung cấp báo cáo lỗi chi tiết
4. Xử lý được file lớn thông qua cơ chế bất đồng bộ
5. API endpoints được cấu hình đúng với phân quyền phù hợp
6. Unit tests đạt coverage > 80%
7. Tài liệu API và template file đầy đủ và chính xác

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Hiệu năng là yếu tố quan trọng khi xử lý file lớn, cần tối ưu quá trình đọc/ghi file và tương tác với DynamoDB
- Cần xem xét khả năng mở rộng để hỗ trợ thêm các định dạng file và cấu trúc dữ liệu trong tương lai
- Việc validate dữ liệu trước khi import là rất quan trọng để đảm bảo tính toàn vẹn của dữ liệu
- Template file nên được thiết kế đơn giản và rõ ràng, với các hướng dẫn cho người dùng
- Có thể xem xét thêm tính năng import/export tăng dần hoặc chỉ import/export dữ liệu thay đổi để tối ưu hiệu năng
- Nên lưu log chi tiết quá trình import/export để phục vụ việc kiểm tra và khắc phục sự cố 