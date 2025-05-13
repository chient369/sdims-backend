**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda functions quản lý điều khoản thanh toán | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions quản lý điều khoản thanh toán của hợp đồng, phục vụ cho việc theo dõi, quản lý các mốc thanh toán và cập nhật trạng thái thu tiền.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-CTR-002  
**Task Name:** Phát triển Lambda functions quản lý điều khoản thanh toán  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-CTR-001 (Triển khai Lambda functions quản lý hợp đồng)

**Các task phụ thuộc vào task này:** 
- BE-RPT-006 (Lấy báo cáo chi tiết tình trạng thanh toán/công nợ)

**Các API:**
- GET /api/v1/contracts/{contractId}/payment-terms (API-CTR-006)
- PUT /api/v1/contracts/payment-terms/{termId}/status (API-CTR-007)
- POST /api/v1/contracts/payment-terms/import-status (API-CTR-008)

## Mô tả

Phát triển các Lambda functions để quản lý điều khoản thanh toán trong hợp đồng, bao gồm các chức năng:
- Lấy danh sách các điều khoản thanh toán của một hợp đồng
- Cập nhật trạng thái thanh toán cho một điều khoản (đã xuất hóa đơn, đã thanh toán, quá hạn)
- Import trạng thái thanh toán từ file (như file Excel từ kế toán)

Các API này sẽ hỗ trợ việc theo dõi tình trạng thanh toán, báo cáo công nợ và cảnh báo thanh toán sắp đến hạn. Khi cập nhật trạng thái thanh toán, hệ thống sẽ tự động cập nhật thông tin tổng quan về thanh toán trong hợp đồng.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách điều khoản thanh toán

- [ ] Triển khai Lambda function xử lý GET /api/v1/contracts/{contractId}/payment-terms:
  - Location: src/functions/payment_terms/list_payment_terms.py
  - Triển khai logic lấy danh sách điều khoản thanh toán:
    - Xác thực và phân quyền người dùng
    - Kiểm tra hợp đồng tồn tại
    - Lấy danh sách các điều khoản thanh toán của hợp đồng từ DynamoDB
    - Hỗ trợ các tham số filter:
      - status: Lọc theo trạng thái (pending, invoiced, paid, overdue, cancelled)
      - due_date_from/due_date_to: Lọc theo khoảng thời gian đến hạn
    - Hỗ trợ sắp xếp theo term_number, due_date
  - Bổ sung thông tin chi tiết cho mỗi điều khoản thanh toán:
    - Số ngày còn lại đến hạn hoặc số ngày quá hạn
    - Tỷ lệ phần trăm so với tổng giá trị hợp đồng
  - Tổng hợp thông tin thanh toán của hợp đồng (tổng số tiền đã thanh toán, phần trăm thanh toán, v.v.)
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function cập nhật trạng thái thanh toán

- [ ] Triển khai Lambda function xử lý PUT /api/v1/contracts/payment-terms/{termId}/status:
  - Location: src/functions/payment_terms/update_payment_term_status.py
  - Triển khai logic cập nhật trạng thái thanh toán:
    - Xác thực và phân quyền (chỉ Admin, Trưởng phòng, Kế toán có quyền)
    - Validate dữ liệu đầu vào:
      - status: Trạng thái mới (pending, invoiced, paid, overdue, cancelled)
      - invoice_number: Số hóa đơn (cho trạng thái invoiced)
      - invoice_date: Ngày hóa đơn
      - payment_date: Ngày thanh toán (cho trạng thái paid)
      - paid_amount: Số tiền đã thanh toán
      - payment_method: Phương thức thanh toán
      - transaction_reference: Mã giao dịch
      - notes: Ghi chú bổ sung
    - Kiểm tra điều khoản thanh toán tồn tại
    - Kiểm tra logic nghiệp vụ (ví dụ: không thể chuyển từ paid về pending)
    - Cập nhật trạng thái và thông tin liên quan
    - Cập nhật thông tin thanh toán tổng quan trên hợp đồng
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: điều khoản không tồn tại, dữ liệu không hợp lệ, v.v.
  - Kích hoạt thông báo nếu cần (ví dụ: khi thanh toán hoàn tất)

### Phát triển Lambda function import trạng thái thanh toán

