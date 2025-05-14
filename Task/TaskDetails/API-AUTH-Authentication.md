**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-27 | AI Assistant | Tạo checklist cho API Authentication | -           | Draft     |
| 1.1     | 2024-07-28 | AI Assistant | Cập nhật trạng thái task đã hoàn thành | -           | Draft     |

---

## 1. Mục tiêu  
Checklist phát triển các API xác thực (Authentication) theo mô hình Lambda serverless, đảm bảo đúng chuẩn, dễ test, dễ bảo trì.

---

## Backend: API/Lambda - Authentication & Authorization

### **API-AUTH-001: POST /api/v1/auth/login** (Xác thực người dùng, trả về token)

- [x] Task 1: Định nghĩa model User mapping DynamoDB (theo dynamodb_structure.json) (High Priority) (Completed)
- [x] Task 2: Tạo repository UserRepository (CRUD, query, tìm theo username) (High Priority, depends on Task 1) (Completed)
- [x] Task 3: Tạo service AuthService.login (xác thực password, tạo JWT) (High Priority, depends on Task 2) (Completed)
- [x] Task 4: Tạo Lambda handler login (High Priority, depends on Task 3) (Completed)
- [x] Task 5: Định nghĩa schema validate input (username, password) (High Priority, song song Task 4) (Completed)
- [x] Task 6: Tạo utility để băm và so sánh password (High Priority, song song Task 3) (Completed)
- [x] Task 7: Tạo utility để tạo và xác thực JWT (High Priority, song song Task 3) (Completed)
- [x] Task 8: Logging, error handling (High Priority, song song Task 4) (Completed)
- [x] Task 9: Viết unit test cho repository (Pytest, mock DynamoDB) (High Priority, song song Task 2) (Completed)
- [x] Task 10: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 3) (Completed)
- [x] Task 11: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4) (Completed)
- [x] Task 12: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler) (Completed)
- [x] Task 13: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler) (Completed)
- [x] Task 14: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên) (Completed)

---

### **API-AUTH-002: POST /api/v1/auth/logout** (Hủy token phía server)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service AuthService.logout (invalidate token) (High Priority)
- [ ] Task 3: Tạo Lambda handler logout (High Priority, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (cần xác thực) (High Priority, song song Task 3)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 7: Update tài liệu checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-AUTH-003: GET /api/v1/auth/me** (Lấy thông tin user hiện tại)

- [ ] Task 1: Tạo service AuthService.get_current_user (từ token) (High Priority)
- [ ] Task 2: Tạo Lambda handler get_current_user (High Priority, depends on Task 1)
- [ ] Task 3: Tạo repository RoleRepository (tìm quyền của role) (High Priority, song song Task 1)
- [ ] Task 4: Xử lý phân quyền (cần xác thực) (High Priority, song song Task 2)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 2)
- [ ] Task 6: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 7: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-AUTH-004: POST /api/v1/auth/refresh-token** (Làm mới token)

- [ ] Task 1: Định nghĩa schema validate input (refresh_token) (High Priority)
- [ ] Task 2: Tạo service AuthService.refresh_token (High Priority)
- [ ] Task 3: Tạo Lambda handler refresh_token (High Priority, depends on Task 2)
- [ ] Task 4: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **Lambda Authorizer (API Gateway Custom Authorizer)**

- [ ] Task 1: Tạo Lambda function authorizer (kiểm tra token) (High Priority)
- [ ] Task 2: Tạo utility đọc/xác thực JWT (High Priority)
- [ ] Task 3: Cấu hình caching token (High Priority)
- [ ] Task 4: Logging, error handling (High Priority)
- [ ] Task 5: Viết unit test cho authorizer (High Priority)
- [ ] Task 6: Khai báo authorizer trong template.yaml (High Priority)
- [ ] Task 7: Kết nối authorizer với các API cần xác thực (High Priority)

---

## Infrastructure (AWS Serverless)

- [x] Task 1: Cập nhật template.yaml cho các function auth (High Priority) (Completed)
- [x] Task 2: Định nghĩa IAM role, policy cho Lambda truy cập DynamoDB (High Priority) (Completed)
- [x] Task 3: Định nghĩa cấu hình bảo mật JWT (key, expiration) (High Priority) (Completed)
- [ ] Task 4: Định nghĩa authorizer và kết nối với API Gateway (High Priority)
- [x] Task 5: Thêm layer common (validation, error, auth) (High Priority) (Completed)
- [x] Task 6: Thêm layer repository (DynamoDB access) (High Priority) (Completed)
- [x] Task 7: Thêm layer service (business logic) (High Priority) (Completed)

---

## Documentation

- [x] Task 1: Update API doc cho API-AUTH-001 (High Priority) (Completed)
- [ ] Task 2: Update API doc cho API-AUTH-002 (High Priority)
- [ ] Task 3: Update API doc cho API-AUTH-003 (High Priority)
- [ ] Task 4: Update API doc cho API-AUTH-004 (High Priority)
- [ ] Task 5: Update doc về authorizer và JWT (High Priority)
- [x] Task 6: Update README hướng dẫn deploy/test (High Priority) (Completed)
- [x] Task 7: Update checklist tiến độ (High Priority) (Completed)

---

## Lưu ý

- Đảm bảo bảo mật cao cho mọi phần của API authentication
- Thực hiện đúng các tiêu chuẩn bảo mật (không lưu plain password, dùng HTTPS, xử lý rate limit...)
- Không bao giờ log/ghi ra JWT token đầy đủ trong log hệ thống
- Đặt thời gian sống (expiration) phù hợp cho token
- Khi hoàn thành task, đánh dấu `[x]` và ghi chú `(Completed)` 