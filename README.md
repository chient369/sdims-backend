# SDIMS - Backend

Hệ thống quản lý nội bộ SDIMS - Backend sử dụng AWS Serverless Application Model (SAM) với Python.

## Cài đặt và Cấu hình

### Yêu cầu
- AWS SAM CLI: [Hướng dẫn cài đặt](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- AWS CLI và thông tin xác thực
- Python 3.13
- Docker (để test locally)

### Cài đặt
1. Clone repository:
```
git clone <repository-url>
cd sdims-backend
```

2. Tạo virtual environment:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt dependencies:
```
pip install -r requirements.txt
```

## Chạy ứng dụng locally
Để chạy ứng dụng trên môi trường local:
```
sam build
sam local start-api
```

## Triển khai lên AWS
Để triển khai lên môi trường AWS:
```
sam build
sam deploy --guided  # Lần đầu tiên
sam deploy           # Các lần sau
```

## Cấu trúc dự án
```
sdims/
├── samconfig.toml             # SAM CLI configuration
├── template.yaml              # Main SAM template
├── src/                       # Source code for Lambda functions
│   ├── auth/                  # Authentication-related Lambda functions
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── logout.py
│   │   ├── refresh_token.py
│   │   └── authorizer.py
│   ├── hrm/                   # HR management Lambda functions
│   │   ├── __init__.py
│   │   ├── employees.py
│   │   └── skills.py
│   ├── margins/               # Margins-related Lambda functions
│   │   ├── __init__.py
│   │   └── calculations.py
│   ├── opportunities/         # Business opportunities Lambda functions
│   │   ├── __init__.py
│   │   └── hubspot_sync.py
│   ├── contracts/             # Contract-related Lambda functions
│   │   ├── __init__.py
│   │   └── file_uploads.py
│   ├── reports/               # Reports/dashboard Lambda functions
│   │   ├── __init__.py
│   │   └── dashboard.py
│   ├── admin/                 # System administration Lambda functions
│   │   ├── __init__.py
│   │   └── users.py
│   └── files/                 # File operations Lambda functions
│       ├── __init__.py
│       ├── create_upload_url.py
│       └── download_file_url.py
├── layers/                    # Shared Lambda Layers
│   ├── common-layer/          # Layer for shared libraries
│   │   └── python/            # Python packages
│   │       ├── common/        # Common utilities package
│   │       │   ├── __init__.py
│   │       │   ├── dynamodb.py
│   │       │   ├── response.py
│   │       │   ├── validation.py
│   │       │   ├── logger.py
│   │       │   ├── auth.py
│   │       │   ├── errors.py
│   │       │   └── s3.py
│   │       └── requirements.txt  # Layer dependencies
├── events/                    # Sample events for API testing
├── tests/                     # Unit and integration tests
│   ├── unit/                  # Unit tests
│   │   ├── __init__.py
│   │   └── common/            # Tests for common utilities
│   │       ├── test_dynamodb.py
│   │       ├── test_response.py
│   │       └── test_validation.py
│   └── integration/           # Integration tests
│       ├── __init__.py
│       └── test_api.py
├── requirements.txt           # Project dependencies
├── pytest.ini                 # Pytest configuration
└── .gitignore                # Git ignore file
```

## Hướng dẫn thêm Lambda Function mới
1. Tạo file Python mới trong thư mục tương ứng trong `src/`
2. Viết code cho handler function
3. Thêm định nghĩa function trong file `template.yaml`
4. Thêm unit test trong thư mục `tests/`
5. Chạy `sam build` và `sam local invoke` để test function

## Lambda Layers
Dự án sử dụng Lambda Layers để chia sẻ code chung giữa các Lambda functions:

- **common-layer**: Chứa các utilities dùng chung (DynamoDB, Response, Validation, Logger, Auth, Errors, S3)

Để sử dụng code từ Layer trong Lambda functions:

```python
# Ví dụ import DynamoDB Repository
from common.dynamodb import DynamoDBRepository

# Ví dụ import Auth Utilities
from common.auth import AuthUtils

# Ví dụ import S3 Utilities
from common.s3 import S3Utils
```

Tất cả các Lambda functions đã được cấu hình để tự động sử dụng Lambda Layer này.

## Quy tắc đặt tên và code style
- Sử dụng `snake_case` cho tên biến và hàm
- Tuân thủ PEP 8
- Sử dụng docstring kiểu Google
- Bắt buộc type hints
- Độ dài dòng tối đa: 100 ký tự

## Hướng dẫn testing
1. Viết unit tests trong thư mục `tests/unit/`
2. Viết integration tests trong thư mục `tests/integration/`
3. Chạy tests:
```
pytest
```
4. Kiểm tra code coverage:
```
pytest --cov=src tests/
``` 