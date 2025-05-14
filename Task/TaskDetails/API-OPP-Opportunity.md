**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-27 | AI Assistant | Tạo checklist cho API Quản lý Cơ hội | -           | Draft     |

---

## 1. Mục tiêu  
Checklist phát triển các API quản lý cơ hội kinh doanh (Opportunity) theo mô hình Lambda serverless, đảm bảo đúng chuẩn, dễ test, dễ bảo trì.

---

## Backend: API/Lambda - Quản lý Cơ hội Kinh doanh

### **API-OPP-001: GET /api/v1/opportunities** (Lấy danh sách cơ hội)

- [ ] Task 1: Định nghĩa model Opportunity mapping DynamoDB (theo dynamodb_structure.json) (High Priority)
- [ ] Task 2: Tạo repository OpportunityRepository (CRUD, query, filter) (High Priority, depends on Task 1)
- [ ] Task 3: Tạo service OpportunityService.get_opportunities (High Priority, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_opportunities (High Priority, depends on Task 3)
- [ ] Task 5: Validate input (query params: page, filter, search...) (High Priority, song song Task 4)
- [ ] Task 6: Xử lý phân quyền (opportunity:read:all/assigned) (High Priority, song song Task 4)
- [ ] Task 7: Logging, error handling (High Priority, song song Task 4)
- [ ] Task 8: Viết unit test cho repository (Pytest, mock DynamoDB) (High Priority, song song Task 2)
- [ ] Task 9: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 3)
- [ ] Task 10: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4)
- [ ] Task 11: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 12: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 13: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-OPP-002: GET /api/v1/opportunities/{oppId}** (Lấy chi tiết cơ hội)

- [ ] Task 1: Tạo service OpportunityService.get_opportunity_detail (High Priority)
- [ ] Task 2: Tạo Lambda handler get_opportunity_detail (High Priority, depends on Task 1)
- [ ] Task 3: Validate input (path parameter) (High Priority, song song Task 2)
- [ ] Task 4: Xử lý phân quyền (opportunity:read:all/assigned) (High Priority, song song Task 2)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 2)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 1)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 2)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-OPP-003: POST /api/v1/opportunities/sync** (Đồng bộ từ Hubspot)

- [ ] Task 1: Thiết kế service OpportunityService.sync_from_hubspot (Thấp)
- [ ] Task 2: Tạo Lambda handler sync_opportunities (Thấp, depends on Task 1)
- [ ] Task 3: Tạo kết nối với Hubspot API (Thấp, song song Task 1)
- [ ] Task 4: Xử lý phân quyền (opportunity-sync:config) (Thấp, song song Task 2)
- [ ] Task 5: Logging, error handling (Thấp, song song Task 2)
- [ ] Task 6: Viết unit test cho service (Pytest, mock Hubspot API) (Thấp, song song Task 1)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Thấp, song song Task 2)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Thấp, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Thấp, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Thấp, sau khi hoàn thành các task trên)

---

