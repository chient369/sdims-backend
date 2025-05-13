**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-02 | Chiến Trần Văn | Định nghĩa chi tiết task Model Mapping Utilities | -           | Draft     |
| 1.1     | 2024-08-15 | Chiến Trần Văn | Cập nhật trạng thái hoàn thành task | -           | Completed |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển các tiện ích giúp chuyển đổi giữa dữ liệu DynamoDB và các model đối tượng Python trong hệ thống. Các tiện ích này sẽ được sử dụng trong tất cả các Lambda functions.

# Chi tiết Task: BE-CORE-002 - Model Mapping Utilities

## Thông tin chung

**Task ID:** BE-CORE-002  
**Task Name:** Phát triển Model Mapping Utilities  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-CORE-001, BE-INF-001, BE-INF-004  
**Các task phụ thuộc vào task này:** Tất cả các Lambda functions API

## Mô tả

Task này bao gồm việc phát triển các tiện ích để thực hiện chuyển đổi dữ liệu giữa:
1. Dữ liệu NoSQL DynamoDB (định dạng dạng phẳng) 
2. Các đối tượng Python cấu trúc (model) theo hướng đối tượng

Hệ thống sử dụng DynamoDB với thiết kế single-table nhưng cần làm việc với dữ liệu theo mô hình hướng đối tượng rõ ràng trong code Python. Các tiện ích này sẽ giúp quá trình chuyển đổi dữ liệu trở nên đơn giản và tự động, đồng thời đảm bảo tính nhất quán trong toàn bộ hệ thống.

## Chi tiết công việc

### Thiết lập Cấu trúc và Định nghĩa Base Models

- [x] Tạo cấu trúc thư mục trong Lambda Layer: `common/models/`
- [x] Định nghĩa các model base classes và decorators:
  - Tạo các tệp: `__init__.py`, `base_model.py`, `decorators.py`, `converters.py`, `mapper.py`
  - Định nghĩa `BaseModel` class làm nền tảng cho tất cả model
  - Tạo các decorators cho định nghĩa DynamoDB mapping

### Xây dựng BaseModel Class

- [x] Phát triển BaseModel với các tính năng sau:
  - Đặc tả và chuyển đổi định dạng dữ liệu tự động
  - Validation data cơ bản
  - Khả năng serialization/deserialization dữ liệu
  - Tracking thay đổi (dirty tracking)
  - Hỗ trợ các kiểu dữ liệu phức tạp (datetime, decimal, enum)
  - Mechanism cho đệ quy và nested objects

### Tạo Annotation và Decorators

- [x] Phát triển decorators và metadata annotations:
  - Decorator `@dynamodb_model` cho class model
  - Decorator `@attribute` cho class properties
  - Decorator `@primary_key`, `@sort_key` cho khóa chính
  - Decorator `@gsi_partition_key`, `@gsi_sort_key` cho GSI
  - Decorator `@auto_generate` cho các trường tự động sinh (UUID, timestamps)
  - Decorator `@validate` cho validation rules
  - Decorator `@default_value` cho giá trị mặc định

### Phát triển Type Converters

- [x] Tạo các type converters để chuyển đổi giữa các định dạng:
  - String converters (với hỗ trợ các format đặc biệt như ngày tháng, UUID)
  - Number converters (với xử lý đặc biệt cho decimal, float)
  - Boolean converters
  - Enum converters
  - List/Set converters
  - Map/Dictionary converters
  - Datetime/Date/Time converters
  - Embedded object converters
  - Custom type converters

### Xây dựng ModelMapper Class

- [x] Phát triển ModelMapper cho việc chuyển đổi giữa model và DynamoDB:
  - Phương thức `to_dynamodb_item()` để chuyển từ object sang DynamoDB item
  - Phương thức `from_dynamodb_item()` để chuyển từ DynamoDB item sang object
  - Phương thức `generate_key()` để tạo key cho query/get
  - Phương thức `generate_gsi_keys()` để tạo keys cho GSI queries
  - Xử lý các trường hợp đặc biệt như sparse indexes và composite keys

### Tích hợp với DynamoDB Repository

- [x] Tích hợp ModelMapper với DynamoDB Repository từ BE-CORE-001:
  - Mở rộng repository để hỗ trợ việc làm việc trực tiếp với model objects
  - Thêm các phương thức mới như `get_model()`, `save_model()`, `query_models()`, v.v.
  - Implement caching cho model metadata để tối ưu hiệu suất

### Phát triển Ví dụ Model Cơ bản

