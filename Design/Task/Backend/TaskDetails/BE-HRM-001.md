**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý thông tin nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý thông tin nhân viên (CRUD), phục vụ cho chức năng quản lý nhân sự (HRM) trong hệ thống.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-001  
**Task Name:** Triển khai Lambda functions quản lý thông tin nhân viên (CRUD)  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)

**Các task phụ thuộc vào task này:** 
- BE-HRM-004 (Triển khai Lambda functions quản lý skills của nhân viên)
- BE-HRM-005 (Phát triển Lambda function tìm kiếm nhân viên theo skills)
- BE-HRM-006 (Triển khai Lambda function gợi ý nhân sự phù hợp)
- BE-HRM-007 (Phát triển Lambda functions quản lý trạng thái nhân viên)
- BE-HRM-008 (Triển khai Lambda function xem lịch sử dự án của nhân viên)
- BE-MGN-001 (Triển khai Lambda functions quản lý chi phí nhân viên)

**Các API:**
- GET /api/v1/employees (API-HRM-001)
- POST /api/v1/employees (API-HRM-002)
- GET /api/v1/employees/{employeeId} (API-HRM-003)
- PUT /api/v1/employees/{employeeId} (API-HRM-004)
- DELETE /api/v1/employees/{employeeId} (API-HRM-005)

## Mô tả

Triển khai các Lambda functions để quản lý thông tin nhân viên trong hệ thống, bao gồm các chức năng:
- Lấy danh sách nhân viên (có phân trang, lọc, tìm kiếm)
- Thêm nhân viên mới
- Xem thông tin chi tiết nhân viên
- Cập nhật thông tin nhân viên
- Xóa nhân viên (soft delete)

Các API sẽ được bảo mật với các quyền truy cập khác nhau dựa trên vai trò người dùng. Chỉ Admin và Trưởng phòng có quyền thêm/xóa nhân viên, trong khi Leader có thể cập nhật một số thông tin của nhân viên trong team của họ, và nhân viên chỉ có thể xem hoặc cập nhật một số thông tin cá nhân giới hạn.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách nhân viên (GET /employees)

- [ ] Triển khai Lambda function xử lý GET /api/v1/employees:
  - Location: src/functions/employees/list_employees.py
  - Triển khai logic lấy danh sách nhân viên:
    - Xác thực và phân quyền người dùng
    - Hỗ trợ các tham số filter: teamId, status, position, availabilityDate, skillId
    - Hỗ trợ tìm kiếm: searchText (tìm theo tên, mã nhân viên)
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy, sortDirection
    - Truy vấn DynamoDB với các Global Secondary Index phù hợp
    - Lọc dữ liệu nhân viên theo quyền của người dùng
  - Triển khai việc tối ưu hiệu năng truy vấn
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function thêm nhân viên mới (POST /employees)

- [ ] Triển khai Lambda function xử lý POST /api/v1/employees:
  - Location: src/functions/employees/create_employee.py
  - Triển khai logic thêm nhân viên mới:
    - Xác thực và phân quyền (chỉ Admin và Trưởng phòng)
    - Validate dữ liệu đầu vào
    - Tạo ID duy nhất cho nhân viên
    - Lưu thông tin nhân viên vào DynamoDB
    - Tự động tạo liên kết với user nếu có thông tin user_id
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: trùng lặp employee_code, dữ liệu không hợp lệ
  - Gửi thông báo (nếu cần) về việc thêm nhân viên mới

### Phát triển Lambda function xem chi tiết nhân viên (GET /employees/{employeeId})

- [ ] Triển khai Lambda function xử lý GET /api/v1/employees/{employeeId}:
  - Location: src/functions/employees/get_employee.py
  - Triển khai logic lấy chi tiết nhân viên:
    - Xác thực và phân quyền (kiểm tra quyền xem thông tin nhân viên)
    - Lấy dữ liệu nhân viên từ DynamoDB
    - Bổ sung thêm thông tin liên quan (team, leader, project hiện tại)
    - Lọc trường thông tin theo quyền người dùng
  - Xử lý trường hợp nhân viên không tồn tại
  - Ghi log truy cập

