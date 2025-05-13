**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý cấu hình hệ thống | -           | Draft     |
| 1.1     | 2025-05-13 | Chiến Trần Văn | Cập nhật thông tin về quyền dựa trên permission_definition.md | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions quản lý cấu hình hệ thống, cho phép quản trị viên cấu hình các thông số và thiết lập hệ thống từ xa.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-ADM-003  
**Task Name:** Phát triển Lambda functions quản lý cấu hình hệ thống  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)

**Các task phụ thuộc vào task này:** 
- BE-OPP-001 (Triển khai Lambda functions đồng bộ dữ liệu từ Hubspot - cần cấu hình API key)
- BE-MGN-003 (Triển khai Lambda function tính toán margin - cần cấu hình ngưỡng margin)

**Các API:**
- GET /api/v1/admin/configs (API-ADM-011)
- PUT /api/v1/admin/configs/{configKey} (API-ADM-012)

## Mô tả

Task này bao gồm việc phát triển Lambda functions để quản lý cấu hình hệ thống, cho phép quản trị viên xem và cập nhật các thông số cấu hình hệ thống từ xa. Các cấu hình này bao gồm các ngưỡng cảnh báo, thông số kết nối API bên ngoài, và các thiết lập chung khác cho hệ thống.

Lambda functions sẽ tương tác với DynamoDB để lưu trữ và truy xuất các giá trị cấu hình, đồng thời cung cấp API endpoints để frontend có thể hiển thị và cập nhật các thông số này. Hệ thống cũng sẽ hỗ trợ phân loại cấu hình theo nhóm để dễ dàng quản lý.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách cấu hình

- [ ] Triển khai Lambda function xử lý GET /api/v1/admin/configs:
  - Location: src/admin/configs.py
  - Triển khai handler function để lấy danh sách cấu hình:
    ```python
    def get_configs(event, context):
        """
        Lambda handler for getting system configurations
        """
        try:
            # Extract query parameters
            query_params = event.get('queryStringParameters', {}) or {}
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check permission (config:read)
            if not auth_context.has_permission('config:read'):
                return Response.forbidden("Permission denied: Requires config:read privilege")
            
            # Extract group filter (optional)
            group = query_params.get('group')
            
            # Create config service
            config_service = ConfigService()
            
            # Fetch configs with optional group filter
            configs = config_service.get_configs(group=group)
            
            return Response.success({
                "configs": configs
            })
        except Exception as e:
            logger.error("Error getting system configurations", exc=e)
            return handle_error(e)
    ```
  - Tạo config repository để truy vấn DynamoDB:
    - Location: src/repositories/config_repository.py
    - Implement phương thức get_configs_by_group

### Phát triển Lambda function cập nhật cấu hình

- [ ] Triển khai Lambda function xử lý PUT /api/v1/admin/configs/{configKey}:
  - Location: src/admin/configs.py
  - Triển khai handler function để cập nhật cấu hình:
    ```python
    def update_config(event, context):
        """
        Lambda handler for updating system configuration
        """
        try:
            # Extract path parameters
            config_key = event.get('pathParameters', {}).get('configKey')
            
            if not config_key:
                return Response.bad_request("Missing configuration key")
            
            # Extract request body
            body = json.loads(event.get('body', '{}'))
            
            if 'value' not in body:
                return Response.bad_request("Missing configuration value")
                
            config_value = body.get('value')
            description = body.get('description')
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check permission (config:update)
            if not auth_context.has_permission('config:update'):
                return Response.forbidden("Permission denied: Requires config:update privilege")
            
            # Create config service
            config_service = ConfigService()
            
            # Check if config exists
            existing_config = config_service.get_config_by_key(config_key)
            if not existing_config:
                return Response.not_found(f"Configuration not found with key: {config_key}")
            
            # Check if config is protected (can't be modified)
            if existing_config.get('is_protected', False):
                return Response.forbidden("Cannot modify protected system configuration")
            
            # Update config
            updated_config = config_service.update_config(
                config_key=config_key,
                config_value=config_value,
                description=description,
                updated_by=auth_context.user_id
            )
            
            # Log the change
            logger.info(f"System configuration '{config_key}' updated by {auth_context.username}")
            
            return Response.success(updated_config)
        except ValidationError as e:
            return Response.bad_request(str(e))
        except Exception as e:
            logger.error(f"Error updating system configuration '{config_key}'", exc=e)
            return handle_error(e)
    ```
  - Tạo phương thức trong config repository để cập nhật cấu hình:
    - Location: src/repositories/config_repository.py
    - Implement phương thức update_config

