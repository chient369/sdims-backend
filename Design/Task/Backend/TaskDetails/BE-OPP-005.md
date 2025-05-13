**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý ghi chú cơ hội | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý ghi chú (notes) cho cơ hội kinh doanh, cho phép người dùng ghi lại các tương tác với khách hàng và cập nhật trạng thái tương tác.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-OPP-005  
**Task Name:** Triển khai Lambda functions quản lý ghi chú cơ hội  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-OPP-003 (Triển khai Lambda functions quản lý cơ hội)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- POST /api/v1/opportunities/{id}/notes (API-OPP-006)
- GET /api/v1/opportunities/{id}/notes (API-OPP-007)

## Mô tả

Triển khai các Lambda functions cho phép người dùng thêm và xem ghi chú (notes) liên quan đến cơ hội kinh doanh. Chức năng này rất quan trọng để theo dõi các tương tác với khách hàng, ghi lại tiến độ của cơ hội, và cập nhật thông tin cho các thành viên trong nhóm.

Mỗi khi một ghi chú mới được thêm vào, hệ thống sẽ tự động cập nhật trường `last_interaction_date` của cơ hội, giúp tính toán chính xác trạng thái follow-up (Red/Yellow/Green) dựa trên thời gian tương tác cuối cùng.

## Chi tiết công việc

### Phát triển Lambda function thêm ghi chú mới

- [ ] Triển khai Lambda function xử lý POST /api/v1/opportunities/{id}/notes:
  - Location: src/functions/opportunity/create_note.py
  - Triển khai logic thêm ghi chú mới:
    - Xác thực người dùng và kiểm tra quyền truy cập
    - Kiểm tra sự tồn tại của cơ hội
    - Tạo ghi chú mới trong bảng OPPORTUNITY_NOTES
    - Cập nhật trường `last_interaction_date` trong bảng OPPORTUNITIES
    - Tính toán lại trạng thái follow-up của cơ hội
  - Triển khai xử lý các trường hợp lỗi:
    - Cơ hội không tồn tại
    - Người dùng không có quyền truy cập
    - Lỗi khi tạo ghi chú hoặc cập nhật dữ liệu

### Phát triển Lambda function xem danh sách ghi chú

- [ ] Triển khai Lambda function xử lý GET /api/v1/opportunities/{id}/notes:
  - Location: src/functions/opportunity/list_notes.py
  - Triển khai logic lấy danh sách ghi chú:
    - Xác thực người dùng và kiểm tra quyền truy cập
    - Kiểm tra sự tồn tại của cơ hội
    - Truy vấn danh sách ghi chú từ bảng OPPORTUNITY_NOTES
    - Hỗ trợ phân trang với tokenization (DynamoDB pagination)
    - Sắp xếp ghi chú theo thời gian tạo (mặc định là mới nhất trước)
  - Triển khai xử lý các trường hợp lỗi:
    - Cơ hội không tồn tại
    - Người dùng không có quyền truy cập

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho ghi chú:
  - Location: src/models/opportunity_note.py
  - Định nghĩa model cho ghi chú cơ hội:
    - Các trường cơ bản: note_id, opportunity_id, content, created_by, created_at, etc.
  - Triển khai các method truy vấn DynamoDB:
    - create_note(opportunity_id, content, created_by)
    - list_notes(opportunity_id, limit, next_token)
    - get_note_by_id(note_id)

- [ ] Cập nhật lớp truy cập dữ liệu cho cơ hội:
  - Location: src/models/opportunity.py
  - Bổ sung method cập nhật thời gian tương tác cuối:
    - update_last_interaction(opportunity_id, interaction_date)
  - Cập nhật method tính toán trạng thái follow-up để sử dụng thời gian tương tác cuối:
    - calculate_follow_up_status(opportunity)

