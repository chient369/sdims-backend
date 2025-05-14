**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-27 | AI Assistant | Tạo checklist cho API Quản lý Hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Checklist phát triển các API quản lý hợp đồng (Contract) theo mô hình Lambda serverless, đảm bảo đúng chuẩn, dễ test, dễ bảo trì.

---

## Backend: API/Lambda - Quản lý Hợp đồng

### **API-CTR-001: GET /api/v1/contracts** (Lấy danh sách hợp đồng)

- [ ] Task 1: Định nghĩa model Contract mapping DynamoDB (theo dynamodb_structure.json) (High Priority)
- [ ] Task 2: Tạo repository ContractRepository (CRUD, query, filter) (High Priority, depends on Task 1)
- [ ] Task 3: Tạo service ContractService.get_contracts (High Priority, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_contracts (High Priority, depends on Task 3)
- [ ] Task 5: Validate input (query params: page, filter, search...) (High Priority, song song Task 4)
- [ ] Task 6: Xử lý phân quyền (contract:read:all/own/assigned) (High Priority, song song Task 4)
- [ ] Task 7: Logging, error handling (High Priority, song song Task 4)
- [ ] Task 8: Viết unit test cho repository (Pytest, mock DynamoDB) (High Priority, song song Task 2)
- [ ] Task 9: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 3)
- [ ] Task 10: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4)
- [ ] Task 11: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 12: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 13: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-002: POST /api/v1/contracts** (Thêm hợp đồng mới)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service ContractService.create_contract (High Priority)
- [ ] Task 3: Tạo Lambda handler create_contract (High Priority, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (contract:create) (High Priority, song song Task 3)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-003: GET /api/v1/contracts/{contractId}** (Lấy chi tiết hợp đồng)

- [ ] Task 1: Tạo service ContractService.get_contract_detail (High Priority)
- [ ] Task 2: Tạo Lambda handler get_contract_detail (High Priority, depends on Task 1)
- [ ] Task 3: Validate input (path parameter) (High Priority, song song Task 2)
- [ ] Task 4: Xử lý phân quyền (contract:read:all/own/assigned) (High Priority, song song Task 2)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 2)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 1)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 2)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-004: PUT /api/v1/contracts/{contractId}** (Cập nhật hợp đồng)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service ContractService.update_contract (High Priority)
- [ ] Task 3: Tạo Lambda handler update_contract (High Priority, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (contract:update:all/own) (High Priority, song song Task 3)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-006: GET /api/v1/contracts/{contractId}/payment-terms** (Lấy điều khoản thanh toán)

- [ ] Task 1: Định nghĩa model ContractPaymentTerm mapping DynamoDB (High Priority)
- [ ] Task 2: Tạo repository ContractPaymentTermRepository (High Priority, depends on Task 1)
- [ ] Task 3: Tạo service ContractService.get_payment_terms (High Priority, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_payment_terms (High Priority, depends on Task 3)
- [ ] Task 5: Validate input (path parameter) (High Priority, song song Task 4)
- [ ] Task 6: Xử lý phân quyền (payment-term:read:all/own/assigned) (High Priority, song song Task 4)
- [ ] Task 7: Logging, error handling (High Priority, song song Task 4)
- [ ] Task 8: Viết unit test cho repository (Pytest, mock DynamoDB) (High Priority, song song Task 2)
- [ ] Task 9: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 3)
- [ ] Task 10: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4)
- [ ] Task 11: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 12: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 13: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-007: PUT /api/v1/contracts/payment-terms/{termId}/status** (Cập nhật trạng thái thanh toán)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service ContractService.update_payment_term_status (High Priority)
- [ ] Task 3: Tạo Lambda handler update_payment_term_status (High Priority, depends on Task 2)
- [ ] Task 4: Xử lý phân quyền (payment-status:update:all) (High Priority, song song Task 3)
- [ ] Task 5: Logging, error handling (High Priority, song song Task 3)
- [ ] Task 6: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 2)
- [ ] Task 7: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 3)
- [ ] Task 8: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 9: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-009: GET /api/v1/contracts/{contractId}/files** (Lấy danh sách file đính kèm)

- [ ] Task 1: Định nghĩa model ContractFile mapping DynamoDB (High Priority)
- [ ] Task 2: Tạo repository ContractFileRepository (High Priority, depends on Task 1)
- [ ] Task 3: Tạo service ContractService.get_contract_files (High Priority, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_contract_files (High Priority, depends on Task 3)
- [ ] Task 5: Validate input (path parameter) (High Priority, song song Task 4)
- [ ] Task 6: Xử lý phân quyền (contract-file:read:all/own/assigned) (High Priority, song song Task 4)
- [ ] Task 7: Logging, error handling (High Priority, song song Task 4)
- [ ] Task 8: Viết unit test cho repository (Pytest, mock DynamoDB) (High Priority, song song Task 2)
- [ ] Task 9: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 3)
- [ ] Task 10: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4)
- [ ] Task 11: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 12: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 13: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-010: POST /api/v1/contracts/{contractId}/files** (Upload file đính kèm)