- [ ] Triển khai Lambda function xử lý POST /api/v1/contracts/payment-terms/import-status:
  - Location: src/functions/payment_terms/import_payment_term_status.py
  - Triển khai logic import trạng thái thanh toán:
    - Xác thực và phân quyền (chỉ Admin, Trưởng phòng, Kế toán có quyền)
    - Xử lý file đầu vào (excel, csv) từ request
    - Validate cấu trúc file và dữ liệu:
      - Kiểm tra các cột bắt buộc (contract_code/id, term_number/id, status, v.v.)
      - Kiểm tra giá trị hợp lệ cho mỗi cột
    - Xử lý từng dòng dữ liệu trong file:
      - Tìm điều khoản thanh toán tương ứng
      - Cập nhật trạng thái và thông tin liên quan
      - Ghi nhận thành công/thất bại cho mỗi dòng
    - Cập nhật thông tin thanh toán tổng quan trên các hợp đồng liên quan
    - Trả về báo cáo kết quả import (số lượng thành công, thất bại, danh sách lỗi)
  - Xử lý các trường hợp lỗi phổ biến: file không đúng định dạng, dữ liệu không hợp lệ, v.v.
  - Ghi log chi tiết quá trình import
  - Hỗ trợ import theo batch cho file lớn

### Phát triển Lambda function tạo reminder tự động

- [ ] Phát triển Lambda function lập lịch để kiểm tra và gửi reminder:
  - Location: src/functions/scheduled/payment_term_reminder.py
  - Triển khai scheduled Lambda function:
    - Lập lịch chạy hàng ngày qua EventBridge
    - Tìm các điều khoản thanh toán sắp đến hạn (ví dụ: trong 7 ngày tới)
    - Tìm các điều khoản đã quá hạn nhưng chưa được đánh dấu overdue
    - Tự động cập nhật trạng thái overdue cho các điều khoản quá hạn
    - Tạo thông báo cho người liên quan (sales, quản lý, kế toán)
    - Tùy chọn: gửi email nhắc nhở
  - Ghi log quá trình thực thi

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho điều khoản thanh toán:
  - Location: src/models/payment_term.py
  - Định nghĩa model cho điều khoản thanh toán:
    - Các trường cơ bản: id, contract_id, term_number, title, description, due_date, amount, currency, percentage, milestone_description
    - Các trường trạng thái: status, invoice_number, invoice_date, invoice_file_id, payment_date, paid_amount, payment_method, transaction_reference, notes
    - Các trường theo dõi: reminder_sent, last_reminder_date, created_at, updated_at, created_by, updated_by
  - Triển khai các method truy vấn DynamoDB:
    - create_payment_term(payment_term_data)
    - get_payment_term(term_id)
    - get_payment_terms_by_contract(contract_id, filters)
    - update_payment_term(term_id, payment_term_data)
    - update_payment_term_status(term_id, status_data)
    - delete_payment_term(term_id)
    - get_payment_terms_by_status(status)
    - get_payment_terms_by_due_date_range(start_date, end_date)
    - calculate_contract_payment_summary(contract_id)

### Phát triển Service Layer

- [ ] Xây dựng service layer cho xử lý nghiệp vụ điều khoản thanh toán:
  - Location: src/services/payment_term_service.py
  - Implement các phương thức:
    - validate_payment_term_status_update(term_id, new_status, data): Kiểm tra hợp lệ của việc cập nhật trạng thái
    - calculate_days_to_due(due_date): Tính số ngày còn lại đến hạn hoặc quá hạn
    - process_file_import(file_content, file_type): Xử lý file import
    - update_contract_payment_status(contract_id): Cập nhật thông tin thanh toán tổng quan của hợp đồng
    - send_payment_reminder(term_id): Gửi thông báo nhắc nhở thanh toán
    - check_due_payments(): Kiểm tra các điều khoản đến hạn/quá hạn

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/contracts/{contractId}/payment-terms:
    - Method: GET
    - Path parameter: contractId
    - Các tham số query: status, due_date_from, due_date_to, sortBy, sortDirection
    - Liên kết với Lambda function list_payment_terms
    - Phân quyền: Authenticated Users với các quyền phù hợp
  - Cấu hình route PUT /api/v1/contracts/payment-terms/{termId}/status:
    - Method: PUT
    - Path parameter: termId
    - Request body: Thông tin cập nhật trạng thái
    - Liên kết với Lambda function update_payment_term_status
    - Phân quyền: Admin, Trưởng phòng, Kế toán
  - Cấu hình route POST /api/v1/contracts/payment-terms/import-status:
    - Method: POST
    - Request body: Multipart form data với file import
    - Liên kết với Lambda function import_payment_term_status
    - Phân quyền: Admin, Trưởng phòng, Kế toán
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Cấu hình Schedule Event

