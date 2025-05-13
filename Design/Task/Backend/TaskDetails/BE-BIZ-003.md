**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task service authentication và authorization | -           | Draft     |
| 1.1     | 2025-05-14 | Chiến Trần Văn | Bổ sung chi tiết xử lý RBAC dựa trên permissions_definition.md | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa chi tiết công việc cần thực hiện để phát triển hệ thống xác thực (authentication) và phân quyền (authorization) trong ứng dụng, bao gồm JWT handling, role-based access control và tích hợp với API Gateway.

# Chi tiết Task: Phát triển service authentication và authorization

## Thông tin chung

**Task ID:** BE-BIZ-003  
**Task Name:** Phát triển service authentication và authorization  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** BE-INF-003, BE-INF-005, BE-CORE-001, BE-ADM-001, BE-ADM-002  
**Các task phụ thuộc vào task này:** BE-AUTH-001, BE-AUTH-002, BE-AUTH-003, BE-AUTH-004  
**Các API:** /api/v1/auth/login, /api/v1/auth/logout, /api/v1/auth/me, /api/v1/auth/refresh-token

## Mô tả

Task này tập trung vào việc phát triển một hệ thống xác thực và phân quyền bảo mật, linh hoạt cho ứng dụng. Các thành phần chính bao gồm:

1. **JWT Handler**: Tạo, xác thực và quản lý JSON Web Tokens để xác thực người dùng qua các API.

2. **Lambda Authorizer**: Triển khai Lambda Authorizer cho API Gateway để bảo vệ các endpoints, đảm bảo chỉ những người dùng được xác thực mới có thể truy cập.

3. **Role-based Access Control**: Phát triển hệ thống phân quyền dựa trên vai trò, cho phép quản lý chi tiết quyền truy cập vào các chức năng của hệ thống.

4. **Refresh Token Mechanism**: Triển khai cơ chế refresh token để cải thiện trải nghiệm người dùng và đảm bảo an toàn.

Hệ thống này sẽ cung cấp nền tảng bảo mật cho tất cả các APIs trong ứng dụng, đảm bảo rằng người dùng chỉ có thể truy cập dữ liệu và chức năng mà họ được phép.

## Chi tiết xử lý RBAC (Role-Based Access Control)

Dựa trên tài liệu định nghĩa quyền trong hệ thống, RBAC sẽ được triển khai như sau:

### 1. Cấu trúc Phân quyền

Hệ thống sẽ tuân theo mô hình 3 lớp:
- **Vai trò (Roles)**: Nhóm quyền gắn với loại người dùng (Admin, Division Manager, Leader, Sales, Employee)
- **Quyền (Permissions)**: Đơn vị quyền nhỏ nhất, định dạng `resource:action[:scope]`
- **Phạm vi (Scopes)**: Giới hạn phạm vi của quyền (own, team, all, basic, assigned)

### 2. Triển khai cấu trúc dữ liệu

- [ ] Xây dựng cấu trúc Permissions trong DynamoDB:
  - Location: src/common/models/auth/permission.py
  - Implement model Permission với các thuộc tính: id, name, description, created_at, updated_at
  - Sử dụng quy tắc đặt tên theo cấu trúc `resource:action[:scope]`
  - Map với cấu trúc lưu trữ trong DynamoDB (PERMISSION entity)

- [ ] Xây dựng cấu trúc Roles trong DynamoDB:
  - Location: src/common/models/auth/role.py
  - Implement model Role với các thuộc tính: id, name, description, permissions (List), created_at, updated_at
  - Map với cấu trúc lưu trữ trong DynamoDB (ROLE entity)
  - Thiết lập các vai trò mặc định: Admin, Division Manager, Leader, Sales, Employee

- [ ] Xây dựng quan hệ User-Role:
  - Location: src/common/models/auth/user_role.py
  - Implement model UserRole để quản lý quan hệ nhiều-nhiều
  - Map với cấu trúc lưu trữ trong DynamoDB (USER_ROLE entity)

### 3. Triển khai Permission Manager

