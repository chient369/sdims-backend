**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda functions quản lý trạng thái nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions quản lý trạng thái nhân viên, bao gồm việc cập nhật trạng thái làm việc hiện tại và phân bổ vào dự án, nhằm theo dõi hiệu quả nguồn lực trong công ty.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-007  
**Task Name:** Phát triển Lambda functions quản lý trạng thái nhân viên  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)

**Các task phụ thuộc vào task này:** 
- BE-HRM-005 (Phát triển Lambda function tìm kiếm nhân viên theo skills)
- BE-HRM-006 (Triển khai Lambda function gợi ý nhân sự phù hợp)
- BE-CTR-004 (Phát triển Lambda functions quản lý nhân sự trong hợp đồng)
- BE-RPT-001 (Phát triển Lambda function lấy dữ liệu tổng hợp cho dashboard)

**Các API:**
- PUT /api/v1/employees/{id}/status (API-HRM-019)
- GET /api/v1/employees/statuses (API-HRM-020)

## Mô tả

Phát triển Lambda functions cho phép quản lý trạng thái của nhân viên trong hệ thống. Trạng thái nhân viên bao gồm các thông tin như:
- Trạng thái làm việc hiện tại (Available, Allocated, PartiallyAllocated, OnLeave, EndingSoon, Resigned)
- Thông tin phân bổ vào dự án (nếu có)
- Tỷ lệ phân bổ thời gian (allocation percentage)
- Thời gian khả dụng (availability date)
- Lịch sử thay đổi trạng thái

Các trạng thái này rất quan trọng để theo dõi nguồn lực của công ty, hỗ trợ tìm kiếm nhân viên phù hợp cho dự án mới và phân tích hiệu quả sử dụng nhân sự. API sẽ cho phép cập nhật trạng thái và cũng hỗ trợ lấy danh sách nhân viên theo trạng thái.

## Chi tiết công việc

### Phát triển Lambda function cập nhật trạng thái nhân viên

- [ ] Triển khai Lambda function xử lý PUT /api/v1/employees/{id}/status:
  - Location: src/functions/employee_status/update_employee_status.py
  - Triển khai logic cập nhật trạng thái:
    - Xác thực và phân quyền (Admin, HR Manager, Division Manager, Team Leader)
    - Validate dữ liệu đầu vào từ request body:
      - status: Trạng thái mới (Available, Allocated, PartiallyAllocated, OnLeave, EndingSoon, Resigned)
      - project_id: ID dự án (nếu status là Allocated hoặc PartiallyAllocated)
      - project_name: Tên dự án (optional, để hiển thị)
      - allocation_percentage: Tỷ lệ phân bổ thời gian (0-100%)
      - availability_date: Ngày khả dụng tiếp theo
      - note: Ghi chú về thay đổi trạng thái
    - Lưu trạng thái mới vào DynamoDB:
      - Cập nhật bảng EMPLOYEES
      - Tạo bản ghi mới trong bảng EMPLOYEE_STATUS_HISTORY
    - Xử lý các trường hợp đặc biệt:
      - Nếu trạng thái mới là Resigned, cập nhật các trường liên quan (end_date, etc.)
      - Nếu trạng thái thay đổi từ Allocated/PartiallyAllocated sang Available, xóa thông tin project_id
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột trạng thái
  - Triển khai cơ chế thông báo khi có thay đổi trạng thái quan trọng

### Phát triển Lambda function lấy danh sách nhân viên theo trạng thái

- [ ] Triển khai Lambda function xử lý GET /api/v1/employees/statuses:
  - Location: src/functions/employee_status/list_employee_statuses.py
  - Triển khai logic lấy danh sách:
    - Xác thực và phân quyền (tùy vào vai trò, có thể xem một phần hoặc toàn bộ)
    - Xử lý các tham số filter:
      - status: Lọc theo trạng thái cụ thể
      - teamId: Lọc theo team
      - projectId: Lọc theo dự án
      - minAllocation: Tỷ lệ phân bổ tối thiểu
      - availableFrom: Khả dụng từ ngày
      - availableTo: Khả dụng đến ngày
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy, sortDirection
    - Truy vấn DynamoDB sử dụng Global Secondary Index
    - Tổng hợp thống kê về số lượng nhân viên theo trạng thái
  - Tối ưu hiệu năng truy vấn
  - Xử lý lỗi và logging

