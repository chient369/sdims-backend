**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function lấy dữ liệu tổng hợp cho dashboard | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function lấy dữ liệu tổng hợp cho dashboard, cung cấp một cái nhìn tổng quan về các metric chính của hệ thống.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-RPT-001  
**Task Name:** Phát triển Lambda function lấy dữ liệu tổng hợp cho dashboard  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)
- BE-MGN-003 (Triển khai Lambda function tính toán margin)
- BE-OPP-003 (Triển khai Lambda functions quản lý cơ hội)
- BE-CTR-001 (Triển khai Lambda functions quản lý hợp đồng)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- GET /api/v1/dashboard/summary (API-RPT-001)

## Mô tả

Task này bao gồm việc phát triển Lambda function để lấy dữ liệu tổng hợp cho dashboard chính của hệ thống. Lambda function này sẽ tổng hợp các thông tin và metrics quan trọng từ các module khác nhau (Nhân sự, Margin, Cơ hội Kinh doanh, Hợp đồng) để hiển thị trên dashboard. Dữ liệu sẽ bao gồm các chỉ số hiệu suất chính (KPIs), tình trạng nhân sự, trạng thái cơ hội kinh doanh, và tình hình hợp đồng/doanh thu.

Function này cần được tối ưu hóa để xử lý nhanh chóng và hiệu quả các truy vấn phức tạp trên DynamoDB, bảo đảm thời gian phản hồi nhanh cho dashboard.

## Chi tiết công việc

### Phát triển Lambda function lấy dữ liệu tổng hợp cho dashboard

- [ ] Triển khai Lambda function xử lý GET /api/v1/dashboard/summary:
  - Location: src/functions/reports/dashboard_summary.py
  - Triển khai handler function:
    ```python
    def handler(event, context):
        """
        Lambda handler for dashboard summary data
        """
        try:
            # Extract query parameters
            query_params = event.get('queryStringParameters', {}) or {}
            
            # Get authentication context
            auth_context = get_auth_context(event)
            
            # Fetch dashboard data
            dashboard_data = get_dashboard_summary(query_params, auth_context)
            
            # Return successful response
            return Response.success(dashboard_data)
        except Exception as e:
            logger.error("Error fetching dashboard summary", exc=e)
            return handle_error(e)
    ```
  - Triển khai logic lấy dữ liệu dashboard:
    - Tạo class `DashboardService` trong src/services/dashboard_service.py
    - Tạo method để lấy thông tin tổng hợp
    - Phân quyền truy cập dữ liệu theo vai trò người dùng

### Phát triển Service Layer cho Dashboard

- [ ] Xây dựng Dashboard Service:
  - Location: src/services/dashboard_service.py
  - Implement các phương thức lấy dữ liệu tổng hợp:
    ```python
    class DashboardService:
        def __init__(self, auth_context):
            self.auth_context = auth_context
            self.employee_repo = EmployeeRepository()
            self.margin_repo = MarginRepository()
            self.opportunity_repo = OpportunityRepository()
            self.contract_repo = ContractRepository()
        
        def get_dashboard_summary(self, params):
            """
            Get aggregated dashboard data
            """
            # Determine user scope (based on roles/teams)
            scope = self._determine_user_scope()
            
            # Get data in parallel using async functions
            results = asyncio.gather(
                self._get_employee_summary(scope),
                self._get_margin_summary(scope),
                self._get_opportunity_summary(scope),
                self._get_contract_summary(scope)
            )
            
            # Combine results
            return {
                "employee": results[0],
                "margin": results[1],
                "opportunity": results[2],
                "contract": results[3],
                "refreshed_at": datetime.now().isoformat()
            }
    ```

### Triển khai các phương thức lấy dữ liệu chi tiết

- [ ] Phát triển các phương thức cho thông tin nhân sự:
  - Location: src/services/dashboard_service.py
  - Implement phương thức:
    ```python
    async def _get_employee_summary(self, scope):
        """
        Get employee metrics for dashboard
        """
        try:
            # Get employee counts by status
            status_counts = await self.employee_repo.count_by_status(scope)
            
            # Get ending soon (next 30 days)
            ending_soon = await self.employee_repo.count_ending_soon(scope, days=30)
            
            # Get utilization rate
            utilization = await self.employee_repo.get_average_utilization(scope)
            
            # Get skill distribution (top skills)
            top_skills = await self.employee_repo.get_top_skills(scope, limit=5)
            
            return {
                "total_employees": sum(status_counts.values()),
                "status_distribution": status_counts,
                "ending_soon": ending_soon,
                "utilization_rate": utilization,
                "top_skills": top_skills
            }
        except Exception as e:
            logger.error("Error getting employee summary", exc=e)
            return {}
    ```

