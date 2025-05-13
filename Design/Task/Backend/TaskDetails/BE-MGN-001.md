**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý chi phí nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý chi phí nhân viên, phục vụ cho việc tính toán margin và theo dõi hiệu suất tài chính.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-MGN-001  
**Task Name:** Triển khai Lambda functions quản lý chi phí nhân viên  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)

**Các task phụ thuộc vào task này:** 
- BE-MGN-003 (Triển khai Lambda function tính toán margin)

**Các API:**
- POST /api/v1/margins/costs/import (API-MGN-001)
- POST /api/v1/margins/costs (API-MGN-002)

## Mô tả

Triển khai các Lambda functions cho phép quản lý chi phí nhân viên trong hệ thống, bao gồm việc nhập liệu thủ công và import dữ liệu từ file. Chi phí nhân viên là thông tin quan trọng để tính toán margin và đánh giá hiệu quả tài chính của dự án và công ty.

Dữ liệu chi phí nhân viên sẽ được cập nhật định kỳ (thường là hàng tháng) và bao gồm các thông tin như: lương cơ bản, phụ cấp, thưởng, các khoản đóng góp bảo hiểm, và các chi phí khác liên quan đến nhân viên.

## Chi tiết công việc

### Phát triển Lambda function nhập/cập nhật chi phí nhân viên

- [ ] Triển khai Lambda function xử lý POST /api/v1/margins/costs:
  - Location: src/functions/margins/update_employee_cost.py
  - Triển khai logic cập nhật chi phí nhân viên:
    - Xác thực và phân quyền (chỉ Admin, Division Manager và Kế toán)
    - Kiểm tra tính hợp lệ của dữ liệu đầu vào
    - Lưu thông tin chi phí vào bảng EMPLOYEE_COSTS trên DynamoDB
    - Cập nhật lịch sử thay đổi
  - Triển khai xử lý cập nhật đồng thời nhiều nhân viên (batch update)
  - Xử lý các trường hợp lỗi và ngoại lệ

### Phát triển Lambda function import chi phí từ file

- [ ] Triển khai Lambda function xử lý POST /api/v1/margins/costs/import:
  - Location: src/functions/margins/import_employee_costs.py
  - Triển khai logic import dữ liệu:
    - Xác thực và phân quyền (chỉ Admin, Division Manager và Kế toán)
    - Xử lý upload file tạm thời lên S3
    - Hỗ trợ các định dạng file: CSV, Excel
    - Đọc và validate dữ liệu từ file
    - Mapping dữ liệu từ file vào cấu trúc EMPLOYEE_COSTS
    - Lưu thông tin chi phí vào DynamoDB
    - Ghi lại lịch sử import và thống kê (số lượng record thành công, thất bại)
  - Triển khai xử lý lỗi và cơ chế rollback khi có lỗi nghiêm trọng
  - Xử lý file dữ liệu lớn (phân trang xử lý)

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho chi phí nhân viên:
  - Location: src/models/employee_cost.py
  - Định nghĩa model cho chi phí nhân viên:
    - Các trường cơ bản: employee_id, year_month, base_salary, allowances, bonuses, insurance, other_costs, total_cost, etc.
  - Triển khai các method truy vấn DynamoDB:
    - create_or_update_cost(employee_id, year_month, cost_data)
    - get_employee_cost(employee_id, year_month)
    - get_employee_costs(employee_ids, from_year_month, to_year_month)
    - batch_update_costs(cost_items)

### Phát triển Utility cho xử lý file

