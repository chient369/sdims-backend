**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai DynamoDB table | -           | Draft     |
| 1.1     | 2024-08-05 | Chiến Trần Văn | Cập nhật tiến độ hoàn thành task | -           | Completed |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để triển khai DynamoDB table theo cấu trúc đã định nghĩa trong tài liệu thiết kế, áp dụng single-table design.

# Chi tiết Task: BE-INF-004 - Triển khai DynamoDB table

## Thông tin chung

**Task ID:** BE-INF-004  
**Task Name:** Triển khai DynamoDB table theo cấu trúc đã định nghĩa  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-INF-001  
**Các task phụ thuộc vào task này:** BE-CORE-001 và tất cả các API cần truy cập dữ liệu

## Mô tả

Task này bao gồm việc định nghĩa và triển khai DynamoDB table cho hệ thống theo thiết kế single-table design như đã được mô tả trong tài liệu DB/dynamodb_structure.json. Bảng sẽ được cấu hình với các khóa chính, các Global Secondary Indexes (GSI), và các thuộc tính phù hợp để hỗ trợ các access patterns đã xác định.

## Chi tiết công việc

### Phân tích cấu trúc DynamoDB đã định nghĩa

- [x] Xem xét kỹ tài liệu BD/DB/dynamodb_structure.json để hiểu rõ:
  - Cấu trúc khóa chính (PK, SK)
  - Các Global Secondary Indexes
  - Các entity types và thuộc tính
  - Các access patterns (cách truy vấn dữ liệu)

### Định nghĩa DynamoDB trong CloudFormation template

- [x] Khai báo DynamoDB table trong template.yaml:
  ```yaml
  SDIMSTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "SDIMS-Main-${Stage}"
      BillingMode: PROVISIONED
      ProvisionedThroughput:
        ReadCapacityUnits: !Ref DynamoDBReadCapacityUnits
        WriteCapacityUnits: !Ref DynamoDBWriteCapacityUnits
      AttributeDefinitions:
        - AttributeName: PK
          AttributeType: S
        - AttributeName: SK
          AttributeType: S
        - AttributeName: GSI1PK
          AttributeType: S
        - AttributeName: GSI1SK
          AttributeType: S
        - AttributeName: GSI2PK
          AttributeType: S
        - AttributeName: GSI2SK
          AttributeType: S
        - AttributeName: GSI3PK
          AttributeType: S
        - AttributeName: GSI3SK
          AttributeType: S
      KeySchema:
        - AttributeName: PK
          KeyType: HASH
        - AttributeName: SK
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: GSI1
          KeySchema:
            - AttributeName: GSI1PK
              KeyType: HASH
            - AttributeName: GSI1SK
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: !Ref DynamoDBGSIReadCapacityUnits
            WriteCapacityUnits: !Ref DynamoDBGSIWriteCapacityUnits
        - IndexName: GSI2
          KeySchema:
            - AttributeName: GSI2PK
              KeyType: HASH
            - AttributeName: GSI2SK
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: !Ref DynamoDBGSIReadCapacityUnits
            WriteCapacityUnits: !Ref DynamoDBGSIWriteCapacityUnits
        - IndexName: GSI3
          KeySchema:
            - AttributeName: GSI3PK
              KeyType: HASH
            - AttributeName: GSI3SK
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: !Ref DynamoDBGSIReadCapacityUnits
            WriteCapacityUnits: !Ref DynamoDBGSIWriteCapacityUnits
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Stage
  ```

### Định nghĩa Parameters cho DynamoDB

- [x] Thêm parameters cho việc cấu hình capacity units:
  ```yaml
  Parameters:
    # ... các parameters khác ...
    DynamoDBReadCapacityUnits:
      Type: Number
      Default: 5
      Description: Read capacity units cho DynamoDB table
      
    DynamoDBWriteCapacityUnits:
      Type: Number
      Default: 5
      Description: Write capacity units cho DynamoDB table
      
    DynamoDBGSIReadCapacityUnits:
      Type: Number
      Default: 5
      Description: Read capacity units cho Global Secondary Indexes
      
    DynamoDBGSIWriteCapacityUnits:
      Type: Number
      Default: 5
      Description: Write capacity units cho Global Secondary Indexes
  ```

### Thiết lập DynamoDB Auto Scaling (optional)

- [x] Cấu hình auto scaling cho DynamoDB table:
  ```yaml
  TableReadScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${SDIMSTable}-read-scaling-policy"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref TableReadScalingTarget
      TargetTrackingScalingPolicyConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: DynamoDBReadCapacityUtilization
        TargetValue: 70
        ScaleInCooldown: 60
        ScaleOutCooldown: 60
        
  TableReadScalingTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 100
      MinCapacity: 5
      ResourceId: !Sub "table/${SDIMSTable}"
      ScalableDimension: dynamodb:table:ReadCapacityUnits
      ServiceNamespace: dynamodb
      RoleARN: !GetAtt ScalingRole.Arn
      
  # Tương tự cho WriteCapacityUnits và GSIs
  ```

### Cấu hình Backup và Recovery

- [x] Thiết lập DynamoDB backup:
  ```yaml
  PointInTimeRecoverySpecification:
    PointInTimeRecoveryEnabled: true
  SSESpecification:
    SSEEnabled: true
  ```

### Tạo script init data (Optional)

- [x] Tạo script để khởi tạo dữ liệu ban đầu:
  - Dữ liệu danh mục (Category)
  - Dữ liệu vai trò (Roles)
  - Dữ liệu quyền (Permissions)
  - User admin ban đầu

### Tài liệu hóa

- [x] Tạo tài liệu mô tả cấu trúc bảng DynamoDB:
  - Mô tả pattern của khóa (PK, SK)
  - Mô tả cách sử dụng các GSI cho các loại truy vấn
  - Hướng dẫn thiết kế truy vấn theo access patterns
  - Hướng dẫn sử dụng single-table design hiệu quả

## Tiêu chí hoàn thành

- [x] DynamoDB table đã được định nghĩa đầy đủ trong template.yaml
- [x] Cấu trúc bảng có đầy đủ các GSI để hỗ trợ tất cả access patterns đã xác định
- [x] (Nếu cần) Auto scaling đã được cấu hình
- [x] Backup và PITR (Point-in-Time Recovery) đã được bật
- [x] Tài liệu hướng dẫn sử dụng DynamoDB đã được tạo

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Single-table design có thể khó hiểu với những người mới, nên đảm bảo tài liệu rõ ràng
- Cần chú ý cấu hình capacity units cho tiết kiệm chi phí nhưng vẫn đảm bảo hiệu suất
- Nên có kế hoạch migration dữ liệu khi có thay đổi cấu trúc bảng
- Đảm bảo tất cả truy vấn đều được index để tránh full table scan
- Xem xét sử dụng các thư viện Python như PynamoDB hoặc AWS Data Mapper để làm việc với DynamoDB
- Tạo các lớp model trong Python để tương tác với DynamoDB theo mô hình OOP
- Sử dụng AWS Lambda Powertools cho Python để cải thiện logging, tracing và theo dõi hiệu suất DynamoDB 