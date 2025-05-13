**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Định nghĩa chi tiết task thiết lập API Gateway | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để thiết lập API Gateway cho hệ thống, bao gồm cấu hình routes, authorizers, CORS và các thiết lập khác.

# Chi tiết Task: BE-INF-006 - Thiết lập API Gateway

## Thông tin chung

**Task ID:** BE-INF-006  
**Task Name:** Thiết lập API Gateway và cấu hình routes, security  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-INF-001  
**Các task phụ thuộc vào task này:** Tất cả các API endpoints

## Mô tả

Task này bao gồm việc thiết lập và cấu hình API Gateway trong AWS SAM/CloudFormation template. API Gateway sẽ là cổng vào cho tất cả các API endpoints của hệ thống. Task này bao gồm cấu hình routes, authorizers, CORS, logging, throttling và các thiết lập bảo mật khác.

## Chi tiết công việc

### Phân tích yêu cầu API

- [ ] Xem xét tài liệu BD/API/api_list.md để xác định:
  - Danh sách các API endpoints
  - Nhóm chức năng API (auth, hrm, contracts, opportunities, etc.)
  - Phương thức HTTP (GET, POST, PUT, DELETE)
  - Các tham số đường dẫn và query
  - Yêu cầu authorizer cho từng endpoint

### Định nghĩa API Gateway trong CloudFormation

- [ ] Tạo định nghĩa API Gateway trong template.yaml:
  ```yaml
  SDIMSApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: !Ref Stage
      EndpointConfiguration: REGIONAL
      Auth:
        DefaultAuthorizer: LambdaTokenAuthorizer
        Authorizers:
          LambdaTokenAuthorizer:
            FunctionPayloadType: TOKEN
            FunctionArn: !GetAtt AuthorizerFunction.Arn
            Identity:
              Header: Authorization
        # Các endpoint không cần authorizer
        ApiKeyRequired: false
      DefinitionBody:
        swagger: "2.0"
        info:
          title: !Sub "SDIMS API - ${Stage}"
          version: "1.0.0"
        paths:
          # Paths được định nghĩa phía dưới
      Cors:
        AllowMethods: "'GET,POST,PUT,DELETE,OPTIONS'"
        AllowHeaders: "'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'"
        AllowOrigin: !Sub "'https://${WebsiteDomainName}'"
        MaxAge: "'3600'"
        AllowCredentials: "'true'"
      GatewayResponses:
        DEFAULT_4XX:
          ResponseParameters:
            Headers:
              Access-Control-Allow-Origin: !Sub "'https://${WebsiteDomainName}'"
              Access-Control-Allow-Headers: "'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'"
              Access-Control-Allow-Methods: "'GET,POST,PUT,DELETE,OPTIONS'"
              Access-Control-Allow-Credentials: "'true'"
        DEFAULT_5XX:
          ResponseParameters:
            Headers:
              Access-Control-Allow-Origin: !Sub "'https://${WebsiteDomainName}'"
              Access-Control-Allow-Headers: "'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'"
              Access-Control-Allow-Methods: "'GET,POST,PUT,DELETE,OPTIONS'"
              Access-Control-Allow-Credentials: "'true'"
      AccessLogSetting:
        DestinationArn: !GetAtt APIGatewayAccessLogGroup.Arn
        Format: '{"requestId":"$context.requestId", "ip":"$context.identity.sourceIp", "caller":"$context.identity.caller", "user":"$context.identity.user", "requestTime":"$context.requestTime", "httpMethod":"$context.httpMethod", "resourcePath":"$context.resourcePath", "status":"$context.status", "protocol":"$context.protocol", "responseLength":"$context.responseLength"}'
  ```

### Tạo Custom Authorizer

