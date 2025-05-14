# Lambda Serverless API Implementation Rules

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-27 | AI Assistant   | Initial implementation rules   | -           | Draft     |

---

## 1. Mục tiêu  
Quy định quy trình, tiêu chuẩn và checklist phát triển chức năng API theo mô hình Lambda Serverless (AWS) cho dự án SDIMS, đảm bảo code nhất quán, dễ bảo trì, dễ test và tuân thủ kiến trúc nhiều tầng.

---

## 2. Quy trình phát triển API Lambda serverless

1. **Xác định chức năng và API**
   - Đọc tài liệu `Design/BD/API/api_list.md`, `Design/DD/API/`, `Design/BD/DB/dynamodb_structure.json` để hiểu rõ yêu cầu, endpoint, model dữ liệu, phân quyền.

2. **Lập checklist task**
   - Chia nhỏ từng API thành các task cụ thể: model, repository, service, handler, validate, test, doc, infra.

3. **Tạo branch Git**
   - Theo chuẩn: `feature/BE-<TASK-ID>-<short-description>`

4. **Phát triển từng layer**
   - **Model**: Định nghĩa class mapping DynamoDB.
   - **Repository**: CRUD/query DynamoDB.
   - **Service**: Xử lý logic nghiệp vụ.
   - **Handler**: Lambda nhận event, gọi service, trả response.
   - **Validate**: Kiểm tra input (Pydantic/marshmallow).
   - **Phân quyền**: Kiểm tra quyền từ JWT.
   - **Logging/Error**: Sử dụng aws_lambda_powertools.Logger, custom exception.

5. **Viết test**
   - Unit test cho từng layer, mock external.
   - Integration test cho handler (giả lập API Gateway event).
   - Đảm bảo coverage ≥ 80%.

6. **Khai báo hạ tầng**
   - Cập nhật `template.yaml` (function, event, IAM, layer, env).

7. **Cập nhật tài liệu**
   - Update README, API doc, checklist task.

8. **Review, test, merge**
   - Chạy test, linter, kiểm tra security, tạo PR, review, merge.

---

## 3. Checklist mẫu phát triển 1 API

- [ ] Định nghĩa model mapping DynamoDB
- [ ] Tạo repository CRUD/query
- [ ] Tạo service xử lý logic
- [ ] Tạo Lambda handler
- [ ] Validate input
- [ ] Xử lý phân quyền
- [ ] Logging, error handling
- [ ] Viết unit test cho từng layer
- [ ] Viết integration test cho handler
- [ ] Khai báo function, event, IAM, layer trong template.yaml
- [ ] Update tài liệu, checklist

---

## 4. Lưu ý coding & testing
- Tách biệt rõ các tầng: handler, service, repository, model.
- Bắt buộc type hint, docstring tiếng Anh, comment rõ ràng.
- Không hard-code secret, validate input kỹ, log đúng mức.
- Mock external khi test, test cả case lỗi và edge case.
- Đảm bảo code coverage ≥ 80%.
- Cập nhật checklist và tài liệu liên tục.

---

## 5. Tham khảo
- Xem thêm guideline chi tiết trong file `Design/BD/FunctionDesign/FunctionList.md`, `Design/BD/API/api_list.md`, `Design/BD/DB/dynamodb_structure.json`, `Design/BD/permissions_definition.md`. 