- [ ] Mở rộng Permission Manager để hỗ trợ đầy đủ cấu trúc quyền:
  - Location: src/common/services/auth/permission_manager.py
  - Cập nhật phương thức `check_permission` để xử lý scope:
    ```python
    def check_permission(self, user_id, permission, resource_id=None):
        """
        Kiểm tra người dùng có quyền cụ thể hay không
        
        Args:
            user_id: ID của người dùng
            permission: Quyền cần kiểm tra (resource:action[:scope])
            resource_id: ID của tài nguyên (optional)
            
        Returns:
            bool: True nếu có quyền, False nếu không
        """
        # Phân tách quyền thành resource, action, scope
        parts = permission.split(':')
        resource = parts[0]
        action = parts[1]
        required_scope = parts[2] if len(parts) > 2 else None
        
        # Lấy quyền của người dùng
        user_permissions = self.get_user_permissions(user_id)
        
        # Kiểm tra quyền chính xác
        if permission in user_permissions:
            return True
            
        # Kiểm tra quyền không có scope
        if required_scope and f"{resource}:{action}" in user_permissions:
            return True
            
        # Kiểm tra quyền với scope rộng hơn
        if required_scope:
            if required_scope == 'team' and f"{resource}:{action}:all" in user_permissions:
                return True
            if required_scope == 'own' and (
                f"{resource}:{action}:all" in user_permissions or 
                f"{resource}:{action}:team" in user_permissions
            ):
                return True
            if required_scope == 'assigned' and f"{resource}:{action}:all" in user_permissions:
                return True
        
        # Kiểm tra quyền truy cập dữ liệu dựa trên resource_id
        if resource_id:
            return self._check_resource_access(user_id, resource, action, resource_id)
            
        return False
    ```

  - Thêm phương thức kiểm tra phạm vi dữ liệu:
    ```python
    def _check_resource_access(self, user_id, resource, action, resource_id):
        """
        Kiểm tra người dùng có quyền truy cập dữ liệu cụ thể không
        
        Args:
            user_id: ID của người dùng
            resource: Loại tài nguyên
            action: Hành động
            resource_id: ID của tài nguyên
            
        Returns:
            bool: True nếu có quyền, False nếu không
        """
        # Lấy thông tin người dùng
        user_info = self._get_user_info(user_id)
        
        # Lấy thông tin tài nguyên
        resource_info = self._get_resource_info(resource, resource_id)
        
        if not resource_info:
            return False
            
        # Admin luôn có quyền
        if user_info.role == 'Admin':
            return True
            
        # Division Manager có quyền truy cập dữ liệu tất cả
        if user_info.role == 'Division Manager':
            return True
            
        # Leader chỉ có quyền truy cập dữ liệu trong team
        if user_info.role == 'Leader' and resource_info.get('team_id') == user_info.team_id:
            return True
            
        # Nhân viên chỉ có quyền truy cập dữ liệu của mình
        if resource_info.get('owner_id') == user_id or resource_info.get('assigned_to_id') == user_id:
            return True
            
        return False
    ```

### 4. Triển khai Role Manager

