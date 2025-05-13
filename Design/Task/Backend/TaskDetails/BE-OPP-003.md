**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý cơ hội kinh doanh | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý cơ hội kinh doanh, bao gồm xem danh sách, lọc, tìm kiếm và xem chi tiết cơ hội.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-OPP-003  
**Task Name:** Triển khai Lambda functions quản lý cơ hội  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-OPP-001 (Triển khai Lambda functions đồng bộ dữ liệu từ Hubspot)

**Các task phụ thuộc vào task này:** 
- BE-OPP-004 (Phát triển Lambda function gán Leader cho cơ hội)
- BE-OPP-005 (Triển khai Lambda functions quản lý ghi chú cơ hội)
- BE-OPP-006 (Phát triển Lambda function đánh dấu ưu tiên onsite)

**Các API:**
- GET /api/v1/opportunities (API-OPP-001)
- GET /api/v1/opportunities/{id} (API-OPP-002)

## Mô tả

Triển khai các Lambda functions cho phép người dùng xem danh sách cơ hội kinh doanh, tìm kiếm, lọc và xem chi tiết cơ hội. Các chức năng này là nền tảng cho các hoạt động quản lý cơ hội tiếp theo như gán leader, quản lý ghi chú và đánh dấu ưu tiên onsite.

Đặc biệt quan trọng, hệ thống cần tính toán tự động trạng thái follow-up (Red/Yellow/Green) dựa trên thời gian tương tác cuối cùng và trạng thái của cơ hội, giúp người dùng dễ dàng xác định các cơ hội cần được ưu tiên xử lý.

## Chi tiết công việc

### Phát triển Lambda function xem danh sách cơ hội

- [ ] Triển khai Lambda function xử lý GET /api/v1/opportunities:
  - Location: src/functions/opportunity/list_opportunities.py
  - Triển khai logic lấy dữ liệu cơ hội:
    - Truy vấn dữ liệu từ bảng OPPORTUNITIES trên DynamoDB
    - Hỗ trợ phân trang với tokenization (DynamoDB pagination)
    - Hỗ trợ lọc theo:
      - Trạng thái cơ hội (status)
      - Trạng thái follow-up (follow_up_status)
      - Leader được gán (assigned_to)
      - Khách hàng (customer_name)
      - Khoảng thời gian (tạo/cập nhật/tương tác cuối)
      - Giá trị dự kiến (potential_value range)
    - Hỗ trợ tìm kiếm text (full-text search) trên các trường:
      - Tên cơ hội (opportunity_name)
      - Mô tả (description)
      - Tên khách hàng (customer_name)
    - Hỗ trợ sắp xếp theo các trường phổ biến:
      - Ngày tạo (created_at)
      - Ngày cập nhật (updated_at)
      - Ngày tương tác cuối (last_interaction_date)
      - Giá trị dự kiến (potential_value)
  - Triển khai tính toán trạng thái follow-up (Red/Yellow/Green):
    - Red: quá thời hạn follow-up và không có tương tác trong thời gian X ngày (mặc định 7 ngày)
    - Yellow: sắp đến thời hạn follow-up (còn 2 ngày)
    - Green: đã có tương tác gần đây hoặc không yêu cầu follow-up

### Phát triển Lambda function xem chi tiết cơ hội

- [ ] Triển khai Lambda function xử lý GET /api/v1/opportunities/{id}:
  - Location: src/functions/opportunity/get_opportunity.py
  - Triển khai logic lấy chi tiết cơ hội:
    - Truy vấn dữ liệu từ bảng OPPORTUNITIES trên DynamoDB theo opportunity_id
    - Kết hợp với dữ liệu từ các bảng liên quan (nếu cần):
      - Thông tin leader được gán
      - Thông tin notes gần đây (3-5 notes mới nhất)
      - Thông tin trạng thái đồng bộ
  - Triển khai logic xử lý lỗi khi không tìm thấy cơ hội

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho cơ hội:
  - Location: src/models/opportunity.py
  - Định nghĩa model cho cơ hội kinh doanh:
    - Các trường cơ bản: id, name, description, status, value, etc.
    - Các trường tính toán: follow_up_status, days_since_last_interaction, etc.
  - Triển khai các method truy vấn DynamoDB:
    - list_opportunities(limit, next_token, filters, search_term, sort_by, sort_order)
    - get_opportunity_by_id(opportunity_id)
    - calculate_follow_up_status(opportunity)
  - Xử lý chuyển đổi giữa DynamoDB Item và model object

### Tích hợp với API Gateway

