**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda functions xem thông tin margin | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions cho phép người dùng xem và phân tích thông tin margin theo nhiều tiêu chí, giúp đánh giá hiệu quả tài chính và đưa ra quyết định kinh doanh.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-MGN-004  
**Task Name:** Phát triển Lambda functions xem thông tin margin  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-MGN-003 (Triển khai Lambda function tính toán margin)

**Các task phụ thuộc vào task này:** 
- BE-RPT-001 (Phát triển Lambda function lấy dữ liệu tổng hợp cho dashboard)
- BE-RPT-003 (Triển khai Lambda functions cho báo cáo chi tiết margin)

**Các API:**
- GET /api/v1/margins/employee (API-MGN-005)
- GET /api/v1/margins/summary (API-MGN-006)

## Mô tả

Phát triển Lambda functions cho phép người dùng xem và phân tích thông tin margin đã được tính toán. Các APIs sẽ hỗ trợ:
1. Xem thông tin margin chi tiết theo từng nhân viên
2. Xem báo cáo tổng hợp margin theo team, thời gian
3. Lọc và sắp xếp dữ liệu margin theo nhiều tiêu chí
4. Phân tích xu hướng margin theo thời gian

Thông tin margin là một trong những chỉ số KPI quan trọng nhất trong hệ thống, giúp quản lý nắm được tình hình tài chính và hiệu quả kinh doanh của từng đơn vị và toàn công ty.

## Chi tiết công việc

### Phát triển Lambda function xem margin theo nhân viên

- [ ] Triển khai Lambda function xử lý GET /api/v1/margins/employee:
  - Location: src/functions/margins/get_employee_margin.py
  - Triển khai logic lấy thông tin margin chi tiết:
    - Xác thực và phân quyền người dùng
    - Lấy dữ liệu margin từ bảng EMPLOYEE_MARGINS
    - Hỗ trợ lọc theo nhiều tiêu chí:
      - Nhân viên cụ thể (employeeId)
      - Khoảng thời gian (fromDate, toDate)
      - Năm-tháng cụ thể (yearMonth)
      - Quý (yearQuarter)
      - Năm (year)
      - Trạng thái margin (marginStatus: RED, YELLOW, GREEN)
    - Bổ sung thông tin chi tiết từ các bảng liên quan:
      - Thông tin nhân viên từ EMPLOYEES
      - Thông tin chi phí từ EMPLOYEE_COSTS
      - Thông tin doanh thu từ EMPLOYEE_REVENUES
    - Hỗ trợ phân trang kết quả
  - Xử lý các trường hợp đặc biệt và tối ưu hiệu năng

### Phát triển Lambda function xem báo cáo tổng hợp margin

- [ ] Triển khai Lambda function xử lý GET /api/v1/margins/summary:
  - Location: src/functions/margins/get_margin_summary.py
  - Triển khai logic lấy báo cáo tổng hợp margin:
    - Xác thực và phân quyền người dùng
    - Lấy dữ liệu margin từ bảng EMPLOYEE_MARGINS
    - Tổng hợp dữ liệu theo nhiều tiêu chí:
      - Theo team (teamId)
      - Theo kỳ báo cáo (period: month, quarter, year)
      - Theo trạng thái (marginStatus)
    - Tính toán các chỉ số tổng hợp:
      - Margin trung bình
      - Tổng chi phí
      - Tổng doanh thu
      - Phân bố trạng thái (số lượng RED, YELLOW, GREEN)
    - Hỗ trợ so sánh với kỳ trước đó
    - Hỗ trợ xuất dữ liệu ra các định dạng khác nhau (JSON, CSV, Excel)
  - Xử lý các trường hợp đặc biệt và tối ưu hiệu năng

### Phát triển Data Access Layer

- [ ] Mở rộng lớp truy cập dữ liệu cho margin:
  - Location: src/models/employee_margin.py
  - Bổ sung các method truy vấn DynamoDB:
    - get_employee_margin_details(employee_id, filters)
    - get_team_margin_summary(team_id, filters)
    - get_margin_by_status(status, filters)
    - get_margin_trends(period_type, filters)
    - export_margin_data(format, filters)

### Phát triển Business Logic Layer

- [ ] Mở rộng lớp business logic cho phân tích margin:
  - Location: src/services/margin_analyzer.py
  - Triển khai các method phân tích:
    - analyze_margin_trends(margins, period_type)
    - calculate_margin_changes(current_margin, previous_margin)
    - identify_critical_cases(margins, threshold)
    - generate_margin_summary_report(margins, groupBy)
    - format_export_data(margins, format)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/margins/employee:
    - Method: GET
    - Các tham số query: employeeId, fromDate, toDate, yearMonth, yearQuarter, year, marginStatus, page, size, sortBy, sortDir
    - Liên kết với Lambda function get_employee_margin
    - Phân quyền: Admin, Division Manager, Team Leader, Employee (giới hạn)
  - Cấu hình route GET /api/v1/margins/summary:
    - Method: GET
    - Các tham số query: teamId, period, fromDate, toDate, yearMonth, yearQuarter, year, groupBy, compareWithPrevious, exportFormat
    - Liên kết với Lambda function get_margin_summary
    - Phân quyền: Admin, Division Manager, Team Leader
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Utility cho xuất dữ liệu

