**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function xem log hệ thống | -           | Draft     |
| 1.1     | 2025-05-13 | Chiến Trần Văn | Cập nhật thông tin về quyền dựa trên permission_definition.md | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function xem log hệ thống, hỗ trợ việc giám sát, theo dõi và gỡ lỗi hệ thống từ xa.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-ADM-004  
**Task Name:** Triển khai Lambda function xem log hệ thống  
**Độ ưu tiên:** Thấp  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-005 (Cấu hình API Gateway)
- BE-INF-006 (Cài đặt monitoring và logging)
- BE-CORE-002 (Phát triển service authentication và authorization)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- GET /api/v1/admin/system-logs (API-ADM-013)

## Mô tả

Task này bao gồm việc phát triển Lambda function để xem log hệ thống, cho phép quản trị viên truy cập và tìm kiếm các log từ CloudWatch Logs. Function này sẽ cung cấp giao diện API để truy vấn log, lọc theo thời gian, mức độ nghiêm trọng, và các từ khóa tìm kiếm, hỗ trợ việc giám sát và gỡ lỗi hệ thống từ xa.

Lambda function sẽ tương tác với CloudWatch Logs API để truy xuất dữ liệu log, đồng thời áp dụng các quy tắc phân quyền để đảm bảo chỉ người dùng có quyền phù hợp mới có thể truy cập thông tin log hệ thống.

## Chi tiết công việc

### Phát triển Lambda function xem log hệ thống

- [ ] Triển khai Lambda function xử lý GET /api/v1/admin/system-logs:
  - Location: src/admin/system_logs.py
  - Triển khai handler function để xem log hệ thống:
    ```python
    def get_system_logs(event, context):
        """
        Lambda handler for retrieving system logs from CloudWatch
        """
        try:
            # Extract query parameters
            query_params = event.get('queryStringParameters', {}) or {}
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check appropriate permission based on user's role
            if auth_context.has_permission('system-log:read:all'):
                # Admin can view all logs
                log_access_level = 'all'
            elif auth_context.has_permission('system-log:read:limited'):
                # Division Manager can view limited logs
                log_access_level = 'limited'
            else:
                return Response.forbidden("Permission denied: Requires system-log:read permission")
            
            # Extract log filter parameters
            log_group = query_params.get('log_group', '/aws/lambda/sdims-prod')
            start_time = int(query_params.get('start_time', int(time.time()) - 86400))  # Default to last 24 hours
            end_time = int(query_params.get('end_time', int(time.time())))
            filter_pattern = query_params.get('filter', '')
            level = query_params.get('level')  # INFO, WARNING, ERROR, etc.
            limit = min(int(query_params.get('limit', 100)), 1000)  # Default 100, max 1000
            
            # Apply level filter if specified
            if level:
                # Append level filter to pattern
                if filter_pattern:
                    filter_pattern = f"{filter_pattern} {level}"
                else:
                    filter_pattern = level
            
            # Create log service
            log_service = LogService()
            
            # Fetch log events with appropriate access level
            logs = log_service.get_logs(
                log_group=log_group,
                start_time=start_time,
                end_time=end_time,
                filter_pattern=filter_pattern,
                limit=limit,
                access_level=log_access_level
            )
            
            return Response.success({
                "logs": logs,
                "filters": {
                    "log_group": log_group,
                    "start_time": start_time,
                    "end_time": end_time,
                    "filter_pattern": filter_pattern,
                    "level": level,
                    "limit": limit,
                    "access_level": log_access_level
                }
            })
        except Exception as e:
            logger.error("Error retrieving system logs", exc=e)
            return handle_error(e)
    ```

### Phát triển Log Service Layer

