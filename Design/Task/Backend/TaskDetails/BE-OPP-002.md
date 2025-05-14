**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function xem log đồng bộ Hubspot | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function xem log đồng bộ dữ liệu từ Hubspot, giúp người dùng có thể theo dõi lịch sử đồng bộ và phát hiện sự cố.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-OPP-002  
**Task Name:** Phát triển Lambda function xem log đồng bộ  
**Độ ưu tiên:** Thấp  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-OPP-001 (Triển khai Lambda functions đồng bộ dữ liệu từ Hubspot)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- GET /api/v1/opportunities/sync/logs (API-OPP-004)

## Mô tả

Triển khai Lambda function cho phép xem và tìm kiếm lịch sử đồng bộ dữ liệu từ Hubspot vào hệ thống. Chức năng này sẽ giúp người dùng:
1. Theo dõi kết quả các lần đồng bộ tự động và thủ công
2. Kiểm tra và phát hiện các sự cố trong quá trình đồng bộ
3. Xem số lượng records được thêm mới, cập nhật hoặc đánh dấu xóa trong mỗi lần đồng bộ
4. Tìm kiếm lịch sử đồng bộ theo thời gian và trạng thái

Chức năng này đặc biệt hữu ích cho việc khắc phục sự cố khi có vấn đề về dữ liệu giữa Hubspot và hệ thống nội bộ.

## Chi tiết công việc

### Triển khai Lambda function xem log đồng bộ

- [ ] Phát triển Lambda function xử lý API requests:
  - Triển khai logic lấy dữ liệu log đồng bộ:
    - Truy vấn dữ liệu từ bảng HUBSPOT_SYNC_LOG trên DynamoDB
    - Hỗ trợ phân trang với tokenization (DynamoDB pagination)
    - Hỗ trợ lọc theo thời gian (date range), trạng thái (success/failed/partial)
    - Hỗ trợ tìm kiếm theo sync_id
  - Hiển thị số liệu thống kê tổng quát (summary):
    - Tổng số records được thêm mới, cập nhật, xóa
    - Tổng thời gian thực hiện đồng bộ
    - Lỗi nếu có

### Cấu hình API Endpoint

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/opportunities/sync/logs:
    - Method: GET
    - Tham số query: page_size, next_token, from_date, to_date, status
    - Liên kết với Lambda function
    - Phân quyền: chỉ Admin và Trưởng phòng mới có quyền xem
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho logs:
  - Định nghĩa model cho log đồng bộ
  - Triển khai các method truy vấn DynamoDB:
    - get_logs(limit, next_token, filters)
    - get_log_by_id(sync_id)
    - get_recent_logs(limit)
  - Xử lý chuyển đổi giữa DynamoDB Item và model object


## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách logs:

```python
# Lấy danh sách logs đồng bộ Hubspot
import requests

def get_hubspot_sync_logs(api_base_url, token, page_size=10, next_token=None, from_date=None, to_date=None, status=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page_size': page_size
    }
    
    if next_token:
        params['next_token'] = next_token
    
    if from_date:
        params['from_date'] = from_date
    
    if to_date:
        params['to_date'] = to_date
    
    if status:
        params['status'] = status
    
    response = requests.get(
        f"{api_base_url}/api/v1/opportunities/sync/logs",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "items": [
#     {
#       "sync_id": "sync-20250513-001",
#       "start_time": "2025-05-13T10:15:30Z",
#       "end_time": "2025-05-13T10:16:45Z",
#       "status": "success",
#       "trigger_type": "manual", // hoặc "scheduled"
#       "triggered_by": "user123", // nếu manual
#       "items_added": 15,
#       "items_updated": 25,
#       "items_deleted": 2,
#       "error_message": null
#     },
#     // ...more items
#   ],
#   "next_token": "eyJsYXN0X2V2YWx1YXRlZF9rZXkiOnsia2V5IjoiMjAyNS0wNS0xM1QxMDoxNTozMFoifX0=", // for pagination
#   "count": 10,
#   "total": 45 // tổng số log thỏa mãn điều kiện filter nếu không dùng phân trang
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy và hiển thị log đồng bộ hoạt động chính xác
2. API endpoint GET /api/v1/opportunities/sync/logs được cấu hình đúng với phân trang và bộ lọc
3. Tài liệu API đầy đủ

## Ước tính thời gian

- 1-2 ngày làm việc

## Ghi chú

- Đảm bảo thiết kế database đúng để hỗ trợ các query pattern cần thiết
- Cân nhắc thời gian lưu trữ logs (TTL) để tránh chi phí lưu trữ quá lớn
- Đảm bảo phân quyền chính xác cho việc xem logs 