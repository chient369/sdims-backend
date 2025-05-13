**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Định nghĩa chi tiết task thiết lập cấu trúc dự án SAM | -           | Draft     |
| 1.1     | 2024-08-01 | Chiến Trần Văn | Cập nhật sử dụng Python thay vì Node.js | -           | Draft     |
| 1.2     | 2024-08-13 | Chiến Trần Văn | Cập nhật hoàn thành task | -           | Completed |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để thiết lập cấu trúc dự án AWS SAM ban đầu, tạo các template và cấu hình cho môi trường phát triển serverless backend sử dụng Python.

# Chi tiết Task: BE-INF-001 - Thiết lập cấu trúc dự án SAM ban đầu

## Thông tin chung

**Task ID:** BE-INF-001  
**Task Name:** Thiết lập cấu trúc dự án SAM ban đầu với file template.yaml  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** Không có  
**Các task phụ thuộc vào task này:** BE-INF-002, BE-INF-003, BE-INF-004, BE-INF-005

## Mô tả

Task này bao gồm việc thiết lập cấu trúc ban đầu cho dự án AWS SAM, bao gồm tạo các file cấu hình, định nghĩa tài nguyên chung và thiết lập môi trường phát triển. Dự án sẽ sử dụng Python làm ngôn ngữ lập trình chính.

## Chi tiết công việc

### Thiết lập cấu trúc thư mục
- [x] Tạo cấu trúc thư mục dự án tuân theo AWS SAM best practices với Python:
  ```
  sdims/
  ├── samconfig.toml             # SAM CLI config file
  ├── template.yaml              # SAM template chính
  ├── src/                       # Thư mục chứa source code các lambda functions
  │   ├── common/                # Code dùng chung cho tất cả các lambda functions
  │   │   ├── __init__.py
  │   │   ├── dynamodb.py        # Utility cho DynamoDB
  │   │   ├── s3.py              # Utility cho S3
  │   │   └── auth.py            # Utility cho Authentication
  │   ├── auth/                  # Các lambda functions liên quan đến authentication
  │   │   ├── __init__.py
  │   │   ├── login.py
  │   │   ├── logout.py
  │   │   ├── refresh_token.py
  │   │   └── authorizer.py
  │   ├── hrm/                   # Các lambda functions liên quan đến quản lý nhân sự
  │   │   ├── __init__.py
  │   │   ├── employees.py
  │   │   └── skills.py
  │   ├── margins/               # Các lambda functions liên quan đến margins
  │   │   ├── __init__.py
  │   │   └── calculations.py
  │   ├── opportunities/         # Các lambda functions liên quan đến cơ hội kinh doanh
  │   │   ├── __init__.py
  │   │   └── hubspot_sync.py
  │   ├── contracts/             # Các lambda functions liên quan đến hợp đồng
  │   │   ├── __init__.py
  │   │   └── file_uploads.py
  │   ├── reports/               # Các lambda functions liên quan đến reports/dashboard
  │   │   ├── __init__.py
  │   │   └── dashboard.py
  │   └── admin/                 # Các lambda functions liên quan đến quản trị hệ thống
  │       ├── __init__.py
  │       └── users.py
  ├── layers/                    # Shared Lambda Layers
  │   ├── common-layer/          # Layer chứa các thư viện dùng chung
  │   │   └── python/            # Chứa các package Python
  │   │       └── requirements.txt  # Dependencies cho layer
  ├── events/                    # Chứa các event mẫu để test API
  ├── tests/                     # Unit tests và integration tests
  │   ├── unit/                  # Unit tests
  │   │   ├── __init__.py
  │   │   └── test_auth.py
  │   └── integration/           # Integration tests
  │       ├── __init__.py
  │       └── test_api.py
  ├── requirements.txt           # Dependencies cho dự án
  ├── pytest.ini                 # Cấu hình pytest
  └── .gitignore                # Git ignore file
  ```

### Cài đặt các công cụ phát triển
- [x] Cài đặt AWS SAM CLI
- [x] Cài đặt AWS CLI
- [x] Cài đặt Python (phiên bản 3.13)
- [x] Cài đặt các công cụ phát triển (pylint, black, pytest, pytest-cov)
- [x] Thiết lập virtual environment cho Python

