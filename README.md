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
├── samconfig.toml             # SAM CLI config file
├── template.yaml              # SAM template chính
├── src/                       # Thư mục chứa source code các lambda functions
│   ├── common/                # Code dùng chung cho tất cả các lambda functions
│   ├── auth/                  # Các lambda functions liên quan đến authentication
│   ├── hrm/                   # Các lambda functions liên quan đến quản lý nhân sự
│   ├── margins/               # Các lambda functions liên quan đến margins
│   ├── opportunities/         # Các lambda functions liên quan đến cơ hội kinh doanh
│   ├── contracts/             # Các lambda functions liên quan đến hợp đồng
│   ├── reports/               # Các lambda functions liên quan đến reports/dashboard
│   └── admin/                 # Các lambda functions liên quan đến quản trị hệ thống
├── layers/                    # Shared Lambda Layers
├── events/                    # Chứa các event mẫu để test API
├── tests/                     # Unit tests và integration tests
├── requirements.txt           # Dependencies cho dự án
├── pytest.ini                 # Cấu hình pytest
└── .gitignore                # Git ignore file
```

## Hướng dẫn thêm Lambda Function mới
1. Tạo file Python mới trong thư mục tương ứng trong `src/`
2. Viết code cho handler function
3. Thêm định nghĩa function trong file `template.yaml`
4. Thêm unit test trong thư mục `tests/`
5. Chạy `sam build` và `sam local invoke` để test function

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