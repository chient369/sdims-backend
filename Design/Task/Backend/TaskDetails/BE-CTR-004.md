**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda functions quản lý nhân sự trong hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions quản lý nhân sự trong hợp đồng, phục vụ cho việc phân bổ, theo dõi tỷ lệ tham gia và tính toán doanh thu/margin cho nhân sự.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-CTR-004  
**Task Name:** Phát triển Lambda functions quản lý nhân sự trong hợp đồng  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-CTR-001 (Triển khai Lambda functions quản lý hợp đồng)
- BE-HRM-006 (Quản lý trạng thái và phân bổ dự án của nhân viên)

**Các task phụ thuộc vào task này:** 
- BE-MGN-002 (Phát triển Lambda function tính toán revenue)
- BE-MGN-003 (Phát triển Lambda function tính toán margin)

**Các API:**
- GET /api/v1/contracts/{contractId}/resources (API-CTR-013)
- POST /api/v1/contracts/{contractId}/resources (API-CTR-014)
- PUT /api/v1/contracts/resources/{resourceId} (API-CTR-015)
- DELETE /api/v1/contracts/resources/{resourceId} (API-CTR-016)

## Mô tả

Phát triển các Lambda functions để quản lý nhân sự trong hợp đồng, bao gồm các chức năng:
- Lấy danh sách nhân sự đã được phân bổ vào một hợp đồng
- Thêm nhân sự vào hợp đồng với tỷ lệ phân bổ, đơn giá và vai trò
- Cập nhật thông tin phân bổ nhân sự (thay đổi tỷ lệ, đơn giá, giai đoạn)
- Xóa nhân sự khỏi hợp đồng

Chức năng này đóng vai trò quan trọng trong việc theo dõi utilization của nhân sự, tính toán doanh thu và margin. Các API sẽ được bảo mật với các quyền truy cập khác nhau dựa trên vai trò người dùng.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách nhân sự trong hợp đồng

- [ ] Triển khai Lambda function xử lý GET /api/v1/contracts/{contractId}/resources:
  - Location: src/functions/contract_resources/list_resources.py
  - Triển khai logic lấy danh sách nhân sự:
    - Xác thực và phân quyền người dùng
    - Kiểm tra hợp đồng tồn tại
    - Lấy danh sách nhân sự đã phân bổ vào hợp đồng từ DynamoDB
    - Hỗ trợ các tham số filter:
      - employee_id: Lọc theo nhân viên cụ thể
      - role: Lọc theo vai trò trong dự án
      - status: Lọc theo trạng thái phân bổ (active, completed, planned)
      - start_date_from/start_date_to: Lọc theo khoảng thời gian bắt đầu
    - Bổ sung thông tin chi tiết nhân viên (tên, team, v.v.)
    - Tính toán thông tin doanh thu dự kiến cho mỗi nhân sự
    - Hỗ trợ sắp xếp theo nhân viên, vai trò, ngày bắt đầu, v.v.
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function thêm nhân sự vào hợp đồng

- [ ] Triển khai Lambda function xử lý POST /api/v1/contracts/{contractId}/resources:
  - Location: src/functions/contract_resources/add_resource.py
  - Triển khai logic thêm nhân sự:
    - Xác thực và phân quyền (chỉ Admin, Trưởng phòng, Leader có quyền)
    - Validate dữ liệu đầu vào:
      - employee_id: ID của nhân viên
      - role: Vai trò trong dự án
      - allocation_percentage: Tỷ lệ phân bổ (%)
      - start_date: Ngày bắt đầu
      - end_date: Ngày kết thúc (dự kiến)
      - rate: Đơn giá (tùy chọn, phụ thuộc vào quyền)
      - currency: Đơn vị tiền tệ
      - rate_type: Loại đơn giá (monthly, daily, hourly)
      - billing_type: Loại tính phí (T&M, Fixed, Non-billable)
      - notes: Ghi chú bổ sung (tùy chọn)
    - Kiểm tra rằng nhân viên tồn tại
    - Kiểm tra tính khả dụng của nhân viên:
      - Tổng tỷ lệ phân bổ không vượt quá 100% trong cùng thời gian
      - Trạng thái nhân viên phù hợp (không trong thời gian nghỉ dài hạn)
    - Tạo bản ghi phân bổ nhân sự trong DynamoDB
    - Cập nhật thông tin nhân viên (nếu cần)
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: nhân viên không tồn tại, xung đột phân bổ, v.v.
  - Kích hoạt thông báo (nếu cần) về việc phân bổ nhân sự mới