### Phát triển Event-Driven Status Updates

- [ ] Triển khai cơ chế cập nhật trạng thái tự động dựa trên sự kiện:
  - Location: src/functions/employee_status/handle_status_events.py
  - Triển khai các logic xử lý sự kiện:
    - Cập nhật trạng thái EndingSoon khi dự án sắp kết thúc
    - Tự động chuyển trạng thái từ OnLeave sang Available khi hết thời gian nghỉ
    - Cập nhật trạng thái khi nhân viên được thêm vào hoặc xóa khỏi dự án
  - Tích hợp với CloudWatch Events để định kỳ kiểm tra và cập nhật trạng thái
  - Tích hợp với DynamoDB Streams để phản ứng với thay đổi dữ liệu

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho employee status:
  - Location: src/models/employee_status.py
  - Định nghĩa model cho trạng thái nhân viên:
    - Các trường cơ bản: employee_id, status, project_id, project_name, allocation_percentage, availability_date, updated_at, updated_by, notes, v.v.
  - Triển khai các method truy vấn DynamoDB:
    - update_employee_status(employee_id, status_data)
    - get_employee_current_status(employee_id)
    - get_employees_by_status(status, filters, pagination)
    - get_employee_status_history(employee_id, from_date, to_date)
    - add_status_history_record(employee_id, old_status, new_status, update_details)
    - get_status_statistics(filters)
    - get_employees_by_project(project_id)

### Phát triển Status Validation Service

- [ ] Xây dựng service xác thực các chuyển đổi trạng thái hợp lệ:
  - Location: src/services/status_validation.py
  - Triển khai các hàm:
    - validate_status_transition(current_status, new_status)
    - validate_status_data(status, status_data)
    - check_project_validity(project_id)
    - check_allocation_conflicts(employee_id, project_id, allocation_percentage)
    - handle_special_transitions(employee_id, current_status, new_status)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route PUT /api/v1/employees/{id}/status:
    - Method: PUT
    - Path parameter: id (employee_id)
    - Request body: Thông tin trạng thái mới
    - Liên kết với Lambda function update_employee_status
    - Phân quyền: Admin, HR Manager, Division Manager, Team Leader
  - Cấu hình route GET /api/v1/employees/statuses:
    - Method: GET
    - Các tham số query: status, teamId, projectId, minAllocation, availableFrom, availableTo, page, size, sortBy, sortDirection
    - Liên kết với Lambda function list_employee_statuses
    - Phân quyền: Admin, HR Manager, Division Manager, Team Leader (với phạm vi quyền khác nhau)
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/employee_status/
  - Test case cho update_employee_status.py:
    - Test các chuyển đổi trạng thái hợp lệ
    - Test các chuyển đổi trạng thái không hợp lệ
    - Test cập nhật với dữ liệu không hợp lệ
    - Test cập nhật khi có xung đột
    - Test phân quyền
  - Test case cho list_employee_statuses.py:
    - Test lấy danh sách với các filter khác nhau
    - Test phân trang
    - Test sắp xếp
    - Test phân quyền
  - Test case cho handle_status_events.py:
    - Test cập nhật tự động trạng thái EndingSoon
    - Test cập nhật tự động từ OnLeave sang Available
    - Test xử lý sự kiện thay đổi dự án

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - PUT /api/v1/employees/{id}/status
    - GET /api/v1/employees/statuses
  - Tài liệu về các trạng thái nhân viên và luồng chuyển đổi hợp lệ
  - Tài liệu về quy trình cập nhật trạng thái tự động
  - Hướng dẫn sử dụng API với các scenarios thực tế

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách cập nhật trạng thái nhân viên:

```python
# Cập nhật trạng thái nhân viên
import requests

def update_employee_status(api_base_url, token, employee_id, status_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.put(
        f"{api_base_url}/api/v1/employees/{employee_id}/status",
        headers=headers,
        json=status_data
    )
    
    return response.json()

# Ví dụ gọi hàm để phân bổ nhân viên vào dự án:
# status_data = {
#     "status": "Allocated",
#     "project_id": "proj123",
#     "project_name": "Banking System",
#     "allocation_percentage": 100,
#     "availability_date": "2025-09-30",  # Dự kiến khả dụng sau khi dự án kết thúc
#     "note": "Assigned to Banking System project as technical lead"
# }
# 
# result = update_employee_status(
#     api_base_url="https://api.example.com",
#     token="your_auth_token",
#     employee_id="emp123",
#     status_data=status_data
# )

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "message": "Trạng thái nhân viên đã được cập nhật thành công",
#   "data": {
#     "employee": {
#       "id": "emp123",
#       "employee_code": "E001",
#       "full_name": "Nguyễn Văn A"
#     },
#     "previous_status": {
#       "status": "Available",
#       "updated_at": "2025-05-01T09:00:00Z"
#     },
#     "current_status": {
#       "status": "Allocated",
#       "project_id": "proj123",
#       "project_name": "Banking System",
#       "allocation_percentage": 100,
#       "availability_date": "2025-09-30",
#       "updated_at": "2025-05-13T16:30:00Z",
#       "updated_by": {
#         "id": "user456",
#         "name": "Trần Thị B"
#       },
#       "note": "Assigned to Banking System project as technical lead"
#     }
#   }
# }
```

Ví dụ về cách lấy danh sách nhân viên theo trạng thái:

```python
# Lấy danh sách nhân viên theo trạng thái
import requests

def get_employees_by_status(api_base_url, token, status=None, team_id=None, available_from=None, 
                          min_allocation=None, page=1, size=20):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page': page,
        'size': size
    }
    
    if status:
        params['status'] = status
    
    if team_id:
        params['teamId'] = team_id
    
    if available_from:
        params['availableFrom'] = available_from
    
    if min_allocation:
        params['minAllocation'] = min_allocation
    
    response = requests.get(
        f"{api_base_url}/api/v1/employees/statuses",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ gọi hàm để lấy nhân viên sắp kết thúc dự án:
# result = get_employees_by_status(
#     api_base_url="https://api.example.com",
#     token="your_auth_token",
#     status="EndingSoon",
#     available_from="2025-06-01"
# )

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "statistics": {
#       "Available": 10,
#       "Allocated": 45,
#       "PartiallyAllocated": 15,
#       "OnLeave": 3,
#       "EndingSoon": 7,
#       "Resigned": 2
#     },
#     "employees": [
#       {
#         "id": "emp234",
#         "employee_code": "E002",
#         "full_name": "Lê Minh C",
#         "position": "Senior Developer",
#         "team": {
#           "id": "team789",
#           "name": "Mobile Team"
#         },
#         "status": {
#           "status": "EndingSoon",
#           "project_id": "proj456",
#           "project_name": "Mobile Banking App",
#           "allocation_percentage": 100,
#           "availability_date": "2025-06-15",
#           "updated_at": "2025-05-10T10:15:00Z"
#         },
#         "skills": ["React Native", "TypeScript", "Mobile Development"],
#         "contact": {
#           "email": "minh.c@company.com",
#           "phone": "0901234567"
#         }
#       },
#       // ... more employees
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 20,
#       "total_items": 7,
#       "total_pages": 1
#     }
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function cập nhật trạng thái nhân viên hoạt động chính xác
2. Lambda function lấy danh sách nhân viên theo trạng thái hoạt động chính xác với đầy đủ các tham số filter
3. Cơ chế cập nhật trạng thái tự động dựa trên sự kiện hoạt động đúng
4. Xác thực đúng các luồng chuyển đổi trạng thái hợp lệ
5. API endpoints được cấu hình đúng với phân quyền phù hợp
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Trạng thái nhân viên rất quan trọng đối với việc lên kế hoạch nguồn lực và phân bổ dự án, cần đảm bảo tính chính xác và kịp thời
- Nên có cơ chế thông báo khi có thay đổi trạng thái quan trọng (ví dụ: thông báo cho Project Manager khi nhân viên sắp kết thúc dự án)
- Lưu ý về việc xử lý xung đột khi một nhân viên được phân bổ vào nhiều dự án (trạng thái PartiallyAllocated)
- Cần lưu lịch sử thay đổi trạng thái để có thể theo dõi và phân tích
- Xem xét việc tích hợp với các hệ thống khác như lịch nghỉ phép, calendar để cập nhật trạng thái tự động chính xác hơn 