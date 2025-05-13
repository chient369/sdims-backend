**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda function tính toán revenue | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda function tính toán revenue dựa trên dữ liệu phân bổ nhân sự vào dự án và hợp đồng, phục vụ cho việc tính toán margin và phân tích hiệu quả tài chính.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-MGN-002  
**Task Name:** Phát triển Lambda function tính toán revenue  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)
- BE-CTR-001 (Triển khai Lambda functions quản lý hợp đồng)
- BE-CTR-004 (Phát triển Lambda functions quản lý nhân sự trong hợp đồng)

**Các task phụ thuộc vào task này:** 
- BE-MGN-003 (Triển khai Lambda function tính toán margin)
- BE-MGN-004 (Phát triển Lambda functions xem thông tin margin)

**Các API:**
- GET /api/v1/margins/revenues (API-MGN-003)

## Mô tả

Phát triển Lambda function để tính toán revenue (doanh thu) dựa trên dữ liệu phân bổ nhân sự vào các dự án và thông tin hợp đồng liên quan. Revenue là thành phần quan trọng trong việc tính toán margin và đánh giá hiệu quả tài chính của công ty.

Hệ thống sẽ tính toán revenue theo nhiều cách:
1. Scheduled task chạy định kỳ (ví dụ: hàng ngày) để cập nhật dữ liệu revenue tự động
2. API endpoint cho phép người dùng có quyền xem thông tin revenue đã được tính toán

Việc tính toán revenue sẽ dựa trên nhiều yếu tố như: loại hợp đồng (fixed price hay time & material), thời gian làm việc của nhân viên trên dự án, tỷ lệ phân bổ, rate card của từng nhân viên, và các điều khoản thanh toán đặc biệt trong hợp đồng.

## Chi tiết công việc

### Phát triển Lambda function tính toán revenue

- [ ] Triển khai Lambda function xử lý tính toán revenue:
  - Location: src/functions/margins/calculate_revenue.py
  - Triển khai logic tính toán revenue:
    - Lấy dữ liệu phân bổ nhân sự từ bảng PROJECT_ALLOCATIONS trên DynamoDB
    - Lấy thông tin hợp đồng và rate card từ bảng CONTRACTS và CONTRACT_EMPLOYEES
    - Tính toán revenue dựa trên các yếu tố:
      - Loại hợp đồng (Fixed Price, Time & Material)
      - Thời gian làm việc của nhân viên trên dự án
      - Tỷ lệ phân bổ (allocation percentage)
      - Rate card của từng nhân viên
      - Các điều khoản thanh toán đặc biệt
    - Lưu kết quả tính toán vào bảng EMPLOYEE_REVENUES
  - Cài đặt tính toán cho nhiều kỳ (tháng, quý, năm)
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function API endpoint xem revenue

- [ ] Triển khai Lambda function xử lý GET /api/v1/margins/revenues:
  - Location: src/functions/margins/get_revenues.py
  - Triển khai logic lấy dữ liệu revenue:
    - Xác thực và phân quyền người dùng
    - Lấy dữ liệu revenue từ bảng EMPLOYEE_REVENUES
    - Hỗ trợ lọc theo nhiều tiêu chí:
      - Thời gian (từ ngày đến ngày, năm-tháng cụ thể, quý)
      - Nhân viên cụ thể hoặc danh sách nhân viên
      - Team/bộ phận
      - Dự án/hợp đồng
    - Hỗ trợ tổng hợp và phân nhóm dữ liệu (by team, by project, etc.)
    - Hỗ trợ phân trang kết quả
  - Xử lý các trường hợp đặc biệt và tối ưu hiệu năng

### Phát triển Scheduled Task tự động tính toán

- [ ] Triển khai CloudWatch Scheduled Event cho việc tính toán tự động:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình schedule expression (ví dụ: cron(0 1 * * ? *) - 1 AM hàng ngày)
  - Liên kết với Lambda function calculate_revenue
  - Cấu hình tham số để chỉ tính toán cho ngày hiện tại/ngày trước đó
  - Cấu hình retry và dead-letter queue

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho revenue:
  - Location: src/models/employee_revenue.py
  - Định nghĩa model cho revenue:
    - Các trường cơ bản: employee_id, year_month, project_id, contract_id, allocation_percentage, billable_days, rate, revenue_amount, etc.
  - Triển khai các method truy vấn DynamoDB:
    - create_or_update_revenue(employee_id, year_month, project_id, revenue_data)
    - get_employee_revenue(employee_id, year_month, project_id)
    - get_employee_revenues(filters)
    - get_aggregated_revenues(groupBy, filters)