### Phát triển Lambda function cập nhật thông tin phân bổ nhân sự

- [ ] Triển khai Lambda function xử lý PUT /api/v1/contracts/resources/{resourceId}:
  - Location: src/functions/contract_resources/update_resource.py
  - Triển khai logic cập nhật thông tin phân bổ:
    - Xác thực và phân quyền (chỉ Admin, Trưởng phòng, Leader có quyền)
    - Validate dữ liệu đầu vào (tương tự như add_resource)
    - Kiểm tra bản ghi phân bổ tồn tại
    - Kiểm tra các ràng buộc và tính khả dụng (như phân bổ đã tồn tại)
    - Cập nhật thông tin phân bổ trong DynamoDB
    - Xử lý thay đổi đặc biệt:
      - Nếu thay đổi tỷ lệ phân bổ, cập nhật tính toán doanh thu
      - Nếu thay đổi thời gian, kiểm tra xung đột và cập nhật
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột
  - Kích hoạt cập nhật thông tin liên quan (nếu cần)

### Phát triển Lambda function xóa nhân sự khỏi hợp đồng

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/contracts/resources/{resourceId}:
  - Location: src/functions/contract_resources/delete_resource.py
  - Triển khai logic xóa nhân sự:
    - Xác thực và phân quyền (chỉ Admin, Trưởng phòng, Leader có quyền)
    - Kiểm tra bản ghi phân bổ tồn tại
    - Kiểm tra các ràng buộc (ví dụ: có thể có logic không cho phép xóa phân bổ đã kết thúc)
    - Xóa bản ghi phân bổ từ DynamoDB hoặc đánh dấu đã xóa (soft delete)
    - Cập nhật thông tin nhân viên (nếu cần)
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột
  - Kích hoạt cập nhật thông tin liên quan (nếu cần)

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho nhân sự trong hợp đồng:
  - Location: src/models/contract_resource.py
  - Định nghĩa model cho phân bổ nhân sự:
    - Các trường cơ bản: id, contract_id, employee_id, role, allocation_percentage
    - Các trường thời gian: start_date, end_date, actual_end_date
    - Các trường tài chính: rate, currency, rate_type, billing_type
    - Các trường trạng thái: status (active, completed, planned)
    - Các trường theo dõi: created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, deleted_by
  - Triển khai các method truy vấn DynamoDB:
    - create_contract_resource(resource_data)
    - get_contract_resource(resource_id)
    - get_contract_resources(contract_id, filters)
    - update_contract_resource(resource_id, resource_data)
    - delete_contract_resource(resource_id)
    - get_employee_allocations(employee_id, date_from, date_to)
    - calculate_employee_total_allocation(employee_id, date)
    - get_contract_resources_by_period(contract_id, date_from, date_to)

### Phát triển Service Layer

