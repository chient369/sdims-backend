**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function đánh dấu ưu tiên onsite | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function đánh dấu ưu tiên onsite cho cơ hội kinh doanh, cho phép đội sales dễ dàng quản lý và xác định các cơ hội cần được ưu tiên theo dõi tại văn phòng.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-OPP-006  
**Task Name:** Phát triển Lambda function đánh dấu ưu tiên onsite  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-OPP-003 (Triển khai Lambda functions quản lý cơ hội)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- PUT /api/v1/opportunities/{id}/onsite (API-OPP-008)

## Mô tả

Triển khai Lambda function cho phép người dùng đánh dấu một cơ hội kinh doanh là "ưu tiên onsite". Tính năng này giúp đội sales dễ dàng đánh dấu và theo dõi các cơ hội cần được ưu tiên xử lý khi họ có mặt tại văn phòng, ví dụ như các cơ hội cần gặp trực tiếp khách hàng, hoặc cơ hội cần thảo luận trực tiếp với đội ngũ kỹ thuật.

Chức năng này hoạt động như một toggle, cho phép bật/tắt trạng thái onsite priority mà không làm thay đổi các thông tin khác của cơ hội.

## Chi tiết công việc

### Phát triển Lambda function chuyển đổi trạng thái ưu tiên onsite

- [ ] Triển khai Lambda function xử lý PUT /api/v1/opportunities/{id}/onsite:
  - Location: src/functions/opportunity/toggle_onsite_priority.py
  - Triển khai logic chuyển đổi trạng thái ưu tiên onsite:
    - Xác thực người dùng và kiểm tra quyền truy cập
    - Kiểm tra sự tồn tại của cơ hội
    - Chuyển đổi trạng thái onsite_priority (true <-> false)
    - Cập nhật thông tin vào DynamoDB
    - Ghi log thay đổi vào OPPORTUNITY_HISTORY
  - Triển khai xử lý các trường hợp lỗi:
    - Cơ hội không tồn tại
    - Người dùng không có quyền truy cập
    - Lỗi khi cập nhật dữ liệu

### Cập nhật Data Access Layer

- [ ] Cập nhật lớp truy cập dữ liệu cho cơ hội:
  - Location: src/models/opportunity.py
  - Bổ sung method chuyển đổi trạng thái ưu tiên onsite:
    - toggle_onsite_priority(opportunity_id, toggled_by)
  - Thêm lịch sử thay đổi:
    - add_opportunity_history(opportunity_id, action_type, details, performed_by)

### Cấu hình API Endpoint

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route PUT /api/v1/opportunities/{id}/onsite:
    - Method: PUT
    - Path parameter: id (opportunity_id)
    - Request body: không yêu cầu (hoặc có thể bao gồm priority_value nếu muốn đặt một giá trị cụ thể thay vì toggle)
    - Liên kết với Lambda function
    - Phân quyền phù hợp (Sales, Team Lead, Admin)
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Cập nhật API Xem danh sách cơ hội

- [ ] Cập nhật Lambda function xem danh sách cơ hội để hỗ trợ lọc theo trạng thái onsite_priority:
  - Location: src/functions/opportunity/list_opportunities.py
  - Bổ sung tham số filter onsite_priority (boolean)
  - Cập nhật query DynamoDB để hỗ trợ filter mới

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/opportunity/
  - Test case cho toggle_onsite_priority.py:
    - Test chuyển đổi từ false sang true
    - Test chuyển đổi từ true sang false
    - Test khi cơ hội không tồn tại
    - Test khi người dùng không có quyền
    - Test ghi log lịch sử thay đổi
  - Test case cho lọc theo onsite_priority:
    - Test filter onsite_priority=true
    - Test filter onsite_priority=false

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho PUT /api/v1/opportunities/{id}/onsite
  - Cập nhật tài liệu API GET /api/v1/opportunities với tham số filter onsite_priority
  - Mô tả cấu trúc request và response
  - Mô tả các trường hợp lỗi và cách xử lý

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách chuyển đổi trạng thái ưu tiên onsite:

```python
# Chuyển đổi trạng thái ưu tiên onsite cho cơ hội
import requests

def toggle_opportunity_onsite_priority(api_base_url, token, opportunity_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.put(
        f"{api_base_url}/api/v1/opportunities/{opportunity_id}/onsite",
        headers=headers
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "opportunity_id": "opp-123456",
#   "opportunity_name": "Website Development Project for ABC Corp",
#   "onsite_priority": true, # Giá trị sau khi toggle
#   "updated_at": "2025-05-13T17:15:30Z",
#   "updated_by": {
#     "user_id": "user123",
#     "name": "Nguyễn Văn A"
#   }
# }
```

Ví dụ về cách lọc danh sách cơ hội theo trạng thái ưu tiên onsite:

```python
# Lấy danh sách cơ hội với filter onsite_priority
def get_onsite_priority_opportunities(api_base_url, token, page_size=10, next_token=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page_size': page_size,
        'onsite_priority': 'true'
    }
    
    if next_token:
        params['next_token'] = next_token
    
    response = requests.get(
        f"{api_base_url}/api/v1/opportunities",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả sẽ trả về danh sách các cơ hội có onsite_priority = true
```

## Tiêu chí hoàn thành

1. Lambda function chuyển đổi trạng thái ưu tiên onsite hoạt động chính xác
2. Trạng thái onsite_priority được cập nhật đúng trong database
3. Lịch sử thay đổi được ghi lại
4. API endpoint được cấu hình đúng với phân quyền
5. API xem danh sách cơ hội hỗ trợ lọc theo trạng thái onsite_priority
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ

## Ước tính thời gian

- 1-2 ngày làm việc

## Ghi chú

- Cân nhắc thêm thuộc tính bổ sung như priority_reason để người dùng có thể ghi chú lý do đánh dấu ưu tiên
- Xem xét triển khai tính năng thông báo cho người được gán (assigned leader) khi có thay đổi trạng thái ưu tiên onsite
- Cân nhắc tính năng hiển thị danh sách ưu tiên onsite trên dashboard chính
- Xem xét tính năng đặt thứ tự ưu tiên (priority order) nếu có nhiều cơ hội được đánh dấu ưu tiên onsite 