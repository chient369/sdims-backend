**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý hợp đồng (CRUD), phục vụ cho việc theo dõi, quản lý thông tin hợp đồng và doanh thu trong hệ thống.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-CTR-001  
**Task Name:** Triển khai Lambda functions quản lý hợp đồng (CRUD)  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-OPP-003 (Triển khai Lambda functions quản lý cơ hội)

**Các task phụ thuộc vào task này:** 
- BE-CTR-002 (Phát triển Lambda functions quản lý điều khoản thanh toán)
- BE-CTR-003 (Triển khai Lambda functions quản lý file đính kèm)
- BE-CTR-004 (Phát triển Lambda functions quản lý nhân sự trong hợp đồng)
- BE-CTR-005 (Triển khai Lambda functions quản lý KPI doanh thu)
- BE-MGN-002 (Phát triển Lambda function tính toán revenue)

**Các API:**
- GET /api/v1/contracts (API-CTR-001)
- POST /api/v1/contracts (API-CTR-002)
- GET /api/v1/contracts/{contractId} (API-CTR-003)
- PUT /api/v1/contracts/{contractId} (API-CTR-004)
- DELETE /api/v1/contracts/{contractId} (API-CTR-005)

## Mô tả

Triển khai các Lambda functions để quản lý thông tin hợp đồng trong hệ thống, bao gồm các chức năng:
- Lấy danh sách hợp đồng (có phân trang, lọc, tìm kiếm)
- Thêm hợp đồng mới
- Xem thông tin chi tiết hợp đồng
- Cập nhật thông tin hợp đồng
- Xóa hợp đồng (soft delete)

Các API sẽ được bảo mật với các quyền truy cập khác nhau dựa trên vai trò người dùng. Việc quản lý hợp đồng sẽ có ảnh hưởng đến các phần khác của hệ thống như tính toán doanh thu, margin, và KPI sales.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách hợp đồng

- [ ] Triển khai Lambda function xử lý GET /api/v1/contracts:
  - Location: src/functions/contracts/list_contracts.py
  - Triển khai logic lấy danh sách hợp đồng:
    - Xác thực và phân quyền người dùng
    - Hỗ trợ các tham số filter:
      - status: Lọc theo trạng thái hợp đồng
      - customer_name: Tìm theo tên khách hàng
      - start_date_from/start_date_to: Lọc theo khoảng thời gian bắt đầu
      - end_date_from/end_date_to: Lọc theo khoảng thời gian kết thúc
      - contract_type: Lọc theo loại hợp đồng
      - sales_person_id: Lọc theo người bán hàng
      - team_id: Lọc theo team
    - Hỗ trợ tìm kiếm theo từ khóa: searchText (tìm theo tên, mã hợp đồng)
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy, sortDirection
    - Truy vấn DynamoDB với các Global Secondary Index phù hợp
    - Lọc dữ liệu hợp đồng theo quyền của người dùng
  - Thiết kế tối ưu truy vấn, đảm bảo hiệu năng khi số lượng hợp đồng lớn
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function thêm hợp đồng mới

- [ ] Triển khai Lambda function xử lý POST /api/v1/contracts:
  - Location: src/functions/contracts/create_contract.py
  - Triển khai logic thêm hợp đồng mới:
    - Xác thực và phân quyền (chỉ Admin, Trưởng phòng, Sales được phép)
    - Validate dữ liệu đầu vào:
      - Thông tin cơ bản: contract_code, name, description, customer_name, customer_contact, v.v.
      - Thông tin tài chính: total_value, currency, contract_type, billing_cycle
      - Thông tin thời gian: sign_date, start_date, end_date
      - Thông tin quản lý: sales_person_id, account_manager_id, team_id, v.v.
    - Tạo ID duy nhất cho hợp đồng
    - Thiết lập giá trị mặc định cho các trường: status (Draft), created_at, updated_at
    - Lưu thông tin hợp đồng vào DynamoDB
    - Xử lý liên kết với cơ hội nếu có opportunity_id
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: trùng mã hợp đồng, dữ liệu không hợp lệ
  - Gửi thông báo (nếu cần) về việc thêm hợp đồng mới

### Phát triển Lambda function xem chi tiết hợp đồng

- [ ] Triển khai Lambda function xử lý GET /api/v1/contracts/{contractId}:
  - Location: src/functions/contracts/get_contract.py
  - Triển khai logic lấy chi tiết hợp đồng:
    - Xác thực và phân quyền (kiểm tra quyền xem thông tin hợp đồng)
    - Lấy dữ liệu hợp đồng từ DynamoDB
    - Bổ sung thông tin liên quan:
      - Tóm tắt về điều khoản thanh toán
      - Thông tin tổng quan về trạng thái thanh toán
      - Thông tin cơ hội liên quan (nếu có)
    - Lọc trường thông tin theo quyền người dùng
  - Xử lý trường hợp hợp đồng không tồn tại
  - Ghi log truy cập

### Phát triển Lambda function cập nhật thông tin hợp đồng