- [ ] Xây dựng Log Service:
  - Location: src/services/log_service.py
  - Implement LogService class với các phương thức:
    ```python
    class LogService:
        def __init__(self):
            self.logs_client = boto3.client('logs')
        
        def get_logs(self, log_group, start_time, end_time, filter_pattern='', limit=100, access_level='all'):
            """
            Fetch log events from CloudWatch Logs with filtering
            
            Args:
                log_group (str): CloudWatch Logs group name
                start_time (int): Start time in Unix timestamp
                end_time (int): End time in Unix timestamp
                filter_pattern (str): CloudWatch Logs filter pattern
                limit (int): Maximum number of log events to return
                access_level (str): Access level ('all' or 'limited')
                
            Returns:
                list: List of log events with parsed message
            """
            try:
                # Convert timestamps to milliseconds for CloudWatch API
                start_time_ms = start_time * 1000
                end_time_ms = end_time * 1000
                
                # For limited access, enforce additional constraints
                if access_level == 'limited':
                    # Restrict time range to last 7 days max for limited users
                    earliest_allowed = int(time.time()) - (7 * 86400)  # 7 days ago
                    if start_time < earliest_allowed:
                        start_time_ms = earliest_allowed * 1000
                    
                    # Add filter to exclude sensitive logs for limited users
                    if filter_pattern:
                        filter_pattern = f"{filter_pattern} -\"credential\" -\"password\" -\"secret\" -\"token\""
                    else:
                        filter_pattern = "-\"credential\" -\"password\" -\"secret\" -\"token\""
                
                # Get log streams for the log group
                response = self.logs_client.filter_log_events(
                    logGroupName=log_group,
                    startTime=start_time_ms,
                    endTime=end_time_ms,
                    filterPattern=filter_pattern,
                    limit=limit
                )
                
                # Extract and parse log events
                logs = []
                for event in response.get('events', []):
                    log_entry = {
                        'timestamp': event.get('timestamp') // 1000,  # Convert back to seconds
                        'datetime': datetime.fromtimestamp(event.get('timestamp') // 1000).isoformat(),
                        'message': event.get('message', ''),
                        'log_stream': event.get('logStreamName')
                    }
                    
                    # Try to parse JSON from message if possible
                    try:
                        message_json = json.loads(log_entry['message'])
                        log_entry['parsed'] = message_json
                        
                        # Extract common fields if present
                        log_entry['level'] = message_json.get('level') or message_json.get('severity')
                        log_entry['service'] = message_json.get('service') or message_json.get('context')
                        log_entry['request_id'] = message_json.get('requestId') or message_json.get('awsRequestId')
                        
                        # For limited access, redact sensitive fields
                        if access_level == 'limited' and message_json:
                            self._redact_sensitive_fields(message_json)
                            log_entry['parsed'] = message_json
                            
                    except (json.JSONDecodeError, TypeError):
                        # Not JSON or invalid - keep as raw message
                        log_entry['parsed'] = None
                        
                        # Try to extract log level from raw message
                        if 'ERROR' in log_entry['message']:
                            log_entry['level'] = 'ERROR'
                        elif 'WARNING' in log_entry['message'] or 'WARN' in log_entry['message']:
                            log_entry['level'] = 'WARNING'
                        elif 'INFO' in log_entry['message']:
                            log_entry['level'] = 'INFO'
                        else:
                            log_entry['level'] = 'UNKNOWN'
                    
                    logs.append(log_entry)
                
                return logs
            
            except Exception as e:
                logger.error(f"Error retrieving logs from CloudWatch: {str(e)}")
                raise
        
        def _redact_sensitive_fields(self, data, sensitive_keys=None):
            """
            Redact sensitive information from log data
            
            Args:
                data (dict): Log data to redact
                sensitive_keys (list): List of sensitive key patterns to redact
            """
            if sensitive_keys is None:
                sensitive_keys = [
                    'password', 'secret', 'token', 'key', 'credential', 'auth',
                    'credit', 'card', 'cvv', 'ssn', 'social', 'account'
                ]
            
            if isinstance(data, dict):
                for key in list(data.keys()):
                    # Check if key contains sensitive information
                    if any(pattern in key.lower() for pattern in sensitive_keys):
                        data[key] = "******REDACTED******"
                    elif isinstance(data[key], (dict, list)):
                        self._redact_sensitive_fields(data[key], sensitive_keys)
            
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, (dict, list)):
                        self._redact_sensitive_fields(item, sensitive_keys)
        
        def get_log_groups(self, access_level='all'):
            """
            Get list of available log groups
            
            Args:
                access_level (str): Access level ('all' or 'limited')
                
            Returns:
                list: List of log group names
            """
            try:
                log_groups = []
                paginator = self.logs_client.get_paginator('describe_log_groups')
                
                for page in paginator.paginate():
                    for log_group in page.get('logGroups', []):
                        group_name = log_group.get('logGroupName')
                        
                        # For limited access, filter out certain log groups
                        if access_level == 'limited':
                            # Skip internal system and security logs for limited users
                            if any(pattern in group_name for pattern in ['/security/', '/auth/', '/internal/']):
                                continue
                        
                        log_groups.append(group_name)
                
                return log_groups
            
            except Exception as e:
                logger.error(f"Error retrieving log groups: {str(e)}")
                raise
    ```

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/admin/system-logs:
    ```yaml
    SystemLogsFunction:
      Type: AWS::Serverless::Function
      Properties:
        CodeUri: src/admin/
        Handler: system_logs.get_system_logs
        Runtime: python3.9
        MemorySize: 256
        Timeout: 30
        Policies:
          - CloudWatchLogsReadOnlyAccess
          - Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:FilterLogEvents
                  - logs:DescribeLogGroups
                  - logs:DescribeLogStreams
                Resource: '*'
        Events:
          ApiEvent:
            Type: Api
            Properties:
              Path: /api/v1/admin/system-logs
              Method: get
              RestApiId: !Ref SDIMSApi
    ```