- [ ] Xây dựng service layer cho xử lý nghiệp vụ phân bổ nhân sự:
  - Location: src/services/contract_resource_service.py
  - Implement các phương thức:
    - validate_resource_allocation(employee_id, allocation_percentage, start_date, end_date): Kiểm tra tính khả dụng
    - calculate_expected_revenue(rate, allocation_percentage, start_date, end_date, rate_type): Tính doanh thu dự kiến
    - check_employee_availability(employee_id, start_date, end_date, required_percentage): Kiểm tra nhân viên có khả năng tham gia không
    - calculate_workdays(start_date, end_date): Tính số ngày làm việc trong khoảng thời gian
    - notify_resource_allocation(resource_id, notification_type): Gửi thông báo

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/contracts/{contractId}/resources:
    - Method: GET
    - Path parameter: contractId
    - Các tham số query: employee_id, role, status, start_date_from, start_date_to, sortBy, sortDirection
    - Liên kết với Lambda function list_resources
    - Phân quyền: Authenticated Users với các quyền phù hợp
  - Cấu hình route POST /api/v1/contracts/{contractId}/resources:
    - Method: POST
    - Path parameter: contractId
    - Request body: Thông tin phân bổ nhân sự
    - Liên kết với Lambda function add_resource
    - Phân quyền: Admin, Trưởng phòng, Leader
  - Cấu hình route PUT /api/v1/contracts/resources/{resourceId}:
    - Method: PUT
    - Path parameter: resourceId
    - Request body: Thông tin cập nhật
    - Liên kết với Lambda function update_resource
    - Phân quyền: Admin, Trưởng phòng, Leader
  - Cấu hình route DELETE /api/v1/contracts/resources/{resourceId}:
    - Method: DELETE
    - Path parameter: resourceId
    - Liên kết với Lambda function delete_resource
    - Phân quyền: Admin, Trưởng phòng, Leader
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/contract_resources/
  - Test case cho list_resources.py:
    - Test lấy danh sách nhân sự trong hợp đồng
    - Test các filter khác nhau
    - Test hợp đồng không tồn tại
    - Test phân quyền
  - Test case cho add_resource.py:
    - Test thêm nhân sự thành công
    - Test với nhân viên không tồn tại
    - Test với xung đột phân bổ
    - Test phân quyền
  - Test case cho update_resource.py:
    - Test cập nhật thông tin phân bổ
    - Test với bản ghi không tồn tại
    - Test với xung đột phân bổ
    - Test phân quyền
  - Test case cho delete_resource.py:
    - Test xóa phân bổ nhân sự thành công
    - Test với bản ghi không tồn tại
    - Test phân quyền
  - Test case cho các method trong contract_resource_service.py:
    - Test validate_resource_allocation
    - Test calculate_expected_revenue
    - Test check_employee_availability
    - Test calculate_workdays

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/contracts/{contractId}/resources
    - POST /api/v1/contracts/{contractId}/resources
    - PUT /api/v1/contracts/resources/{resourceId}
    - DELETE /api/v1/contracts/resources/{resourceId}
  - Tài liệu mô tả quy trình phân bổ nhân sự và các trạng thái
  - Tài liệu hướng dẫn tính toán tỷ lệ phân bổ và doanh thu
  - Tài liệu quyền truy cập và sử dụng API

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách nhân sự trong hợp đồng:

```python
# Lấy danh sách nhân sự trong hợp đồng
import requests

def get_contract_resources(api_base_url, token, contract_id, role=None, status='active'):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {}
    
    if role:
        params['role'] = role
    
    if status:
        params['status'] = status
    
    response = requests.get(
        f"{api_base_url}/api/v1/contracts/{contract_id}/resources",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "contract": {
#       "id": "contract123",
#       "contract_code": "CTR-2025-001",
#       "name": "Phát triển phần mềm XYZ"
#     },
#     "resources": [
#       {
#         "id": "resource123",
#         "employee": {
#           "id": "emp456",
#           "full_name": "Nguyễn Văn A",
#           "team": "Development",
#           "position": "Senior Developer"
#         },
#         "role": "Lead Developer",
#         "allocation_percentage": 75,
#         "start_date": "2025-04-01",
#         "end_date": "2025-12-31",
#         "status": "active",
#         "rate": 40,
#         "currency": "USD",
#         "rate_type": "daily",
#         "billing_type": "T&M",
#         "expected_revenue": 6600,  # (40 USD/day * ~22 work days * 9 months * 0.75)
#         "worked_days": 28,
#         "remaining_days": 169
#       },
#       {
#         "id": "resource456",
#         "employee": {
#           "id": "emp789",
#           "full_name": "Trần Thị B",
#           "team": "QA",
#           "position": "QA Engineer"
#         },
#         "role": "QA Engineer",
#         "allocation_percentage": 50,
#         "start_date": "2025-04-15",
#         "end_date": "2025-12-31",
#         "status": "active",
#         "rate": 30,
#         "currency": "USD",
#         "rate_type": "daily",
#         "billing_type": "T&M",
#         "expected_revenue": 3300,  # (30 USD/day * ~22 work days * 8.5 months * 0.5)
#         "worked_days": 20,
#         "remaining_days": 160
#       }
#       // ... more resources
#     ],
#     "summary": {
#       "total_resources": 5,
#       "total_expected_revenue": 18150,
#       "currency": "USD",
#       "active_resources": 5,
#       "completed_resources": 0
#     }
#   }
# }
```

Ví dụ về cách thêm nhân sự vào hợp đồng:

```python
# Thêm nhân sự vào hợp đồng
import requests

def add_contract_resource(api_base_url, token, contract_id, resource_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/contracts/{contract_id}/resources",
        headers=headers,
        json=resource_data
    )
    
    return response.json()

# Dữ liệu đầu vào:
# resource_data = {
#   "employee_id": "emp123",
#   "role": "Frontend Developer",
#   "allocation_percentage": 50,
#   "start_date": "2025-06-01",
#   "end_date": "2025-09-30",
#   "rate": 35,
#   "currency": "USD",
#   "rate_type": "daily",
#   "billing_type": "T&M",
#   "notes": "Hỗ trợ phát triển UI"
# }

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 201,
#   "message": "Nhân sự đã được thêm vào hợp đồng thành công",
#   "data": {
#     "id": "resource789",
#     "contract_id": "contract123",
#     "employee": {
#       "id": "emp123",
#       "full_name": "Lê Văn C"
#     },
#     "role": "Frontend Developer",
#     "allocation_percentage": 50,
#     "start_date": "2025-06-01",
#     "end_date": "2025-09-30",
#     "status": "planned",
#     "created_at": "2025-05-13T10:45:00Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách nhân sự trong hợp đồng hoạt động chính xác với đầy đủ thông tin và khả năng lọc
2. Lambda function thêm nhân sự vào hợp đồng hoạt động chính xác với validation và kiểm tra tính khả dụng
3. Lambda function cập nhật thông tin phân bổ nhân sự hoạt động chính xác
4. Lambda function xóa nhân sự khỏi hợp đồng hoạt động chính xác
5. Service layer xử lý nghiệp vụ phân bổ nhân sự hoạt động chính xác, đặc biệt là việc kiểm tra xung đột và tính toán doanh thu
6. API endpoints được cấu hình đúng với phân quyền phù hợp
7. Unit tests đạt coverage > 80%
8. Tài liệu API và quy trình phân bổ nhân sự đầy đủ, chính xác

## Ước tính thời gian

- 5-6 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý đến logic kiểm tra tính khả dụng của nhân viên khi phân bổ vào hợp đồng
- Tổng tỷ lệ phân bổ của một nhân viên trong cùng thời gian không được vượt quá 100%
- Cần tích hợp chặt chẽ với module quản lý nhân sự (HRM) để có thông tin cập nhật về trạng thái nhân viên
- Việc tính toán doanh thu dự kiến cần dựa trên đơn giá, tỷ lệ phân bổ và số ngày làm việc thực tế trong giai đoạn
- Nên có cơ chế thông báo tự động khi có thay đổi về phân bổ nhân sự
- Cần lưu lịch sử thay đổi để theo dõi các cập nhật về phân bổ nhân sự
</rewritten_file> 