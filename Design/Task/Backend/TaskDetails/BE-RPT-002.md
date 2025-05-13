**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function báo cáo danh sách nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function báo cáo chi tiết danh sách nhân viên, bao gồm thông tin về kỹ năng và các chỉ số hiệu suất liên quan.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-RPT-002  
**Task Name:** Phát triển Lambda function báo cáo chi tiết danh sách nhân viên  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)
- BE-HRM-004 (Triển khai Lambda functions quản lý skills của nhân viên)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- GET /api/v1/reports/employee-list (API-RPT-002)

## Mô tả

Task này bao gồm việc phát triển Lambda function để tạo báo cáo chi tiết về danh sách nhân viên, bao gồm thông tin cá nhân cơ bản, kỹ năng, dự án đang tham gia, và các chỉ số hiệu suất. Báo cáo này sẽ hỗ trợ các tính năng lọc phức tạp và xuất dữ liệu sang định dạng file (Excel/CSV) để phân tích sâu hơn.

Function này sẽ cung cấp các tham số truy vấn linh hoạt cho phép người dùng tùy chỉnh báo cáo theo nhiều tiêu chí (team, trạng thái, kỹ năng, v.v.), đảm bảo phân quyền dữ liệu phù hợp dựa trên vai trò của người dùng.

## Chi tiết công việc

### Phát triển Lambda function tạo báo cáo danh sách nhân viên

- [ ] Triển khai Lambda function xử lý GET /api/v1/reports/employee-list:
  - Location: src/functions/reports/employee_list_report.py
  - Triển khai handler function:
    ```python
    def handler(event, context):
        """
        Lambda handler for employee list detailed report
        """
        try:
            # Extract query parameters
            query_params = event.get('queryStringParameters', {}) or {}
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Check if export is requested
            export_format = query_params.get('export')
            
            # Create report service
            report_service = EmployeeReportService(auth_context)
            
            # Fetch employee list data with filters
            if export_format:
                # Generate export file
                result = report_service.generate_employee_export(query_params, export_format)
                return Response.file_download(result['file_url'], result['filename'])
            else:
                # Return paginated data
                result = report_service.get_employee_list_report(query_params)
                return Response.success(result)
        except Exception as e:
            logger.error("Error generating employee list report", exc=e)
            return handle_error(e)
    ```

### Phát triển Service Layer cho Employee Report

- [ ] Xây dựng Employee Report Service:
  - Location: src/services/report_service.py
  - Implement class Report Service:
    ```python
    class EmployeeReportService:
        def __init__(self, auth_context):
            self.auth_context = auth_context
            self.employee_repo = EmployeeRepository()
            self.skill_repo = SkillRepository()
            self.project_repo = ProjectRepository()
            self.margin_repo = MarginRepository()
        
        def get_employee_list_report(self, params):
            """
            Get detailed employee list report with pagination
            """
            # Extract pagination and filter parameters
            page = int(params.get('page', 1))
            size = min(int(params.get('size', 20)), 100)  # Limit max page size
            
            # Extract other filters
            team_id = params.get('team_id')
            status = params.get('status')
            skill_ids = params.get('skill_ids', '').split(',') if params.get('skill_ids') else None
            search_query = params.get('query')
            
            # Determine scope based on user role
            scope = self._determine_user_scope()
            
            # Validate access based on scope
            if team_id and not self._has_access_to_team(team_id, scope):
                raise PermissionError(f"User doesn't have access to team {team_id}")
            
            # Build filters object
            filters = {
                'team_id': team_id,
                'status': status,
                'skill_ids': skill_ids,
                'search_query': search_query,
                # Add more filters as needed
            }
            
            # Get paginated employees
            result = self.employee_repo.get_employees_with_details(
                scope=scope,
                filters=filters,
                page=page,
                size=size
            )
            
            # Enrich result with additional data
            self._enrich_employee_data(result['items'])
            
            return {
                'items': result['items'],
                'total': result['total'],
                'page': page,
                'size': size,
                'total_pages': math.ceil(result['total'] / size)
            }
        
        def generate_employee_export(self, params, export_format):
            """
            Generate employee report export file (Excel/CSV)
            """
            # Remove pagination to get all results
            params.pop('page', None)
            params.pop('size', None)
            
            # Override size with a large number (use with caution)
            params['size'] = 1000  # Reasonable limit for exports
            
            # Get all data
            report_data = self.get_employee_list_report(params)
            
            # Generate file
            if export_format.lower() == 'excel':
                file_path = self._generate_excel_export(report_data['items'])
                filename = f"employee_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            elif export_format.lower() == 'csv':
                file_path = self._generate_csv_export(report_data['items'])
                filename = f"employee_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            else:
                raise ValueError(f"Unsupported export format: {export_format}")
            
            # Upload to S3
            s3_key = f"exports/{filename}"
            s3_url = self._upload_to_s3(file_path, s3_key)
            
            return {
                'file_url': s3_url,
                'filename': filename
            }
    ```