- [ ] Thiết lập EventBridge schedule cho reminder:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình EventBridge rule chạy hàng ngày:
    - Schedule expression: cron(0 1 * * ? *)  # Chạy lúc 1:00 UTC hàng ngày
    - Target: Lambda function payment_term_reminder
    - Input: {}
  - Cấu hình permission cho EventBridge để invoke Lambda

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/payment_terms/
  - Test case cho list_payment_terms.py:
    - Test lấy danh sách điều khoản thanh toán của hợp đồng
    - Test filter theo status
    - Test filter theo khoảng thời gian
    - Test sắp xếp theo term_number/due_date
    - Test hợp đồng không tồn tại
    - Test phân quyền
  - Test case cho update_payment_term_status.py:
    - Test cập nhật từng loại trạng thái
    - Test cập nhật với dữ liệu không hợp lệ
    - Test ràng buộc giữa các trạng thái
    - Test điều khoản thanh toán không tồn tại
    - Test phân quyền
  - Test case cho import_payment_term_status.py:
    - Test import file hợp lệ
    - Test import file không đúng cấu trúc
    - Test import với dữ liệu không hợp lệ
    - Test phân quyền
  - Test case cho payment_term_reminder.py:
    - Test tìm các điều khoản sắp đến hạn
    - Test cập nhật trạng thái overdue
    - Test tạo thông báo
  - Test case cho các method trong payment_term_service.py:
    - Test validate_payment_term_status_update
    - Test calculate_days_to_due
    - Test process_file_import
    - Test update_contract_payment_status

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/contracts/{contractId}/payment-terms
    - PUT /api/v1/contracts/payment-terms/{termId}/status
    - POST /api/v1/contracts/payment-terms/import-status
  - Tài liệu mô tả quy trình quản lý thanh toán và trạng thái các điều khoản
  - Tài liệu hướng dẫn cấu trúc file import và cách thực hiện import
  - Tài liệu quyền truy cập và sử dụng API

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách điều khoản thanh toán của một hợp đồng:

```python
# Lấy danh sách điều khoản thanh toán của một hợp đồng
import requests

def get_payment_terms(api_base_url, token, contract_id, status=None, due_date_from=None, due_date_to=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {}
    
    if status:
        params['status'] = status
    
    if due_date_from:
        params['due_date_from'] = due_date_from
    
    if due_date_to:
        params['due_date_to'] = due_date_to
    
    response = requests.get(
        f"{api_base_url}/api/v1/contracts/{contract_id}/payment-terms",
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
#       "name": "Phát triển phần mềm XYZ",
#       "total_value": 1200000000,
#       "currency": "VND",
#       "payment_summary": {
#         "total_terms": 4,
#         "paid_amount": 300000000,
#         "paid_percentage": 25,
#         "remaining_amount": 900000000,
#         "next_due_date": "2025-06-01",
#         "next_due_amount": 300000000
#       }
#     },
#     "payment_terms": [
#       {
#         "id": "term123",
#         "term_number": 1,
#         "title": "Tạm ứng",
#         "description": "Thanh toán đặt cọc khi ký hợp đồng",
#         "due_date": "2025-04-01",
#         "amount": 300000000,
#         "currency": "VND",
#         "percentage": 25,
#         "milestone_description": "Ký hợp đồng",
#         "status": "paid",
#         "invoice_number": "INV-2025-001",
#         "invoice_date": "2025-04-02",
#         "payment_date": "2025-04-05",
#         "paid_amount": 300000000,
#         "days_status": "completed",
#         "created_at": "2025-03-15T10:30:00Z",
#         "updated_at": "2025-04-05T14:15:00Z"
#       },
#       {
#         "id": "term456",
#         "term_number": 2,
#         "title": "Milestone 1",
#         "description": "Hoàn thành phân tích yêu cầu và thiết kế",
#         "due_date": "2025-06-01",
#         "amount": 300000000,
#         "currency": "VND",
#         "percentage": 25,
#         "milestone_description": "Bàn giao tài liệu thiết kế",
#         "status": "pending",
#         "days_to_due": 18,
#         "days_status": "upcoming",
#         "created_at": "2025-03-15T10:30:00Z",
#         "updated_at": "2025-03-15T10:30:00Z"
#       },
#       // ... more payment terms
#     ]
#   }
# }
```