- [ ] Xây dựng utility xử lý file Excel và CSV:
  - Location: src/common/file_utils.py
  - Triển khai các functions:
    - parse_excel_file(file_path, sheet_name)
    - parse_csv_file(file_path, delimiter)
    - validate_cost_data(data)
    - map_file_data_to_model(file_data)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route POST /api/v1/margins/costs:
    - Method: POST
    - Request body: Thông tin chi phí nhân viên
    - Liên kết với Lambda function update_employee_cost
    - Phân quyền: Admin, Division Manager, Kế toán
  - Cấu hình route POST /api/v1/margins/costs/import:
    - Method: POST
    - Request body: Multipart/form-data với file đính kèm
    - Liên kết với Lambda function import_employee_costs
    - Phân quyền: Admin, Division Manager, Kế toán
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/margins/
  - Test case cho update_employee_cost.py:
    - Test cập nhật chi phí thành công
    - Test batch update
    - Test với dữ liệu không hợp lệ
    - Test phân quyền
  - Test case cho import_employee_costs.py:
    - Test import từ file Excel thành công
    - Test import từ file CSV thành công
    - Test với file không hợp lệ
    - Test rollback khi có lỗi
  - Test case cho các utility:
    - Test parse_excel_file
    - Test parse_csv_file
    - Test validate_cost_data

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - POST /api/v1/margins/costs
    - POST /api/v1/margins/costs/import
  - Tài liệu mẫu file import (template)
  - Hướng dẫn sử dụng API và xử lý lỗi

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách cập nhật chi phí nhân viên:

```python
# Cập nhật chi phí cho một nhân viên
import requests

def update_employee_cost(api_base_url, token, employee_id, year_month, cost_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'employee_id': employee_id,
        'year_month': year_month,  # Format: 'YYYY-MM'
        'base_salary': cost_data.get('base_salary', 0),
        'allowances': cost_data.get('allowances', 0),
        'bonuses': cost_data.get('bonuses', 0),
        'insurance': cost_data.get('insurance', 0),
        'other_costs': cost_data.get('other_costs', 0)
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/margins/costs",
        headers=headers,
        json=payload
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "message": "Cập nhật chi phí nhân viên thành công",
#   "data": {
#     "employee_id": "emp123",
#     "employee_name": "Nguyễn Văn A",
#     "year_month": "2025-05",
#     "total_cost": 25000000,
#     "updated_at": "2025-05-13T14:30:00Z",
#     "updated_by": "user456"
#   }
# }
```

Ví dụ về cách import chi phí từ file:

```python
# Import chi phí từ file Excel
import requests

def import_employee_costs(api_base_url, token, file_path):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    with open(file_path, 'rb') as file:
        files = {
            'file': (file_path.split('/')[-1], file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        response = requests.post(
            f"{api_base_url}/api/v1/margins/costs/import",
            headers=headers,
            files=files
        )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "message": "Import chi phí nhân viên thành công",
#   "data": {
#     "total_records": 50,
#     "successful_records": 48,
#     "failed_records": 2,
#     "errors": [
#       {
#         "row": 5,
#         "employee_id": "emp789",
#         "error": "Nhân viên không tồn tại"
#       },
#       {
#         "row": 12,
#         "employee_id": "emp456",
#         "error": "Dữ liệu không hợp lệ: base_salary phải là số dương"
#       }
#     ],
#     "import_id": "imp-20250513-001",
#     "imported_at": "2025-05-13T15:45:30Z",
#     "imported_by": "user456"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function cập nhật chi phí nhân viên hoạt động chính xác
2. Lambda function import chi phí từ file hoạt động chính xác
3. Hỗ trợ đầy đủ các định dạng file (CSV, Excel)
4. Validation dữ liệu đầy đủ và xử lý lỗi hợp lý
5. API endpoints được cấu hình đúng với phân quyền
6. Unit tests đạt coverage > 80%
7. Tài liệu API và template file import đầy đủ

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Đảm bảo tính bảo mật cao cho dữ liệu chi phí nhân viên
- Cần lưu lịch sử thay đổi chi phí để có thể theo dõi và audit
- Xem xét việc thêm chức năng xuất dữ liệu chi phí ra file trong tương lai
- Đảm bảo xử lý hiệu quả với dataset lớn (hàng trăm đến hàng nghìn nhân viên) 