- [ ] Phát triển các phương thức cho thông tin margin:
  - Location: src/services/dashboard_service.py
  - Implement phương thức:
    ```python
    async def _get_margin_summary(self, scope):
        """
        Get margin metrics for dashboard
        """
        try:
            # Get current month margins
            current_month = datetime.now().strftime("%Y-%m")
            margins = await self.margin_repo.get_margins_by_period(scope, current_month)
            
            # Calculate averages and distributions
            avg_margin = self._calculate_average_margin(margins)
            margin_distribution = self._calculate_margin_distribution(margins)
            
            # Get trend data (last 6 months)
            trend = await self.margin_repo.get_margin_trend(scope, months=6)
            
            return {
                "average_margin": avg_margin,
                "margin_distribution": margin_distribution,
                "margin_trend": trend
            }
        except Exception as e:
            logger.error("Error getting margin summary", exc=e)
            return {}
    ```

- [ ] Phát triển các phương thức cho thông tin cơ hội kinh doanh:
  - Location: src/services/dashboard_service.py
  - Implement phương thức:
    ```python
    async def _get_opportunity_summary(self, scope):
        """
        Get opportunity metrics for dashboard
        """
        try:
            # Get counts by deal stage
            stage_counts = await self.opportunity_repo.count_by_stage(scope)
            
            # Get counts by follow-up status
            followup_counts = await self.opportunity_repo.count_by_followup_status(scope)
            
            # Get recent opportunities (last 30 days)
            recent = await self.opportunity_repo.get_recent_opportunities(scope, days=30, limit=5)
            
            # Get closing opportunities (next 30 days)
            closing_soon = await self.opportunity_repo.get_closing_soon(scope, days=30, limit=5)
            
            return {
                "total_opportunities": sum(stage_counts.values()),
                "stage_distribution": stage_counts,
                "followup_distribution": followup_counts,
                "recent_opportunities": recent,
                "closing_soon": closing_soon
            }
        except Exception as e:
            logger.error("Error getting opportunity summary", exc=e)
            return {}
    ```

- [ ] Phát triển các phương thức cho thông tin hợp đồng và doanh thu:
  - Location: src/services/dashboard_service.py
  - Implement phương thức:
    ```python
    async def _get_contract_summary(self, scope):
        """
        Get contract and revenue metrics for dashboard
        """
        try:
            # Get counts by status
            status_counts = await self.contract_repo.count_by_status(scope)
            
            # Get revenue metrics (current year)
            current_year = datetime.now().year
            revenue = await self.contract_repo.get_revenue_metrics(scope, year=current_year)
            
            # Get payment status overview
            payment_status = await self.contract_repo.get_payment_status_overview(scope)
            
            # Get expiring contracts (next 90 days)
            expiring = await self.contract_repo.get_expiring_contracts(scope, days=90, limit=5)
            
            return {
                "total_contracts": sum(status_counts.values()),
                "status_distribution": status_counts,
                "revenue_metrics": revenue,
                "payment_status": payment_status,
                "expiring_contracts": expiring
            }
        except Exception as e:
            logger.error("Error getting contract summary", exc=e)
            return {}
    ```

### Tối ưu hóa truy vấn và caching

- [ ] Triển khai cơ chế caching cho dữ liệu dashboard:
  - Location: src/services/dashboard_service.py
  - Implement cơ chế cache:
    ```python
    class DashboardCache:
        """
        Cache for dashboard data
        """
        def __init__(self, ttl_seconds=300):
            self.cache = {}
            self.ttl_seconds = ttl_seconds
        
        def get(self, key):
            """Get data from cache"""
            cache_item = self.cache.get(key)
            if not cache_item:
                return None
                
            # Check if cache is still valid
            if time.time() - cache_item["timestamp"] > self.ttl_seconds:
                return None
                
            return cache_item["data"]
            
        def set(self, key, data):
            """Set data in cache"""
            self.cache[key] = {
                "data": data,
                "timestamp": time.time()
            }
            
        def invalidate(self, key=None):
            """Invalidate cache"""
            if key:
                if key in self.cache:
                    del self.cache[key]
            else:
                self.cache = {}
    ```

- [ ] Tối ưu hóa truy vấn DynamoDB cho dữ liệu tổng hợp:
  - Location: src/models/employee.py, src/models/margin.py, src/models/opportunity.py, src/models/contract.py
  - Triển khai các phương thức truy vấn hiệu quả sử dụng GSIs

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/dashboard/summary:
    ```yaml
    DashboardSummaryFunction:
      Type: AWS::Serverless::Function
      Properties:
        CodeUri: src/functions/reports/
        Handler: dashboard_summary.handler
        Policies:
          - DynamoDBReadPolicy:
              TableName: !Ref SDIMSTable
        Events:
          ApiEvent:
            Type: Api
            Properties:
              Path: /api/v1/dashboard/summary
              Method: get
              RestApiId: !Ref SDIMSApi
    ```

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/reports/
  - Test case cho dashboard_summary.py:
    - Test lấy dữ liệu dashboard thành công
    - Test xử lý lỗi
    - Test phân quyền
  - Test case cho dashboard_service.py:
    - Test các phương thức lấy dữ liệu thành phần
    - Test caching mechanism

