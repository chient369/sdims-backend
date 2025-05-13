**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task thiết lập môi trường testing | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa chi tiết công việc thiết lập môi trường testing cho việc phát triển, debug và chạy các tests tự động cho hệ thống serverless, bao gồm các công cụ mô phỏng dịch vụ AWS để giảm sự phụ thuộc vào tài nguyên cloud thực sự.

# Chi tiết Task: Thiết lập môi trường testing

## Thông tin chung

**Task ID:** BE-TEST-003  
**Task Name:** Thiết lập môi trường testing  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** BE-INF-001, BE-INF-004, BE-INF-005  
**Các task phụ thuộc vào task này:** BE-TEST-001, BE-TEST-002  

## Mô tả

Task này bao gồm việc thiết lập một môi trường testing hoàn chỉnh cho việc phát triển và kiểm thử các Lambda functions và các thành phần backend khác. Môi trường này sẽ sử dụng các công cụ giả lập dịch vụ AWS như DynamoDB Local, LocalStack (cho S3, SQS, SNS), và AWS SAM CLI để chạy Lambda functions cục bộ. Mục tiêu là tạo ra một môi trường đáng tin cậy, dễ sử dụng và được tự động hóa cao để các nhà phát triển có thể kiểm thử code nhanh chóng mà không cần triển khai lên AWS.

## Chi tiết công việc

### Cài đặt và cấu hình DynamoDB Local

- [ ] Thiết lập DynamoDB Local:
  - Location: tools/testing/dynamodb-local/
  - Cấu hình Docker image cho DynamoDB Local
  - Tạo script khởi động và dừng DynamoDB Local
  - Phát triển utility script để tạo bảng và khởi tạo dữ liệu mẫu
  - Viết documentation về cách sử dụng

- [ ] Phát triển utility classes để tương tác với DynamoDB Local:
  - Location: src/core/test_utils/dynamodb/
  - Tạo wrapper class cho DynamoDB client để kết nối tới DynamoDB Local
  - Phát triển functions để seed dữ liệu test
  - Tạo các helpers để dễ dàng kiểm tra trạng thái dữ liệu trong tests

### Cài đặt và cấu hình LocalStack

- [ ] Thiết lập LocalStack cho các dịch vụ AWS khác:
  - Location: tools/testing/localstack/
  - Cấu hình Docker image cho LocalStack
  - Tạo script khởi động và dừng LocalStack
  - Cấu hình các dịch vụ AWS cần thiết (S3, SQS, SNS, etc.)
  - Viết documentation về cách sử dụng

- [ ] Phát triển utility classes để tương tác với LocalStack:
  - Location: src/core/test_utils/localstack/
  - Tạo wrapper classes cho S3, SQS, SNS clients
  - Phát triển functions để khởi tạo buckets, queues, topics
  - Tạo các helpers để dễ dàng kiểm tra trạng thái các tài nguyên

### Cấu hình AWS SAM CLI cho local development

- [ ] Thiết lập môi trường phát triển cục bộ với AWS SAM CLI:
  - Location: tools/testing/sam-local/
  - Cấu hình template.yaml cho môi trường local
  - Tạo các environment variables cần thiết
  - Phát triển script để chạy Lambda functions cục bộ
  - Cấu hình kết nối giữa Lambda local với DynamoDB Local và LocalStack

- [ ] Tạo các mocks và stubs cho các dịch vụ AWS khác:
  - Location: src/core/test_utils/mocks/
  - Phát triển mock cho Hubspot API
  - Tạo mocks cho các dịch vụ email
  - Phát triển mocks cho các dependancies bên ngoài khác

### Thiết lập API Gateway Local

- [ ] Cấu hình API Gateway local:
  - Location: tools/testing/api-gateway/
  - Thiết lập API Gateway Express
  - Cấu hình routing để kết nối với Lambda functions local
  - Thiết lập test endpoints cho API testing
  - Cấu hình CORS và authorization

### Tích hợp cục bộ

- [ ] Tích hợp tất cả các thành phần:
  - Location: tools/testing/
  - Tạo Docker Compose file để khởi động toàn bộ môi trường testing
  - Phát triển script khởi động một-chạm cho môi trường testing
  - Thiết lập kết nối giữa các thành phần (Lambda, API Gateway, DynamoDB, S3)
  - Tạo các scripts để khởi tạo dữ liệu mẫu cho toàn bộ hệ thống

### Tự động hóa setup môi trường tests

- [ ] Tạo script tự động cho CI/CD:
  - Location: .github/scripts/ hoặc .aws/
  - Phát triển script tự động setup môi trường testing trong CI/CD
  - Cấu hình GitHub Actions hoặc AWS CodeBuild để chạy môi trường testing
  - Tạo workflow tự động cho việc chạy tests

