**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Định nghĩa chi tiết task tạo S3 buckets cho tài liệu và uploads | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để tạo và cấu hình S3 buckets cho việc lưu trữ tài liệu, file uploads và các tài nguyên static khác trong hệ thống.

# Chi tiết Task: BE-INF-005 - Tạo S3 buckets cho tài liệu và uploads

## Thông tin chung

**Task ID:** BE-INF-005  
**Task Name:** Tạo S3 buckets cho tài liệu và uploads  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-INF-001  
**Các task phụ thuộc vào task này:** BE-MOD-004 (Contract API), BE-MOD-005 (Report API), các API cần lưu trữ file

## Mô tả

Task này bao gồm việc định nghĩa và tạo S3 buckets cho việc lưu trữ tài liệu, file uploads và các tài nguyên static của hệ thống. Các bucket cần được cấu hình theo best practices, đảm bảo tính bảo mật và hiệu suất cao. Các S3 buckets sẽ được sử dụng để lưu trữ tài liệu đính kèm của hợp đồng, hình ảnh profile, tài liệu báo cáo và các tài liệu khác.

## Chi tiết công việc

### Phân tích nhu cầu lưu trữ

- [ ] Xác định các loại tài liệu cần lưu trữ:
  - Tài liệu đính kèm hợp đồng
  - Hình ảnh profile của người dùng
  - Tài liệu báo cáo (PDF, Excel)
  - Tài liệu opportunity
  - Backup dữ liệu
  - Các tài nguyên static (nếu có)

### Định nghĩa S3 Buckets trong CloudFormation

- [ ] Tạo S3 bucket cho tài liệu đính kèm:
  ```yaml
  AttachmentsBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: !Sub "sdims-attachments-${Stage}-${AWS::AccountId}"
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders:
              - "*"
            AllowedMethods:
              - GET
              - PUT
              - POST
              - DELETE
              - HEAD
            AllowedOrigins:
              - !Sub "https://${WebsiteDomainName}"
            MaxAge: 3600
      LifecycleConfiguration:
        Rules:
          - Id: TransitionToIA
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA
  ```

- [ ] Tạo S3 bucket cho profile images:
  ```yaml
  ProfileImagesBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: !Sub "sdims-profile-images-${Stage}-${AWS::AccountId}"
      # Các cấu hình tương tự như AttachmentsBucket
  ```

- [ ] Tạo S3 bucket cho backup dữ liệu:
  ```yaml
  BackupBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: !Sub "sdims-backups-${Stage}-${AWS::AccountId}"
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: ExpireOldBackups
            Status: Enabled
            ExpirationInDays: 365
  ```

### Cấu hình Bảo mật cho S3 Buckets

- [ ] Tạo bucket policy cho mỗi bucket:
  ```yaml
  AttachmentsBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref AttachmentsBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Deny
            Principal: '*'
            Action: 's3:*'
            Resource:
              - !Sub "${AttachmentsBucket.Arn}/*"
              - !Sub "${AttachmentsBucket.Arn}"
            Condition:
              Bool:
                aws:SecureTransport: false
  ```

### Thiết lập IAM Roles cho S3 access

- [ ] Đảm bảo IAM Roles được cấu hình đúng để truy cập S3 buckets:
  - Lambda functions có quyền đọc/ghi vào buckets tương ứng
  - Sử dụng nguyên tắc least privilege

### Cấu hình Presigned URLs