### Triển khai các phương thức lấy và xử lý dữ liệu chi tiết

- [ ] Phát triển phương thức truy vấn và lọc data nhân viên:
  - Location: src/repositories/employee_repository.py
  - Implement phương thức:
    ```python
    def get_employees_with_details(self, scope, filters, page=1, size=20):
        """
        Get employees with detailed information, filtered and paginated
        """
        # Prepare query parameters
        key_condition_expression = None
        filter_expression = None
        expression_attr_values = {}
        expression_attr_names = {}
        
        # Build GSI query based on filters
        index_name = self._determine_best_index(filters)
        
        # Apply team filter if provided and authorized
        if filters.get('team_id'):
            key_condition_expression = Key('GSI3PK').eq(f"EMPLOYEE_TEAM#{filters['team_id']}")
            # Use GSI3
            index_name = 'GSI3'
        elif filters.get('status'):
            # Use GSI2 for status-based queries
            key_condition_expression = Key('GSI2PK').eq(f"EMPLOYEE_STATUS#{filters['status']}")
            index_name = 'GSI2'
        else:
            # Default to scanning all employees in scope
            key_condition_expression = Key('GSI1PK').eq('EMPLOYEE')
            index_name = 'GSI1'
        
        # Apply additional filters
        if filters.get('search_query'):
            search_term = filters['search_query'].lower()
            # Create search filter expression
            filter_expression = Attr('full_name').contains(search_term) | \
                                Attr('employee_code').contains(search_term) | \
                                Attr('position').contains(search_term)
        
        # Execute query with pagination
        last_evaluated_key = None
        if page > 1:
            # Calculate start key for pagination
            # This is simplified, in real implementation we'd need to handle this more efficiently
            for i in range(1, page):
                temp_result = self.table.query(
                    IndexName=index_name,
                    KeyConditionExpression=key_condition_expression,
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_attr_values,
                    ExpressionAttributeNames=expression_attr_names,
                    Limit=size,
                    ExclusiveStartKey=last_evaluated_key
                )
                last_evaluated_key = temp_result.get('LastEvaluatedKey')
                if not last_evaluated_key:
                    break
        
        # Execute final query
        result = self.table.query(
            IndexName=index_name,
            KeyConditionExpression=key_condition_expression,
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attr_values,
            ExpressionAttributeNames=expression_attr_names,
            Limit=size,
            ExclusiveStartKey=last_evaluated_key
        )
        
        # Process results
        items = result.get('Items', [])
        
        # If skill_ids filter is provided, apply it in-memory after fetching data
        if filters.get('skill_ids'):
            items = self._filter_by_skills(items, filters['skill_ids'])
        
        # Get total count (might require separate query for accurate results)
        total = self._get_total_count(key_condition_expression, filter_expression,
                                     expression_attr_values, expression_attr_names, index_name)
        
        return {
            'items': items,
            'total': total,
            'last_evaluated_key': result.get('LastEvaluatedKey')
        }
    ```