- [ ] Mở rộng Role Manager để quản lý vai trò theo yêu cầu:
  - Location: src/common/services/auth/role_manager.py
  - Implement phương thức lấy thông tin vai trò:
    ```python
    def get_role_details(self, role_name):
        """
        Lấy thông tin chi tiết về vai trò
        
        Args:
            role_name: Tên vai trò
            
        Returns:
            dict: Thông tin vai trò bao gồm permissions
        """
        # Truy vấn DynamoDB để lấy thông tin vai trò
        response = self.dynamodb.query(
            TableName=self.table_name,
            IndexName='GSI1',
            KeyConditionExpression='GSI1PK = :pk AND GSI1SK = :sk',
            ExpressionAttributeValues={
                ':pk': {'S': 'ROLE'},
                ':sk': {'S': role_name}
            }
        )
        
        if 'Items' in response and response['Items']:
            item = response['Items'][0]
            return {
                'id': item['id']['S'],
                'name': item['name']['S'],
                'description': item.get('description', {}).get('S', ''),
                'permissions': item.get('permissions', {}).get('L', [])
            }
        
        return None
    ```

  - Implement phương thức gán quyền cho vai trò:
    ```python
    def assign_permission_to_role(self, role_id, permission_id):
        """
        Gán quyền cho vai trò
        
        Args:
            role_id: ID của vai trò
            permission_id: ID của quyền
            
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            # Thêm permission vào danh sách permissions của role
            self.dynamodb.update_item(
                TableName=self.table_name,
                Key={
                    'PK': {'S': f'ROLE#{role_id}'},
                    'SK': {'S': f'METADATA#{role_id}'}
                },
                UpdateExpression='ADD permissions :p',
                ExpressionAttributeValues={
                    ':p': {'SS': [permission_id]}
                }
            )
            return True
        except Exception as e:
            logger.error(f"Error assigning permission to role: {str(e)}")
            return False
    ```

### 5. Triển khai Access Control List (ACL)

- [ ] Xây dựng Access Control List cho resource-level access:
  - Location: src/common/services/auth/acl.py
  - Implement các phương thức quản lý ACL:
    ```python
    def can_access(self, user_id, resource_type, resource_id, action):
        """
        Kiểm tra người dùng có quyền thực hiện hành động với tài nguyên cụ thể
        
        Args:
            user_id: ID của người dùng
            resource_type: Loại tài nguyên (employee, opportunity, contract...)
            resource_id: ID của tài nguyên
            action: Hành động (read, create, update, delete)
            
        Returns:
            bool: True nếu có quyền, False nếu không
        """
        # Lấy thông tin người dùng
        user_info = self._get_user_info(user_id)
        
        # Lấy thông tin resource
        resource_info = self._get_resource_info(resource_type, resource_id)
        
        if not resource_info:
            return False
        
        # Xác định phạm vi truy cập dữ liệu
        access_level = self._determine_access_level(user_info, resource_info)
        
        # Dựa vào phạm vi để kiểm tra quyền
        permission_to_check = f"{resource_type}:{action}"
        
        # Kiểm tra quyền theo phạm vi
        if access_level == 'all':
            return self.permission_manager.check_permission(user_id, f"{permission_to_check}:all") or \
                   self.permission_manager.check_permission(user_id, permission_to_check)
        elif access_level == 'team':
            return self.permission_manager.check_permission(user_id, f"{permission_to_check}:team") or \
                   self.permission_manager.check_permission(user_id, f"{permission_to_check}:all") or \
                   self.permission_manager.check_permission(user_id, permission_to_check)
        elif access_level == 'own':
            return self.permission_manager.check_permission(user_id, f"{permission_to_check}:own") or \
                   self.permission_manager.check_permission(user_id, f"{permission_to_check}:team") or \
                   self.permission_manager.check_permission(user_id, f"{permission_to_check}:all") or \
                   self.permission_manager.check_permission(user_id, permission_to_check)
        elif access_level == 'assigned':
            return self.permission_manager.check_permission(user_id, f"{permission_to_check}:assigned") or \
                   self.permission_manager.check_permission(user_id, f"{permission_to_check}:all") or \
                   self.permission_manager.check_permission(user_id, permission_to_check)
        
        return False
    ```

  - Implement phương thức xác định phạm vi truy cập:
    ```python
    def _determine_access_level(self, user_info, resource_info):
        """
        Xác định phạm vi truy cập dữ liệu dựa trên user và resource
        
        Args:
            user_info: Thông tin người dùng
            resource_info: Thông tin tài nguyên
            
        Returns:
            str: Phạm vi truy cập ('all', 'team', 'own', 'assigned', 'none')
        """
        # Lấy thông tin role từ database
        role_manager = RoleManager()
        admin_roles = role_manager.get_roles_with_permission('*:*')  # Lấy role có quyền admin
        division_manager_roles = role_manager.get_roles_with_permission('*:*:all')  # Lấy role có quyền division manager
        
        # Admin hoặc Division Manager có quyền truy cập tất cả
        if user_info.role in admin_roles or user_info.role in division_manager_roles:
            return 'all'
        
        # Kiểm tra phạm vi team dựa trên quyền từ DB
        team_level_roles = role_manager.get_roles_with_permission_pattern('*:*:team')
        if user_info.role in team_level_roles:
            if resource_info.get('team_id') == user_info.team_id:
                return 'team'
            
            # Nếu resource được gán cho user
            if resource_info.get('assigned_to_id') == user_info.id:
                return 'assigned'
        
        # Kiểm tra Sales role từ DB
        sales_roles = role_manager.get_roles_with_permission_pattern('opportunity:*:own')
        if user_info.role in sales_roles:
            if resource_info.get('created_by') == user_info.id or \
               resource_info.get('owner_id') == user_info.id:
                return 'own'
        
        # Nhân viên chỉ truy cập dữ liệu của mình
        if resource_info.get('owner_id') == user_info.id or \
           resource_info.get('user_id') == user_info.id or \
           resource_info.get('employee_id') == user_info.id:
            return 'own'
        
        return 'none'
    ```

  - Thêm phương thức hỗ trợ để lấy thông tin role từ database:
    ```python
    class RoleManager:
        # ... existing code ...
        
        def get_roles_with_permission(self, permission):
            """
            Lấy danh sách các role có permission chỉ định
            
            Args:
                permission: Permission cần kiểm tra
                
            Returns:
                list: Danh sách role names
            """
            # Truy vấn DynamoDB để lấy các roles có permission
            response = self.dynamodb.scan(
                TableName=self.table_name,
                FilterExpression='contains(permissions, :perm)',
                ExpressionAttributeValues={
                    ':perm': {'S': permission}
                }
            )
            
            if 'Items' in response:
                return [item['name']['S'] for item in response['Items']]
            return []
        
        def get_roles_with_permission_pattern(self, pattern):
            """
            Lấy danh sách các role có permission khớp với pattern
            
            Args:
                pattern: Pattern của permission (có thể có wildcards *)
                
            Returns:
                list: Danh sách role names
            """
            # Chuyển pattern thành regex
            import re
            regex_pattern = pattern.replace('*', '.*')
            
            # Truy vấn tất cả roles
            response = self.dynamodb.scan(
                TableName=self.table_name,
                IndexName='GSI1',
                FilterExpression='begins_with(GSI1PK, :pk)',
                ExpressionAttributeValues={
                    ':pk': {'S': 'ROLE'}
                }
            )
            
            if 'Items' not in response:
                return []
            
            # Lọc roles có permissions khớp với pattern
            result = []
            for item in response['Items']:
                if 'permissions' not in item:
                    continue
                
                permissions = item.get('permissions', {}).get('SS', [])
                for perm in permissions:
                    if re.match(regex_pattern, perm):
                        result.append(item['name']['S'])
                        break
            
            return result
    ```