### Tạo file template.yaml
- [x] Tạo file template.yaml với các phần cơ bản:
  ```yaml
  AWSTemplateFormatVersion: '2010-09-09'
  Transform: AWS::Serverless-2016-10-31
  Description: SDIMS - Internal Management System
  
  # Global config áp dụng cho tất cả các functions
  Globals:
    Function:
      Timeout: 30
      MemorySize: 256
      Runtime: python3.13
      Environment:
        Variables:
          LOG_LEVEL: INFO
          STAGE: !Ref Stage
          # Các biến môi trường khác
  
  # Parameters
  Parameters:
    Stage:
      Type: String
      Default: dev
      AllowedValues:
        - dev
        - staging
        - prod
      Description: Deployment stage

  # Resources
  Resources:
    # Lambda Functions sẽ được định nghĩa ở đây
    CommonLayer:
      Type: AWS::Serverless::LayerVersion
      Properties:
        LayerName: common-layer
        Description: Common utilities layer
        ContentUri: layers/common-layer/
        CompatibleRuntimes:
          - python3.13
        RetentionPolicy: Retain
    
    # Định nghĩa API Gateway
    # Định nghĩa DynamoDB Table
    # Định nghĩa S3 Bucket
    # Định nghĩa IAM Roles và Policies
    
  # Outputs để export các giá trị cần thiết
  Outputs:
    CommonLayerArn:
      Description: "ARN of the Common Layer"
      Value: !Ref CommonLayer
  ```

### Cấu hình môi trường phát triển
- [x] Thiết lập file samconfig.toml cho các môi trường:
  ```toml
  version = 0.1
  [default]
  [default.deploy]
  [default.deploy.parameters]
  stack_name = "sdims-backend"
  s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-xxxx"
  s3_prefix = "sdims-backend"
  region = "ap-southeast-1"
  capabilities = "CAPABILITY_IAM"
  parameter_overrides = "Stage=dev"
  
  [staging]
  [staging.deploy]
  [staging.deploy.parameters]
  stack_name = "sdims-backend-staging"
  parameter_overrides = "Stage=staging"
  
  [prod]
  [prod.deploy]
  [prod.deploy.parameters]
  stack_name = "sdims-backend-prod"
  parameter_overrides = "Stage=prod"
  ```

### Tạo file requirements.txt
- [x] Tạo file requirements.txt cho dự án Python:
  ```
  boto3==1.28.0
  pyjwt==2.8.0
  python-dotenv==1.0.0
  requests==2.31.0
  aws-lambda-powertools==2.25.0
  pytest==7.4.0
  pytest-cov==4.1.0
  black==23.7.0
  pylint==2.17.5
  ```

### Thiết lập layer cho Python
- [x] Tạo requirements.txt cho common layer:
  ```
  # layers/common-layer/python/requirements.txt
  boto3==1.28.0
  pyjwt==2.8.0
  aws-lambda-powertools==2.25.0
  ```

### Viết tài liệu hướng dẫn cơ bản
- [x] Tạo README.md với hướng dẫn:
  - Cài đặt và cấu hình dự án
  - Cách chạy ứng dụng locally
  - Cách thêm một Lambda function mới
  - Cấu trúc dự án
  - Quy tắc đặt tên và code style
  - Hướng dẫn testing

## Tiêu chí hoàn thành
- [x] Cấu trúc dự án được thiết lập đầy đủ
- [x] template.yaml được tạo và có thể build thành công
- [x] samconfig.toml được cấu hình cho các môi trường
- [x] Có thể chạy `sam build` thành công
- [x] Tài liệu hướng dẫn được tạo

## Ước tính thời gian
- 1-2 ngày làm việc

## Ghi chú
- Sử dụng Python 3.13 cho Lambda functions
- Cần xác định AWS region chính để triển khai
- Stage mặc định là "dev"
- Cân nhắc sử dụng AWS Lambda Powertools cho việc logging, tracing và monitoring 