Ví dụ về cách cập nhật trạng thái điều khoản thanh toán:

```python
# Cập nhật trạng thái điều khoản thanh toán
import requests

def update_payment_term_status(api_base_url, token, term_id, status_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.put(
        f"{api_base_url}/api/v1/contracts/payment-terms/{term_id}/status",
        headers=headers,
        json=status_data
    )
    
    return response.json()

# Dữ liệu đầu vào (ví dụ đánh dấu đã xuất hóa đơn):
# status_data = {
#   "status": "invoiced",
#   "invoice_number": "INV-2025-005",
#   "invoice_date": "2025-05-13",
#   "notes": "Đã xuất hóa đơn, chờ thanh toán trong 15 ngày"
# }

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "message": "Trạng thái điều khoản thanh toán đã được cập nhật thành công",
#   "data": {
#     "id": "term456",
#     "term_number": 2,
#     "contract_id": "contract123",
#     "status": "invoiced",
#     "previous_status": "pending",
#     "invoice_number": "INV-2025-005",
#     "invoice_date": "2025-05-13",
#     "updated_at": "2025-05-13T11:20:00Z"
#   }
# }
```

Ví dụ về cách import trạng thái thanh toán từ file:

```python
# Import trạng thái thanh toán từ file
import requests

def import_payment_term_status(api_base_url, token, file_path):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    files = {
        'file': ('payment_status.xlsx', open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/contracts/payment-terms/import-status",
        headers=headers,
        files=files
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "message": "Import trạng thái thanh toán hoàn tất",
#   "data": {
#     "total_records": 15,
#     "success_count": 13,
#     "failed_count": 2,
#     "errors": [
#       {
#         "row": 5,
#         "message": "Điều khoản thanh toán không tồn tại"
#       },
#       {
#         "row": 12,
#         "message": "Dữ liệu không hợp lệ: Ngày thanh toán thiếu"
#       }
#     ],
#     "updated_contracts": [
#       {
#         "id": "contract123",
#         "contract_code": "CTR-2025-001",
#         "updated_terms": 2
#       },
#       {
#         "id": "contract456",
#         "contract_code": "CTR-2025-002",
#         "updated_terms": 3
#       }
#       // ... more contracts
#     ]
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách điều khoản thanh toán hoạt động chính xác với khả năng lọc theo trạng thái và khoảng thời gian
2. Lambda function cập nhật trạng thái thanh toán hoạt động chính xác với validation đầy đủ
3. Lambda function import trạng thái thanh toán từ file hoạt động chính xác, hỗ trợ định dạng Excel/CSV
4. Lambda function reminder tự động hoạt động theo lịch và cảnh báo chính xác
5. Cơ chế cập nhật tổng quan về thanh toán trong hợp đồng hoạt động chính xác
6. API endpoints được cấu hình đúng với phân quyền phù hợp
7. EventBridge schedule được cấu hình đúng cho reminder
8. Unit tests đạt coverage > 80%
9. Tài liệu API và quy trình quản lý thanh toán đầy đủ, chính xác

## Ước tính thời gian

- 5-6 ngày làm việc

## Ghi chú

- Cần thiết kế cấu trúc file import linh hoạt nhưng đủ thông tin để cập nhật đúng điều khoản thanh toán
- Quá trình cập nhật trạng thái thanh toán cần ghi log chi tiết để phục vụ audit
- Cần có cơ chế đồng bộ với kế toán, đảm bảo thông tin thanh toán chính xác
- Chức năng reminder cần có khả năng cấu hình thời gian cảnh báo (ví dụ: 7 ngày, 3 ngày trước khi đến hạn)
- Cần xử lý các trường hợp thanh toán một phần, nhiều lần thanh toán cho một điều khoản 