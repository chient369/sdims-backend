# API Validation Framework

## Giới thiệu

API Validation Framework là một công cụ toàn diện để xác thực dữ liệu đầu vào cho các API endpoints trong hệ thống SDIMS. Framework này cung cấp cách tiếp cận nhất quán để xác thực dữ liệu và trả về thông báo lỗi chuẩn hóa.

## Tính năng

- Xác thực dữ liệu dựa trên schema và rules
- Hỗ trợ xác thực request body, query string, path parameters và headers
- Tự động chuyển đổi kiểu dữ liệu khi cần
- Cung cấp thông báo lỗi chi tiết và hữu ích
- Tích hợp với hệ thống xử lý lỗi của ứng dụng
- Hỗ trợ đa ngôn ngữ cho thông báo lỗi

## Cài đặt

Framework này được cung cấp như một phần của common-layer. Không cần cài đặt thêm.

## Sử dụng cơ bản

### 1. Sử dụng decorator `@validate_request`

Cách đơn giản nhất để xác thực request là sử dụng decorator `@validate_request`:

```python
from common.validation import validate_request, RequiredRule, StringRule, EmailRule
from common.response import Response

# Định nghĩa schema
create_user_schema = {
    "body": {
        "name": [RequiredRule(), StringRule(min_length=2, max_length=50)],
        "email": [RequiredRule(), EmailRule()],
        "role": [StringRule(enum=["admin", "user", "guest"])]
    }
}

# Sử dụng decorator để validate request
@validate_request(schema=create_user_schema)
def create_user_handler(event, context):
    # Các tham số đã được xác thực tại điểm này
    # Nếu có lỗi validation, decorator sẽ tự động xử lý và trả về lỗi
    
    # Lấy dữ liệu đã được xác thực
    body = event.get("body", {})
    
    # Xử lý nghiệp vụ...
    
    return Response.success({"message": "User created successfully"})
```

### 2. Sử dụng SchemaValidator trực tiếp

Nếu cần xác thực dữ liệu ở bất kỳ đâu trong code, bạn có thể sử dụng `SchemaValidator` trực tiếp:

```python
from common.validation import SchemaValidator, RequiredRule, StringRule
from common.errors import ValidationError

# Định nghĩa schema
schema = {
    "username": [RequiredRule(), StringRule(min_length=3, max_length=20)],
    "password": [RequiredRule(), StringRule(min_length=8)]
}

# Xác thực dữ liệu
data = {"username": "user1", "password": "short"}
validator = SchemaValidator(schema)
result = validator.validate(data)

if not result.is_valid:
    # Xử lý lỗi
    errors = result.get_errors_list()
    raise ValidationError("Validation failed", details={"errors": errors})
```

## Validation Rules

Framework cung cấp các rule validation sau:

### RequiredRule

Yêu cầu một giá trị phải tồn tại và không rỗng.

```python
RequiredRule(message="Field is required")
```

### StringRule

Xác thực giá trị là một chuỗi với các ràng buộc tùy chọn.

```python
StringRule(
    min_length=None,  # Độ dài tối thiểu
    max_length=None,  # Độ dài tối đa
    pattern=None,     # Regex pattern
    enum=None,        # Danh sách giá trị được phép
    message=None      # Thông báo lỗi tùy chỉnh
)
```

### NumberRule

Xác thực giá trị là một số với các ràng buộc tùy chọn.

```python
NumberRule(
    min_value=None,  # Giá trị tối thiểu
    max_value=None,  # Giá trị tối đa
    is_integer=False, # Yêu cầu là số nguyên
    message=None     # Thông báo lỗi tùy chỉnh
)
```

### BooleanRule

Xác thực giá trị là một boolean.

```python
BooleanRule(message=None)
```

### DateRule

Xác thực giá trị là một ngày tháng với các ràng buộc tùy chọn.

```python
DateRule(
    min_date=None,  # Ngày tối thiểu
    max_date=None,  # Ngày tối đa
    format=None,    # Định dạng ngày tháng
    message=None    # Thông báo lỗi tùy chỉnh
)
```

### EnumRule

Xác thực giá trị nằm trong danh sách các giá trị được phép.

```python
EnumRule(
    allowed_values=[], # Danh sách giá trị được phép
    message=None       # Thông báo lỗi tùy chỉnh
)
```

### ArrayRule

Xác thực giá trị là một mảng với các ràng buộc tùy chọn.

```python
ArrayRule(
    min_items=None,    # Số lượng phần tử tối thiểu
    max_items=None,    # Số lượng phần tử tối đa
    unique_items=False, # Yêu cầu các phần tử là duy nhất
    item_validator=None, # Validator cho từng phần tử
    message=None        # Thông báo lỗi tùy chỉnh
)
```

### ObjectRule

Xác thực giá trị là một object với các ràng buộc tùy chọn.

```python
ObjectRule(
    properties=None,            # Dictionary các property validators
    required_properties=None,   # Danh sách property bắt buộc
    additional_properties=True, # Cho phép thuộc tính bổ sung
    message=None                # Thông báo lỗi tùy chỉnh
)
```

### EmailRule

Xác thực giá trị là một địa chỉ email hợp lệ.

