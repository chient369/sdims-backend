**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-03 | Chiến Trần Văn | Định nghĩa chi tiết task API Validation Framework | -           | Draft     |
| 1.1     | 2024-08-14 | Chiến Trần Văn | Cập nhật trạng thái hoàn thành task | -           | Completed |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển một framework validation API toàn diện cho backend system. Framework này sẽ chuẩn hóa việc kiểm tra và xác thực đầu vào cho tất cả các Lambda functions API.

# Chi tiết Task: BE-CORE-003 - API Validation Framework

## Thông tin chung

**Task ID:** BE-CORE-003  
**Task Name:** Phát triển API Validation Framework  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-CORE-001  
**Các task phụ thuộc vào task này:** Tất cả các Lambda functions API
**Trạng thái:** Hoàn thành (Completed)

## Mô tả

Task này bao gồm việc phát triển một framework để xác thực dữ liệu đầu vào cho các API endpoints, đảm bảo tính nhất quán trong kiểm tra dữ liệu và cung cấp thông báo lỗi chuẩn hóa. Framework này sẽ hỗ trợ kiểm tra request parameters, query strings, path parameters, và request body, tích hợp chặt chẽ với API Gateway và Lambda functions.

## Chi tiết công việc

### Thiết kế Framework Architecture

- [x] Thiết kế cấu trúc tổng thể của validation framework:
  - Xây dựng theo mô hình kết hợp schema-based và rule-based validation
  - Tạo cơ chế để tích hợp validation với Lambda API handlers
  - Thiết kế hệ thống thông báo lỗi chuẩn hóa
  - Đảm bảo hiệu suất tối ưu cho các API có tần suất sử dụng cao

### Xây dựng Schema Validation Component

- [x] Phát triển component chịu trách nhiệm schema validation:
  - Tạo các lớp SchemaValidator để xác thực cấu trúc JSON
  - Hỗ trợ định nghĩa schema dưới dạng Python dictionaries
  - Cung cấp cơ chế kiểm tra kiểu dữ liệu, giá trị, các ràng buộc
  - Xây dựng cách định nghĩa schema theo từng API endpoint
  - Tích hợp với tiêu chuẩn OpenAPI/Swagger

### Phát triển Rule-based Validation Component

- [x] Xây dựng component rule-based validation:
  - Tạo các lớp Rule đại diện cho các quy tắc validation khác nhau
  - Cung cấp cơ chế tạo và kết hợp các rule đơn giản thành rule phức tạp
  - Hỗ trợ validation có điều kiện và phụ thuộc lẫn nhau giữa các trường
  - Xây dựng custom rule cho các trường hợp đặc biệt

### Xây dựng Validation Decorator

- [x] Phát triển decorator `@validate_request` để đơn giản hóa việc áp dụng validation:
  - Tạo decorator có thể áp dụng cho các Lambda handler
  - Hỗ trợ các tham số cấu hình khác nhau (validate body, query string, path params, etc.)
  - Tự động kết nối với schema và rules đã định nghĩa
  - Cung cấp cơ chế bypass validation cho một số trường hợp đặc biệt
  - Xử lý các trường hợp ngoại lệ và lỗi validation

### Xây dựng Validation Rules Catalog

- [x] Phát triển bộ rules cho các trường hợp thông dụng:
  - Rules cho kiểu dữ liệu cơ bản (string, number, boolean, date, etc.)
  - Rules cho định dạng (email, phone, UUID, date formats, etc.)
  - Rules cho giá trị (min/max, regex pattern, enum, etc.)
  - Rules cho tập hợp (min/max items, unique items, etc.)
  - Rules cho đối tượng phức tạp (required fields, dependencies, etc.)
  - Rules cho validation nghiệp vụ đặc thù (ví dụ: trạng thái hợp lệ, etc.)

### Xây dựng Error Response Standardization

- [x] Phát triển chuẩn hóa thông báo lỗi:
  - Định nghĩa response structure cho các lỗi validation
  - Ánh xạ lỗi validation với các error code từ API-errors-list
  - Hỗ trợ đa ngôn ngữ cho thông báo lỗi
  - Cung cấp thông báo lỗi chi tiết và hữu ích cho người dùng
  - Tích hợp với error handling utility trong BE-CORE-001

### Xây dựng Middleware Integration

