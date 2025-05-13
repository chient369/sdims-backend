**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Định nghĩa chi tiết task định nghĩa IAM Roles và Policies | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để tạo và cấu hình IAM Roles và Policies cho các Lambda functions với quyền tối thiểu theo nguyên tắc least privilege.

# Chi tiết Task: BE-INF-003 - Định nghĩa IAM Roles và Policies

## Thông tin chung

**Task ID:** BE-INF-003  
**Task Name:** Định nghĩa IAM Roles và Policies cho Lambda functions  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-INF-001  
**Các task phụ thuộc vào task này:** Tất cả các Lambda functions

## Mô tả

Task này bao gồm việc định nghĩa các IAM Roles và Policies cần thiết cho các Lambda functions trong hệ thống, tuân theo nguyên tắc least privilege (quyền tối thiểu cần thiết). Mỗi loại Lambda function sẽ được gán với role phù hợp, chỉ có quyền truy cập vào các tài nguyên mà nó cần.

## Chi tiết công việc

### Phân tích các nhóm Lambda functions

- [ ] Xác định các nhóm chức năng chính và quyền truy cập cần thiết:
  - Lambda functions xử lý Authentication (cần access Cognito/user table)
  - Lambda functions quản lý nhân sự (cần quyền đọc/ghi vào các bảng nhân sự, skills)
  - Lambda functions quản lý margins (cần quyền đọc/ghi vào bảng costs, revenues)
  - Lambda functions quản lý cơ hội kinh doanh (cần quyền gọi Hubspot API, đọc/ghi bảng opportunities)
  - Lambda functions quản lý hợp đồng (cần quyền đọc/ghi bảng contracts, upload files)
  - Lambda functions báo cáo/dashboard (cần quyền đọc nhiều bảng dữ liệu)
  - Lambda functions quản trị hệ thống (cần quyền cao)

### Định nghĩa Base Lambda Execution Role

- [ ] Tạo role cơ bản cho tất cả Lambda functions trong template.yaml:
  ```yaml
  BaseLambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: 'sts:AssumeRole'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
  ```

### Định nghĩa DynamoDB Table Access Policies

- [ ] Tạo policy cho quyền đọc DynamoDB:
  ```yaml
  DynamoDBReadPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - 'dynamodb:GetItem'
              - 'dynamodb:BatchGetItem'
              - 'dynamodb:Query'
              - 'dynamodb:Scan'
            Resource:
              - !GetAtt SDIMSTable.Arn
              - !Sub "${SDIMSTable.Arn}/index/*"
  ```

- [ ] Tạo policy cho quyền đọc/ghi DynamoDB:
  ```yaml
  DynamoDBReadWritePolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - 'dynamodb:GetItem'
              - 'dynamodb:BatchGetItem'
              - 'dynamodb:Query'
              - 'dynamodb:Scan'
              - 'dynamodb:PutItem'
              - 'dynamodb:UpdateItem'
              - 'dynamodb:DeleteItem'
              - 'dynamodb:BatchWriteItem'
            Resource:
              - !GetAtt SDIMSTable.Arn
              - !Sub "${SDIMSTable.Arn}/index/*"
  ```

### Định nghĩa S3 Access Policies

- [ ] Tạo policy cho quyền đọc S3:
  ```yaml
  S3ReadPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - 's3:GetObject'
              - 's3:ListBucket'
            Resource:
              - !Sub "arn:aws:s3:::${AttachmentsBucket}"
              - !Sub "arn:aws:s3:::${AttachmentsBucket}/*"
  ```

- [ ] Tạo policy cho quyền đọc/ghi S3:
  ```yaml
  S3ReadWritePolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - 's3:GetObject'
              - 's3:ListBucket'
              - 's3:PutObject'
              - 's3:DeleteObject'
            Resource:
              - !Sub "arn:aws:s3:::${AttachmentsBucket}"
              - !Sub "arn:aws:s3:::${AttachmentsBucket}/*"
  ```

### Định nghĩa Specialized Roles cho từng nhóm Lambda

- [ ] Tạo Role cho Authentication functions:
  ```yaml
  AuthFunctionsRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: 'sts:AssumeRole'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        - !Ref DynamoDBReadWritePolicy
  ```

- [ ] Tạo Role cho HRM functions:
  ```yaml
  HRMFunctionsRole:
    Type: AWS::IAM::Role
    # Tương tự nhưng có thể thêm quyền khác
  ```

- [ ] Tạo Role cho Contract functions có quyền S3:
  ```yaml
  ContractFunctionsRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: 'sts:AssumeRole'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        - !Ref DynamoDBReadWritePolicy
        - !Ref S3ReadWritePolicy
  ```

- [ ] Tạo Role cho Opportunity functions có quyền gọi API bên ngoài:
  ```yaml
  OpportunityFunctionsRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: 'sts:AssumeRole'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        - !Ref DynamoDBReadWritePolicy
      Policies:
        - PolicyName: HubspotAPIAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'secretsmanager:GetSecretValue'
                Resource: !Sub "arn:aws:secretsmanager:${AWS::Region}:${AWS::AccountId}:secret:hubspot-api-*"
  ```

- [ ] Tạo Role cho Admin functions với quyền cao hơn:
  ```yaml
  AdminFunctionsRole:
    Type: AWS::IAM::Role
    # Quyền quản trị hệ thống
  ```

### Áp dụng Roles vào Lambda functions

- [ ] Cập nhật template.yaml để áp dụng roles cho các Lambda functions dựa trên nhóm chức năng

### Tài liệu hóa

- [ ] Tạo tài liệu mô tả các IAM Roles và Policies:
  - Danh sách các role và mục đích sử dụng
  - Quyền chi tiết của từng role
  - Hướng dẫn khi nào sử dụng role nào

## Tiêu chí hoàn thành

- Tất cả các IAM Roles và Policies được định nghĩa trong template.yaml
- Mỗi role có các quyền tối thiểu cần thiết theo nguyên tắc least privilege
- Các Lambda functions được gán role phù hợp
- Tài liệu mô tả các IAM Roles và Policies đã được tạo

## Ước tính thời gian

- 1-2 ngày làm việc

## Ghi chú

- Nên thường xuyên kiểm tra và cập nhật quyền hạn khi có thêm yêu cầu mới
- IAM Policies nên được kiểm tra định kỳ về bảo mật
- Tránh sử dụng quyền * (wildcard) khi có thể
- Trong định nghĩa Roles, cần đảm bảo runtime là Python 3.13
- Cân nhắc sử dụng AWS Lambda Powertools cho Python để cải thiện logging, tracing và monitoring 