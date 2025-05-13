**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý người dùng | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions quản lý người dùng, bao gồm các chức năng tạo, đọc, cập nhật và xóa thông tin người dùng trong hệ thống.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-ADM-001  
**Task Name:** Phát triển Lambda functions quản lý người dùng  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-AUTH-001 (Triển khai Lambda function đăng nhập)

**Các task phụ thuộc vào task này:** 
- BE-ADM-002 (Triển khai Lambda functions quản lý vai trò và phân quyền)

**Các API:**
- GET /api/v1/admin/users (API-ADM-001)
- POST /api/v1/admin/users (API-ADM-002)
- GET /api/v1/admin/users/{userId} (API-ADM-003)
- PUT /api/v1/admin/users/{userId} (API-ADM-004)
- DELETE /api/v1/admin/users/{userId} (API-ADM-005)

## Mô tả

Task này bao gồm việc phát triển các Lambda functions để quản lý người dùng trong hệ thống, chỉ dành cho người dùng có vai trò Admin. Các functions này sẽ cho phép quản trị viên tạo mới, xem, cập nhật thông tin và xóa người dùng. Chức năng này đặc biệt quan trọng cho việc quản lý quyền truy cập hệ thống và duy trì an ninh.

Các Lambda functions sẽ tương tác với DynamoDB để lưu trữ và truy xuất thông tin người dùng, đồng thời đảm bảo các quy tắc bảo mật như mã hóa mật khẩu và xác thực quyền truy cập trước khi thực hiện các thao tác CRUD.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách người dùng

- [ ] Triển khai Lambda function xử lý GET /api/v1/admin/users:
  - Location: src/admin/users.py
  - Triển khai handler function để lấy danh sách người dùng:
    ```python
    def get_users(event, context):
        """
        Lambda handler for getting user list
        """
        try:
            # Extract query parameters
            query_params = event.get('queryStringParameters', {}) or {}
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check user:read permission
            if not auth_context.has_permission('user:read'):
                return Response.forbidden("Permission denied: Requires user:read privilege")
            
            # Extract pagination and filter parameters
            page = int(query_params.get('page', 1))
            size = min(int(query_params.get('size', 20)), 100)  # Limit max page size
            search_query = query_params.get('query')
            status = query_params.get('status')
            
            # Create user service
            user_service = UserService()
            
            # Fetch users with filters
            result = user_service.get_users(
                page=page,
                size=size,
                search_query=search_query,
                status=status
            )
            
            return Response.success(result)
        except Exception as e:
            logger.error("Error getting users", exc=e)
            return handle_error(e)
    ```
  - Tạo user repository để truy vấn DynamoDB:
    - Location: src/repositories/user_repository.py
    - Implement phương thức get_users_with_pagination

### Phát triển Lambda function tạo người dùng mới

