**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function gán Leader cho cơ hội | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function cho phép gán Leader phụ trách cho cơ hội kinh doanh và gửi thông báo tới người được gán nhiệm vụ.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-OPP-004  
**Task Name:** Phát triển Lambda function gán Leader cho cơ hội  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-OPP-003 (Triển khai Lambda functions quản lý cơ hội)
- BE-NOT-001 (Triển khai hệ thống thông báo) - *Nếu có*

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- POST /api/v1/opportunities/{id}/assign (API-OPP-005)

## Mô tả

Triển khai Lambda function cho phép Admin hoặc Trưởng phòng gán một Leader phụ trách cho một cơ hội kinh doanh. Chức năng này bao gồm cập nhật thông tin Leader được gán trong dữ liệu cơ hội và gửi thông báo cho người được gán nhiệm vụ.

Việc gán Leader cho mỗi cơ hội kinh doanh là bước quan trọng trong quy trình quản lý cơ hội, giúp xác định rõ trách nhiệm và đảm bảo mỗi cơ hội đều được theo dõi và xử lý kịp thời.

## Chi tiết công việc

### Phát triển Lambda function gán Leader cho cơ hội

- [ ] Triển khai Lambda function xử lý POST /api/v1/opportunities/{id}/assign:
  - Triển khai logic gán Leader cho cơ hội:
    - Xác thực và kiểm tra quyền hạn của người thực hiện gán (Admin hoặc Trưởng phòng)
    - Kiểm tra sự tồn tại của cơ hội và người dùng được gán
    - Cập nhật thông tin Leader được gán trong bảng OPPORTUNITIES
    - Ghi lại lịch sử thay đổi Leader trong bảng OPPORTUNITY_HISTORY
    - Gửi thông báo cho người được gán nhiệm vụ
  - Triển khai xử lý các trường hợp lỗi:
    - Cơ hội không tồn tại
    - Người dùng được gán không tồn tại hoặc không có quyền phù hợp
    - Người thực hiện gán không có quyền
    - Lỗi khi cập nhật dữ liệu

### Cập nhật Data Access Layer

- [ ] Cập nhật lớp truy cập dữ liệu cho cơ hội:
  - Bổ sung method cập nhật Leader:
    - assign_leader(opportunity_id, leader_id, assigned_by)
  - Thêm lịch sử thay đổi:
    - add_opportunity_history(opportunity_id, action_type, details, performed_by)

### Phát triển hệ thống thông báo

- [ ] Triển khai service gửi thông báo:
  - Cài đặt method gửi thông báo khi được gán:
    - send_assignment_notification(leader_id, opportunity_id, opportunity_name, assigned_by)
  - Tích hợp với Amazon SNS hoặc SES để gửi email thông báo
  - Tích hợp với cơ chế thông báo trong ứng dụng (nếu có)

### Cấu hình API Endpoint

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route POST /api/v1/opportunities/{id}/assign:
    - Method: POST
    - Path parameter: id (opportunity_id)
    - Request body: leader_id
    - Liên kết với Lambda function
    - Phân quyền: chỉ Admin và Trưởng phòng mới có quyền
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền


### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho POST /api/v1/opportunities/{id}/assign
  - Mô tả cấu trúc request và response
  - Mô tả các trường hợp lỗi và cách xử lý
  - Mô tả quy trình gửi thông báo

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách gán Leader cho cơ hội:

```python
# Gán Leader cho cơ hội
import requests

def assign_leader_to_opportunity(api_base_url, token, opportunity_id, leader_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'leader_id': leader_id
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/opportunities/{opportunity_id}/assign",
        headers=headers,
        json=payload
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "success": true,
#   "message": "Leader assigned successfully",
#   "opportunity": {
#     "opportunity_id": "opp-123456",
#     "opportunity_name": "Website Development Project for ABC Corp",
#     "assigned_to": {
#       "user_id": "user456",
#       "name": "Trần Thị B"
#     },
#     "assigned_at": "2025-05-13T15:30:00Z",
#     "assigned_by": {
#       "user_id": "user789",
#       "name": "Lê Văn C"
#     }
#   },
#   "notification_sent": true
# }
```

## Tiêu chí hoàn thành

1. Lambda function gán Leader cho cơ hội hoạt động chính xác
2. Thông tin gán Leader được cập nhật vào database
3. Lịch sử thay đổi được ghi lại
4. Thông báo được gửi đến Leader được gán
5. API endpoint được cấu hình đúng với phân quyền

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Đảm bảo thông báo được gửi một cách không đồng bộ để tránh làm chậm API response
- Cân nhắc triển khai cơ chế retry cho việc gửi thông báo nếu có lỗi
- Đảm bảo các quyền truy cập được kiểm tra chặt chẽ để chỉ người dùng có quyền mới có thể gán Leader
- Xem xét thêm tùy chọn tự động gán Leader dựa trên logic phân bổ tải (load balancing) nếu cần thiết 