### Phát triển Config Service Layer

- [ ] Xây dựng Config Service:
  - Location: src/services/config_service.py
  - Implement ConfigService class với các phương thức:
    - get_configs: Lấy danh sách cấu hình (tùy chọn lọc theo nhóm)
    - get_config_by_key: Lấy cấu hình theo key
    - update_config: Cập nhật giá trị cấu hình
    - validate_config_value: Xác thực giá trị cấu hình (dựa trên loại dữ liệu)
    - initialize_default_configs: Khởi tạo các cấu hình mặc định

- [ ] Tạo lớp ConfigCache để lưu cache cấu hình:
  - Location: src/services/config_service.py
  - Implement ConfigCache class với các phương thức:
    - get: Lấy giá trị cấu hình từ cache
    - set: Cập nhật giá trị cấu hình trong cache
    - invalidate: Xóa cache của một hoặc tất cả cấu hình

### Tạo cơ chế khởi tạo cấu hình mặc định

- [ ] Triển khai script khởi tạo cấu hình mặc định:
  - Location: src/scripts/initialize_configs.py
  - Định nghĩa các cấu hình mặc định cho hệ thống:
    ```python
    DEFAULT_CONFIGS = [
        # Margin thresholds
        {
            "config_key": "margin.threshold.red",
            "config_value": "20",
            "description": "Red margin threshold percentage",
            "group": "margin",
            "data_type": "number",
            "is_protected": False
        },
        {
            "config_key": "margin.threshold.yellow",
            "config_value": "30",
            "description": "Yellow margin threshold percentage",
            "group": "margin",
            "data_type": "number",
            "is_protected": False
        },
        {
            "config_key": "margin.threshold.green",
            "config_value": "40",
            "description": "Green margin threshold percentage",
            "group": "margin",
            "data_type": "number",
            "is_protected": False
        },
        
        # Opportunity follow-up thresholds (days)
        {
            "config_key": "opportunity.followup.red",
            "config_value": "14",
            "description": "Red follow-up threshold in days",
            "group": "opportunity",
            "data_type": "number",
            "is_protected": False
        },
        {
            "config_key": "opportunity.followup.yellow",
            "config_value": "7",
            "description": "Yellow follow-up threshold in days",
            "group": "opportunity",
            "data_type": "number",
            "is_protected": False
        },
        
        # Hubspot API configuration
        {
            "config_key": "integration.hubspot.api_key",
            "config_value": "",
            "description": "Hubspot API key",
            "group": "integration",
            "data_type": "string",
            "is_protected": False
        },
        {
            "config_key": "integration.hubspot.sync_enabled",
            "config_value": "false",
            "description": "Enable/disable Hubspot synchronization",
            "group": "integration",
            "data_type": "boolean",
            "is_protected": False
        },
        {
            "config_key": "integration.hubspot.sync_interval",
            "config_value": "60",
            "description": "Hubspot sync interval in minutes",
            "group": "integration",
            "data_type": "number",
            "is_protected": False
        },
        
        # Email notification settings
        {
            "config_key": "notification.email.enabled",
            "config_value": "true",
            "description": "Enable/disable email notifications",
            "group": "notification",
            "data_type": "boolean",
            "is_protected": False
        },
        {
            "config_key": "notification.email.sender",
            "config_value": "noreply@example.com",
            "description": "Sender email address for notifications",
            "group": "notification",
            "data_type": "string",
            "is_protected": False
        },
        
        # System settings
        {
            "config_key": "system.company_name",
            "config_value": "SDIMS",
            "description": "Company name displayed in emails and UI",
            "group": "system",
            "data_type": "string",
            "is_protected": False
        },
        {
            "config_key": "system.version",
            "config_value": "1.0.0",
            "description": "System version",
            "group": "system",
            "data_type": "string",
            "is_protected": True
        },
        
        # Alert thresholds
        {
            "config_key": "alert.margin.enabled",
            "config_value": "true",
            "description": "Enable/disable margin alerts",
            "group": "alert",
            "data_type": "boolean",
            "is_protected": False
        },
        {
            "config_key": "alert.opportunity.enabled",
            "config_value": "true", 
            "description": "Enable/disable opportunity alerts",
            "group": "alert",
            "data_type": "boolean",
            "is_protected": False
        },
        {
            "config_key": "alert.payment.enabled",
            "config_value": "true",
            "description": "Enable/disable payment alerts",
            "group": "alert", 
            "data_type": "boolean",
            "is_protected": False
        }
    ]
    ```
  - Triển khai phương thức để khởi tạo cấu hình mặc định khi deploy hệ thống

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình các routes:
    - GET /api/v1/admin/configs
    - PUT /api/v1/admin/configs/{configKey}

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/admin/
  - Test case cho handler functions trong configs.py
  - Test case cho ConfigService
  - Test case cho ConfigRepository