- [x] Xây dựng một số model ví dụ để minh họa cách sử dụng:
  - User model
  - Employee model
  - Opportunity model
  - Contract model

### Viết Unit Tests

- [x] Viết unit tests cho các chức năng của model mapping:
  - Tests cho BaseModel class
  - Tests cho decorators và annotations
  - Tests cho type converters
  - Tests cho ModelMapper
  - Tests cho integration với DynamoDB Repository
  - Tests cho các trường hợp dữ liệu đặc biệt

### Tài liệu hóa

- [x] Tạo tài liệu hướng dẫn sử dụng Model Mapping Utilities:
  - Cách định nghĩa model với decorators
  - Cách sử dụng type converters
  - Cách làm việc với repository và model
  - Các best practices
  - Ví dụ cụ thể

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách mong muốn sử dụng model mapping utilities khi hoàn thành:

```python
from common.models import BaseModel, dynamodb_model, attribute, primary_key, sort_key
from common.models.converters import StringConverter, DateTimeConverter, BooleanConverter
from datetime import datetime
import uuid

@dynamodb_model(table_name="SDIMS_Main")
class User(BaseModel):
    @primary_key
    @attribute(converter=StringConverter)
    def id(self) -> str:
        return f"USER#{self._id}"
    
    @sort_key
    @attribute(converter=StringConverter)
    def metadata(self) -> str:
        return "METADATA"
    
    @attribute(name="_id", converter=StringConverter, auto_generate=uuid.uuid4)
    def user_id(self) -> str:
        return self._id
    
    @attribute(converter=StringConverter)
    def username(self) -> str:
        return self._username
    
    @attribute(converter=StringConverter)
    def email(self) -> str:
        return self._email
    
    @attribute(converter=BooleanConverter, default_value=True)
    def is_active(self) -> bool:
        return self._is_active
    
    @attribute(converter=DateTimeConverter, auto_generate=datetime.now)
    def created_at(self) -> datetime:
        return self._created_at
    
    def __init__(self, username: str, email: str, is_active: bool = True, **kwargs):
        self._username = username
        self._email = email
        self._is_active = is_active
        super().__init__(**kwargs)

# Sử dụng với repository
from common.dynamodb import DynamoDBRepository

repo = DynamoDBRepository()

# Tạo user mới
user = User(username="johndoe", email="john.doe@example.com")
repo.save_model(user)

# Query user
user = repo.get_model(User, user_id="123")
users = repo.query_models(User, 
                         key_condition_expression="GSI1PK = :pk AND begins_with(GSI1SK, :sk)",
                         expression_attribute_values={":pk": "USER", ":sk": "john"},
                         index_name="GSI1")
```

## Tiêu chí hoàn thành

- Các tiện ích model mapping được thiết kế và phát triển đầy đủ
- Tất cả các chức năng chuyển đổi được unit test kỹ lưỡng
- Các ví dụ mô tả cách sử dụng rõ ràng
- Tài liệu hướng dẫn chi tiết được tạo
- Tích hợp thành công với DynamoDB Repository từ BE-CORE-001

## Ước tính thời gian

- 4-5 ngày làm việc

## Ghi chú

- Các tiện ích model mapping phải đảm bảo hiệu suất cao và không gây tác động nghiêm trọng đến thời gian xử lý API
- Cần đặc biệt lưu ý đến việc xử lý lỗi và ném ngoại lệ phù hợp khi có lỗi chuyển đổi dữ liệu
- Việc chuyển đổi phải xử lý được cả dữ liệu không đầy đủ và các trường hợp khác biệt giữa các phiên bản model
- Tích hợp với Type hints và annotations của Python để cải thiện trải nghiệm phát triển 

## Tóm tắt kết quả

Task Model Mapping Utilities đã được hoàn thành với tất cả yêu cầu đã được đáp ứng. Các chức năng chính đã được triển khai:

1. **BaseModel**: Lớp cơ sở cho tất cả model với khả năng theo dõi thay đổi và chuyển đổi dữ liệu
2. **Decorators**: Các decorator đầy đủ để định nghĩa model và thuộc tính
3. **Converters**: Bộ chuyển đổi kiểu dữ liệu đa dạng
4. **ModelMapper**: Lớp chuyển đổi giữa model và DynamoDB
5. **Tích hợp Repository**: Phương thức làm việc trực tiếp với model

Toàn bộ mã nguồn đã được test với độ phủ test cao và các vấn đề nhập/xuất module đã được giải quyết. Hướng dẫn sử dụng đã được cung cấp trong tài liệu README. 