- [ ] Cấu hình API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/opportunities:
    - Các tham số query: page_size, next_token, các tham số filter và search
    - Liên kết với Lambda function list_opportunities
    - Phân quyền phù hợp
  - Cấu hình route GET /api/v1/opportunities/{id}:
    - Path parameter: id
    - Liên kết với Lambda function get_opportunity
    - Phân quyền phù hợp
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/opportunity/
  - Test case cho list_opportunities.py:
    - Test lấy danh sách cơ hội với các filter khác nhau
    - Test phân trang
    - Test tìm kiếm text
    - Test sắp xếp
    - Test tính toán trạng thái follow-up
    - Test xử lý lỗi
  - Test case cho get_opportunity.py:
    - Test lấy chi tiết cơ hội thành công
    - Test xử lý khi cơ hội không tồn tại
    - Test xử lý các trường hợp lỗi

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/opportunities
    - GET /api/v1/opportunities/{id}
  - Mô tả cấu trúc dữ liệu cơ hội (Opportunity)
  - Mô tả các tham số filter, search và sắp xếp
  - Mô tả logic tính toán trạng thái follow-up

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách cơ hội:

```python
# Lấy danh sách cơ hội với filter
import requests

def get_opportunities(api_base_url, token, page_size=10, next_token=None, status=None, 
                     follow_up_status=None, assigned_to=None, search_term=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page_size': page_size
    }
    
    if next_token:
        params['next_token'] = next_token
    
    if status:
        params['status'] = status
    
    if follow_up_status:
        params['follow_up_status'] = follow_up_status
    
    if assigned_to:
        params['assigned_to'] = assigned_to
    
    if search_term:
        params['search'] = search_term
    
    response = requests.get(
        f"{api_base_url}/api/v1/opportunities",
        headers=headers,
        params=params
    )
    
    return response.json()

# Lấy chi tiết một cơ hội
def get_opportunity_details(api_base_url, token, opportunity_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{api_base_url}/api/v1/opportunities/{opportunity_id}",
        headers=headers
    )
    
    return response.json()

# Kết quả mong đợi cho danh sách cơ hội:
# {
#   "items": [
#     {
#       "opportunity_id": "opp-123456",
#       "opportunity_name": "Website Development Project for ABC Corp",
#       "customer_name": "ABC Corporation",
#       "status": "IN_PROGRESS",
#       "potential_value": 75000,
#       "created_at": "2025-04-01T10:00:00Z",
#       "last_interaction_date": "2025-05-10T14:30:00Z",
#       "follow_up_status": "GREEN",
#       "assigned_to": {
#         "user_id": "user123",
#         "name": "Nguyễn Văn A"
#       },
#       "hubspot_id": "hubspot-deal-12345"
#     },
#     // ... more items
#   ],
#   "next_token": "eyJsYXN0X2V2YWx1YXRlZF9rZXkiOnsia2V5IjoiMjAyNS0wNS0xM1QxMDoxNTozMFoifX0=",
#   "count": 10,
#   "total": 45
# }

# Kết quả mong đợi cho chi tiết cơ hội:
# {
#   "opportunity_id": "opp-123456",
#   "opportunity_name": "Website Development Project for ABC Corp",
#   "customer_name": "ABC Corporation",
#   "description": "ABC Corporation needs a new website with e-commerce capabilities...",
#   "status": "IN_PROGRESS",
#   "potential_value": 75000,
#   "probability": 80,
#   "expected_close_date": "2025-07-15T00:00:00Z",
#   "created_at": "2025-04-01T10:00:00Z",
#   "updated_at": "2025-05-10T14:30:00Z",
#   "last_interaction_date": "2025-05-10T14:30:00Z",
#   "follow_up_status": "GREEN",
#   "days_since_last_interaction": 3,
#   "assigned_to": {
#     "user_id": "user123",
#     "name": "Nguyễn Văn A",
#     "email": "nguyen.van.a@company.com"
#   },
#   "onsite_priority": false,
#   "hubspot_id": "hubspot-deal-12345",
#   "last_sync_at": "2025-05-12T08:15:00Z",
#   "sync_status": "SUCCESS",
#   "recent_notes": [
#     {
#       "note_id": "note-123",
#       "content": "Đã gọi điện và đặt lịch hẹn gặp khách hàng vào tuần sau",
#       "created_by": "Nguyễn Văn A",
#       "created_at": "2025-05-10T14:30:00Z"
#     },
#     // ... more notes
#   ]
# }
```

## Tiêu chí hoàn thành

1. Lambda function xem danh sách cơ hội hoạt động chính xác với đầy đủ chức năng filter, search và sort
2. Lambda function xem chi tiết cơ hội hoạt động chính xác
3. Tính toán chính xác trạng thái follow-up (Red/Yellow/Green)
4. API endpoints được cấu hình đúng với phân trang và phân quyền
5. Unit tests đạt coverage > 80%
6. Tài liệu API đầy đủ

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Cân nhắc sử dụng GSI (Global Secondary Indexes) trong DynamoDB để hỗ trợ các query pattern phức tạp
- Đảm bảo hiệu suất cao khi tìm kiếm và lọc trên dataset lớn
- Tính toán follow-up status có thể được thực hiện on-the-fly hoặc được lưu trữ và cập nhật định kỳ, tùy thuộc vào yêu cầu hiệu suất
- Cân nhắc việc sử dụng caching (như ElastiCache) cho các truy vấn phổ biến 