### Tạo Documentation

- [ ] Viết tài liệu API swagger cho các endpoints:
  - GET /api/v1/admin/configs
  - PUT /api/v1/admin/configs/{configKey}

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để quản lý cấu hình hệ thống:

```python
# Lấy danh sách cấu hình hệ thống
import requests

def get_configs(api_base_url, token, group=None):
    """
    Get system configurations with optional group filter
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {}
    if group:
        params['group'] = group
    
    response = requests.get(
        f"{api_base_url}/api/v1/admin/configs",
        headers=headers,
        params=params
    )
    
    return response.json()

# Cập nhật cấu hình hệ thống
def update_config(api_base_url, token, config_key, config_value, description=None):
    """
    Update system configuration
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'value': config_value
    }
    
    if description:
        data['description'] = description
    
    response = requests.put(
        f"{api_base_url}/api/v1/admin/configs/{config_key}",
        headers=headers,
        json=data
    )
    
    return response.json()

# Ví dụ lấy cấu hình margin:
margin_configs = get_configs('https://api.example.com', 'admin_token', group='margin')

# Ví dụ cập nhật ngưỡng margin:
update_result = update_config(
    'https://api.example.com',
    'admin_token',
    'margin.threshold.red',
    '25',
    'Updated red margin threshold percentage'
)
```

## Tiêu chí hoàn thành

1. Lambda functions được triển khai và hoạt động chính xác:
   - GET /api/v1/admin/configs
   - PUT /api/v1/admin/configs/{configKey}
2. Xác thực quyền truy cập được áp dụng đúng:
   - Quyền `config:read` cho API GET /api/v1/admin/configs
   - Quyền `config:update` cho API PUT /api/v1/admin/configs/{configKey}
3. Cơ chế khởi tạo cấu hình mặc định hoạt động khi deploy hệ thống
4. Cơ chế cache cấu hình được triển khai để tối ưu hiệu năng
5. Xử lý đúng các trường hợp đặc biệt (cấu hình protected không thể sửa)
6. Xác thực dữ liệu đầu vào dựa trên loại dữ liệu của cấu hình
7. Unit tests đạt coverage > 80%
8. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Sử dụng cấu trúc DynamoDB đã định nghĩa trong SYSTEM_CONFIG entity để lưu trữ cấu hình
- Triển khai cơ chế cache để tránh truy vấn DynamoDB quá nhiều khi đọc cấu hình
- Cần bảo mật các cấu hình nhạy cảm như API keys (không trả về giá trị đầy đủ qua API)
- Tất cả thay đổi cấu hình cần được ghi log đầy đủ
- Cơ chế xác thực giá trị cấu hình dựa trên data_type để tránh lỗi khi sử dụng (ví dụ: number phải là số)
- Cấu hình phân loại theo nhóm (group) để dễ quản lý (margin, opportunity, integration, notification, system, alert)
- Theo permissions_definition.md, quyền `config:read` được cấp cho Admin, Division Manager, và Leader, trong khi quyền `config:update` chỉ được cấp cho Admin 