- [ ] Triển khai Lambda function xử lý PUT /api/v1/contracts/{contractId}:
  - Location: src/functions/contracts/update_contract.py
  - Triển khai logic cập nhật thông tin hợp đồng:
    - Xác thực và phân quyền (kiểm tra quyền cập nhật hợp đồng)
    - Validate dữ liệu đầu vào
    - Lấy thông tin hiện tại của hợp đồng
    - Kiểm tra và xử lý thay đổi trạng thái hợp đồng (nếu có):
      - Lưu trạng thái trước đó vào previous_status
      - Cập nhật status_change_date
    - Cập nhật các trường được phép theo quyền người dùng
    - Tự động cập nhật updated_at và updated_by
    - Lưu thông tin đã cập nhật vào DynamoDB
    - Ghi log thay đổi (contract_history)
  - Xử lý các trường hợp lỗi và xung đột dữ liệu
  - Kích hoạt cập nhật thông tin liên quan (nếu cần):
    - Cập nhật KPI doanh thu nếu là hợp đồng mới ký
    - Cập nhật doanh thu dự kiến cho tính toán margin

### Phát triển Lambda function xóa hợp đồng

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/contracts/{contractId}:
  - Location: src/functions/contracts/delete_contract.py
  - Triển khai logic xóa mềm (soft delete) hợp đồng:
    - Xác thực và phân quyền (chỉ Admin và Trưởng phòng)
    - Kiểm tra ràng buộc dữ liệu (có thể xóa hay không)
    - Cập nhật is_deleted=true, deleted_at và deleted_by
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột
  - Gửi thông báo (nếu cần) về việc xóa hợp đồng

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho hợp đồng:
  - Location: src/models/contract.py
  - Định nghĩa model cho hợp đồng:
    - Các trường cơ bản: id, contract_code, name, description, customer_name, v.v.
    - Các trường tài chính: total_value, total_value_usd, currency, exchange_rate, v.v.
    - Các trường thời gian: sign_date, start_date, end_date
    - Các trường trạng thái: status, previous_status, status_change_date
    - Các trường liên kết: opportunity_id, project_id, team_id, sales_person_id, v.v.
    - Các trường metadata: created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, deleted_by
  - Triển khai các method truy vấn DynamoDB:
    - create_contract(contract_data)
    - get_contract(contract_id)
    - get_contracts(filters, pagination)
    - update_contract(contract_id, contract_data)
    - delete_contract(contract_id)
    - get_contracts_by_customer(customer_name)
    - get_contracts_by_status(status)
    - get_contracts_by_period(start_date_from, start_date_to)
    - get_contracts_by_sales_person(sales_person_id)

### Phát triển Service Layer

- [ ] Xây dựng service layer cho xử lý nghiệp vụ hợp đồng:
  - Location: src/services/contract_service.py
  - Implement các phương thức:
    - validate_contract_data(contract_data): Kiểm tra và chuẩn hóa dữ liệu hợp đồng
    - convert_currency_to_usd(value, currency, exchange_rate): Quy đổi giá trị hợp đồng sang USD
    - calculate_payment_status(contract_id): Tính toán trạng thái thanh toán của hợp đồng
    - notify_contract_changes(contract_id, change_type): Gửi thông báo khi có thay đổi hợp đồng
    - log_contract_history(contract_id, type, field, old_value, new_value): Ghi log thay đổi hợp đồng

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/contracts:
    - Method: GET
    - Các tham số query: status, customer_name, start_date_from, start_date_to, end_date_from, end_date_to, contract_type, sales_person_id, team_id, searchText, page, size, sortBy, sortDirection
    - Liên kết với Lambda function list_contracts
  - Cấu hình route POST /api/v1/contracts:
    - Method: POST
    - Request body: Thông tin hợp đồng
    - Liên kết với Lambda function create_contract
  - Cấu hình route GET /api/v1/contracts/{contractId}:
    - Method: GET
    - Path parameter: contractId
    - Liên kết với Lambda function get_contract
  - Cấu hình route PUT /api/v1/contracts/{contractId}:
    - Method: PUT
    - Path parameter: contractId
    - Request body: Thông tin cập nhật
    - Liên kết với Lambda function update_contract
  - Cấu hình route DELETE /api/v1/contracts/{contractId}:
    - Method: DELETE
    - Path parameter: contractId
    - Liên kết với Lambda function delete_contract
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/contracts/
  - Test case cho list_contracts.py:
    - Test lấy danh sách với các filter khác nhau
    - Test phân trang
    - Test sắp xếp
    - Test tìm kiếm
    - Test phân quyền
  - Test case cho create_contract.py:
    - Test tạo hợp đồng thành công
    - Test với dữ liệu không hợp lệ
    - Test trùng mã hợp đồng
    - Test phân quyền
  - Test case cho get_contract.py:
    - Test lấy thông tin chi tiết
    - Test hợp đồng không tồn tại
    - Test phân quyền
  - Test case cho update_contract.py:
    - Test cập nhật thành công
    - Test thay đổi trạng thái
    - Test với dữ liệu không hợp lệ
    - Test phân quyền
  - Test case cho delete_contract.py:
    - Test xóa thành công
    - Test xóa hợp đồng không tồn tại
    - Test phân quyền
  - Test case cho các method trong contract_service.py:
    - Test validate_contract_data
    - Test convert_currency_to_usd
    - Test calculate_payment_status
    - Test log_contract_history

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/contracts
    - POST /api/v1/contracts
    - GET /api/v1/contracts/{contractId}
    - PUT /api/v1/contracts/{contractId}
    - DELETE /api/v1/contracts/{contractId}
  - Tài liệu quyền truy cập và sử dụng API
  - Tài liệu mô tả các trạng thái hợp đồng và business rules

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách hợp đồng với các tham số filter:

```python
# Lấy danh sách hợp đồng theo trạng thái và khách hàng
import requests

def get_contracts(api_base_url, token, status=None, customer_name=None, sales_person_id=None, page=1, size=10):
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
    
    if customer_name:
        params['customer_name'] = customer_name
    
    if sales_person_id:
        params['sales_person_id'] = sales_person_id
    
    response = requests.get(
        f"{api_base_url}/api/v1/contracts",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "contracts": [
#       {
#         "id": "contract123",
#         "contract_code": "CTR-2025-001",
#         "name": "Phát triển phần mềm XYZ",
#         "customer_name": "Công ty ABC",
#         "sign_date": "2025-03-15",
#         "start_date": "2025-04-01",
#         "end_date": "2025-12-31",
#         "total_value": 1200000000,
#         "currency": "VND",
#         "status": "Active",
#         "contract_type": "TimeAndMaterial",
#         "sales_person": {
#           "id": "user456",
#           "full_name": "Nguyễn Văn A"
#         },
#         "payment_status": {
#           "status": "partial",
#           "paid_percentage": 25,
#           "next_due_date": "2025-06-01"
#         }
#       },
#       // ... more contracts
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 10,
#       "total_items": 28,
#       "total_pages": 3
#     }
#   }
# }
```

Ví dụ về cách thêm hợp đồng mới:

```python
# Thêm hợp đồng mới
import requests

def create_contract(api_base_url, token, contract_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/contracts",
        headers=headers,
        json=contract_data
    )
    
    return response.json()

# Dữ liệu đầu vào:
# contract_data = {
#   "contract_code": "CTR-2025-005",
#   "name": "Bảo trì hệ thống ERP",
#   "description": "Dịch vụ bảo trì và nâng cấp hệ thống ERP trong 1 năm",
#   "customer_name": "Công ty DEF",
#   "customer_contact": "Lê Thị B",
#   "customer_email": "le.b@company-def.com",
#   "customer_phone": "0987654321",
#   "opportunity_id": "opp789",  # Tùy chọn, liên kết với cơ hội
#   "team_id": "team123",
#   "sign_date": "2025-05-10",
#   "start_date": "2025-06-01",
#   "end_date": "2026-05-31",
#   "total_value": 360000000,
#   "currency": "VND",
#   "exchange_rate": 24500,  # Tỷ giá VND/USD
#   "contract_type": "Maintenance",
#   "billing_cycle": "Quarterly",
#   "sales_person_id": "user456",
#   "account_manager_id": "user789"
# }

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 201,
#   "message": "Hợp đồng đã được tạo thành công",
#   "data": {
#     "id": "contract456",
#     "contract_code": "CTR-2025-005",
#     "name": "Bảo trì hệ thống ERP",
#     "customer_name": "Công ty DEF",
#     "status": "Draft",
#     "created_at": "2025-05-13T10:30:00Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách hợp đồng hoạt động chính xác với đầy đủ chức năng filter, search và phân trang
2. Lambda function thêm hợp đồng mới hoạt động chính xác với validation đầy đủ
3. Lambda function xem chi tiết hợp đồng hoạt động chính xác
4. Lambda function cập nhật thông tin hợp đồng hoạt động chính xác với xử lý thay đổi trạng thái hợp đồng
5. Lambda function xóa hợp đồng (soft delete) hoạt động chính xác
6. Service layer xử lý nghiệp vụ hợp đồng hoạt động chính xác
7. API endpoints được cấu hình đúng với phân quyền
8. Unit tests đạt coverage > 80%
9. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 6-7 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý đến phân quyền truy cập dữ liệu hợp đồng, đảm bảo thông tin nhạy cảm chỉ được xem bởi người có quyền phù hợp
- Khi xóa hợp đồng, cần kiểm tra kỹ các ràng buộc với dự án, điều khoản thanh toán, doanh thu đã ghi nhận
- Quá trình thay đổi trạng thái hợp đồng cần được ghi log chi tiết để theo dõi lịch sử
- Khi tạo hoặc cập nhật hợp đồng, cần cân nhắc việc tự động cập nhật doanh thu thực tế cho KPI sales
- Cần tích hợp chặt chẽ với phần tính toán margin và revenue 