### 6. Triển khai JWT Payload với Permission

- [ ] Mở rộng JWT Payload để bao gồm thông tin quyền:
  - Location: src/common/services/auth/jwt_service.py
  - Cập nhật phương thức tạo token:
    ```python
    def generate_token(self, user_id, expiry=3600):
        """
        Tạo JWT access token với thông tin người dùng và quyền
        
        Args:
            user_id: ID của người dùng
            expiry: Thời gian hết hạn (giây)
            
        Returns:
            str: JWT token
        """
        # Lấy thông tin người dùng
        user_info = self._get_user_info(user_id)
        if not user_info:
            raise ValueError(f"User not found: {user_id}")
        
        # Lấy quyền của người dùng
        user_permissions = self.permission_manager.get_user_permissions(user_id)
        
        # Lấy roles của người dùng
        user_roles = self.role_manager.get_user_roles(user_id)
        
        # Tạo payload cho token
        now = int(time.time())
        payload = {
            'sub': user_id,
            'name': user_info.full_name,
            'role': user_roles[0] if user_roles else None,  # Vai trò chính
            'teamId': user_info.team_id if hasattr(user_info, 'team_id') else None,
            'permissions': user_permissions,  # Danh sách quyền
            'iat': now,
            'exp': now + expiry
        }
        
        # Ký JWT
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    ```