- [ ] Tạo Lambda function cho authorizer:
  ```python
  # src/auth/authorizer.py
  import os
  import json
  import jwt
  import logging
  from aws_lambda_powertools import Logger
  
  logger = Logger(service="auth-service")
  
  def handler(event, context):
      try:
          # Lấy token từ Authorization header
          auth_header = event.get('authorizationToken')
          if not auth_header or not auth_header.startswith('Bearer '):
              logger.warning("Invalid authorization header format")
              return generate_policy('user', 'Deny', event['methodArn'])
          
          token = auth_header.split(' ')[1]
          
          # Verify token
          jwt_secret = os.environ.get('JWT_SECRET')
          decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
          
          # Tạo IAM policy dựa trên thông tin user và permissions
          user_id = decoded_token.get('sub')
          roles = decoded_token.get('roles', [])
          
          # Generate policy cho user
          return generate_policy(user_id, 'Allow', event['methodArn'], {
              'userId': user_id,
              'roles': json.dumps(roles)
          })
      except jwt.ExpiredSignatureError:
          logger.warning("Token has expired")
          return generate_policy('user', 'Deny', event['methodArn'])
      except jwt.InvalidTokenError:
          logger.warning("Invalid token")
          return generate_policy('user', 'Deny', event['methodArn'])
      except Exception as e:
          logger.exception("Authorizer error")
          return generate_policy('user', 'Deny', event['methodArn'])
  
  # Hàm tạo IAM policy
  def generate_policy(principal_id, effect, resource, context=None):
      auth_response = {
          'principalId': principal_id
      }
      
      if effect and resource:
          policy_document = {
              'Version': '2012-10-17',
              'Statement': [
                  {
                      'Effect': effect,
                      'Resource': resource,
                      'Action': 'execute-api:Invoke'
                  }
              ]
          }
          
          auth_response['policyDocument'] = policy_document
      
      # Context sẽ được truyền đến Lambda function
      if context:
          auth_response['context'] = context
      
      return auth_response
  ```

- [ ] Định nghĩa Lambda Authorizer trong template.yaml:
  ```yaml
  AuthorizerFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/auth/
      Handler: authorizer.handler
      Runtime: python3.9
      Environment:
        Variables:
          JWT_SECRET: !Ref JWTSecret
      Policies:
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - 'logs:CreateLogGroup'
                - 'logs:CreateLogStream'
                - 'logs:PutLogEvents'
              Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/*"
  ```

### Định nghĩa API Routes/Paths

- [ ] Tạo cấu trúc routes cho API:
  ```yaml
  DefinitionBody:
    swagger: "2.0"
    info:
      title: !Sub "SDIMS API - ${Stage}"
      version: "1.0.0"
    paths:
      /auth/login:
        post:
          x-amazon-apigateway-integration:
            uri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LoginFunction.Arn}/invocations"
            passthroughBehavior: "when_no_match"
            httpMethod: "POST"
            type: "aws_proxy"
          responses: {}
          security: []  # Không yêu cầu auth
          
      /auth/refresh-token:
        post:
          x-amazon-apigateway-integration:
            uri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${RefreshTokenFunction.Arn}/invocations"
            passthroughBehavior: "when_no_match"
            httpMethod: "POST"
            type: "aws_proxy"
          responses: {}
          security: []  # Không yêu cầu auth
          
      /users:
        get:
          x-amazon-apigateway-integration:
            uri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${GetUsersFunction.Arn}/invocations"
            passthroughBehavior: "when_no_match"
            httpMethod: "POST"
            type: "aws_proxy"
          responses: {}
          security:
            - LambdaTokenAuthorizer: []
  ```

### Triển khai mẫu Lambda handler function cho API endpoints