### Cấu hình API Endpoints

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route POST /api/v1/opportunities/{id}/notes:
    - Method: POST
    - Path parameter: id (opportunity_id)
    - Request body: content (nội dung ghi chú)
    - Liên kết với Lambda function
    - Phân quyền phù hợp
  - Cấu hình route GET /api/v1/opportunities/{id}/notes:
    - Method: GET
    - Path parameter: id (opportunity_id)
    - Tham số query: page_size, next_token
    - Liên kết với Lambda function
    - Phân quyền phù hợp
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/opportunity/
  - Test case cho create_note.py:
    - Test tạo ghi chú thành công
    - Test cập nhật last_interaction_date
    - Test khi cơ hội không tồn tại
    - Test khi người dùng không có quyền
  - Test case cho list_notes.py:
    - Test lấy danh sách ghi chú
    - Test phân trang
    - Test sắp xếp theo thời gian
    - Test khi cơ hội không tồn tại
  - Test case cho models:
    - Test các method truy cập dữ liệu

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - POST /api/v1/opportunities/{id}/notes
    - GET /api/v1/opportunities/{id}/notes
  - Mô tả cấu trúc request và response
  - Mô tả cách thức cập nhật last_interaction_date và ảnh hưởng đến trạng thái follow-up

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách thêm và xem ghi chú cơ hội:

```python
# Thêm ghi chú mới cho cơ hội
import requests

def add_opportunity_note(api_base_url, token, opportunity_id, content):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'content': content
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/opportunities/{opportunity_id}/notes",
        headers=headers,
        json=payload
    )
    
    return response.json()

# Kết quả mong đợi khi thêm ghi chú:
# {
#   "note_id": "note-123456",
#   "opportunity_id": "opp-123456",
#   "content": "Đã gọi điện và trao đổi với khách hàng về yêu cầu dự án. Họ rất quan tâm và sẽ gửi brief vào tuần sau.",
#   "created_by": {
#     "user_id": "user123",
#     "name": "Nguyễn Văn A"
#   },
#   "created_at": "2025-05-13T16:45:30Z",
#   "opportunity_updated": {
#     "last_interaction_date": "2025-05-13T16:45:30Z",
#     "follow_up_status": "GREEN"
#   }
# }

# Lấy danh sách ghi chú của cơ hội
def get_opportunity_notes(api_base_url, token, opportunity_id, page_size=10, next_token=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page_size': page_size
    }
    
    if next_token:
        params['next_token'] = next_token
    
    response = requests.get(
        f"{api_base_url}/api/v1/opportunities/{opportunity_id}/notes",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi khi lấy danh sách ghi chú:
# {
#   "items": [
#     {
#       "note_id": "note-123456",
#       "opportunity_id": "opp-123456",
#       "content": "Đã gọi điện và trao đổi với khách hàng về yêu cầu dự án. Họ rất quan tâm và sẽ gửi brief vào tuần sau.",
#       "created_by": {
#         "user_id": "user123",
#         "name": "Nguyễn Văn A"
#       },
#       "created_at": "2025-05-13T16:45:30Z"
#     },
#     {
#       "note_id": "note-123455",
#       "opportunity_id": "opp-123456",
#       "content": "Đã nhận được email từ khách hàng về ngân sách dự kiến.",
#       "created_by": {
#         "user_id": "user456",
#         "name": "Trần Thị B"
#       },
#       "created_at": "2025-05-10T09:15:00Z"
#     },
#     // ... more notes
#   ],
#   "next_token": "eyJsYXN0X2V2YWx1YXRlZF9rZXkiOnsia2V5IjoiMjAyNS0wNS0xMFQwOToxNTowMFoifX0=",
#   "count": 10
# }
```

## Tiêu chí hoàn thành

1. Lambda function thêm ghi chú hoạt động chính xác
2. Lambda function xem danh sách ghi chú hoạt động chính xác
3. Trường `last_interaction_date` được cập nhật đúng khi thêm ghi chú mới
4. Trạng thái follow-up được tính toán lại chính xác
5. API endpoints được cấu hình đúng với phân trang và phân quyền
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý đến hiệu suất khi có nhiều ghi chú cho một cơ hội
- Xem xét giới hạn số lượng ghi chú hiển thị trong API xem chi tiết cơ hội để đảm bảo hiệu suất
- Cân nhắc việc triển khai các cơ chế thông báo cho những người liên quan khi có ghi chú mới
- Xem xét liệu có nên yêu cầu loại ghi chú (ví dụ: cuộc gọi, email, cuộc họp) để phân loại các tương tác 