- [ ] Task 1: Định nghĩa schema validate input (Pydantic/marshmallow) (High Priority)
- [ ] Task 2: Tạo service ContractService.upload_contract_file (High Priority)
- [ ] Task 3: Tạo utility để xử lý upload file lên S3 (High Priority, song song Task 2)
- [ ] Task 4: Tạo Lambda handler upload_contract_file (High Priority, depends on Task 2, Task 3)
- [ ] Task 5: Xử lý phân quyền (contract-file:create:all/own) (High Priority, song song Task 4)
- [ ] Task 6: Logging, error handling (High Priority, song song Task 4)
- [ ] Task 7: Viết unit test cho service (Pytest, mock repo, mock S3) (High Priority, song song Task 2)
- [ ] Task 8: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4)
- [ ] Task 9: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 10: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 11: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

### **API-CTR-012: GET /api/v1/contracts/{contractId}/employees** (Lấy nhân viên trong hợp đồng)

- [ ] Task 1: Định nghĩa model ContractEmployee mapping DynamoDB (High Priority)
- [ ] Task 2: Tạo repository ContractEmployeeRepository (High Priority, depends on Task 1)
- [ ] Task 3: Tạo service ContractService.get_contract_employees (High Priority, depends on Task 2)
- [ ] Task 4: Tạo Lambda handler get_contract_employees (High Priority, depends on Task 3)
- [ ] Task 5: Validate input (path parameter) (High Priority, song song Task 4)
- [ ] Task 6: Xử lý phân quyền (contract:read:all/own/assigned) (High Priority, song song Task 4)
- [ ] Task 7: Logging, error handling (High Priority, song song Task 4)
- [ ] Task 8: Viết unit test cho repository (Pytest, mock DynamoDB) (High Priority, song song Task 2)
- [ ] Task 9: Viết unit test cho service (Pytest, mock repo) (High Priority, song song Task 3)
- [ ] Task 10: Viết unit test cho handler (mock event, mock service) (High Priority, song song Task 4)
- [ ] Task 11: Viết integration test cho handler (giả lập API Gateway) (High Priority, sau khi hoàn thành handler)
- [ ] Task 12: Khai báo function, event, IAM, layer trong template.yaml (High Priority, sau khi hoàn thành handler)
- [ ] Task 13: Update tài liệu API, checklist, README (High Priority, sau khi hoàn thành các task trên)

---

## Infrastructure (AWS Serverless)

- [ ] Task 1: Cập nhật template.yaml cho các function hợp đồng (High Priority)
- [ ] Task 2: Định nghĩa IAM role, policy cho Lambda truy cập DynamoDB (High Priority)
- [ ] Task 3: Định nghĩa IAM role, policy cho Lambda truy cập S3 (High Priority)
- [ ] Task 4: Thiết lập S3 bucket cho file đính kèm hợp đồng (High Priority)
- [ ] Task 5: Thêm layer common (validation, error, auth) (High Priority)
- [ ] Task 6: Thêm layer repository (DynamoDB access) (High Priority)
- [ ] Task 7: Thêm layer service (business logic) (High Priority)
- [ ] Task 8: Thêm layer file (xử lý file S3) (High Priority)

---

## Documentation

- [ ] Task 1: Update API doc cho API-CTR-001 (High Priority)
- [ ] Task 2: Update API doc cho API-CTR-002 (High Priority)
- [ ] Task 3: Update API doc cho API-CTR-003 (High Priority)
- [ ] Task 4: Update API doc cho API-CTR-004 (High Priority)
- [ ] Task 5: Update API doc cho API-CTR-006 (High Priority)
- [ ] Task 6: Update API doc cho API-CTR-007 (High Priority)
- [ ] Task 7: Update API doc cho API-CTR-009 (High Priority)
- [ ] Task 8: Update API doc cho API-CTR-010 (High Priority)
- [ ] Task 9: Update API doc cho API-CTR-012 (High Priority)
- [ ] Task 10: Update README hướng dẫn deploy/test (High Priority)
- [ ] Task 11: Update README hướng dẫn xử lý file S3 (High Priority)
- [ ] Task 12: Update checklist tiến độ (High Priority)

---

## Testing

- [ ] Task 1: Đảm bảo coverage ≥ 80% cho các function (High Priority)
- [ ] Task 2: Mock DynamoDB cho unit test (High Priority)
- [ ] Task 3: Mock S3 cho unit test (High Priority)
- [ ] Task 4: Test case bao gồm happy path và error case (High Priority)
- [ ] Task 5: Test phân quyền (quyền hợp lệ và không hợp lệ) (High Priority)
- [ ] Task 6: Test xử lý file (upload, get) (High Priority)

---

## Lưu ý

- Đảm bảo validate input kỹ để tránh lỗi, đặc biệt là input từ người dùng
- Kiểm tra phân quyền chặt chẽ theo quy định trong BD/permissions_definition.md
- Xử lý kỹ upload file (kiểm tra file type, size, virus scan nếu cần)
- Khi hoàn thành task, đánh dấu `[x]` và ghi chú `(Completed)` 