### 7. Triển khai API Validation dựa trên Permission

- [ ] Xây dựng decorator để kiểm tra quyền trong API:
  - Location: src/common/decorators/permission.py
  - Implement decorator `require_permission`:
    ```python
    def require_permission(permission):
        """
        Decorator kiểm tra quyền truy cập API
        
        Args:
            permission: Quyền cần kiểm tra (resource:action[:scope])
            
        Returns:
            Decorator function
        """
        def decorator(handler):
            @functools.wraps(handler)
            def wrapper(event, context):
                # Lấy và xác thực token từ request
                token = _extract_token_from_event(event)
                if not token:
                    return _create_error_response(401, "E1001", "Unauthorized: Missing token")
                
                try:
                    # Xác thực token
                    jwt_service = JWTService()
                    is_valid, token_data = jwt_service.validate_token(token)
                    
                    if not is_valid:
                        return _create_error_response(401, "E1000", "Unauthorized: Invalid token")
                    
                    # Kiểm tra quyền
                    user_id = token_data.get('sub')
                    user_permissions = token_data.get('permissions', [])
                    
                    # Kiểm tra quyền từ token
                    if not _has_permission(permission, user_permissions):
                        return _create_error_response(403, "E1002", f"Forbidden: Missing required permission: {permission}")
                    
                    # Gắn thông tin user vào event để handler sử dụng
                    event['requestContext']['authorizer'] = {
                        'userId': user_id,
                        'permissions': user_permissions,
                        'role': token_data.get('role'),
                        'teamId': token_data.get('teamId')
                    }
                    
                    # Gọi handler gốc
                    return handler(event, context)
                except Exception as e:
                    logger.error(f"Error in permission check: {str(e)}")
                    return _create_error_response(500, "E6000", "Internal server error")
            
            return wrapper
        
        return decorator
    ```

  - Implement helper function để kiểm tra quyền:
    ```python
    def _has_permission(required_permission, user_permissions):
        """
        Kiểm tra người dùng có quyền cụ thể không
        
        Args:
            required_permission: Quyền cần kiểm tra
            user_permissions: Danh sách quyền của người dùng
            
        Returns:
            bool: True nếu có quyền, False nếu không
        """
        # Phân tách quyền thành resource, action, scope
        parts = required_permission.split(':')
        resource = parts[0]
        action = parts[1]
        required_scope = parts[2] if len(parts) > 2 else None
        
        # Kiểm tra quyền chính xác
        if required_permission in user_permissions:
            return True
            
        # Kiểm tra quyền không có scope
        if required_scope and f"{resource}:{action}" in user_permissions:
            return True
            
        # Kiểm tra quyền với scope rộng hơn
        if required_scope:
            if required_scope == 'team' and f"{resource}:{action}:all" in user_permissions:
                return True
            if required_scope == 'own' and (
                f"{resource}:{action}:all" in user_permissions or 
                f"{resource}:{action}:team" in user_permissions
            ):
                return True
            if required_scope == 'assigned' and f"{resource}:{action}:all" in user_permissions:
                return True
        
        return False
    ```

### 8. Tích hợp với Lambda Functions