- [ ] Triển khai Lambda function xử lý POST /api/v1/admin/users:
  - Location: src/admin/users.py
  - Triển khai handler function để tạo người dùng mới:
    ```python
    def create_user(event, context):
        """
        Lambda handler for creating a new user
        """
        try:
            # Extract request body
            body = json.loads(event.get('body', '{}'))
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check user:create permission
            if not auth_context.has_permission('user:create'):
                return Response.forbidden("Permission denied: Requires user:create privilege")
            
            # Create user service
            user_service = UserService()
            
            # Validate required fields
            required_fields = ['username', 'email', 'full_name', 'role_id']
            for field in required_fields:
                if not body.get(field):
                    return Response.bad_request(f"Missing required field: {field}")
            
            # Create user
            new_user = user_service.create_user(body, created_by=auth_context.user_id)
            
            return Response.created(new_user)
        except DuplicateError as e:
            return Response.conflict(str(e))
        except Exception as e:
            logger.error("Error creating user", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong user repository để thêm người dùng:
    - Location: src/repositories/user_repository.py
    - Implement phương thức create_user

### Phát triển Lambda function lấy thông tin chi tiết người dùng

- [ ] Triển khai Lambda function xử lý GET /api/v1/admin/users/{userId}:
  - Location: src/admin/users.py
  - Triển khai handler function để lấy thông tin chi tiết người dùng:
    ```python
    def get_user_detail(event, context):
        """
        Lambda handler for getting user details
        """
        try:
            # Extract path parameters
            user_id = event.get('pathParameters', {}).get('userId')
            
            if not user_id:
                return Response.bad_request("Missing user ID")
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check user:read permission
            if not auth_context.has_permission('user:read'):
                return Response.forbidden("Permission denied: Requires user:read privilege")
            
            # Create user service
            user_service = UserService()
            
            # Get user details
            user = user_service.get_user_by_id(user_id)
            
            if not user:
                return Response.not_found(f"User not found with ID: {user_id}")
            
            return Response.success(user)
        except Exception as e:
            logger.error("Error getting user details", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong user repository để lấy thông tin người dùng:
    - Location: src/repositories/user_repository.py
    - Implement phương thức get_user_by_id

### Phát triển Lambda function cập nhật thông tin người dùng

- [ ] Triển khai Lambda function xử lý PUT /api/v1/admin/users/{userId}:
  - Location: src/admin/users.py
  - Triển khai handler function để cập nhật thông tin người dùng:
    ```python
    def update_user(event, context):
        """
        Lambda handler for updating user
        """
        try:
            # Extract path parameters
            user_id = event.get('pathParameters', {}).get('userId')
            
            if not user_id:
                return Response.bad_request("Missing user ID")
            
            # Extract request body
            body = json.loads(event.get('body', '{}'))
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check user:update permission
            if not auth_context.has_permission('user:update'):
                return Response.forbidden("Permission denied: Requires user:update privilege")
            
            # Create user service
            user_service = UserService()
            
            # Check if user exists
            existing_user = user_service.get_user_by_id(user_id)
            if not existing_user:
                return Response.not_found(f"User not found with ID: {user_id}")
            
            # Update user
            updated_user = user_service.update_user(user_id, body, updated_by=auth_context.user_id)
            
            return Response.success(updated_user)
        except DuplicateError as e:
            return Response.conflict(str(e))
        except Exception as e:
            logger.error("Error updating user", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong user repository để cập nhật thông tin người dùng:
    - Location: src/repositories/user_repository.py
    - Implement phương thức update_user

### Phát triển Lambda function xóa người dùng

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/admin/users/{userId}:
  - Location: src/admin/users.py
  - Triển khai handler function để xóa người dùng:
    ```python
    def delete_user(event, context):
        """
        Lambda handler for deleting user
        """
        try:
            # Extract path parameters
            user_id = event.get('pathParameters', {}).get('userId')
            
            if not user_id:
                return Response.bad_request("Missing user ID")
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check user:delete permission
            if not auth_context.has_permission('user:delete'):
                return Response.forbidden("Permission denied: Requires user:delete privilege")
            
            # Create user service
            user_service = UserService()
            
            # Check if user exists
            existing_user = user_service.get_user_by_id(user_id)
            if not existing_user:
                return Response.not_found(f"User not found with ID: {user_id}")
            
            # Prevent self-deletion
            if user_id == auth_context.user_id:
                return Response.bad_request("Cannot delete your own account")
            
            # Delete user
            user_service.delete_user(user_id)
            
            return Response.success({"message": "User deleted successfully"})
        except Exception as e:
            logger.error("Error deleting user", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong user repository để xóa người dùng:
    - Location: src/repositories/user_repository.py
    - Implement phương thức delete_user (soft delete)

### Phát triển User Service Layer

- [ ] Xây dựng User Service:
  - Location: src/services/user_service.py
  - Implement UserService class với các phương thức:
    - get_users: Lấy danh sách người dùng có phân trang
    - create_user: Tạo người dùng mới (mã hóa mật khẩu)
    - get_user_by_id: Lấy thông tin chi tiết người dùng
    - update_user: Cập nhật thông tin người dùng
    - delete_user: Xóa người dùng (soft delete)
    - reset_password: Đặt lại mật khẩu người dùng

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình các routes:
    - GET /api/v1/admin/users
    - POST /api/v1/admin/users
    - GET /api/v1/admin/users/{userId}
    - PUT /api/v1/admin/users/{userId}
    - DELETE /api/v1/admin/users/{userId}

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/admin/
  - Test case cho các handler functions trong users.py
  - Test case cho UserService
  - Test case cho UserRepository

### Tạo Documentation

- [ ] Viết tài liệu API swagger cho các endpoints:
  - GET /api/v1/admin/users
  - POST /api/v1/admin/users
  - GET /api/v1/admin/users/{userId}
  - PUT /api/v1/admin/users/{userId}
  - DELETE /api/v1/admin/users/{userId}

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để quản lý người dùng:

```python
# Lấy danh sách người dùng
import requests

def get_users(api_base_url, token, params=None):
    """
    Get list of users with pagination and filters
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{api_base_url}/api/v1/admin/users",
        headers=headers,
        params=params
    )
    
    return response.json()

# Tạo người dùng mới
def create_user(api_base_url, token, user_data):
    """
    Create a new user
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/admin/users",
        headers=headers,
        json=user_data
    )
    
    return response.json()

# Ví dụ tạo người dùng:
new_user = {
    'username': 'johndoe',
    'email': 'john.doe@example.com',
    'full_name': 'John Doe',
    'role_id': 'role_staff',
    'password': 'SecurePassword123'
}
result = create_user('https://api.example.com', 'admin_token', new_user)
```

## Tiêu chí hoàn thành

1. Tất cả Lambda functions được triển khai và hoạt động chính xác:
   - GET /api/v1/admin/users
   - POST /api/v1/admin/users
   - GET /api/v1/admin/users/{userId}
   - PUT /api/v1/admin/users/{userId}
   - DELETE /api/v1/admin/users/{userId}
2. Xác thực quyền truy cập được áp dụng đúng cho tất cả endpoints:
   - Quyền `user:read` cho các API GET
   - Quyền `user:create` cho API POST
   - Quyền `user:update` cho API PUT
   - Quyền `user:delete` cho API DELETE
3. Mật khẩu được mã hóa an toàn khi lưu trữ trong DynamoDB
4. Xử lý lỗi và validation đầy đủ, trả về mã lỗi phù hợp
5. Unit tests đạt coverage > 80%
6. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Cần đảm bảo mã hóa mật khẩu trước khi lưu vào DynamoDB sử dụng thuật toán mạnh (bcrypt)
- Thực hiện xóa mềm (soft delete) thay vì xóa cứng (hard delete) người dùng để duy trì tham chiếu lịch sử
- Kiểm tra kỹ các trường hợp đặc biệt như không thể xóa người dùng admin cuối cùng hoặc tự xóa tài khoản đang đăng nhập
- Cân nhắc sử dụng GSI1 (GSI1PK = "USER", GSI1SK = username) cho truy vấn theo tên người dùng
- Cân nhắc thêm chức năng reset mật khẩu và khóa/mở khóa tài khoản người dùng
- Theo permissions_definition.md, tất cả các quyền liên quan đến quản lý người dùng (user:read, user:create, user:update, user:delete) chỉ được gán cho vai trò Admin 