- [ ] Xây dựng utility xử lý xuất dữ liệu:
  - Location: src/common/export_utils.py
  - Triển khai các functions:
    - export_to_csv(data, headers)
    - export_to_excel(data, headers, sheet_name)
    - format_margin_data_for_export(margins, format)
    - upload_export_file_to_s3(file_data, format, filename)
    - generate_download_url(s3_key)

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/margins/
  - Test case cho get_employee_margin.py:
    - Test lấy margin theo nhân viên
    - Test lọc theo các tiêu chí khác nhau
    - Test phân trang
    - Test phân quyền
  - Test case cho get_margin_summary.py:
    - Test tổng hợp margin theo team
    - Test tổng hợp theo kỳ báo cáo
    - Test so sánh với kỳ trước
    - Test xuất dữ liệu
  - Test case cho các service và utility:
    - Test margin_analyzer
    - Test export_utils

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/margins/employee
    - GET /api/v1/margins/summary
  - Tài liệu mô tả cấu trúc dữ liệu margin
  - Tài liệu giải thích các phương pháp tổng hợp và phân tích margin
  - Hướng dẫn sử dụng API và các tham số filter, sort

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách xem thông tin margin của nhân viên:

```python
# Xem thông tin margin của một nhân viên trong một khoảng thời gian
import requests

def get_employee_margin(api_base_url, token, employee_id=None, from_date=None, to_date=None, margin_status=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {}
    
    if employee_id:
        params['employeeId'] = employee_id
    
    if from_date:
        params['fromDate'] = from_date
    
    if to_date:
        params['toDate'] = to_date
    
    if margin_status:
        params['marginStatus'] = margin_status
    
    response = requests.get(
        f"{api_base_url}/api/v1/margins/employee",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "employee": {
#       "id": "emp123",
#       "name": "Nguyễn Văn A",
#       "position": "Senior Developer",
#       "team": {
#         "id": "team456",
#         "name": "Java Team"
#       }
#     },
#     "period": {
#       "fromDate": "2025-01-01",
#       "toDate": "2025-05-31"
#     },
#     "summary": {
#       "averageMargin": 32.5,
#       "totalCost": 125000000,
#       "totalRevenue": 185000000,
#       "currentStatus": "YELLOW",
#       "statusDistribution": {
#         "RED": 1,
#         "YELLOW": 3,
#         "GREEN": 1
#       }
#     },
#     "details": [
#       {
#         "yearMonth": "2025-05",
#         "cost": 25000000,
#         "revenue": 40000000,
#         "margin": 37.5,
#         "marginStatus": "GREEN",
#         "projects": [
#           {
#             "id": "proj789",
#             "name": "Banking System",
#             "allocation": 100,
#             "revenue": 40000000
#           }
#         ]
#       },
#       // ... more months
#     ],
#     "trends": {
#       "marginTrend": [25.0, 28.5, 30.0, 33.5, 37.5],
#       "months": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
#     },
#     "pagination": {
#       "page": 1,
#       "pageSize": 10,
#       "totalItems": 5,
#       "totalPages": 1
#     }
#   }
# }
```

Ví dụ về cách xem báo cáo tổng hợp margin:

```python
# Xem báo cáo tổng hợp margin theo team và kỳ báo cáo
import requests

def get_margin_summary(api_base_url, token, team_id=None, period='month', year_month=None, compare_with_previous=True):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'period': period,
        'compareWithPrevious': str(compare_with_previous).lower()
    }
    
    if team_id:
        params['teamId'] = team_id
    
    if year_month:
        params['yearMonth'] = year_month
    
    response = requests.get(
        f"{api_base_url}/api/v1/margins/summary",
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
#       "previousPeriod": "2025-04"
#     },
#     "summary": {
#       "totalCost": 750000000,
#       "totalRevenue": 1125000000,
#       "totalMargin": 33.33,
#       "previousMargin": 31.25,
#       "marginChange": "+2.08%",
#       "marginStatus": "YELLOW",
#       "statusDistribution": {
#         "RED": 8,
#         "YELLOW": 15,
#         "GREEN": 12
#       }
#     },
#     "teamBreakdown": [
#       {
#         "teamId": "team456",
#         "teamName": "Java Team",
#         "cost": 300000000,
#         "revenue": 450000000,
#         "margin": 33.33,
#         "previousMargin": 32.00,
#         "marginChange": "+1.33%",
#         "employeeCount": 15,
#         "statusCounts": {
#           "RED": 3,
#           "YELLOW": 7,
#           "GREEN": 5
#         }
#       },
#       // ... more teams
#     ],
#     "exportUrls": {
#       "csv": "https://api.example.com/exports/margin-summary-2025-05.csv",
#       "excel": "https://api.example.com/exports/margin-summary-2025-05.xlsx"
#     }
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function xem margin theo nhân viên hoạt động chính xác với đầy đủ chức năng filter và sort
2. Lambda function xem báo cáo tổng hợp margin hoạt động chính xác với khả năng phân tích và so sánh
3. Chức năng xuất dữ liệu ra các định dạng khác nhau hoạt động đúng
4. API endpoints được cấu hình đúng với phân quyền phù hợp
5. Hiển thị chính xác trạng thái margin (Red/Yellow/Green) và các thông tin liên quan
6. Hiệu năng tốt khi xử lý dữ liệu lớn và tổng hợp
7. Unit tests đạt coverage > 80%
8. Tài liệu API và tài liệu kỹ thuật đầy đủ

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Chú ý đến việc phân quyền - mỗi người dùng chỉ nên xem được những thông tin margin họ có quyền truy cập
- Leader chỉ nên xem được margin của nhân viên trong team của họ
- Division Manager có thể xem margin của tất cả nhân viên trong bộ phận
- Nhân viên chỉ xem được margin của chính họ (nếu được cấp quyền)
- Xem xét việc cache dữ liệu tổng hợp để tăng hiệu năng cho các báo cáo thường xuyên xem
- Nên có khả năng đặt cảnh báo khi margin giảm xuống dưới một ngưỡng nhất định 