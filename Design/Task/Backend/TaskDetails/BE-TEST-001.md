**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task viết unit tests cho các Lambda functions | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa chi tiết các công việc cần thực hiện để viết unit tests cho các Lambda functions của hệ thống, đảm bảo tính đúng đắn của logic nghiệp vụ, xử lý lỗi và tương tác với các dịch vụ AWS.

# Chi tiết Task: Viết unit tests cho các Lambda functions

## Thông tin chung

**Task ID:** BE-TEST-001  
**Task Name:** Viết unit tests cho các Lambda functions  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** BE-INF-001, BE-CORE-001, BE-CORE-002, BE-CORE-003  
**Các task phụ thuộc vào task này:** BE-DEPLOY-001  

## Mô tả

Task này bao gồm việc phát triển các unit tests toàn diện cho tất cả các Lambda functions trong hệ thống. Các tests sẽ tập trung vào việc kiểm tra logic nghiệp vụ, xử lý đầu vào, xử lý lỗi và mock các dịch vụ AWS như DynamoDB, S3. Mục tiêu là đạt được test coverage tối thiểu 80% cho tất cả các Lambda functions.

## Chi tiết công việc

### Cấu trúc và thiết lập testing framework

- [ ] Thiết lập môi trường testing và framework:
  - Location: tests/
  - Cài đặt pytest và các plugins cần thiết (pytest-cov, pytest-mock)
  - Tạo các fixtures và helpers cho testing
  - Cấu hình pytest.ini hoặc conftest.py

- [ ] Thiết lập các utility cho mocking AWS services:
  - Location: tests/mocks/
  - Tạo mock cho DynamoDB
  - Tạo mock cho S3
  - Tạo mock cho các dịch vụ AWS khác (SQS, SNS, etc.)
  - Tạo mock cho API Gateway events

### Viết tests cho Core Services

- [ ] Viết tests cho lớp truy xuất DynamoDB:
  - Location: tests/core/db/
  - Test CRUD operations
  - Test các hàm truy vấn phức tạp
  - Test xử lý lỗi và retry logic
  - Test pagination và filtering

- [ ] Viết tests cho middleware và xử lý request/response:
  - Location: tests/core/middleware/
  - Test validation logic
  - Test error handling
  - Test logging middleware
  - Test authentication middleware

- [ ] Viết tests cho authentication và authorization:
  - Location: tests/core/auth/
  - Test JWT generation và validation
  - Test role-based access control
  - Test lambda authorizer
  - Test token refresh logic

### Viết tests cho các Lambda functions theo module

- [ ] Viết tests cho module Quản lý Nhân sự:
  - Location: tests/modules/hrm/
  - Test employee CRUD operations
  - Test skill management functions
  - Test employee search và recommendation
  - Test status management

- [ ] Viết tests cho module Quản lý Hiệu suất & Margin:
  - Location: tests/modules/margin/
  - Test cost management
  - Test revenue calculation
  - Test margin calculation
  - Test margin report generation

- [ ] Viết tests cho module Quản lý Cơ hội Kinh doanh:
  - Location: tests/modules/opportunity/
  - Test Hubspot sync
  - Test opportunity status calculation
  - Test assignment logic
  - Test notes management

- [ ] Viết tests cho module Quản lý Hợp đồng & Doanh thu:
  - Location: tests/modules/contract/
  - Test contract CRUD operations
  - Test payment terms management
  - Test file attachment handling
  - Test KPI management

- [ ] Viết tests cho module Dashboard & Báo cáo:
  - Location: tests/modules/report/
  - Test dashboard data generation
  - Test report functions

- [ ] Viết tests cho module Quản trị Hệ thống:
  - Location: tests/modules/admin/
  - Test user management
  - Test role management
  - Test system configuration
  - Test system logs

### Tích hợp vào CI/CD

- [ ] Tích hợp tests vào CI/CD pipeline:
  - Location: .github/workflows/ hoặc buildspec.yml
  - Cấu hình chạy tests tự động khi push code
  - Cấu hình báo cáo test coverage
  - Thiết lập ngưỡng coverage tối thiểu (80%)

### Tạo Documentation

- [ ] Viết tài liệu hướng dẫn testing:
  - Location: docs/testing/
  - Hướng dẫn thiết lập môi trường testing
  - Hướng dẫn viết tests
  - Hướng dẫn chạy tests
  - Hướng dẫn đọc báo cáo coverage

## Ví dụ cách viết unit test cho Lambda function

Dưới đây là ví dụ về cách viết unit test cho một Lambda function:

```python
# tests/modules/hrm/test_employee_crud.py
import json
import pytest
from unittest.mock import MagicMock, patch

from modules.hrm.employee_crud import handle_get_employee

@pytest.fixture
def dynamodb_mock():
    with patch('core.db.dynamodb.DynamoDBClient') as mock:
        client_instance = MagicMock()
        mock.return_value = client_instance
        yield client_instance

@pytest.fixture
def api_gateway_event():
    return {
        'pathParameters': {'id': 'emp-123'},
        'requestContext': {
            'authorizer': {
                'claims': {'sub': 'user-1', 'scope': 'admin'}
            }
        }
    }

def test_get_employee_success(dynamodb_mock, api_gateway_event):
    # Arrange
    employee_data = {
        'PK': 'EMP#emp-123',
        'SK': 'PROFILE',
        'id': 'emp-123',
        'name': 'John Doe',
        'email': 'john@example.com',
        'status': 'ACTIVE'
    }
    dynamodb_mock.get_item.return_value = employee_data
    
    # Act
    response = handle_get_employee(api_gateway_event, {})
    
    # Assert
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['id'] == 'emp-123'
    assert body['name'] == 'John Doe'
    assert 'status' in body
    dynamodb_mock.get_item.assert_called_once_with(
        'EMP#emp-123', 'PROFILE'
    )

def test_get_employee_not_found(dynamodb_mock, api_gateway_event):
    # Arrange
    dynamodb_mock.get_item.return_value = None
    
    # Act
    response = handle_get_employee(api_gateway_event, {})
    
    # Assert
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert 'error' in body
    assert 'not found' in body['error'].lower()
```

## Tiêu chí hoàn thành

1. Tất cả các core services có unit tests đạt coverage ít nhất 80%
2. Tất cả các Lambda functions có unit tests đạt coverage ít nhất 80%
3. CI/CD pipeline được cấu hình để chạy tests tự động
4. Tests chạy nhanh và ổn định (không flaky tests)
5. Coverage report được tạo và lưu trữ sau mỗi lần chạy tests
6. Tài liệu hướng dẫn testing được hoàn thiện

## Ước tính thời gian

- 12-15 ngày làm việc

## Ghi chú

- Ưu tiên viết tests cho các core services và các Lambda functions có độ ưu tiên cao trước
- Sử dụng mocking cho các dịch vụ AWS để tránh phụ thuộc vào hạ tầng thực
- Tránh tạo integration tests trong task này (sẽ được thực hiện trong task BE-TEST-002)
- Cân nhắc sử dụng các testing patterns như Arrange-Act-Assert để cấu trúc tests rõ ràng
- Tham khảo AWS Lambda testing best practices để đảm bảo unit tests hiệu quả 