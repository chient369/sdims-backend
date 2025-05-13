**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý vai trò và phân quyền | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý vai trò và phân quyền, bao gồm chức năng tạo, cập nhật, xóa vai trò và gán/gỡ quyền cho vai trò.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-ADM-002  
**Task Name:** Triển khai Lambda functions quản lý vai trò và phân quyền  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-AUTH-001 (Triển khai Lambda function đăng nhập)

**Các task phụ thuộc vào task này:** 
- BE-AUTH-003 (Triển khai Lambda function lấy thông tin người dùng hiện tại - vì cần thông tin về quyền)

**Các API:**
- GET /api/v1/admin/roles (API-ADM-006)
- POST /api/v1/admin/roles (API-ADM-007)
- PUT /api/v1/admin/roles/{roleId} (API-ADM-008)
- DELETE /api/v1/admin/roles/{roleId} (API-ADM-009)
- GET /api/v1/admin/permissions (API-ADM-010)

## Mô tả

Task này bao gồm việc phát triển các Lambda functions để quản lý vai trò và phân quyền trong hệ thống. Đây là một phần quan trọng của module quản trị hệ thống, cho phép quản trị viên tạo và quản lý các vai trò (roles) với các quyền (permissions) cụ thể, đảm bảo kiểm soát truy cập chặt chẽ đến các tính năng của hệ thống.

Các functions này sẽ tương tác với DynamoDB để lưu trữ thông tin về vai trò và quyền, cũng như quản lý mối quan hệ giữa vai trò và quyền. Functions này cũng sẽ hỗ trợ việc gán/gỡ quyền khỏi vai trò và đảm bảo tính nhất quán trong hệ thống phân quyền.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách vai trò

- [ ] Triển khai Lambda function xử lý GET /api/v1/admin/roles:
  - Location: src/admin/roles.py
  - Triển khai handler function để lấy danh sách vai trò:
    ```python
    def get_roles(event, context):
        """
        Lambda handler for getting roles list
        """
        try:
            # Extract query parameters
            query_params = event.get('queryStringParameters', {}) or {}
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check role:read permission
            if not auth_context.has_permission('role:read'):
                return Response.forbidden("Permission denied: Requires role:read privilege")
            
            # Extract pagination parameters
            page = int(query_params.get('page', 1))
            size = min(int(query_params.get('size', 20)), 100)  # Limit max page size
            
            # Create role service
            role_service = RoleService()
            
            # Fetch roles with pagination
            result = role_service.get_roles(page=page, size=size)
            
            return Response.success(result)
        except Exception as e:
            logger.error("Error getting roles", exc=e)
            return handle_error(e)
    ```
  - Tạo role repository để truy vấn DynamoDB:
    - Location: src/repositories/role_repository.py
    - Implement phương thức get_roles_with_pagination

### Phát triển Lambda function tạo vai trò mới

