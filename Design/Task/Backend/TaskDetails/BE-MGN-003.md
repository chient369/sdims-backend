**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function tính toán margin | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function tính toán margin từ dữ liệu chi phí (cost) và doanh thu (revenue), cung cấp thông tin quan trọng để đánh giá hiệu quả tài chính của dự án và công ty.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-MGN-003  
**Task Name:** Triển khai Lambda function tính toán margin  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-MGN-001 (Triển khai Lambda functions quản lý chi phí nhân viên)
- BE-MGN-002 (Phát triển Lambda function tính toán revenue)

**Các task phụ thuộc vào task này:** 
- BE-MGN-004 (Phát triển Lambda functions xem thông tin margin)
- BE-RPT-001 (Phát triển Lambda function lấy dữ liệu tổng hợp cho dashboard)

**Các API:**
- GET /api/v1/margins/calculations (API-MGN-004)

## Mô tả

Triển khai Lambda function tính toán margin bằng cách so sánh dữ liệu chi phí (cost) và doanh thu (revenue) của nhân viên trong các kỳ báo cáo khác nhau. Margin là chỉ số quan trọng để đánh giá hiệu quả tài chính của các dự án và toàn công ty.

Hệ thống sẽ tính toán margin theo các cách sau:
1. Scheduled task chạy định kỳ (hàng ngày) để tự động cập nhật dữ liệu margin
2. API endpoint cho phép kích hoạt tính toán lại margin theo yêu cầu
3. Tự động tính toán margin mỗi khi có sự thay đổi trong dữ liệu chi phí hoặc doanh thu

Dựa trên giá trị margin, hệ thống sẽ tự động xác định trạng thái (Red/Yellow/Green) theo các ngưỡng đã được cấu hình, giúp quản lý dễ dàng nhận biết các dự án hoặc nhân viên có vấn đề về hiệu quả tài chính.

## Chi tiết công việc

### Phát triển Lambda function tính toán margin

- [ ] Triển khai Lambda function xử lý tính toán margin:
  - Location: src/functions/margins/calculate_margin.py
  - Triển khai logic tính toán margin:
    - Lấy dữ liệu chi phí từ bảng EMPLOYEE_COSTS
    - Lấy dữ liệu doanh thu từ bảng EMPLOYEE_REVENUES
    - Tính toán margin theo công thức: Margin (%) = ((Revenue - Cost) / Revenue) * 100
    - Xác định trạng thái Red/Yellow/Green dựa trên ngưỡng margin:
      - Red: Margin <= 25%
      - Yellow: 25% < Margin <= 35%
      - Green: Margin > 35%
    - Lưu kết quả tính toán vào bảng EMPLOYEE_MARGINS
  - Cài đặt tính toán cho nhiều cấp độ:
    - Theo từng nhân viên
    - Tổng hợp theo team
    - Tổng hợp theo dự án
    - Tổng hợp theo kỳ báo cáo (tháng, quý, năm)
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function API endpoint tính toán lại margin

- [ ] Triển khai Lambda function xử lý GET /api/v1/margins/calculations:
  - Location: src/functions/margins/trigger_margin_calculation.py
  - Triển khai logic kích hoạt tính toán lại margin:
    - Xác thực và phân quyền người dùng (chỉ Admin và Division Manager)
    - Hỗ trợ tính toán lại cho:
      - Một nhân viên cụ thể
      - Một team cụ thể
      - Một kỳ báo cáo cụ thể (tháng, quý, năm)
      - Kết hợp các điều kiện trên
    - Ghi lại lịch sử tính toán lại (người yêu cầu, thời gian, phạm vi)
    - Trả về kết quả tính toán tổng hợp

### Phát triển Scheduled Task tự động tính toán

- [ ] Triển khai CloudWatch Scheduled Event cho việc tính toán tự động:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình schedule expression (ví dụ: cron(0 2 * * ? *) - 2 AM hàng ngày)
  - Liên kết với Lambda function calculate_margin
  - Cấu hình để chạy sau khi tính toán revenue hoàn tất
  - Cấu hình retry và dead-letter queue

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho margin:
  - Location: src/models/employee_margin.py
  - Định nghĩa model cho margin:
    - Các trường cơ bản: employee_id, year_month, team_id, project_id, cost, revenue, margin_percentage, margin_status, etc.
  - Triển khai các method truy vấn DynamoDB:
    - create_or_update_margin(employee_id, year_month, margin_data)
    - get_employee_margin(employee_id, year_month)
    - get_employee_margins(filters)
    - get_aggregated_margins(groupBy, filters)
    - get_margin_history(employee_id, from_year_month, to_year_month)

### Phát triển Business Logic Layer