- [ ] Phát triển phương thức làm giàu dữ liệu nhân viên:
  - Location: src/services/report_service.py
  - Implement phương thức:
    ```python
    def _enrich_employee_data(self, employees):
        """
        Enrich employee data with skills and current project details
        """
        if not employees:
            return
            
        # Collect IDs for batch operations
        employee_ids = [emp['id'] for emp in employees]
        
        # Batch get skills for all employees
        employee_skills = self.skill_repo.get_skills_for_employees(employee_ids)
        
        # Batch get project history for employees
        project_history = self.project_repo.get_current_projects(employee_ids)
        
        # If applicable, get margin data
        if self.auth_context.has_permission('margin:read'):
            # Only fetch margin if user has permission
            current_month = datetime.now().strftime('%Y-%m')
            margin_data = self.margin_repo.get_employee_margins(employee_ids, current_month)
        else:
            margin_data = {}
        
        # Add data to each employee
        for employee in employees:
            employee_id = employee['id']
            
            # Add skills
            employee['skills'] = employee_skills.get(employee_id, [])
            
            # Add current project
            employee['current_project'] = project_history.get(employee_id)
            
            # Add margin data if available
            if employee_id in margin_data and self.auth_context.has_permission('margin:read'):
                employee['margin'] = margin_data[employee_id]
    ```

- [ ] Phát triển phương thức tạo file export:
  - Location: src/services/report_service.py
  - Implement phương thức Excel export:
    ```python
    def _generate_excel_export(self, employees):
        """
        Generate Excel export file from employee data
        """
        # Create a workbook and add a worksheet
        workbook = xlsxwriter.Workbook('/tmp/employee_report.xlsx')
        worksheet = workbook.add_worksheet('Employees')
        
        # Add headers with formatting
        headers = [
            'Employee ID', 'Full Name', 'Position', 'Team', 'Status',
            'Current Project', 'Project Role', 'Allocation', 'End Date',
            'Skills', 'Contact Email', 'Phone'
        ]
        
        # Add margin data headers if user has permission
        if self.auth_context.has_permission('margin:read'):
            headers.extend(['Cost', 'Revenue', 'Margin'])
        
        # Format headers
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        # Write headers
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)  # Set column width
        
        # Write data
        row = 1
        for employee in employees:
            col = 0
            worksheet.write(row, col, employee.get('employee_code', ''))
            col += 1
            worksheet.write(row, col, employee.get('full_name', ''))
            col += 1
            worksheet.write(row, col, employee.get('position', ''))
            col += 1
            worksheet.write(row, col, employee.get('team_name', ''))
            col += 1
            worksheet.write(row, col, employee.get('current_status', ''))
            col += 1
            worksheet.write(row, col, employee.get('current_project_name', ''))
            col += 1
            worksheet.write(row, col, employee.get('project_role', ''))
            col += 1
            worksheet.write(row, col, employee.get('allocation_percentage', 0))
            col += 1
            worksheet.write(row, col, employee.get('expected_end_date', ''))
            col += 1
            
            # Format skills list
            skills_str = ', '.join([s.get('name', '') for s in employee.get('skills', [])])
            worksheet.write(row, col, skills_str)
            col += 1
            
            worksheet.write(row, col, employee.get('company_email', ''))
            col += 1
            worksheet.write(row, col, employee.get('phone_number', ''))
            col += 1
            
            # Add margin data if available and permitted
            if self.auth_context.has_permission('margin:read') and 'margin' in employee:
                worksheet.write(row, col, employee['margin'].get('cost_amount', 0))
                col += 1
                worksheet.write(row, col, employee['margin'].get('revenue_amount', 0))
                col += 1
                worksheet.write(row, col, employee['margin'].get('margin_percentage', 0))
                col += 1
            
            row += 1
        
        # Finalize workbook
        workbook.close()
        
        return '/tmp/employee_report.xlsx'
    ```
  
  - Implement phương thức CSV export:
    ```python
    def _generate_csv_export(self, employees):
        """
        Generate CSV export file from employee data
        """
        csv_file = '/tmp/employee_report.csv'
        
        # Define fields based on permissions
        fields = [
            'employee_code', 'full_name', 'position', 'team_name', 'current_status',
            'current_project_name', 'project_role', 'allocation_percentage', 'expected_end_date',
            'skills', 'company_email', 'phone_number'
        ]
        
        # Add margin fields if user has permission
        if self.auth_context.has_permission('margin:read'):
            fields.extend(['cost_amount', 'revenue_amount', 'margin_percentage'])
        
        with open(csv_file, 'w', newline='') as f:
            # Create CSV writer
            writer = csv.DictWriter(f, fieldnames=fields)
            
            # Write header
            writer.writeheader()
            
            # Write data rows
            for employee in employees:
                # Prepare row data
                row = {field: employee.get(field, '') for field in fields}
                
                # Special handling for skills
                if 'skills' in fields:
                    row['skills'] = ', '.join([s.get('name', '') for s in employee.get('skills', [])])
                
                # Handle margin data
                if self.auth_context.has_permission('margin:read') and 'margin' in employee:
                    row['cost_amount'] = employee['margin'].get('cost_amount', 0)
                    row['revenue_amount'] = employee['margin'].get('revenue_amount', 0)
                    row['margin_percentage'] = employee['margin'].get('margin_percentage', 0)
                
                writer.writerow(row)
        
        return csv_file
    ```