- [ ] Tạo mẫu Lambda handler cho API endpoint:
  ```python
  # src/auth/login.py
  import json
  import os
  import time
  import jwt
  import boto3
  from aws_lambda_powertools import Logger, Tracer
  from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, Response

  logger = Logger(service="auth-service")
  tracer = Tracer(service="auth-service")
  app = ApiGatewayResolver()

  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(os.environ.get('TABLE_NAME'))

  @app.post("/auth/login")
  @tracer.capture_method
  def login():
      try:
          # Lấy body từ request
          body = app.current_event.json_body
          username = body.get('username')
          password = body.get('password')
          
          if not username or not password:
              return Response(
                  status_code=400,
                  content_type="application/json",
                  body=json.dumps({
                      "message": "Username và password là bắt buộc"
                  })
              )
          
          # Kiểm tra user trong DynamoDB
          response = table.get_item(
              Key={
                  'PK': f'USER#{username}',
                  'SK': 'PROFILE'
              }
          )
          
          user = response.get('Item')
          if not user:
              return Response(
                  status_code=401,
                  content_type="application/json",
                  body=json.dumps({
                      "message": "Tài khoản hoặc mật khẩu không đúng"
                  })
              )
          
          # Kiểm tra password (giả định đã được hash)
          # Trong thực tế, cần sử dụng so sánh hash an toàn
          if user.get('password') != password:  # Đây chỉ là ví dụ, không nên so sánh password trực tiếp
              return Response(
                  status_code=401,
                  content_type="application/json",
                  body=json.dumps({
                      "message": "Tài khoản hoặc mật khẩu không đúng"
                  })
              )
          
          # Tạo token
          current_time = int(time.time())
          jwt_secret = os.environ.get('JWT_SECRET')
          
          access_token = jwt.encode({
              'sub': user.get('userId'),
              'name': user.get('name'),
              'email': user.get('email'),
              'roles': user.get('roles', []),
              'iat': current_time,
              'exp': current_time + 3600  # 1 giờ
          }, jwt_secret, algorithm='HS256')
          
          refresh_token = jwt.encode({
              'sub': user.get('userId'),
              'iat': current_time,
              'exp': current_time + 2592000  # 30 ngày
          }, jwt_secret, algorithm='HS256')
          
          return Response(
              status_code=200,
              content_type="application/json",
              body=json.dumps({
                  "accessToken": access_token,
                  "refreshToken": refresh_token,
                  "expiresIn": 3600,
                  "user": {
                      "userId": user.get('userId'),
                      "name": user.get('name'),
                      "email": user.get('email'),
                      "roles": user.get('roles', [])
                  }
              })
          )
      except Exception as e:
          logger.exception("Error during login")
          return Response(
              status_code=500,
              content_type="application/json",
              body=json.dumps({
                  "message": "Internal server error"
              })
          )

  @tracer.capture_lambda_handler
  def handler(event, context):
      return app.resolve(event, context)
  ```

### Cấu hình API Gateway Logging

- [ ] Tạo CloudWatch Logs cho API Gateway:
  ```yaml
  APIGatewayAccessLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/apigateway/${SDIMSApi}-${Stage}-access-logs"
      RetentionInDays: 90
  ```

### Cấu hình Custom Domain (Optional)

- [ ] Thiết lập custom domain cho API:
  ```yaml
  APIDomainName:
    Type: AWS::ApiGateway::DomainName
    Properties:
      DomainName: !Sub "api.${WebsiteDomainName}"
      CertificateArn: !Ref CertificateArn
      EndpointConfiguration:
        Types:
          - REGIONAL
        
  APIMapping:
    Type: AWS::ApiGateway::BasePathMapping
    Properties:
      DomainName: !Ref APIDomainName
      RestApiId: !Ref SDIMSApi
      Stage: !Ref Stage
  ```

### Cấu hình WAF (Web Application Firewall) (Optional)

- [ ] Thiết lập WAF cho API Gateway để bảo vệ khỏi các tấn công phổ biến:
  ```yaml
  ApiGatewayWaf:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: !Sub "${AWS::StackName}-api-waf"
      Scope: REGIONAL
      DefaultAction:
        Allow: {}
      VisibilityConfig:
        SampledRequestsEnabled: true
        CloudWatchMetricsEnabled: true
        MetricName: !Sub "${AWS::StackName}-api-waf-metrics"
      Rules:
        - Name: AWSManagedRulesCommonRuleSet
          Priority: 0
          OverrideAction:
            None: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: AWSManagedRulesCommonRuleSetMetric
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesCommonRuleSet
  ```

### Tài liệu hóa

- [ ] Tạo tài liệu mô tả API Gateway:
  - Danh sách các endpoints
  - Cấu trúc request và response
  - Cách sử dụng authorizer
  - Các lỗi và cách xử lý
  - Thông tin về throttling và quotas

## Tiêu chí hoàn thành

- API Gateway được định nghĩa đầy đủ trong template.yaml
- Lambda Authorizer được triển khai
- Routes cho tất cả các API endpoints được cấu hình
- CORS được cấu hình đúng
- Logging và monitoring được thiết lập
- (Optional) Custom domain được cấu hình
- (Optional) WAF được cấu hình để bảo vệ API
- Tài liệu hướng dẫn sử dụng API được tạo

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Xem xét việc thiết lập API keys cho các dịch vụ bên thứ ba
- Cân nhắc việc thiết lập usage plans và throttling cho các API endpoints
- Nên kiểm tra kỹ các CORS settings để đảm bảo hoạt động với frontend
- Trong môi trường production, nên sử dụng API Gateway custom domain và HTTPS
- Sử dụng AWS Lambda Powertools cho Python để cải thiện logging, tracing và monitoring 