**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-12 | Chiến Trần Văn | Tạo quy tắc thực hiện chung cho các task backend | -           | Draft     |

---

## 1. Mục tiêu  
Xác định các quy tắc và tiêu chuẩn thực hiện task chung cho các developer backend nhằm đảm bảo tính nhất quán trong toàn bộ hệ thống.

# Quy tắc Thực hiện Task Backend

## Tổng quan

Tài liệu này định nghĩa các tiêu chuẩn và quy tắc lập trình chung mà tất cả các task backend cần tuân thủ. Mục đích là đảm bảo tính nhất quán trong mã nguồn, dễ bảo trì, và tuân thủ các nguyên tắc thiết kế hiện đại.

## Cấu trúc dự án

### Lambda Layer
- Sử dụng Lambda Layer cho mã dùng chung giữa các function
- Layer đã được thiết lập:
  - `common-layer`: Utilities cơ bản (BE-CORE-001)
  - `auth-layer`: Xác thực và phân quyền (BE-AUTH-001)
  - `api-utils-layer`: Tích hợp API Gateway (BE-CORE-006)

## Tiêu chuẩn mã nguồn

### Ngôn ngữ lập trình
- Python 3.13
- Tuân thủ PEP 8
- Độ dài dòng tối đa: 100 ký tự
- Sử dụng 4 khoảng trắng cho indentation

### Type Hinting
- Bắt buộc sử dụng type hints cho tất cả các functions và methods
- Sử dụng thư viện `typing` cho các type phức tạp
- Ví dụ:
  ```python
  from typing import Dict, List, Optional, Any
  
  def process_data(input_data: Dict[str, Any], options: Optional[List[str]] = None) -> Dict[str, Any]:
      # ...
  ```

### Docstring
- Sử dụng docstring kiểu Google cho tất cả các functions và classes
- Bao gồm mô tả, parameters, returns, raises (nếu có)
- Ví dụ:
  ```python
  def fetch_user(user_id: str) -> Dict[str, Any]:
      """
      Retrieve user information from database.
      
      Args:
          user_id: The ID of the user to retrieve
          
      Returns:
          A dictionary containing user information
          
      Raises:
          NotFoundException: If user is not found
          DatabaseError: If database connection fails
      """
      # ...
  ```

### Xử lý lỗi
- Sử dụng custom exceptions từ `common.errors`
- Luôn catch lỗi cụ thể, không dùng bare except
- Log đầy đủ thông tin lỗi
- Lỗi cần được classify theo đúng loại trong API errors list

### Logging
- Sử dụng `aws_lambda_powertools.Logger`
- Mỗi module/class cần tạo logger riêng với service name phù hợp
- Log đầy đủ thông tin ở các mức độ phù hợp (INFO, ERROR, DEBUG)
- Không log thông tin nhạy cảm (mật khẩu, token, etc.)

### Testing
- 80% code coverage là yêu cầu tối thiểu
- Dùng pytest cho unit tests
- Mocking cho các external dependencies
- Viết tests cho các trường hợp lỗi và edge cases

## Quy tắc lập trình

### Clean Code
- Tên biến/hàm rõ ràng, có ý nghĩa (descriptive names)
- Một hàm chỉ thực hiện một nhiệm vụ duy nhất (Single Responsibility)
- Functions không nên quá 30 dòng code
- Tránh duplicate code, ưu tiên DRY (Don't Repeat Yourself)
- Tất cả các hằng số phải được định nghĩa ở đầu file/module

### Thiết kế
- Tuân thủ nguyên tắc SOLID
- Dependency Injection khi thích hợp
- Factory pattern cho các đối tượng phức tạp
- Tách biệt rõ ràng các layers (controller, service, repository)

### AWS Serverless
- Tối ưu hóa Lambda cold start
- Tránh tạo connections trong handler function
- Sử dụng global scope cho các kết nối tới dịch vụ (DynamoDB, etc.)
- Xử lý timeout và retry phù hợp
- Sử dụng X-Ray cho tracing khi cần

### DynamoDB
- Tuân thủ quy tắc access pattern đã định nghĩa
- Sử dụng DynamoDBRepository từ common layer
- Tối ưu hóa query để giảm RCU/WCU
- Thiết kế model object mapping đúng chuẩn

### Bảo mật
- Không hard-code secrets, sử dụng AWS Secrets Manager hoặc Parameter Store
- Validate tất cả đầu vào từ client
- Sanitize dữ liệu trước khi sử dụng trong các câu query
- Tuân thủ least privilege principle cho IAM roles
- Xử lý các lỗ hổng phổ biến (injection, XSS, CSRF)

## Quy trình làm việc

### Git
- Mỗi task nên được làm trên branch riêng
- Format branch name: `feature/BE-TASK-ID-short-description`
- Commit message rõ ràng, tham chiếu đến task ID
- Pull request cần có mô tả chi tiết những gì đã làm

### CI/CD
- Viết unit tests trước khi submit PR
- Đảm bảo tất cả các tests pass
- Fix tất cả các code smells và warnings từ linter
- Kiểm tra security vulnerabilities trước khi deploy

### Documentation
- Update README.md cho mỗi Lambda function
- Mô tả rõ API specs (nếu có)
- Ghi chú các decisions và trade-offs quan trọng
- Sử dụng diagrams khi cần thiết để mô tả flows phức tạp

## Tiêu chí hoàn thành

Task được xem là hoàn thành khi:

1. Code đáp ứng tất cả các yêu cầu trong task description
2. Đã pass tất cả unit tests
3. Code coverage đạt tối thiểu 80%
4. Không có lỗi bảo mật tiềm ẩn
5. Tuân thủ tất cả các quy tắc và tiêu chuẩn trong tài liệu này
6. Documentation đầy đủ
7. Đã được code review và approve

## Tài nguyên tham khảo

- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) 