**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function đồng bộ dữ liệu từ Hubspot | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function đồng bộ dữ liệu cơ hội kinh doanh từ Hubspot vào hệ thống, đảm bảo dữ liệu được cập nhật chính xác và kịp thời.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-OPP-001  
**Task Name:** Triển khai Lambda functions đồng bộ dữ liệu từ Hubspot  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-ADM-003 (Phát triển Lambda functions quản lý cấu hình hệ thống)

**Các task phụ thuộc vào task này:** 
- BE-OPP-002 (Phát triển Lambda function xem log đồng bộ)
- BE-OPP-003 (Triển khai Lambda functions quản lý cơ hội)

**Các API:**
- POST /api/v1/opportunities/sync (API-OPP-003)

## Mô tả

Triển khai các Lambda function để đồng bộ dữ liệu cơ hội kinh doanh từ Hubspot CRM vào hệ thống nội bộ. Các function này sẽ được kích hoạt thông qua hai cơ chế:
1. Đồng bộ thủ công: API endpoint cho phép người dùng có quyền (Admin/Trưởng phòng) kích hoạt đồng bộ theo yêu cầu
2. Đồng bộ tự động: CloudWatch Events scheduled event kích hoạt Lambda function định kỳ (mặc định là mỗi 3 giờ)

Chức năng này đóng vai trò quan trọng trong việc đảm bảo dữ liệu cơ hội kinh doanh luôn được cập nhật giữa Hubspot và hệ thống nội bộ, giúp đội Sales và các Leaders theo dõi và phản ứng kịp thời với các cơ hội mới hoặc thay đổi trạng thái từ Hubspot.

## Chi tiết công việc

### Phát triển dịch vụ tích hợp Hubspot API

- [ ] Xây dựng lớp service tích hợp với Hubspot API:
  - Location: src/services/hubspot_service.py
  - Cài đặt các function kết nối với Hubspot API sử dụng thư viện hubspot-api-client
  - Triển khai chức năng lấy danh sách deals từ Hubspot với phân trang
  - Xử lý authentication với Hubspot (OAuth hoặc API key)
  - Thêm caching để tối ưu hóa request
  - Cài đặt retry logic và error handling cho API calls

### Triển khai Lambda function đồng bộ dữ liệu

- [ ] Phát triển Lambda function xử lý đồng bộ:
  - Location: src/functions/opportunity/sync_hubspot.py
  - Triển khai logic đồng bộ dữ liệu:
    - Lấy thông tin cấu hình Hubspot API từ DynamoDB (SystemConfig)
    - Kết nối và lấy dữ liệu từ Hubspot API 
    - So sánh và xác định deals cần thêm mới/cập nhật/đánh dấu xóa
    - Chuyển đổi dữ liệu từ định dạng Hubspot sang định dạng lưu trữ trong DynamoDB
    - Thực hiện batch write vào DynamoDB
  - Cài đặt cơ chế tracking đồng bộ:
    - Cập nhật trường sync_status, last_sync_at cho mỗi record
    - Lưu log đồng bộ vào bảng HUBSPOT_SYNC_LOG
  - Xử lý các trường hợp đặc biệt:
    - Deals bị xóa trong Hubspot
    - Xung đột dữ liệu
    - Deals được cập nhật thủ công trong hệ thống nội bộ

### Triển khai API endpoint cho đồng bộ thủ công

- [ ] Phát triển API endpoint cho đồng bộ thủ công:
  - Location: src/functions/opportunity/trigger_sync.py
  - Cài đặt Lambda function xử lý POST request:
    - Kiểm tra quyền truy cập (chỉ Admin/Trưởng phòng)
    - Gọi Lambda function đồng bộ không đồng bộ (asynchronous invocation)
    - Trả về phản hồi ngay lập tức cho người dùng
  - Cấu hình API Gateway:
    - Định tuyến POST /api/v1/opportunities/sync
    - Tích hợp với Lambda Authorizer

### Cấu hình CloudWatch Events cho đồng bộ tự động

- [ ] Thiết lập CloudWatch scheduled event:
  - Location: template.yaml (trong phần Resources)
  - Tạo rule với mẫu cron/rate (mặc định: rate(3 hours))
  - Liên kết với Lambda function đồng bộ
  - Cấu hình để scheduled event có thể được bật/tắt thông qua cấu hình hệ thống

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/opportunity/
  - Test các thành phần:
    - Test hubspot_service.py (mock API responses)
    - Test sync_hubspot.py (mock DynamoDB, Hubspot Service)
    - Test trigger_sync.py (auth checks, invocation)
  - Test các cases:
    - Đồng bộ thành công
    - Xử lý lỗi Hubspot API
    - Xử lý lỗi DynamoDB
    - Xử lý deals bị xóa

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho POST /api/v1/opportunities/sync 
  - Tài liệu mô tả cơ chế đồng bộ và các trường hợp xử lý
  - Tài liệu cấu hình Hubspot connection

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách kích hoạt đồng bộ thủ công:

```python
# Kích hoạt thủ công thông qua API
import requests

def trigger_hubspot_sync(api_base_url, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/opportunities/sync",
        headers=headers
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "message": "Hubspot sync started successfully", 
#   "sync_id": "sync-20250513-001"
# }
```

Flow tự động đồng bộ:
1. CloudWatch scheduled event kích hoạt theo lịch
2. Lambda function sync_hubspot được gọi
3. Dữ liệu cơ hội được đồng bộ từ Hubspot vào DynamoDB
4. Log đồng bộ được lưu vào HUBSPOT_SYNC_LOG
5. Người dùng có thể xem thông tin đồng bộ qua API log

## Tiêu chí hoàn thành

1. Lambda function đồng bộ dữ liệu từ Hubspot hoạt động đúng
2. API endpoint đồng bộ thủ công hoạt động với việc xác thực và phân quyền
3. CloudWatch Events được cấu hình để kích hoạt đồng bộ tự động
4. Log đồng bộ được lưu trữ chính xác
5. Unit tests đạt coverage > 80%
6. Documentation đầy đủ cho API và cơ chế đồng bộ

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Cần cấu hình rate limit phù hợp để tránh vượt quá hạn ngạch Hubspot API
- Lưu ý xử lý các trường hợp đồng bộ một lượng lớn deals để đảm bảo Lambda không timeout
- Cơ chế đồng bộ nên hỗ trợ incremental sync để tối ưu hiệu suất
- Cân nhắc sử dụng SQS queue để xử lý đồng bộ số lượng lớn deals 