- [ ] Tạo utility function cho presigned URLs:
  ```python
  # src/common/s3_utils.py
  import os
  import boto3
  from aws_lambda_powertools import Logger
  
  logger = Logger(service="s3-service")
  s3_client = boto3.client('s3')
  
  def create_presigned_upload_url(bucket, key, content_type, expires_in=3600):
      """
      Tạo presigned URL cho việc upload file
      
      Parameters:
      -----------
      bucket : str
          Tên bucket
      key : str
          Object key (đường dẫn file)
      content_type : str
          MIME type của file
      expires_in : int, optional
          Thời gian hết hạn (seconds), mặc định là 3600
          
      Returns:
      --------
      str
          Presigned URL
      """
      try:
          params = {
              'Bucket': bucket,
              'Key': key,
              'ContentType': content_type
          }
          
          presigned_url = s3_client.generate_presigned_url(
              'put_object',
              Params=params,
              ExpiresIn=expires_in
          )
          
          return presigned_url
      except Exception as e:
          logger.exception(f"Error creating presigned upload URL for {bucket}/{key}")
          raise
  
  def create_presigned_get_url(bucket, key, expires_in=3600):
      """
      Tạo presigned URL cho việc download file
      
      Parameters:
      -----------
      bucket : str
          Tên bucket
      key : str
          Object key (đường dẫn file)
      expires_in : int, optional
          Thời gian hết hạn (seconds), mặc định là 3600
          
      Returns:
      --------
      str
          Presigned URL
      """
      try:
          params = {
              'Bucket': bucket,
              'Key': key
          }
          
          presigned_url = s3_client.generate_presigned_url(
              'get_object',
              Params=params,
              ExpiresIn=expires_in
          )
          
          return presigned_url
      except Exception as e:
          logger.exception(f"Error creating presigned get URL for {bucket}/{key}")
          raise
  ```

### Tạo Lambda Functions cho file uploads

- [ ] Tạo Lambda function để tạo presigned URL:
  ```python
  # src/common/handlers/create_upload_url.py
  import os
  import json
  import time
  from aws_lambda_powertools import Logger, Tracer
  from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, Response
  from src.common.s3_utils import create_presigned_upload_url
  
  logger = Logger(service="file-upload-service")
  tracer = Tracer(service="file-upload-service")
  app = ApiGatewayResolver()
  
  @app.post("/files/upload-url")
  @tracer.capture_method
  def get_upload_url():
      try:
          # Lấy body từ request
          body = app.current_event.json_body
          file_name = body.get('fileName')
          content_type = body.get('contentType')
          folder_path = body.get('folderPath', 'default')
          
          if not file_name or not content_type:
              return Response(
                  status_code=400,
                  content_type="application/json",
                  body=json.dumps({
                      "message": "fileName và contentType là bắt buộc"
                  })
              )
          
          # Tạo unique key cho file
          key = f"{folder_path}/{int(time.time())}-{file_name}"
          attachments_bucket = os.environ.get('ATTACHMENTS_BUCKET')
          
          # Tạo presigned URL
          presigned_url = create_presigned_upload_url(
              attachments_bucket,
              key,
              content_type
          )
          
          return Response(
              status_code=200,
              content_type="application/json",
              body=json.dumps({
                  "uploadUrl": presigned_url,
                  "key": key
              })
          )
      except Exception as e:
          logger.exception("Error creating presigned URL")
          return Response(
              status_code=500,
              content_type="application/json",
              body=json.dumps({
                  "message": "Error creating upload URL"
              })
          )
  
  @tracer.capture_lambda_handler
  def handler(event, context):
      return app.resolve(event, context)
  ```

### Tài liệu hóa

- [ ] Tạo tài liệu hướng dẫn sử dụng S3 buckets:
  - Cấu trúc và mục đích của mỗi bucket
  - Quy ước đặt tên cho objects/files
  - Cách sử dụng presigned URLs
  - Các best practices khi làm việc với S3
  - Kiểm soát chi phí và lifecycle management

## Tiêu chí hoàn thành

- Các S3 buckets đã được định nghĩa đầy đủ trong template.yaml
- Cấu hình bảo mật đã được thiết lập cho mỗi bucket
- Presigned URL utilities đã được triển khai
- Lambda function để tạo presigned URLs đã được triển khai
- Tài liệu hướng dẫn sử dụng S3 buckets đã được tạo

## Ước tính thời gian

- 1-2 ngày làm việc

## Ghi chú

- Cần đảm bảo rằng các buckets không được public và chỉ có thể truy cập thông qua presigned URLs
- Cân nhắc cấu hình lifecycle policies để quản lý vòng đời của objects và tiết kiệm chi phí
- Nên sử dụng server-side encryption cho tất cả objects trong bucket
- Cân nhắc cấu hình versioning để có thể phục hồi files nếu cần
- Sử dụng AWS Lambda Powertools để cải thiện logging và monitoring 