**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function báo cáo danh sách cơ hội | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function báo cáo chi tiết danh sách cơ hội kinh doanh, hỗ trợ việc phân tích và theo dõi cơ hội.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-RPT-004  
**Task Name:** Triển khai Lambda function báo cáo danh sách cơ hội  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-OPP-001 (Triển khai Lambda functions quản lý danh sách cơ hội)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- GET /api/v1/reports/opportunity-list (API-RPT-004)

## Mô tả

Task này bao gồm việc phát triển Lambda function để tạo báo cáo chi tiết về danh sách cơ hội kinh doanh, bao gồm thông tin về khách hàng, giai đoạn đàm phán, người phụ trách, và các chỉ số liên quan. Báo cáo này sẽ hỗ trợ việc lọc theo nhiều tiêu chí khác nhau và cho phép xuất dữ liệu ra file (Excel/CSV) để phân tích chuyên sâu.

Lambda function sẽ tương tác với DynamoDB để truy xuất thông tin cơ hội và cung cấp một API endpoint để frontend có thể hiển thị báo cáo hoặc tải xuống báo cáo dưới dạng file.

## Chi tiết công việc

### Phát triển Lambda function tạo báo cáo danh sách cơ hội

- [ ] Triển khai Lambda function xử lý GET /api/v1/reports/opportunity-list:
  - Location: src/functions/reports/opportunity_list_report.py
  - Triển khai handler function cho endpoint API-RPT-004
  - Xử lý các tham số truy vấn và lọc
  - Hỗ trợ xuất dữ liệu sang file Excel/CSV

### Phát triển Service Layer cho Opportunity Report

- [ ] Xây dựng Opportunity Report Service:
  - Location: src/services/opportunity_report_service.py
  - Implement OpportunityReportService class
  - Phương thức get_opportunity_list_report để lấy dữ liệu báo cáo theo các bộ lọc
  - Phương thức generate_opportunity_export để tạo file export

### Triển khai các phương thức truy vấn và xử lý dữ liệu cơ hội

- [ ] Phát triển phương thức truy vấn dữ liệu cơ hội:
  - Location: src/repositories/opportunity_repository.py
  - Implement phương thức get_opportunities_with_details
  - Tối ưu hóa truy vấn DynamoDB sử dụng GSI phù hợp
  - Hỗ trợ các bộ lọc (deal_stage, followup_status, assigned_to_id, date_range)

- [ ] Phát triển phương thức làm giàu dữ liệu cơ hội:
  - Location: src/services/opportunity_report_service.py
  - Thêm thông tin người phụ trách và ghi chú mới nhất
  - Tính toán các trường dẫn xuất (thời gian trong giai đoạn hiện tại, ngày tương tác cuối)

- [ ] Phát triển phương thức tạo file export:
  - Location: src/services/opportunity_report_service.py
  - Hỗ trợ định dạng Excel và CSV
  - Bao gồm thông tin tóm tắt (summary) và dữ liệu chi tiết

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/reports/opportunity-list
  - Thiết lập IAM Policies cho phép đọc DynamoDB và ghi S3

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/reports/
  - Test case cho opportunity_list_report.py
  - Test case cho opportunity_report_service.py

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để lấy báo cáo danh sách cơ hội:

```python
# Lấy báo cáo danh sách cơ hội
import requests

def get_opportunity_list_report(api_base_url, token, filters=None, page=1, size=20, export_format=None):
    """
    Get opportunity list report with various filters
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
        f"{api_base_url}/api/v1/reports/opportunity-list",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ sử dụng:
filters = {
    'deal_stage': 'qualified,proposal',
    'followup_status': 'Yellow,Red',
    'assigned_to_id': 'user123',
    'from_date': '2025-01-01',
    'to_date': '2025-05-31'
}
opportunity_report = get_opportunity_list_report('https://api.example.com', 'token123', filters=filters)
```

## Tiêu chí hoàn thành

1. Lambda function được triển khai và hoạt động chính xác với API GET /api/v1/reports/opportunity-list
2. API hỗ trợ đầy đủ các tham số lọc (deal_stage, followup_status, assigned_to_id, date_range)
3. Phân quyền truy cập dữ liệu được áp dụng đúng (Sales, Leader, Admin)
4. Các truy vấn DynamoDB được tối ưu hóa và hiệu quả
5. Cơ chế export file Excel/CSV được triển khai đúng
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Cần đảm bảo phân quyền phù hợp - người dùng chỉ có thể xem cơ hội thuộc phạm vi quản lý của họ
- Sử dụng GSI1 (deal_stage), GSI2 (followup_status), GSI3 (assigned_to_id) để tối ưu hóa truy vấn
- Với các báo cáo có nhiều tiêu chí lọc phức tạp, cần cân nhắc hiệu suất truy vấn DynamoDB
- Báo cáo cơ hội nên bao gồm thông tin ghi chú mới nhất và lịch sử trạng thái để có cái nhìn toàn diện
- Đối với file export, cần cân nhắc giới hạn số lượng bản ghi để tránh time-out của Lambda function 