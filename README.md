# SDIMS Backend - Tài liệu & Hướng dẫn triển khai

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-28 | AI Assistant | Tạo README mô tả cấu trúc tài liệu, hướng dẫn run và triển khai | -           | Draft     |

---

## 1. Cấu trúc tài liệu dự án

```
Backend/
├── Design/                  # Tài liệu thiết kế hệ thống
│   ├── BD/                  # Business Design (API, DB, Function, Permission)
│   │   ├── API/             # Danh sách API, errors, mô tả endpoint
│   │   ├── DB/              # Cấu trúc DynamoDB
│   │   ├── FunctionDesign/  # Mô tả chức năng nghiệp vụ
│   │   └── permissions_definition.md # Định nghĩa quyền
│   └── DD/                  # Detailed Design (API chi tiết, màn hình)
├── src/                     # Source code Lambda functions
│   ├── functions/           # Lambda handler theo domain
│   ├── layers/              # Shared Lambda Layers (common, repo, service)
├── Task/                    # Checklist, tiến độ, rule triển khai
│   ├── TaskDetails/         # Checklist chi tiết cho từng API/module
│   ├── TaskStatus/          # Tổng quan trạng thái phát triển
│   └── Template.md          # Template checklist mẫu
├── tests/                   # Unit test, integration test
├── requirements.txt         # Python dependencies
├── template.yaml            # AWS SAM template
└── README.md                # Tài liệu này
```

**Các file quan trọng:**
- `Design/BD/API/api_list.md`: Danh sách API tổng quan
- `Design/BD/DB/dynamodb_structure.json`: Cấu trúc DynamoDB
- `Task/TaskDetails/`: Checklist chi tiết từng API
- `Task/TaskDetails/TaskImplementationRules.md`: Rule triển khai task
- `Task/TaskStatus/API-development-status.md`: Bảng trạng thái phát triển
- `template.yaml`: Khai báo hạ tầng AWS SAM

---

## 2. Hướng dẫn run local/unit test

### 2.1. Cài đặt môi trường
- Python >= 3.13
- pip install -r requirements.txt
- Cài đặt AWS SAM CLI (nếu muốn run local lambda): https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

### 2.2. Chạy unit test
```bash
pytest tests/unit/
```

### 2.3. Chạy integration test
```bash
pytest tests/integration/
```

### 2.4. Run local Lambda function (SAM)
```bash
sam local invoke <FunctionLogicalId> --event events/<event_file>.json
```

### 2.5. Run local API Gateway (SAM)
```bash
sam local start-api
```

---

## 3. Hướng dẫn triển khai (deploy)

### 3.1. Build & deploy với AWS SAM
```bash
sam build
sam deploy --guided
```

- Cấu hình các biến môi trường, IAM role, DynamoDB, S3... trong `template.yaml`
- Đảm bảo đã cấu hình AWS CLI với quyền phù hợp

### 3.2. Quy trình phát triển 1 API mới
1. Đọc tài liệu thiết kế (Design/BD/API, DB, FunctionDesign)
2. Lập checklist task trong `Task/TaskDetails/`
3. Tạo branch mới theo chuẩn
4. Viết unit test trước, sau đó code từng layer (model, repo, service, handler)
5. Đảm bảo test coverage ≥ 80%
6. Cập nhật template.yaml, tài liệu, checklist
7. Tạo pull request, review, merge
8. Deploy lên môi trường test/staging

### 3.3. Lưu ý khi triển khai
- Không hard-code secret, dùng AWS Secrets Manager/Parameter Store
- Validate input kỹ, log đúng mức, không log thông tin nhạy cảm
- Đảm bảo phân quyền đúng theo `permissions_definition.md`
- Cập nhật checklist tiến độ sau mỗi task

---

## 4. Liên hệ & đóng góp
- Đọc kỹ các rule trong `Task/TaskDetails/TaskImplementationRules.md` trước khi code
- Mọi thắc mắc, góp ý gửi về nhóm phát triển Backend SDIMS 