- [ ] Tích hợp với Lambda Function cho Login API:
  - Location: src/functions/auth/login.py
  - Bổ sung logic để trả về token với đầy đủ thông tin quyền:
    ```python
    def handler(event, context):
        try:
            # Parse request body
            body = json.loads(event.get('body', '{}'))
            username = body.get('username')
            password = body.get('password')
            remember_me = body.get('remember_me', False)
            
            if not username or not password:
                return _create_error_response(400, "E2001", "Thiếu tham số bắt buộc")
            
            # Authenticate user
            auth_service = AuthenticationService()
            login_result = auth_service.login(username, password)
            
            if not login_result.success:
                return _create_error_response(401, "E1005", "Sai tên đăng nhập hoặc mật khẩu")
            
            # Kiểm tra tài khoản bị khóa
            if not login_result.user_active:
                return _create_error_response(401, "E1004", "Tài khoản bị khóa")
            
            # Lấy thông tin quyền
            permission_manager = PermissionManager()
            permissions = permission_manager.get_user_permissions(login_result.user_id)
            
            # Lấy thông tin role
            role_manager = RoleManager()
            roles = role_manager.get_user_roles(login_result.user_id)
            role = roles[0] if roles else None
            
            # Xác định thời gian hết hạn token
            expires_in = 86400 if remember_me else 3600  # 24h nếu remember_me, ngược lại 1h
            
            # Create response with tokens and user info
            response = {
                "status": "success",
                "code": 200,
                "data": {
                    "token": login_result.access_token,
                    "token_type": "Bearer",
                    "expires_in": expires_in,
                    "refresh_token": login_result.refresh_token,
                    "user": {
                        "id": login_result.user_id,
                        "username": login_result.username,
                        "email": login_result.email,
                        "fullname": login_result.full_name,
                        "role": role,
                        "permissions": permissions
                    }
                }
            }
            
            return {
                'statusCode': 200,
                'body': json.dumps(response),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        except Exception as e:
            logger.error(f"Error in login handler: {str(e)}")
            return _create_error_response(500, "E6000", "Internal server error")
    ```

- [ ] Tích hợp với Lambda Function cho Get Current User API:
  - Location: src/functions/auth/me.py
  - Sử dụng decorator require_permission:
    ```python
    from common.decorators.permission import require_permission

    @require_permission('user:read:own')
    def handler(event, context):
        try:
            # Lấy thông tin user từ context
            authorizer = event.get('requestContext', {}).get('authorizer', {})
            user_id = authorizer.get('userId')
            
            if not user_id:
                return _create_error_response(401, "E1001", "Unauthorized")
            
            # Lấy thông tin chi tiết user
            user_service = UserService()
            user_info = user_service.get_user_by_id(user_id)
            
            if not user_info:
                return _create_error_response(404, "E3005", "User not found")
            
            # Lấy quyền của user
            permission_manager = PermissionManager()
            permissions = permission_manager.get_user_permissions(user_id)
            
            # Lấy role của user
            role_manager = RoleManager()
            roles = role_manager.get_user_roles(user_id)
            role_info = role_manager.get_role_details(roles[0]) if roles else None
            
            # Chuẩn bị response
            response = {
                "status": "success",
                "code": 200,
                "data": {
                    "id": user_info.id,
                    "username": user_info.username,
                    "email": user_info.email,
                    "fullName": user_info.full_name,
                    "avatar": user_info.profile_picture_url,
                    "role": {
                        "id": role_info.get('id') if role_info else None,
                        "name": role_info.get('name') if role_info else None
                    },
                    "permissions": permissions,
                    "lastLogin": user_info.last_login_at
                }
            }
            
            return {
                'statusCode': 200,
                'body': json.dumps(response),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        except Exception as e:
            logger.error(f"Error in get current user handler: {str(e)}")
            return _create_error_response(500, "E6000", "Internal server error")
    ```

- [ ] Implement Refresh Token Lambda:
  - Location: src/functions/auth/refresh_token.py
  - Tạo Lambda function xử lý refresh token request
  - Xác thực refresh token và tạo access token mới
  - Xử lý các trường hợp lỗi và bảo mật

### Phát triển Unit Tests

- [ ] Viết unit tests cho JWT Service:
  - Location: tests/common/services/auth/test_jwt_service.py
  - Test tạo, xác thực và giải mã token
  - Test xử lý các trường hợp lỗi và token hết hạn
  - Test signature verification

- [ ] Viết unit tests cho Lambda Authorizer:
  - Location: tests/functions/auth/test_authorizer.py
  - Test xác thực request với các trường hợp khác nhau
  - Test tạo policy document
  - Test xử lý lỗi