### Phát triển Business Logic Layer

- [ ] Triển khai lớp business logic cho tính toán revenue:
  - Location: src/services/revenue_calculator.py
  - Triển khai các method tính toán:
    - calculate_fixed_price_revenue(contract, allocations, period)
    - calculate_time_material_revenue(contract, allocations, rates, period)
    - calculate_special_terms_revenue(contract, terms, period)
    - aggregate_revenue_by_employee(revenues)
    - aggregate_revenue_by_team(revenues)
    - aggregate_revenue_by_project(revenues)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/margins/revenues:
    - Method: GET
    - Các tham số query: teamId, period, fromDate, toDate, yearMonth, yearQuarter, year, groupBy, employeeId, projectId, etc.
    - Liên kết với Lambda function get_revenues
    - Phân quyền: Admin, Division Manager, Team Leader
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/margins/
  - Test case cho calculate_revenue.py:
    - Test tính toán revenue cho fixed price
    - Test tính toán revenue cho time & material
    - Test với các điều khoản đặc biệt
    - Test xử lý lỗi
  - Test case cho get_revenues.py:
    - Test lấy dữ liệu revenue với các filter khác nhau
    - Test phân trang
    - Test tổng hợp và phân nhóm
    - Test phân quyền
  - Test case cho các service:
    - Test revenue_calculator với các trường hợp khác nhau

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho endpoint:
    - GET /api/v1/margins/revenues
  - Tài liệu mô tả thuật toán tính toán revenue
  - Tài liệu các quy tắc nghiệp vụ liên quan đến revenue

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy thông tin revenue:

```python
# Lấy thông tin revenue theo team và kỳ báo cáo
import requests

def get_team_revenues(api_base_url, token, team_id=None, period='month', year_month=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'period': period
    }
    
    if team_id:
        params['teamId'] = team_id
    
    if year_month:
        params['yearMonth'] = year_month
    
    response = requests.get(
        f"{api_base_url}/api/v1/margins/revenues",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "period": {
#       "type": "month",
#       "yearMonth": "2025-05",
#       "startDate": "2025-05-01",
#       "endDate": "2025-05-31"
#     },
#     "summary": {
#       "totalRevenue": 500000000,
#       "averageRatePerDay": 2500000,
#       "totalEmployees": 25,
#       "totalProjects": 8
#     },
#     "details": [
#       {
#         "teamId": "team123",
#         "teamName": "Java Team",
#         "employees": [
#           {
#             "employeeId": "emp456",
#             "employeeName": "Nguyễn Văn A",
#             "position": "Senior Developer",
#             "revenue": 25000000,
#             "billableDays": 20,
#             "projects": [
#               {
#                 "projectId": "proj789",
#                 "projectName": "Banking System",
#                 "contractId": "con123",
#                 "allocation": 100,
#                 "billableDays": 20,
#                 "rate": 1250000,
#                 "revenue": 25000000
#               }
#             ]
#           },
#           // ... more employees
#         ],
#         "teamRevenue": 120000000,
#         "teamBillableDays": 95
#       },
#       // ... more teams
#     ],
#     "pagination": {
#       "page": 1,
#       "pageSize": 10,
#       "totalItems": 5,
#       "totalPages": 1
#     }
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function tính toán revenue hoạt động chính xác cho các loại hợp đồng khác nhau
2. Scheduled task tự động tính toán revenue chạy đúng lịch và xử lý lỗi phù hợp
3. API endpoint GET /api/v1/margins/revenues trả về dữ liệu đúng với các tùy chọn lọc và phân nhóm
4. Xử lý phân quyền đúng (Admin, Division Manager, Team Leader có quyền xem khác nhau)
5. Hỗ trợ tổng hợp và phân nhóm dữ liệu theo nhiều tiêu chí
6. Unit tests đạt coverage > 80%
7. Tài liệu API và tài liệu kỹ thuật đầy đủ

## Ước tính thời gian

- 4-5 ngày làm việc

## Ghi chú

- Công thức tính revenue có thể phức tạp và thay đổi theo loại hợp đồng, cần tham khảo kỹ các ràng buộc từ bộ phận tài chính
- Cần đảm bảo hiệu năng khi xử lý dữ liệu lớn, đặc biệt khi tổng hợp theo team/project
- Xem xét việc caching kết quả tính toán để tránh tính lại nhiều lần
- Cho phép điều chỉnh thủ công kết quả tính toán trong trường hợp cần thiết
- Lưu ý về sự chính xác khi làm việc với số thập phân và tiền tệ 