```python
EmailRule(message=None)
```

### URLRule

Xác thực giá trị là một URL hợp lệ.

```python
URLRule(message=None)
```

### PhoneRule

Xác thực giá trị là một số điện thoại hợp lệ.

```python
PhoneRule(message=None)
```

## Common Validations

Framework cung cấp một bộ các validation phổ biến thông qua class `CommonValidations`:

```python
from common.validation import CommonValidations

# Sử dụng các validation đã định nghĩa sẵn
user_schema = {
    "id": CommonValidations.UUID,
    "email": CommonValidations.required(CommonValidations.EMAIL),
    "age": CommonValidations.POSITIVE_INTEGER,
    "phone": CommonValidations.PHONE
}

# Các methods tiện ích
CommonValidations.required(validation_rules)  # Làm một field trở thành bắt buộc
CommonValidations.string(min_length, max_length, pattern, message, required)
CommonValidations.number(min_value, max_value, is_integer, message, required)
CommonValidations.enum(allowed_values, message, required)
# ... và nhiều methods khác
```

## Schema Templates

Framework cung cấp các template schema phổ biến thông qua class `SchemaTemplates`:

```python
from common.validation import SchemaTemplates

# Sử dụng các template đã định nghĩa sẵn
user_list_schema = {
    "query_string": SchemaTemplates.combine(
        SchemaTemplates.PAGINATION_PARAMS,
        SchemaTemplates.SEARCH_PARAMS
    )
}

# Phương thức combine để kết hợp nhiều schema
combined_schema = SchemaTemplates.combine(
    SchemaTemplates.PAGINATION_PARAMS,
    SchemaTemplates.DATE_RANGE_PARAMS
)
```

## Format lỗi

Khi validation thất bại, framework sẽ trả về lỗi theo định dạng sau:

```json
{
  "status": "error",
  "code": "E2000",
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "email",
      "message": "Email không đúng định dạng"
    },
    {
      "field": "name",
      "message": "Trường 'name' phải có ít nhất 2 ký tự"
    }
  ]
}
```

## Ví dụ chi tiết

### Ví dụ 1: Xác thực API tạo nhân viên

```python
from common.validation import validate_request, RequiredRule, StringRule, EmailRule, PhoneRule
from common.response import Response
from common.errors import BadRequestError

# Định nghĩa schema
create_employee_schema = {
    "body": {
        "first_name": [RequiredRule(), StringRule(min_length=2, max_length=50)],
        "last_name": [RequiredRule(), StringRule(min_length=2, max_length=50)],
        "email": [RequiredRule(), EmailRule()],
        "position": [RequiredRule(), StringRule()],
        "team_id": [StringRule(pattern=r"^TEAM-[A-Z0-9]{8}$")], 
        "phone_number": [StringRule(pattern=r"^\+[0-9]{10,15}$")]
    },
    "query_string": {
        "include_skills": [StringRule(enum=["true", "false"])],
    }
}

# Sử dụng decorator để validate request
@validate_request(schema=create_employee_schema)
def create_employee_handler(event, context):
    try:
        body = event.get("body", {})
        
        # Tạo nhân viên mới...
        
        return Response.success({"message": "Employee created successfully", "id": "EMP-12345"})
    except Exception as e:
        return Response.error(str(e), 400)
```

### Ví dụ 2: Sử dụng Schema Templates và CommonValidations

```python
from common.validation import validate_request, CommonValidations, SchemaTemplates
from common.response import Response

# Định nghĩa schema
list_employees_schema = {
    "query_string": SchemaTemplates.combine(
        SchemaTemplates.PAGINATION_PARAMS,
        SchemaTemplates.SEARCH_PARAMS,
        {
            "team_id": CommonValidations.string(pattern=r"^TEAM-[A-Z0-9]{8}$"),
            "status": CommonValidations.enum(["active", "inactive", "on_leave"]),
            "hire_date_from": CommonValidations.DATE,
            "hire_date_to": CommonValidations.DATE
        }
    )
}

@validate_request(schema=list_employees_schema)
def list_employees_handler(event, context):
    query_params = event.get("queryStringParameters", {})
    
    # Xử lý query params
    page = int(query_params.get("page", 1))
    size = int(query_params.get("size", 20))
    
    # Lấy danh sách nhân viên...
    
    return Response.paginated(
        items=[],  # Items for this page
        count=100,  # Total number of items
        page=page,
        page_size=size,
        has_more=(page * size < 100)  # Whether there are more pages
    )
```

## Best Practices

1. **Định nghĩa schema riêng biệt**: Tách các schema validation ra thành các file riêng biệt để dễ quản lý.

2. **Sử dụng thông báo lỗi rõ ràng**: Cung cấp thông báo lỗi hữu ích cho người dùng.

3. **Tái sử dụng các validation phổ biến**: Sử dụng `CommonValidations` và `SchemaTemplates` để tránh lặp lại code.

4. **Xử lý lỗi nhất quán**: Đảm bảo tất cả các API của bạn xử lý lỗi validation theo cùng một cách.

5. **Test validation logic**: Viết unit tests cho các validation rules và schema của bạn. 