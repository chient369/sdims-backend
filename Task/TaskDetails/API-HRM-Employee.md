**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-27 | AI Assistant | Tạo checklist cho API Quản lý Nhân sự | -           | Draft     |

---

## 1. Mục tiêu  
Checklist phát triển các API quản lý nhân sự (HRM) theo mô hình Lambda serverless, đảm bảo đúng chuẩn, dễ test, dễ bảo trì.

---

## Backend: API/Lambda - Quản lý Nhân sự

### **API-HRM-001: GET /api/v1/employees** (Lấy danh sách nhân viên)

- [ ] Task 1: Định nghĩa model Employee mapping DynamoDB (theo dynamodb_structure.json) (High Priority)
- [ ] Task 2: Tạo repository EmployeeRepository (CRUD, query, filter) (High Priority, depends on Task 1)
- [ ] Task 3: Tạo service EmployeeService.get_employees (High Priority, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_employees (High Priority, depends on Task 3)
- [ ] Task 5: Validate input (query params: page, filter, ...) (High Priority, song song Task 4)
- [ ] Task 6: Xử lý phân quyền (employee:read:all/team/own) (High Priority, song song Task 4)
- [ ] Task 7: Logging, error handling (High Priority, song song Task 4)
- [ ] Task 8: Viết unit test cho repository (Pytest, mock DynamoDB) (High Priority, song song Task 2)
- [ ] Task 9: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 3)
- [ ] Task 10: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4)
- [ ] Task 11: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 12: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 13: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-HRM-002: POST /api/v1/employees** (Thêm nhân viên mới)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service EmployeeService.create_employee (High Priority)
- [ ] Task 3: Tạo Lambda handler create_employee (High Priority, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (employee:create) (High Priority, song song Task 3)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-HRM-003: GET /api/v1/employees/{employeeId}** (Xem thông tin chi tiết nhân viên)

- [ ] Task 1: Tạo service EmployeeService.get_employee_detail (High Priority)
- [ ] Task 2: Tạo Lambda handler get_employee_detail (High Priority, depends on Task 1)
- [ ] Task 3: Validate input (path parameter) (High Priority, song song Task 2)
- [ ] Task 4: Xử lý phân quyền (employee:read:all/team/own) (High Priority, song song Task 2)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 2)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 1)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 2)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-HRM-004: PUT /api/v1/employees/{employeeId}** (Cập nhật thông tin nhân viên)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service EmployeeService.update_employee (High Priority)
- [ ] Task 3: Tạo Lambda handler update_employee (High Priority, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (employee:update:all/team/own) (High Priority, song song Task 3)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-HRM-005: DELETE /api/v1/employees/{employeeId}** (Xóa nhân viên - soft delete)

- [ ] Task 1: Tạo service EmployeeService.delete_employee (Trung bình)
- [ ] Task 2: Tạo Lambda handler delete_employee (Trung bình, depends on Task 1)
- [ ] Task 3: Validate input (path parameter) (Trung bình, song song Task 2)
- [ ] Task 4: Xử lý phân quyền (employee:delete) (Trung bình, song song Task 2)
- [ ] Task 5: Logging, error handling (Trung bình, song song Task 2)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 1)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 2)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

## Infrastructure (AWS Serverless)

- [ ] Task 1: Cập nhật template.yaml cho các function nhân sự (High Priority)
- [ ] Task 2: Định nghĩa IAM role, policy cho Lambda truy cập DynamoDB (High Priority)
- [ ] Task 3: Thêm layer common (validation, error, auth) (High Priority)
- [ ] Task 4: Thêm layer repository (DynamoDB access) (High Priority)
- [ ] Task 5: Thêm layer service (business logic) (High Priority)

---

## Documentation

- [ ] Task 1: Update API doc cho API-HRM-001 (High Priority)
- [ ] Task 2: Update API doc cho API-HRM-002 (High Priority)
- [ ] Task 3: Update API doc cho API-HRM-003 (High Priority)
- [ ] Task 4: Update API doc cho API-HRM-004 (High Priority)
- [ ] Task 5: Update API doc cho API-HRM-005 (Trung bình)
- [ ] Task 6: Update README hướng dẫn deploy/test (High Priority)
- [ ] Task 7: Update checklist tiến độ (High Priority)

---

## Testing

- [ ] Task 1: Đảm bảo coverage ≥ 80% cho các function (High Priority)
- [ ] Task 2: Mock DynamoDB cho unit test (High Priority)
- [ ] Task 3: Test case bao gồm happy path và error case (High Priority)
- [ ] Task 4: Test phân quyền (quyền hợp lệ và không hợp lệ) (High Priority)

---

## Lưu ý

- Đảm bảo validate input kỹ để tránh lỗi, đặc biệt là input từ người dùng
- Kiểm tra phân quyền chặt chẽ theo quy định trong BD/permissions_definition.md
- Khi hoàn thành task, đánh dấu `[x]` và ghi chú `(Completed)` 