- [ ] Viết unit tests cho RBAC:
  - Location: tests/common/services/auth/test_permission_manager.py, test_role_manager.py
  - Test kiểm tra quyền và vai trò
  - Test phân quyền phức tạp
  - Test hiệu suất với nhiều quyền/vai trò

- [ ] Viết unit tests cho Authentication Service:
  - Location: tests/common/services/auth/test_auth_service.py
  - Test login, logout, refresh token
  - Test xử lý lỗi và bảo mật
  - Test session management

### Tích hợp và Documentation

- [ ] Tích hợp với API Gateway:
  - Cấu hình Authorizer trong API Gateway
  - Áp dụng Authorizer cho các endpoints
  - Test end-to-end authentication flow

- [ ] Viết tài liệu API và hướng dẫn sử dụng:
  - Tạo API documentation cho authentication/authorization endpoints
  - Viết hướng dẫn tích hợp cho frontend
  - Viết hướng dẫn bảo mật và phân quyền

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng JWT Service:

```python
# Sử dụng JWT Service
from common.services.auth.jwt_service import JWTService

# Khởi tạo service
jwt_service = JWTService()

# Tạo token cho người dùng
user_data = {
    "user_id": "USER-123",
    "username": "john.doe",
    "roles": ["employee", "manager"],
    "permissions": ["read:employees", "write:employees"]
}

# Tạo JWT access token
access_token = jwt_service.generate_token(
    user_id="USER-123",
    user_data=user_data,
    expiry=3600  # 1 giờ
)

# Xác thực token
try:
    is_valid, token_data = jwt_service.validate_token(access_token)
    if is_valid:
        print(f"Token valid for user: {token_data['user_id']}")
    else:
        print("Token invalid")
except Exception as e:
    print(f"Error validating token: {str(e)}")
```

Ví dụ về cách sử dụng Permission Manager:

```python
# Sử dụng Permission Manager
from common.services.auth.permission_manager import PermissionManager

# Khởi tạo service
permission_manager = PermissionManager()

# Kiểm tra quyền của người dùng
user_id = "USER-123"
permission = "read:employees"
resource_id = "EMP-456"  # Optional, có thể là None

has_permission = permission_manager.check_permission(user_id, permission, resource_id)

if has_permission:
    print(f"User {user_id} has permission {permission} for resource {resource_id}")
else:
    print(f"User {user_id} does not have permission {permission} for resource {resource_id}")

# Lấy tất cả quyền của người dùng
user_permissions = permission_manager.get_user_permissions(user_id)
print(f"User permissions: {user_permissions}")
```

## Tiêu chí hoàn thành

1. JWT handling được triển khai đầy đủ với các cơ chế bảo mật tiêu chuẩn
2. Lambda Authorizer hoạt động chính xác và được tích hợp với API Gateway
3. Hệ thống RBAC linh hoạt, có khả năng phân quyền chi tiết đến cấp độ tài nguyên
4. Cơ chế refresh token hoạt động ổn định và bảo mật
5. Các API authentication hoạt động đúng và xử lý lỗi hiệu quả
6. Unit tests đạt coverage ít nhất 90% cho tất cả các services
7. Tài liệu API và hướng dẫn tích hợp đầy đủ

## Ước tính thời gian

- 8-10 ngày làm việc

## Ghi chú

- Sử dụng các chuẩn bảo mật tốt nhất cho JWT, bao gồm token expiration, chữ ký, và validation
- Cần đặc biệt chú ý đến các vấn đề bảo mật như token theft, CSRF, và XSS
- Thiết kế cấu trúc permission sao cho dễ mở rộng trong tương lai và tương thích với complex access controls
- Lưu ý về hiệu suất của các phương thức kiểm tra quyền, đặc biệt là khi hệ thống có nhiều người dùng
- Đảm bảo logging đầy đủ để theo dõi và phát hiện các vấn đề bảo mật
- Cân nhắc triển khai rate limiting để ngăn chặn brute force attacks 