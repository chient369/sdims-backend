**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function báo cáo chi tiết margin | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function báo cáo chi tiết margin, cung cấp thông tin về hiệu suất tài chính của nhân viên và dự án.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-RPT-003  
**Task Name:** Triển khai Lambda function báo cáo chi tiết margin  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)
- BE-MGN-003 (Triển khai Lambda function tính toán margin)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- GET /api/v1/reports/margin-detail (API-RPT-003)

## Mô tả

Task này bao gồm việc phát triển Lambda function để tạo báo cáo chi tiết về margin của nhân viên và dự án. Báo cáo margin cung cấp thông tin về chi phí, doanh thu và tỷ lệ margin, hỗ trợ việc phân tích hiệu quả tài chính và ra quyết định. Function này sẽ hỗ trợ các tính năng lọc, phân trang và xuất dữ liệu sang các định dạng phù hợp (Excel/CSV).

Đây là API có dữ liệu nhạy cảm và cần được bảo vệ nghiêm ngặt, chỉ có người dùng với quyền hạn phù hợp mới có thể truy cập.

## Chi tiết công việc

### Phát triển Lambda function tạo báo cáo chi tiết margin

- [ ] Triển khai Lambda function xử lý GET /api/v1/reports/margin-detail:
  - Location: src/functions/reports/margin_detail_report.py
  - Triển khai handler function cho endpoint API-RPT-003
  - Xác thực quyền truy cập dữ liệu margin
  - Xử lý các tham số truy vấn và lọc
  - Hỗ trợ xuất dữ liệu sang file Excel/CSV

### Phát triển Service Layer cho Margin Report

- [ ] Xây dựng Margin Report Service:
  - Location: src/services/margin_report_service.py
  - Implement MarginReportService class
  - Phương thức get_margin_detail_report để lấy dữ liệu báo cáo theo các bộ lọc
  - Phương thức generate_margin_export để tạo file export

### Triển khai các phương thức truy vấn và xử lý dữ liệu margin

- [ ] Phát triển phương thức truy vấn dữ liệu margin:
  - Location: src/repositories/margin_repository.py
  - Implement phương thức get_margin_details
  - Tối ưu hóa truy vấn DynamoDB sử dụng GSI phù hợp
  - Hỗ trợ các bộ lọc (period, team_id, project_id, status, employee_id)

- [ ] Phát triển phương thức làm giàu dữ liệu margin:
  - Location: src/services/margin_report_service.py
  - Thêm thông tin nhân viên và dự án vào dữ liệu margin
  - Tính toán các trường dẫn xuất (margin amount, margin percentage)

- [ ] Phát triển phương thức tạo file export:
  - Location: src/services/margin_report_service.py
  - Hỗ trợ định dạng Excel và CSV
  - Bao gồm thông tin tóm tắt (summary) và dữ liệu chi tiết

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/reports/margin-detail
  - Thiết lập IAM Policies cho phép đọc DynamoDB và ghi S3

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/reports/
  - Test case cho margin_detail_report.py
  - Test case cho margin_report_service.py

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để lấy báo cáo chi tiết margin:

```python
# Lấy báo cáo chi tiết margin
import requests

def get_margin_detail_report(api_base_url, token, filters=None, page=1, size=20, export_format=None):
    """
    Get margin detail report with various filters
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Build query parameters
    params = {
        'page': page,
        'size': size
    }
    
    # Add filters if provided
    if filters:
        params.update(filters)
    
    # Add export format if provided
    if export_format:
        params['export'] = export_format
    
    response = requests.get(
        f"{api_base_url}/api/v1/reports/margin-detail",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ sử dụng:
filters = {
    'period': '2025-04',
    'team_id': 'team123',
    'status': 'Red'
}
margin_report = get_margin_detail_report('https://api.example.com', 'token123', filters=filters)
```

## Tiêu chí hoàn thành

1. Lambda function được triển khai và hoạt động chính xác với API GET /api/v1/reports/margin-detail
2. API hỗ trợ đầy đủ các tham số lọc (period, team_id, project_id, status, employee_id)
3. Phân quyền truy cập dữ liệu được áp dụng đúng
4. Các truy vấn DynamoDB được tối ưu hóa và hiệu quả
5. Cơ chế export file Excel/CSV được triển khai đúng
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Dữ liệu margin là thông tin nhạy cảm, cần triển khai phân quyền truy cập nghiêm ngặt
- Sử dụng GSI phù hợp để tối ưu hóa truy vấn margin theo các điều kiện lọc khác nhau
- Cần tối ưu hóa cơ chế truy vấn và làm giàu dữ liệu để giảm số lượng truy vấn DynamoDB
- File export có thể lớn nếu có nhiều dữ liệu, cần xử lý hiệu quả trong giới hạn của Lambda 