### Phát triển Lambda function cập nhật thông tin nhân viên (PUT /employees/{employeeId})

- [ ] Triển khai Lambda function xử lý PUT /api/v1/employees/{employeeId}:
  - Location: src/functions/employees/update_employee.py
  - Triển khai logic cập nhật thông tin nhân viên:
    - Xác thực và phân quyền (kiểm tra quyền cập nhật thông tin nhân viên)
    - Validate dữ liệu đầu vào
    - Lấy thông tin hiện tại của nhân viên
    - Cập nhật các trường được phép theo quyền người dùng
    - Lưu thông tin đã cập nhật vào DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột dữ liệu
  - Gửi thông báo (nếu cần) về việc cập nhật thông tin nhân viên

### Phát triển Lambda function xóa nhân viên (DELETE /employees/{employeeId})

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/employees/{employeeId}:
  - Location: src/functions/employees/delete_employee.py
  - Triển khai logic xóa mềm (soft delete) nhân viên:
    - Xác thực và phân quyền (chỉ Admin và Trưởng phòng)
    - Kiểm tra ràng buộc dữ liệu (nhân viên đang trong dự án, có liên kết quan trọng)
    - Cập nhật deleted_at và is_deleted cho nhân viên
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột
  - Gửi thông báo (nếu cần) về việc xóa nhân viên

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho nhân viên:
  - Location: src/models/employee.py
  - Định nghĩa model cho nhân viên:
    - Các trường cơ bản: id, user_id, employee_code, first_name, last_name, full_name, birth_date, hire_date, v.v.
    - Các trường trạng thái hiện tại: current_status, current_project_id, current_project_name, allocation_percentage, v.v.
  - Triển khai các method truy vấn DynamoDB:
    - create_employee(employee_data)
    - get_employee(employee_id)
    - get_employees(filters, pagination)
    - update_employee(employee_id, employee_data)
    - delete_employee(employee_id)
    - get_employees_by_team(team_id)
    - get_employees_by_status(status)
    - search_employees(search_text)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/employees:
    - Method: GET
    - Các tham số query: teamId, status, position, availabilityDate, skillId, searchText, page, size, sortBy, sortDirection
    - Liên kết với Lambda function list_employees
  - Cấu hình route POST /api/v1/employees:
    - Method: POST
    - Request body: Thông tin nhân viên
    - Liên kết với Lambda function create_employee
  - Cấu hình route GET /api/v1/employees/{employeeId}:
    - Method: GET
    - Path parameter: employeeId
    - Liên kết với Lambda function get_employee
  - Cấu hình route PUT /api/v1/employees/{employeeId}:
    - Method: PUT
    - Path parameter: employeeId
    - Request body: Thông tin cập nhật
    - Liên kết với Lambda function update_employee
  - Cấu hình route DELETE /api/v1/employees/{employeeId}:
    - Method: DELETE
    - Path parameter: employeeId
    - Liên kết với Lambda function delete_employee
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/employees/
  - Test case cho list_employees.py:
    - Test lấy danh sách với các filter khác nhau
    - Test phân trang
    - Test sắp xếp
    - Test tìm kiếm
    - Test phân quyền
  - Test case cho create_employee.py:
    - Test tạo nhân viên thành công
    - Test với dữ liệu không hợp lệ
    - Test trùng mã nhân viên
    - Test phân quyền
  - Test case cho get_employee.py:
    - Test lấy thông tin chi tiết
    - Test nhân viên không tồn tại
    - Test phân quyền
  - Test case cho update_employee.py:
    - Test cập nhật thành công
    - Test với dữ liệu không hợp lệ
    - Test phân quyền
  - Test case cho delete_employee.py:
    - Test xóa thành công
    - Test xóa nhân viên đang trong dự án
    - Test phân quyền

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/employees
    - POST /api/v1/employees
    - GET /api/v1/employees/{employeeId}
    - PUT /api/v1/employees/{employeeId}
    - DELETE /api/v1/employees/{employeeId}
  - Tài liệu quyền truy cập và sử dụng API
  - Tài liệu mô tả các tham số filter, search và phân trang

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách nhân viên với các tham số filter:

```python
# Lấy danh sách nhân viên theo team và trạng thái
import requests

def get_employees(api_base_url, token, team_id=None, status=None, search_text=None, page=1, size=10):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page': page,
        'size': size
    }
    
    if team_id:
        params['teamId'] = team_id
    
    if status:
        params['status'] = status
    
    if search_text:
        params['searchText'] = search_text
    
    response = requests.get(
        f"{api_base_url}/api/v1/employees",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "employees": [
#       {
#         "id": "emp123",
#         "employee_code": "E001",
#         "full_name": "Nguyễn Văn A",
#         "position": "Senior Developer",
#         "team": {
#           "id": "team456",
#           "name": "Java Team"
#         },
#         "current_status": "Allocated",
#         "current_project": {
#           "id": "proj789",
#           "name": "Banking System"
#         },
#         "allocation_percentage": 100,
#         "skills": ["Java", "Spring Boot", "Microservices"],
#         "margin_status": "GREEN"
#       },
#       // ... more employees
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 10,
#       "total_items": 45,
#       "total_pages": 5
#     }
#   }
# }
```

Ví dụ về cách thêm nhân viên mới:

```python
# Thêm nhân viên mới
import requests

def create_employee(api_base_url, token, employee_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/employees",
        headers=headers,
        json=employee_data
    )
    
    return response.json()

# Dữ liệu đầu vào:
# employee_data = {
#   "employee_code": "E045",
#   "first_name": "Văn",
#   "last_name": "Trần",
#   "birth_date": "1990-05-15",
#   "hire_date": "2023-03-01",
#   "company_email": "van.tran@company.com",
#   "internal_account": "vantran123",
#   "position": "Backend Developer",
#   "team_id": "team456",
#   "phone_number": "0987654321",
#   "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
#   "emergency_contact": {
#     "name": "Trần Thị B",
#     "phone": "0912345678",
#     "relation": "Vợ"
#   }
# }

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 201,
#   "message": "Nhân viên đã được tạo thành công",
#   "data": {
#     "id": "emp456",
#     "employee_code": "E045",
#     "full_name": "Trần Văn",
#     "current_status": "Available",
#     "created_at": "2025-05-13T10:30:00Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách nhân viên hoạt động chính xác với đầy đủ chức năng filter, search và phân trang
2. Lambda function thêm nhân viên mới hoạt động chính xác với validation đầy đủ
3. Lambda function xem chi tiết nhân viên hoạt động chính xác
4. Lambda function cập nhật thông tin nhân viên hoạt động chính xác với phân quyền phù hợp
5. Lambda function xóa nhân viên (soft delete) hoạt động chính xác
6. API endpoints được cấu hình đúng với phân quyền
7. Unit tests đạt coverage > 80%
8. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 5-6 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý đến phân quyền truy cập dữ liệu nhân viên, đảm bảo thông tin nhạy cảm chỉ được xem bởi người có quyền phù hợp
- Trường status của nhân viên có các giá trị: Allocated, Available, EndingSoon, OnLeave, Resigned
- Khi xóa nhân viên, cần kiểm tra kỹ các ràng buộc với dự án, hợp đồng hiện tại
- Nên validate dữ liệu đầu vào kỹ lưỡng, đặc biệt là các trường như email, số điện thoại, ngày tháng
- Cân nhắc việc sử dụng transaction khi cập nhật nhiều thông tin liên quan đến nhân viên 