- [ ] Triển khai Lambda function xử lý POST /api/v1/admin/roles:
  - Location: src/admin/roles.py
  - Triển khai handler function để tạo vai trò mới:
    ```python
    def create_role(event, context):
        """
        Lambda handler for creating a new role
        """
        try:
            # Extract request body
            body = json.loads(event.get('body', '{}'))
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check role:create permission
            if not auth_context.has_permission('role:create'):
                return Response.forbidden("Permission denied: Requires role:create privilege")
            
            # Validate required fields
            required_fields = ['name', 'description']
            for field in required_fields:
                if not body.get(field):
                    return Response.bad_request(f"Missing required field: {field}")
            
            # Create role service
            role_service = RoleService()
            
            # Create role
            new_role = role_service.create_role(
                name=body.get('name'),
                description=body.get('description'),
                permissions=body.get('permissions', []),
                created_by=auth_context.user_id
            )
            
            return Response.created(new_role)
        except DuplicateError as e:
            return Response.conflict(str(e))
        except Exception as e:
            logger.error("Error creating role", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong role repository để thêm vai trò:
    - Location: src/repositories/role_repository.py
    - Implement phương thức create_role

### Phát triển Lambda function cập nhật vai trò

- [ ] Triển khai Lambda function xử lý PUT /api/v1/admin/roles/{roleId}:
  - Location: src/admin/roles.py
  - Triển khai handler function để cập nhật vai trò:
    ```python
    def update_role(event, context):
        """
        Lambda handler for updating a role
        """
        try:
            # Extract path parameters
            role_id = event.get('pathParameters', {}).get('roleId')
            
            if not role_id:
                return Response.bad_request("Missing role ID")
            
            # Extract request body
            body = json.loads(event.get('body', '{}'))
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check role:update permission
            if not auth_context.has_permission('role:update'):
                return Response.forbidden("Permission denied: Requires role:update privilege")
            
            # Create role service
            role_service = RoleService()
            
            # Check if role exists
            existing_role = role_service.get_role_by_id(role_id)
            if not existing_role:
                return Response.not_found(f"Role not found with ID: {role_id}")
            
            # Prevent updating built-in roles (like 'admin')
            if existing_role.get('is_system_role', False):
                return Response.forbidden("Cannot modify system-defined roles")
            
            # Update role
            updated_role = role_service.update_role(
                role_id=role_id,
                name=body.get('name'),
                description=body.get('description'),
                permissions=body.get('permissions'),
                updated_by=auth_context.user_id
            )
            
            return Response.success(updated_role)
        except DuplicateError as e:
            return Response.conflict(str(e))
        except Exception as e:
            logger.error("Error updating role", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong role repository để cập nhật vai trò:
    - Location: src/repositories/role_repository.py
    - Implement phương thức update_role

### Phát triển Lambda function xóa vai trò

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/admin/roles/{roleId}:
  - Location: src/admin/roles.py
  - Triển khai handler function để xóa vai trò:
    ```python
    def delete_role(event, context):
        """
        Lambda handler for deleting a role
        """
        try:
            # Extract path parameters
            role_id = event.get('pathParameters', {}).get('roleId')
            
            if not role_id:
                return Response.bad_request("Missing role ID")
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check role:delete permission
            if not auth_context.has_permission('role:delete'):
                return Response.forbidden("Permission denied: Requires role:delete privilege")
            
            # Create role service
            role_service = RoleService()
            
            # Check if role exists
            existing_role = role_service.get_role_by_id(role_id)
            if not existing_role:
                return Response.not_found(f"Role not found with ID: {role_id}")
            
            # Prevent deleting built-in roles (like 'admin')
            if existing_role.get('is_system_role', False):
                return Response.forbidden("Cannot delete system-defined roles")
            
            # Check if role is assigned to users
            if role_service.is_role_assigned_to_users(role_id):
                return Response.conflict("Cannot delete role as it is assigned to one or more users")
            
            # Delete role
            role_service.delete_role(role_id)
            
            return Response.success({"message": "Role deleted successfully"})
        except Exception as e:
            logger.error("Error deleting role", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong role repository để xóa vai trò:
    - Location: src/repositories/role_repository.py
    - Implement phương thức delete_role

### Phát triển Lambda function lấy danh sách quyền

- [ ] Triển khai Lambda function xử lý GET /api/v1/admin/permissions:
  - Location: src/admin/roles.py
  - Triển khai handler function để lấy danh sách quyền:
    ```python
    def get_permissions(event, context):
        """
        Lambda handler for getting system permissions list
        """
        try:
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check permission:read permission
            if not auth_context.has_permission('permission:read'):
                return Response.forbidden("Permission denied: Requires permission:read privilege")
            
            # Create role service
            role_service = RoleService()
            
            # Fetch all system permissions
            permissions = role_service.get_all_permissions()
            
            return Response.success({
                "permissions": permissions
            })
        except Exception as e:
            logger.error("Error getting permissions", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong role repository để lấy danh sách quyền:
    - Location: src/repositories/role_repository.py
    - Implement phương thức get_all_permissions

### Phát triển Role Service Layer

- [ ] Xây dựng Role Service:
  - Location: src/services/role_service.py
  - Implement RoleService class với các phương thức:
    - get_roles: Lấy danh sách vai trò có phân trang
    - get_role_by_id: Lấy thông tin vai trò theo ID
    - create_role: Tạo vai trò mới
    - update_role: Cập nhật thông tin vai trò
    - delete_role: Xóa vai trò
    - is_role_assigned_to_users: Kiểm tra vai trò có được gán cho người dùng không
    - get_all_permissions: Lấy danh sách tất cả quyền trong hệ thống

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình các routes:
    - GET /api/v1/admin/roles
    - POST /api/v1/admin/roles
    - PUT /api/v1/admin/roles/{roleId}
    - DELETE /api/v1/admin/roles/{roleId}
    - GET /api/v1/admin/permissions

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/admin/
  - Test case cho các handler functions trong roles.py
  - Test case cho RoleService
  - Test case cho RoleRepository

### Tạo Documentation

- [ ] Viết tài liệu API swagger cho các endpoints:
  - GET /api/v1/admin/roles
  - POST /api/v1/admin/roles
  - PUT /api/v1/admin/roles/{roleId}
  - DELETE /api/v1/admin/roles/{roleId}
  - GET /api/v1/admin/permissions

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để quản lý vai trò và phân quyền:

```python
# Lấy danh sách vai trò
import requests

def get_roles(api_base_url, token, params=None):
    """
    Get list of roles with pagination
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{api_base_url}/api/v1/admin/roles",
        headers=headers,
        params=params
    )
    
    return response.json()

# Tạo vai trò mới
def create_role(api_base_url, token, role_data):
    """
    Create a new role
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/admin/roles",
        headers=headers,
        json=role_data
    )
    
    return response.json()

# Cập nhật vai trò
def update_role(api_base_url, token, role_id, role_data):
    """
    Update an existing role
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.put(
        f"{api_base_url}/api/v1/admin/roles/{role_id}",
        headers=headers,
        json=role_data
    )
    
    return response.json()

# Lấy danh sách quyền
def get_permissions(api_base_url, token):
    """
    Get list of system permissions
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{api_base_url}/api/v1/admin/permissions",
        headers=headers
    )
    
    return response.json()

# Ví dụ tạo vai trò:
new_role = {
    'name': 'Project Manager',
    'description': 'Manages projects and team allocations',
    'permissions': [
        'employee:read',
        'employee:update:status',
        'project:read',
        'project:create',
        'project:update',
        'project:delete',
        'opportunity:read',
        'contract:read'
    ]
}
result = create_role('https://api.example.com', 'admin_token', new_role)
```

## Tiêu chí hoàn thành

1. Tất cả Lambda functions được triển khai và hoạt động chính xác:
   - GET /api/v1/admin/roles
   - POST /api/v1/admin/roles
   - PUT /api/v1/admin/roles/{roleId}
   - DELETE /api/v1/admin/roles/{roleId}
   - GET /api/v1/admin/permissions
2. Xác thực quyền truy cập được áp dụng đúng cho tất cả endpoints:
   - Quyền `role:read` cho API GET /api/v1/admin/roles
   - Quyền `role:create` cho API POST /api/v1/admin/roles
   - Quyền `role:update` cho API PUT /api/v1/admin/roles/{roleId}
   - Quyền `role:delete` cho API DELETE /api/v1/admin/roles/{roleId}
   - Quyền `permission:read` cho API GET /api/v1/admin/permissions
3. Hệ thống xử lý đúng các trường hợp đặc biệt (vai trò hệ thống không thể sửa/xóa, vai trò đã gán cho người dùng không thể xóa)
4. Các quyền được định nghĩa rõ ràng và đầy đủ cho tất cả các chức năng của hệ thống
5. Unit tests đạt coverage > 80%
6. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Cần đảm bảo tạo sẵn các vai trò mặc định như 'Admin', 'Division Manager', 'Leader', 'Sales', 'Employee' với các quyền phù hợp theo permissions_definition.md
- Sử dụng GSI1 (GSI1PK = "ROLE", GSI1SK = name) cho truy vấn vai trò theo tên
- Vì đây là phần quan trọng của hệ thống bảo mật, cần kiểm tra kỹ việc cập nhật vai trò không gây ảnh hưởng đến người dùng đang sử dụng
- Cần lưu log đầy đủ khi có thay đổi đến vai trò và quyền
- Nên phân loại quyền theo module (ví dụ: 'employee:', 'project:', 'opportunity:') và hành động ('read', 'create', 'update', 'delete')
- Theo permissions_definition.md, tất cả các quyền quản lý vai trò và phân quyền (role:read, role:create, role:update, role:delete, permission:read, permission:assign) chỉ được gán cho vai trò Admin
- Cấu trúc quyền hỗ trợ các phạm vi khác nhau: resource:action[:scope] (ví dụ: employee:read:all, employee:read:team, employee:read:own) 