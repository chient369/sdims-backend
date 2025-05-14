**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-27 | AI Assistant | Tạo checklist cho API Quản trị Hệ thống | -           | Draft     |

---

## 1. Mục tiêu  
Checklist phát triển các API quản trị hệ thống (Admin) theo mô hình Lambda serverless, đảm bảo đúng chuẩn, dễ test, dễ bảo trì.

---

## Backend: API/Lambda - Quản trị Hệ thống (Admin)

### **API-ADM-001: GET /api/v1/admin/users** (Lấy danh sách người dùng)

- [ ] Task 1: Tạo service AdminService.get_users (Trung bình)
- [ ] Task 2: Tạo Lambda handler get_users (Trung bình, depends on Task 1)
- [ ] Task 3: Validate input (query params) (Trung bình, song song Task 2)
- [ ] Task 4: Xử lý phân quyền (user:read) (Trung bình, song song Task 2)
- [ ] Task 5: Logging, error handling (Trung bình, song song Task 2)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 1)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 2)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-002: POST /api/v1/admin/users** (Tạo người dùng mới)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (Trung bình)
- [ ] Task 2: Tạo service AdminService.create_user (Trung bình)
- [ ] Task 3: Tạo Lambda handler create_user (Trung bình, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (user:create) (Trung bình, song song Task 3)
- [ ] Task 5: Logging, error handling (Trung bình, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-004: PUT /api/v1/admin/users/{userId}** (Cập nhật thông tin người dùng)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (Trung bình)
- [ ] Task 2: Tạo service AdminService.update_user (Trung bình)
- [ ] Task 3: Tạo Lambda handler update_user (Trung bình, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (user:update) (Trung bình, song song Task 3)
- [ ] Task 5: Logging, error handling (Trung bình, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-006: GET /api/v1/admin/roles** (Lấy danh sách vai trò)

- [ ] Task 1: Định nghĩa model Role mapping DynamoDB (Trung bình)
- [ ] Task 2: Tạo repository RoleRepository (CRUD, query) (Trung bình, depends on Task 1)
- [ ] Task 3: Tạo service AdminService.get_roles (Trung bình, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_roles (Trung bình, depends on Task 3)
- [ ] Task 5: Xử lý phân quyền (role:read) (Trung bình, song song Task 4)
- [ ] Task 6: Logging, error handling (Trung bình, song song Task 4)
- [ ] Task 7: Viết unit test cho repository (Pytest, mock DynamoDB) (Trung bình, song song Task 2)
- [ ] Task 8: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 3)
- [ ] Task 9: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 4)
- [ ] Task 10: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 11: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 12: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-008: PUT /api/v1/admin/roles/{roleId}** (Cập nhật vai trò)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (Trung bình)
- [ ] Task 2: Tạo service AdminService.update_role (Trung bình)
- [ ] Task 3: Tạo Lambda handler update_role (Trung bình, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (role:update) (Trung bình, song song Task 3)
- [ ] Task 5: Logging, error handling (Trung bình, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-010: GET /api/v1/admin/permissions** (Lấy danh sách quyền)

- [ ] Task 1: Định nghĩa model Permission mapping DynamoDB (Trung bình)
- [ ] Task 2: Tạo repository PermissionRepository (Trung bình, depends on Task 1)
- [ ] Task 3: Tạo service AdminService.get_permissions (Trung bình, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_permissions (Trung bình, depends on Task 3)
- [ ] Task 5: Xử lý phân quyền (permission:read) (Trung bình, song song Task 4)
- [ ] Task 6: Logging, error handling (Trung bình, song song Task 4)
- [ ] Task 7: Viết unit test cho repository (Pytest, mock DynamoDB) (Trung bình, song song Task 2)
- [ ] Task 8: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 3)
- [ ] Task 9: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 4)
- [ ] Task 10: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 11: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 12: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-011: GET /api/v1/admin/configs** (Lấy danh sách cấu hình hệ thống)

- [ ] Task 1: Định nghĩa model SystemConfig mapping DynamoDB (Trung bình)
- [ ] Task 2: Tạo repository SystemConfigRepository (Trung bình, depends on Task 1)
- [ ] Task 3: Tạo service AdminService.get_configs (Trung bình, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_configs (Trung bình, depends on Task 3)
- [ ] Task 5: Xử lý phân quyền (config:read) (Trung bình, song song Task 4)
- [ ] Task 6: Logging, error handling (Trung bình, song song Task 4)
- [ ] Task 7: Viết unit test cho repository (Pytest, mock DynamoDB) (Trung bình, song song Task 2)
- [ ] Task 8: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 3)
- [ ] Task 9: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 4)
- [ ] Task 10: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 11: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 12: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-012: PUT /api/v1/admin/configs/{configKey}** (Cập nhật cấu hình)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (Trung bình)
- [ ] Task 2: Tạo service AdminService.update_config (Trung bình)
- [ ] Task 3: Tạo Lambda handler update_config (Trung bình, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (config:update) (Trung bình, song song Task 3)
- [ ] Task 5: Logging, error handling (Trung bình, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

### **API-ADM-013: GET /api/v1/admin/system-logs** (Xem log hệ thống)

- [ ] Task 1: Tạo service AdminService.get_system_logs (Trung bình)
- [ ] Task 2: Tạo Lambda handler get_system_logs (Trung bình, depends on Task 1)
- [ ] Task 3: Tạo utility tương tác với CloudWatch Logs (Trung bình, song song Task 1)
- [ ] Task 4: Validate input (query params: từ, đến, filter...) (Trung bình, song song Task 2)
- [ ] Task 5: Xử lý phân quyền (system-log:read:all/limited) (Trung bình, song song Task 2)
- [ ] Task 6: Logging, error handling (Trung bình, song song Task 2)
- [ ] Task 7: Viết unit test cho service (Pytest, mock CloudWatch) (Trung bình, song song Task 1)
- [ ] Task 8: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 2)
- [ ] Task 9: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 11: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

## Infrastructure (AWS Serverless)

- [ ] Task 1: Cập nhật template.yaml cho các function admin (Trung bình)
- [ ] Task 2: Định nghĩa IAM role, policy cho Lambda truy cập DynamoDB (Trung bình)
- [ ] Task 3: Định nghĩa IAM role, policy cho Lambda truy cập CloudWatch Logs (Trung bình)
- [ ] Task 4: Thêm layer common (validation, error, auth) (Trung bình)
- [ ] Task 5: Thêm layer repository (DynamoDB access) (Trung bình)
- [ ] Task 6: Thêm layer service (business logic) (Trung bình)
- [ ] Task 7: Thêm layer logs (CloudWatch Logs access) (Trung bình)

---

## Documentation

- [ ] Task 1: Update API doc cho API-ADM-001 (Trung bình)
- [ ] Task 2: Update API doc cho API-ADM-002 (Trung bình)
- [ ] Task 3: Update API doc cho API-ADM-004 (Trung bình)
- [ ] Task 4: Update API doc cho API-ADM-006 (Trung bình)
- [ ] Task 5: Update API doc cho API-ADM-008 (Trung bình)
- [ ] Task 6: Update API doc cho API-ADM-010 (Trung bình)
- [ ] Task 7: Update API doc cho API-ADM-011 (Trung bình)
- [ ] Task 8: Update API doc cho API-ADM-012 (Trung bình)
- [ ] Task 9: Update API doc cho API-ADM-013 (Trung bình)
- [ ] Task 10: Update README hướng dẫn deploy/test (Trung bình)
- [ ] Task 11: Update checklist tiến độ (Trung bình)

---

## Testing

- [ ] Task 1: Đảm bảo coverage ≥ 80% cho các function (Trung bình)
- [ ] Task 2: Mock DynamoDB cho unit test (Trung bình)
- [ ] Task 3: Mock CloudWatch Logs cho unit test (Trung bình)
- [ ] Task 4: Test case bao gồm happy path và error case (Trung bình)
- [ ] Task 5: Test phân quyền (quyền hợp lệ và không hợp lệ) (Trung bình)

---

## Lưu ý

- Đảm bảo xử lý phân quyền chặt chẽ vì đây là các chức năng admin với quyền cao
- Validate input kỹ, đặc biệt là ở các API cập nhật cấu hình hệ thống
- Lưu log chi tiết các hoạt động admin (ai thực hiện, thời gian, hành động, kết quả)
- Khi hoàn thành task, đánh dấu `[x]` và ghi chú `(Completed)` 