- [x] Phát triển cơ chế middleware để tích hợp validation với request handling:
  - Tạo middlewares cho các loại request khác nhau
  - Hỗ trợ validation theo request context
  - Cung cấp cơ chế để chọn schema validation dựa trên endpoint và HTTP method
  - Tích hợp với các middleware khác trong hệ thống

### Phát triển Schema Repository

- [x] Xây dựng repository cho việc quản lý và sử dụng lại các schema:
  - Cung cấp các schema cơ bản được sử dụng nhiều
  - Hỗ trợ tái sử dụng và kế thừa schema
  - Các schema mẫu cho các entity chính của hệ thống
  - Cơ chế cập nhật và phiên bản của schema

### Phát triển Unit Tests

- [x] Viết unit tests cho framework validation:
  - Tests cho SchemaValidator
  - Tests cho Rule-based Validation
  - Tests cho Validation Decorator
  - Tests cho Error Response Standardization
  - Tests cho Schema Repository
  - Tests cho các tình huống validation phức tạp và đặc biệt

### Xây dựng Tài liệu và Ví dụ

- [x] Tạo tài liệu hướng dẫn sử dụng Validation Framework:
  - Cách sử dụng decorator `@validate_request`
  - Cách định nghĩa schema
  - Cách xây dựng custom rules
  - Các best practices
  - Xử lý các trường hợp ngoại lệ

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách mong muốn sử dụng API Validation Framework khi hoàn thành:

```python
from common.validation import validate_request, StringRule, IntegerRule, EmailRule, RequiredRule
from common.response import Response
from common.errors import BadRequestError

# Định nghĩa schema cho API
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
    # Các tham số đã được validate tại điểm này
    # Nếu có lỗi validation, decorator sẽ trả về lỗi và không thực hiện code bên dưới
    
    body = event.get("body", {})
    
    # Xử lý nghiệp vụ
    try:
        # Tạo nhân viên mới...
        return Response.success({"message": "Employee created successfully", "id": new_employee_id})
    except Exception as e:
        # Xử lý lỗi nghiệp vụ
        raise BadRequestError(str(e))
```

Ví dụ về thông báo lỗi trả về:

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
      "field": "team_id",
      "message": "Team ID không đúng định dạng, phải có dạng TEAM-XXXXXXXX"
    }
  ]
}
```

## Tiêu chí hoàn thành

- [x] API Validation Framework được thiết kế và phát triển đầy đủ
- [x] Tất cả các chức năng validation được unit test kỹ lưỡng
- [x] Tích hợp thành công với error handling từ BE-CORE-001
- [x] Tài liệu hướng dẫn chi tiết và các ví dụ được tạo
- [x] Framework đã được thử nghiệm với ít nhất 5 API endpoint khác nhau

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Validation framework cần được thiết kế để cân bằng giữa tính linh hoạt và dễ sử dụng
- Cần đảm bảo validation không gây tác động lớn đến hiệu suất API
- Các thông báo lỗi phải rõ ràng, hữu ích, và tuân theo chuẩn định nghĩa trong api_errors_list.md
- Framework cần hỗ trợ cả validation đơn giản và phức tạp
- Cần đặc biệt chú ý đến khả năng mở rộng và bảo trì 

## Kết quả hoàn thành

API Validation Framework đã được phát triển thành công với đầy đủ các tính năng yêu cầu:

1. **Validation Rules**: 
   - Hỗ trợ nhiều loại rules (Required, String, Number, Boolean, Email, Date, Enum, Array, Object, URL, Phone)
   - Khả năng tùy chỉnh message lỗi cho từng rule
   - Hỗ trợ validation phức tạp với nested objects và arrays

2. **Schema Validation**:
   - Validation của nhiều loại tham số (body, query string, path params, headers)
   - Hỗ trợ schema phức tạp với nhiều tầng lồng nhau
   - Thông báo lỗi rõ ràng, chi tiết

3. **Validation Decorator**:
   - Dễ dàng áp dụng cho Lambda handlers
   - Tích hợp các tùy chọn cấu hình
   - Xử lý lỗi và chuyển đổi sang API errors

4. **Utilities**:
   - CommonValidations cung cấp các validation patterns phổ biến
   - SchemaTemplates hỗ trợ tái sử dụng schema
   - Unit tests toàn diện

5. **Tài liệu**:
   - README.md đầy đủ với cách sử dụng, ví dụ, best practices
   - Examples cho từng trường hợp sử dụng

Framework đã sẵn sàng để sử dụng trong tất cả các Lambda functions API của hệ thống. 