### **API-OPP-005: POST /api/v1/opportunities/{oppId}/assign** (Gán Leader cho cơ hội)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service OpportunityService.assign_leader (High Priority)
- [ ] Task 3: Tạo Lambda handler assign_leader (High Priority, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (opportunity-assign:update:all) (High Priority, song song Task 3)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-OPP-006: POST /api/v1/opportunities/{oppId}/notes** (Thêm ghi chú cơ hội)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Định nghĩa model OpportunityNote (High Priority)
- [ ] Task 3: Tạo repository OpportunityNoteRepository (High Priority, depends on Task 2)
- [ ] Task 4: Tạo service OpportunityService.add_note (High Priority, depends on Task 3)
- [ ] Task 5: Tạo Lambda handler add_opportunity_note (High Priority, depends on Task 4)
- [ ] Task 6: Xử lý phân quyền (opportunity-note:create:all/assigned) (High Priority, song song Task 5)
- [ ] Task 7: Logging, error handling (High Priority, song song Task 5)
- [ ] Task 8: Viết unit test cho repository (High Priority, song song Task 3)
- [ ] Task 9: Viết unit test cho service (High Priority, song song Task 4)
- [ ] Task 10: Viết unit test cho handler (High Priority, song song Task 5)
- [ ] Task 11: Viết integration test cho handler (High Priority, sau khi hoàn thành handler)
- [ ] Task 12: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 13: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-OPP-007: GET /api/v1/opportunities/{oppId}/notes** (Lấy danh sách ghi chú)

- [ ] Task 1: Tạo service OpportunityService.get_opportunity_notes (High Priority)
- [ ] Task 2: Tạo Lambda handler get_opportunity_notes (High Priority, depends on Task 1)
- [ ] Task 3: Validate input (path parameter) (High Priority, song song Task 2)
- [ ] Task 4: Xử lý phân quyền (opportunity-note:read:all/assigned) (High Priority, song song Task 2)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 2)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 1)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 2)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-OPP-008: PUT /api/v1/opportunities/{oppId}/onsite** (Đánh dấu ưu tiên Onsite)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (Trung bình)
- [ ] Task 2: Tạo service OpportunityService.update_onsite_priority (Trung bình)
- [ ] Task 3: Tạo Lambda handler update_onsite_priority (Trung bình, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (opportunity-onsite:update:all/assigned) (Trung bình, song song Task 3)
- [ ] Task 5: Logging, error handling (Trung bình, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (Trung bình, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (Trung bình, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (Trung bình, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (Trung bình, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (Trung bình, sau khi hoàn thành các task trên)

---

## Infrastructure (AWS Serverless)

- [ ] Task 1: Cập nhật template.yaml cho các function cơ hội (High Priority)
- [ ] Task 2: Định nghĩa IAM role, policy cho Lambda truy cập DynamoDB (High Priority)
- [ ] Task 3: Định nghĩa IAM role, policy cho Lambda kết nối Hubspot API (Thấp)
- [ ] Task 4: Cấu hình cron trigger cho đồng bộ tự động Hubspot (Thấp)
- [ ] Task 5: Thêm layer common (validation, error, auth) (High Priority)
- [ ] Task 6: Thêm layer repository (DynamoDB access) (High Priority)
- [ ] Task 7: Thêm layer service (business logic) (High Priority)
- [ ] Task 8: Thêm layer hubspot (kết nối Hubspot API) (Thấp)

---

## Documentation

- [ ] Task 1: Update API doc cho API-OPP-001 (High Priority)
- [ ] Task 2: Update API doc cho API-OPP-002 (High Priority)
- [ ] Task 3: Update API doc cho API-OPP-003 (Thấp)
- [ ] Task 4: Update API doc cho API-OPP-005 (High Priority)
- [ ] Task 5: Update API doc cho API-OPP-006 (High Priority)
- [ ] Task 6: Update API doc cho API-OPP-007 (High Priority)
- [ ] Task 7: Update API doc cho API-OPP-008 (Trung bình)
- [ ] Task 8: Update README hướng dẫn deploy/test (High Priority)
- [ ] Task 9: Update README hướng dẫn kết nối Hubspot API (Thấp)
- [ ] Task 10: Update checklist tiến độ (High Priority)

---

## Testing

- [ ] Task 1: Đảm bảo coverage ≥ 80% cho các function (High Priority)
- [ ] Task 2: Mock DynamoDB cho unit test (High Priority)
- [ ] Task 3: Mock Hubspot API cho unit test (Thấp)
- [ ] Task 4: Test case bao gồm happy path và error case (High Priority)
- [ ] Task 5: Test phân quyền (quyền hợp lệ và không hợp lệ) (High Priority)

---

## Lưu ý

- Đảm bảo validate input kỹ để tránh lỗi, đặc biệt là input từ người dùng
- Kiểm tra phân quyền chặt chẽ theo quy định trong BD/permissions_definition.md
- Xử lý kỹ lỗi kết nối Hubspot API (retry, timeout, logging)
- Khi hoàn thành task, đánh dấu `[x]` và ghi chú `(Completed)` 