### Tạo Documentation

- [ ] Viết tài liệu API swagger cho endpoint:
  - GET /api/v1/dashboard/summary
  - Các tham số query string hỗ trợ
  - Mô tả cấu trúc response

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API để lấy dữ liệu dashboard:

```python
# Lấy dữ liệu dashboard
import requests

def get_dashboard_summary(api_base_url, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{api_base_url}/api/v1/dashboard/summary",
        headers=headers
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "employee": {
#       "total_employees": 125,
#       "status_distribution": {
#         "Allocated": 78,
#         "Available": 32,
#         "EndingSoon": 8,
#         "OnLeave": 5,
#         "Resigned": 2
#       },
#       "ending_soon": 12,
#       "utilization_rate": 83.5,
#       "top_skills": [
#         {"name": "Java", "count": 35},
#         {"name": "JavaScript", "count": 28},
#         {"name": "Python", "count": 25},
#         {"name": "React", "count": 22},
#         {"name": "AWS", "count": 18}
#       ]
#     },
#     "margin": {
#       "average_margin": 38.2,
#       "margin_distribution": {
#         "Red": 15,
#         "Yellow": 24,
#         "Green": 86
#       },
#       "margin_trend": [
#         {"month": "2024-12", "value": 36.8},
#         {"month": "2025-01", "value": 37.2},
#         {"month": "2025-02", "value": 37.5},
#         {"month": "2025-03", "value": 37.9},
#         {"month": "2025-04", "value": 38.1},
#         {"month": "2025-05", "value": 38.2}
#       ]
#     },
#     "opportunity": {
#       "total_opportunities": 42,
#       "stage_distribution": {
#         "new": 5,
#         "contacted": 8,
#         "qualified": 10,
#         "proposal": 7,
#         "negotiation": 6,
#         "won": 3,
#         "lost": 2,
#         "closed": 1
#       },
#       "followup_distribution": {
#         "Red": 4,
#         "Yellow": 12,
#         "Green": 26
#       },
#       "recent_opportunities": [
#         {
#           "id": "opp123",
#           "name": "Web Application Project",
#           "customer_name": "ABC Corp",
#           "deal_stage": "qualified",
#           "created_at": "2025-05-01T14:30:00Z"
#         },
#         // ... more opportunities
#       ],
#       "closing_soon": [
#         {
#           "id": "opp456",
#           "name": "Mobile App Development",
#           "customer_name": "XYZ Inc",
#           "deal_stage": "negotiation",
#           "closing_date": "2025-05-30"
#         },
#         // ... more opportunities
#       ]
#     },
#     "contract": {
#       "total_contracts": 38,
#       "status_distribution": {
#         "Draft": 3,
#         "InReview": 2,
#         "Approved": 1,
#         "Active": 25,
#         "InProgress": 2,
#         "OnHold": 1,
#         "Completed": 3,
#         "Terminated": 0,
#         "Expired": 1
#       },
#       "revenue_metrics": {
#         "total_value": 12500000,
#         "received_value": 7200000,
#         "outstanding_value": 5300000
#       },
#       "payment_status": {
#         "unpaid": 5,
#         "partial": 8,
#         "paid": 22,
#         "overdue": 3
#       },
#       "expiring_contracts": [
#         {
#           "id": "ctr789",
#           "name": "Maintenance Services",
#           "customer_name": "DEF Corp",
#           "end_date": "2025-06-15",
#           "status": "Active"
#         },
#         // ... more contracts
#       ]
#     },
#     "refreshed_at": "2025-05-13T10:15:30Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function được triển khai và hoạt động chính xác với API GET /api/v1/dashboard/summary
2. Service layer cho Dashboard được phát triển đầy đủ với các phương thức lấy dữ liệu từ các module khác nhau
3. Cơ chế caching được triển khai để tối ưu hiệu năng
4. Truy vấn DynamoDB được tối ưu hóa để giảm thiểu chi phí và thời gian phản hồi
5. Phân quyền truy cập dữ liệu được triển khai đúng theo vai trò người dùng
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Ưu tiên hiệu năng khi truy vấn dữ liệu từ DynamoDB vì dashboard là chức năng được truy cập thường xuyên
- Sử dụng caching để giảm tải cho DynamoDB và cải thiện thời gian phản hồi
- Cần phân quyền dữ liệu dashboard theo vai trò, team, và phạm vi quản lý của người dùng
- Dashboard data nên được refresh định kỳ thay vì mỗi lần truy cập để tránh quá tải hệ thống
- Cần xử lý các trường hợp khi dữ liệu một số module không khả dụng, đảm bảo dashboard vẫn hoạt động với các dữ liệu còn lại 