- [ ] Phát triển script dọn dẹp và khởi tạo lại môi trường:
  - Location: tools/testing/
  - Tạo script để reset dữ liệu giữa các lần chạy test
  - Phát triển script kiểm tra trạng thái môi trường

### Tạo Documentation

- [ ] Viết tài liệu hướng dẫn setup và sử dụng môi trường testing:
  - Location: docs/testing/environment/
  - Hướng dẫn cài đặt môi trường từ đầu
  - Hướng dẫn chạy Lambda functions cục bộ
  - Hướng dẫn tương tác với các dịch vụ giả lập
  - Hướng dẫn debug và troubleshooting
  - Tài liệu về best practices khi làm việc với môi trường testing

## Ví dụ file cấu hình

Dưới đây là ví dụ về file Docker Compose để thiết lập môi trường testing:

```yaml
# tools/testing/docker-compose.yml
version: '3.8'

services:
  dynamodb-local:
    image: amazon/dynamodb-local:latest
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    command: "-jar DynamoDBLocal.jar -sharedDb -inMemory"
    networks:
      - test-network

  localstack:
    image: localstack/localstack:latest
    container_name: localstack
    ports:
      - "4566:4566"
      - "4571:4571"
    environment:
      - SERVICES=s3,sqs,sns
      - DEBUG=1
      - DATA_DIR=/tmp/localstack/data
    volumes:
      - ./localstack:/tmp/localstack
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - test-network

  api-gateway:
    build:
      context: ./api-gateway
      dockerfile: Dockerfile
    container_name: api-gateway
    depends_on:
      - localstack
      - dynamodb-local
    ports:
      - "3000:3000"
    environment:
      - DYNAMODB_ENDPOINT=http://dynamodb-local:8000
      - LOCALSTACK_ENDPOINT=http://localstack:4566
    networks:
      - test-network

networks:
  test-network:
    driver: bridge
```

## Ví dụ script khởi tạo DynamoDB

Dưới đây là ví dụ về script khởi tạo DynamoDB Local:

```python
# tools/testing/dynamodb-local/init-db.py
import boto3
import json
import os

def create_tables():
    """Create DynamoDB tables for local development."""
    # Connect to DynamoDB Local
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',
        region_name='us-east-1',
        aws_access_key_id='dummy',
        aws_secret_access_key='dummy'
    )
    
    # Create main table with GSIs
    table = dynamodb.create_table(
        TableName='InternalManagementSystem',
        KeySchema=[
            {'AttributeName': 'PK', 'KeyType': 'HASH'},
            {'AttributeName': 'SK', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1SK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI2PK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI2SK', 'AttributeType': 'S'},
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'GSI1',
                'KeySchema': [
                    {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5
                }
            },
            {
                'IndexName': 'GSI2',
                'KeySchema': [
                    {'AttributeName': 'GSI2PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'GSI2SK', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5
                }
            }
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    
    print(f"Table {table.table_name} created successfully")
    
    # Load test data
    load_test_data(dynamodb)

def load_test_data(dynamodb):
    """Load test data from JSON files into DynamoDB tables."""
    table = dynamodb.Table('InternalManagementSystem')
    data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            with open(os.path.join(data_dir, filename), 'r') as f:
                items = json.load(f)
                for item in items:
                    table.put_item(Item=item)
            print(f"Loaded test data from {filename}")

if __name__ == '__main__':
    create_tables()
```

## Tiêu chí hoàn thành

1. Môi trường testing cục bộ hoàn chỉnh đã được thiết lập và có thể khởi động bằng một lệnh duy nhất
2. DynamoDB Local được cấu hình đúng với cấu trúc bảng giống như môi trường production
3. LocalStack được cấu hình để giả lập các dịch vụ AWS cần thiết (S3, SQS, SNS)
4. AWS SAM CLI được cấu hình để có thể chạy Lambda functions cục bộ
5. API Gateway local được thiết lập để kiểm thử API endpoints
6. Scripts tự động hóa đã được phát triển để khởi tạo dữ liệu test
7. Tài liệu hướng dẫn đầy đủ đã được viết về cách sử dụng môi trường testing
8. CI/CD pipeline có thể tự động thiết lập môi trường testing để chạy tests

## Ước tính thời gian

- 7-9 ngày làm việc

## Ghi chú

- Môi trường testing phải hoạt động được trên cả Windows, macOS và Linux để phục vụ cho tất cả các nhà phát triển
- Docker là yêu cầu bắt buộc để chạy môi trường testing, cần đảm bảo hướng dẫn cài đặt Docker rõ ràng
- Cân nhắc sử dụng các công cụ như testcontainers để đơn giản hóa việc quản lý môi trường testing
- Đảm bảo resources sử dụng cho môi trường testing không quá lớn để có thể chạy trên máy tính của nhà phát triển
- Cần thêm các ví dụ về cách chạy unit tests và integration tests trong môi trường này 