- [ ] Phát triển phương thức upload file sang S3:
  - Location: src/services/report_service.py
  - Implement phương thức:
    ```python
    def _upload_to_s3(self, file_path, s3_key):
        """
        Upload file to S3 and return signed URL
        """
        # Get S3 bucket name from environment
        bucket_name = os.environ.get('EXPORT_BUCKET_NAME')
        
        # Upload file to S3
        s3_client = boto3.client('s3')
        s3_client.upload_file(
            file_path,
            bucket_name,
            s3_key,
            ExtraArgs={'ContentDisposition': f'attachment; filename="{os.path.basename(file_path)}"'}
        )
        
        # Generate pre-signed URL with short expiration
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        
        return url
    ```

### Cấu hình API Gateway và IAM Permissions

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình endpoint GET /api/v1/reports/employee-list:
    ```yaml
    EmployeeListReportFunction:
      Type: AWS::Serverless::Function
      Properties:
        CodeUri: src/functions/reports/
        Handler: employee_list_report.handler
        Policies:
          - DynamoDBReadPolicy:
              TableName: !Ref SDIMSTable
          - S3WritePolicy:
              BucketName: !Ref ExportBucket
        Environment:
          Variables:
            EXPORT_BUCKET_NAME: !Ref ExportBucket
        Events:
          ApiEvent:
            Type: Api
            Properties:
              Path: /api/v1/reports/employee-list
              Method: get
              RestApiId: !Ref SDIMSApi
    
    ExportBucket:
      Type: AWS::S3::Bucket
      Properties:
        BucketName: !Sub "${AWS::StackName}-exports"
        LifecycleConfiguration:
          Rules:
            - ExpirationInDays: 7  # Auto-delete after 7 days
              Status: Enabled
    ```

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/reports/
  - Test case cho employee_list_report.py:
    - Test lấy dữ liệu báo cáo thành công
    - Test xuất file Excel/CSV
    - Test xử lý lỗi
    - Test phân quyền khi xem dữ liệu margin
  - Test case cho report_service.py:
    - Test lọc nhân viên theo các tiêu chí khác nhau
    - Test làm giàu dữ liệu nhân viên
    - Test tạo và upload file export

### Tạo Documentation

- [ ] Viết tài liệu API swagger cho endpoint:
  - GET /api/v1/reports/employee-list
  - Tham số lọc và phân trang
  - Tham số xuất file
  - Cấu trúc response

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để lấy báo cáo danh sách nhân viên:

```python
# Lấy báo cáo danh sách nhân viên
import requests

def get_employee_list_report(api_base_url, token, filters=None, page=1, size=20, export_format=None):
    """
    Get employee list report with various filters
    
    :param api_base_url: Base URL of the API
    :param token: Auth token
    :param filters: Dictionary of filters (team_id, status, skill_ids, query)
    :param page: Page number (for pagination)
    :param size: Page size (for pagination)
    :param export_format: Export format ('excel' or 'csv') or None for JSON
    :return: JSON response or download URL for export
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Build query parameters
    params = {
        'page': page,
        'size': size
    }
    
    # Add filters if provided
    if filters:
        params.update(filters)
    
    # Add export format if provided
    if export_format:
        params['export'] = export_format
    
    response = requests.get(
        f"{api_base_url}/api/v1/reports/employee-list",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ sử dụng:
# 1. Lấy danh sách nhân viên với lọc
filters = {
    'team_id': 'team123',
    'status': 'Available',
    'skill_ids': 'skill1,skill2',
    'query': 'Java'
}
employees = get_employee_list_report('https://api.example.com', 'token123', filters=filters)

# 2. Xuất file Excel
excel_export = get_employee_list_report(
    'https://api.example.com', 
    'token123', 
    filters=filters,
    export_format='excel'
)

# Kết quả mong đợi khi gọi API (không yêu cầu export):
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "items": [
#       {
#         "id": "emp123",
#         "employee_code": "E001",
#         "full_name": "John Doe",
#         "position": "Senior Software Engineer",
#         "team_id": "team123",
#         "team_name": "Software Development",
#         "current_status": "Allocated",
#         "current_project_id": "proj456",
#         "current_project_name": "CRM Enhancement",
#         "project_role": "Tech Lead",
#         "allocation_percentage": 100,
#         "expected_end_date": "2025-08-30",
#         "company_email": "john.doe@company.com",
#         "phone_number": "+84912345678",
#         "skills": [
#           {"id": "skill1", "name": "Java", "level": 4},
#           {"id": "skill2", "name": "Spring Boot", "level": 3},
#           {"id": "skill3", "name": "AWS", "level": 4}
#         ],
#         "margin": {
#           "cost_amount": 2000,
#           "revenue_amount": 3500,
#           "margin_percentage": 42.85
#         }
#       },
#       // ... more employees
#     ],
#     "total": 28,
#     "page": 1,
#     "size": 20,
#     "total_pages": 2
#   }
# }

# Kết quả mong đợi khi xuất file:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "file_url": "https://s3-presigned-url-to-download-file.com/...",
#     "filename": "employee_report_20250513_120530.xlsx"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function được triển khai và hoạt động chính xác với API GET /api/v1/reports/employee-list
2. API hỗ trợ đầy đủ các tham số lọc và phân trang
3. Cơ chế export file Excel/CSV được triển khai và hoạt động đúng
4. Phân quyền truy cập dữ liệu được áp dụng (đặc biệt là dữ liệu margin)
5. Các truy vấn DynamoDB được tối ưu hóa và hiệu quả
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Cần xử lý cẩn thận với quyền xem dữ liệu margin vì đây là thông tin nhạy cảm
- Khi export dữ liệu lớn, cần xử lý hiệu quả để tránh time-out của Lambda (có thể cần triển khai cơ chế export không đồng bộ nếu số lượng nhân viên rất lớn)
- File export nên được đặt trong S3 bucket có cấu hình lifecycle policy để tự động xóa sau một khoảng thời gian nhất định
- Cần đảm bảo truy vấn DynamoDB hiệu quả, sử dụng GSI phù hợp dựa trên các điều kiện lọc
- Với các tham số lọc phức tạp (ví dụ: lọc theo skills), có thể cần xử lý thêm sau khi truy vấn DynamoDB