- [ ] Triển khai lớp business logic cho tính toán margin:
  - Location: src/services/margin_calculator.py
  - Triển khai các method tính toán:
    - calculate_employee_margin(employee_id, period)
    - calculate_team_margin(team_id, period)
    - calculate_project_margin(project_id, period)
    - calculate_overall_margin(period)
    - determine_margin_status(margin_percentage, thresholds)
    - aggregate_margins_by_team(margins)
    - aggregate_margins_by_project(margins)
    - aggregate_margins_by_period(margins, period_type)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/margins/calculations:
    - Method: GET
    - Các tham số query: employeeId, teamId, period, yearMonth, yearQuarter, year, recalculate (boolean)
    - Liên kết với Lambda function trigger_margin_calculation
    - Phân quyền: Admin, Division Manager
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển cơ chế tự động tính toán khi dữ liệu thay đổi

- [ ] Triển khai DynamoDB Streams và Lambda function xử lý:
  - Location: src/functions/margins/handle_data_change.py
  - Cấu hình DynamoDB Streams trên bảng EMPLOYEE_COSTS và EMPLOYEE_REVENUES
  - Triển khai Lambda function để xử lý sự kiện thay đổi dữ liệu:
    - Phát hiện loại thay đổi (Insert, Modify, Remove)
    - Xác định phạm vi cần tính toán lại margin
    - Gọi margin_calculator service để cập nhật margin

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/margins/
  - Test case cho calculate_margin.py:
    - Test tính toán margin cho từng nhân viên
    - Test tính toán margin tổng hợp theo team
    - Test tính toán margin tổng hợp theo dự án
    - Test xác định trạng thái margin (Red/Yellow/Green)
    - Test xử lý lỗi
  - Test case cho trigger_margin_calculation.py:
    - Test kích hoạt tính toán lại margin với các tham số khác nhau
    - Test phân quyền
  - Test case cho handle_data_change.py:
    - Test xử lý sự kiện thay đổi dữ liệu chi phí
    - Test xử lý sự kiện thay đổi dữ liệu doanh thu
  - Test case cho các service:
    - Test margin_calculator với các trường hợp khác nhau

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho endpoint:
    - GET /api/v1/margins/calculations
  - Tài liệu mô tả thuật toán tính toán margin
  - Tài liệu giải thích các ngưỡng Red/Yellow/Green
  - Tài liệu về quy trình tính toán tự động và cách trigger thủ công

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách kích hoạt tính toán lại margin:

```python
# Kích hoạt tính toán lại margin cho một team trong một tháng cụ thể
import requests

def trigger_margin_calculation(api_base_url, token, team_id=None, year_month=None, recalculate=True):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'recalculate': str(recalculate).lower()
    }
    
    if team_id:
        params['teamId'] = team_id
    
    if year_month:
        params['yearMonth'] = year_month
    
    response = requests.get(
        f"{api_base_url}/api/v1/margins/calculations",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "calculationId": "calc-20250513-001",
#     "calculatedAt": "2025-05-13T16:30:45Z",
#     "requestedBy": {
#       "userId": "user123",
#       "name": "Nguyễn Văn A"
#     },
#     "scope": {
#       "teamId": "team456",
#       "teamName": "Java Team",
#       "period": {
#         "type": "month",
#         "yearMonth": "2025-05"
#       }
#     },
#     "summary": {
#       "totalEmployees": 15,
#       "totalCost": 300000000,
#       "totalRevenue": 450000000,
#       "totalMargin": 33.33,
#       "marginStatus": "YELLOW",
#       "statusDistribution": {
#         "RED": 4,
#         "YELLOW": 6,
#         "GREEN": 5
#       }
#     },
#     "details": [
#       {
#         "employeeId": "emp789",
#         "employeeName": "Trần Thị B",
#         "position": "Senior Developer",
#         "cost": 25000000,
#         "revenue": 40000000,
#         "margin": 37.5,
#         "marginStatus": "GREEN"
#       },
#       // ... more employees
#     ]
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function tính toán margin hoạt động chính xác với các cấp độ tổng hợp khác nhau
2. Scheduled task tự động tính toán margin chạy đúng lịch và xử lý lỗi phù hợp
3. API endpoint GET /api/v1/margins/calculations hoạt động chính xác
4. Cơ chế tự động tính toán lại margin khi dữ liệu thay đổi hoạt động đúng
5. Xác định chính xác trạng thái margin (Red/Yellow/Green) dựa trên ngưỡng
6. Xử lý phân quyền đúng (Admin, Division Manager có quyền khác nhau)
7. Unit tests đạt coverage > 80%
8. Tài liệu API và tài liệu kỹ thuật đầy đủ

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Ngưỡng margin (Red/Yellow/Green) nên được lưu trong bảng cấu hình hệ thống và có thể điều chỉnh bởi Admin
- Cần đặc biệt chú ý đến hiệu năng khi tính toán margin cho dataset lớn, cân nhắc sử dụng tính toán batch
- Xem xét việc lưu trữ lịch sử margin để theo dõi xu hướng theo thời gian
- Đảm bảo xử lý các trường hợp đặc biệt: nhân viên không có doanh thu, doanh thu âm, chi phí không xác định, etc.
- Cân nhắc việc hiển thị cảnh báo hoặc thông báo khi margin giảm đáng kể so với kỳ trước 