### Triển khai IAM Policies

- [ ] Cấu hình IAM Policies cho Lambda function:
  - Location: template.yaml
  - Thêm policies cho phép đọc CloudWatch Logs:
    ```yaml
    Policies:
      - CloudWatchLogsReadOnlyAccess
      - Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - logs:FilterLogEvents
              - logs:DescribeLogGroups
              - logs:DescribeLogStreams
            Resource: '*'
    ```

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/admin/
  - Test case cho system_logs.py
  - Test case cho LogService

### Tạo Documentation

- [ ] Viết tài liệu API swagger cho endpoint:
  - GET /api/v1/admin/system-logs

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để xem log hệ thống:

```python
# Xem log hệ thống
import requests
import time

def get_system_logs(api_base_url, token, filters=None):
    """
    Get system logs with filtering options
    
    Args:
        api_base_url (str): Base URL of the API
        token (str): Authentication token
        filters (dict): Dictionary of filter parameters:
            - log_group: CloudWatch log group name
            - start_time: Start time (Unix timestamp)
            - end_time: End time (Unix timestamp)
            - filter: Text filter pattern
            - level: Log level (INFO, WARNING, ERROR)
            - limit: Maximum number of logs to return
    
    Returns:
        dict: API response with logs
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Default parameters
    params = {
        'log_group': '/aws/lambda/sdims-prod',
        'start_time': int(time.time()) - 3600,  # Last hour
        'end_time': int(time.time()),
        'limit': 100
    }
    
    # Update with custom filters if provided
    if filters:
        params.update(filters)
    
    response = requests.get(
        f"{api_base_url}/api/v1/admin/system-logs",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ sử dụng:
# Tìm log lỗi trong 24 giờ qua
error_logs = get_system_logs(
    'https://api.example.com',
    'admin_token',
    {
        'level': 'ERROR',
        'start_time': int(time.time()) - 86400,  # 24 hours ago
        'limit': 50
    }
)

# Tìm log liên quan đến một RequestId cụ thể
request_logs = get_system_logs(
    'https://api.example.com',
    'admin_token',
    {
        'filter': 'f76e782f-55c3-4cc3-9534-4f2992dd6b91',
        'limit': 20
    }
)
```

## Tiêu chí hoàn thành

1. Lambda function được triển khai và hoạt động chính xác với API GET /api/v1/admin/system-logs
2. API hỗ trợ đầy đủ các tham số lọc (log_group, start_time, end_time, filter, level, limit)
3. Xác thực quyền truy cập được áp dụng đúng:
   - Quyền `system-log:read:all` cho Admin để xem toàn bộ log không giới hạn
   - Quyền `system-log:read:limited` cho Division Manager để xem log với giới hạn
4. IAM policies được cấu hình đúng để cho phép truy cập CloudWatch Logs
5. Xử lý hiệu quả và tối ưu khi truy xuất volume log lớn
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Cần cân nhắc về hiệu năng khi truy vấn volume log lớn, nên giới hạn thời gian truy vấn và số lượng kết quả trả về
- Lambda có giới hạn thời gian thực thi (timeout), cần xử lý trường hợp truy vấn quá nhiều log
- Nên áp dụng caching cho các truy vấn log phổ biến để cải thiện hiệu năng
- Đối với người dùng có quyền `system-log:read:limited` (Division Manager), cần thực hiện redact thông tin nhạy cảm và giới hạn phạm vi truy cập
- Chỉ người dùng có quyền `system-log:read:all` (Admin) mới có thể truy cập đầy đủ thông tin log hệ thống
- Truy vấn CloudWatch Logs có thể phát sinh chi phí, nên tối ưu số lượng và tần suất truy vấn
- Nên cung cấp thêm endpoints phụ trợ để lấy danh sách log groups có sẵn, với phân quyền tương ứng 