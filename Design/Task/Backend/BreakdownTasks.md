**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Phân tích và chia nhỏ task cho backend | -           | Draft     |
| 1.1     | 2024-08-01 | Chiến Trần Văn | Thêm mã task theo định dạng BE-xxx-xxx | -           | Draft     |
| 1.2     | 2024-08-01 | Chiến Trần Văn | Bổ sung các API authentication và authorization | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này phân tích và chia nhỏ công việc phát triển backend cho Hệ thống Quản lý Nội bộ (Internal Management System) dựa trên kiến trúc AWS SAM serverless với Lambda, DynamoDB, S3 và API Gateway.

# Task Breakdown: Backend Implementation (AWS SAM Serverless)

## Infrastructure (AWS SAM / CloudFormation)

- [x] **BE-INF-001**: Thiết lập cấu trúc dự án SAM ban đầu với file template.yaml (High Priority)
  - Cấu hình môi trường (staging, production)
  - Định nghĩa các parameter và tài nguyên chung

- [x] **BE-INF-002**: Xây dựng CI/CD pipeline cho deployment (High Priority)
  - Cấu hình GitHub Actions/AWS CodePipeline 
  - Thiết lập quy trình deploy tự động cho các môi trường

- [ ] **BE-INF-003**: Định nghĩa IAM Roles và Policies cho Lambda functions (High Priority)
  - Tạo các IAM role với quyền tối thiểu theo nguyên tắc least privilege
  - Cấu hình permissions cho các dịch vụ DynamoDB, S3

- [x] **BE-INF-004**: Triển khai DynamoDB table theo cấu trúc đã định nghĩa (High Priority)
  - Tạo single-table design với các GSI đã định nghĩa trong tài liệu
  - Cấu hình capacity mode (provisioned)
  - Thiết lập các tham số backup và recovery

- [x] **BE-INF-005**: Cấu hình API Gateway cho REST API (High Priority)
  - Xác định resources và methods 
  - Thiết lập các API stages
  - Cấu hình CORS, response/request mapping templates

- [ ] **BE-INF-006**: Cài đặt monitoring và logging (Medium Priority)
  - Thiết lập CloudWatch alarms
  - Cấu hình X-Ray tracing
  - Tích hợp logging framework

- [ ] **BE-INF-007**: Cấu hình S3 bucket lưu trữ tệp đính kèm (Medium Priority)
  - Thiết lập lifecycle policies
  - Cấu hình mã hóa và permissions

## Core Services & Libraries

- [x] **BE-CORE-001**: Phát triển Common Services Utilities (High Priority)
  - Xây dựng lớp DynamoDB Repository cho CRUD operations
  - Phát triển utility classes cho response handling
  - Tạo các utility cho error handling và logging
  - Thiết lập Lambda Layer cho common utilities

- [x] **BE-CORE-002**: Phát triển Model Mapping Utilities (High Priority)
  - Tạo cơ chế chuyển đổi giữa DynamoDB items và Python objects
  - Phát triển decorators và annotations cho data mapping
  - Xây dựng type converters cho các kiểu dữ liệu khác nhau
  - Tích hợp với DynamoDB Repository

- [x] **BE-CORE-003**: Phát triển API Validation Framework (High Priority)
  - Xây dựng schema validation component
  - Phát triển rule-based validation component
  - Tạo validation decorators cho Lambda handlers
  - Chuẩn hóa error responses

- [ ] **BE-CORE-004**: Phát triển Event Bus & Message Queue (Medium Priority)
  - Triển khai các utilities để tích hợp với SNS/SQS
  - Tạo cơ chế publish/subscribe cho các sự kiện hệ thống
  - Xây dựng handler cho async processing
  - Implement retry mechanism và dead-letter queue

- [x] **BE-CORE-005**: Phát triển File Storage Utilities (Medium Priority)
  - Xây dựng APIs upload/download file từ S3
  - Tạo cơ chế quản lý metadata của file
  - Phát triển tiện ích xử lý file (tạo thumbnail, validate)
  - Triển khai access control cho file

- [x] **BE-CORE-006**: Phát triển API Gateway Integration Utilities (Medium Priority)
  - Tạo các utilities để xử lý API Gateway events
  - Phát triển middleware cho request/response processing
  - Xây dựng cơ chế routing và endpoint discovery
  - Tích hợp với validation framework

- [ ] **BE-CORE-007**: Phát triển Database Migration Framework (Low Priority)
  - Xây dựng cơ chế version control cho database schema
  - Tạo utilities để thực hiện data migration
  - Phát triển tools cho schema verification
  - Triển khai cơ chế backup và rollback

## Business Logic & Services

- [ ] **BE-BIZ-001**: Xây dựng service cho business rules và calculations (Medium Priority)
  - Tính toán Margin từ cost và revenue
  - Xác định trạng thái Follow-up (Red/Yellow/Green)
  - Tính toán utilization rate của nhân viên
  - Phát triển các business rule engines

- [ ] **BE-BIZ-002**: Phát triển service notification (Low Priority)
  - Xây dựng template engine cho email
  - Tích hợp với dịch vụ gửi email (SES)
  - Phát triển in-app notifications
  - Tạo scheduler cho các thông báo định kỳ

- [ ] **BE-BIZ-003**: Phát triển service authentication và authorization (High Priority)
  - Tích hợp Lambda Authorizer cho API Gateway
  - Triển khai JWT handling và validation
  - Phát triển role-based access control
  - Xây dựng cơ chế refresh token

## Authentication & Authorization

- [ ] **BE-AUTH-001**: Triển khai Lambda function đăng nhập (High Priority)
  - POST /api/v1/auth/login
  - Xác thực người dùng và trả về token (JWT)
  - Xử lý các trường hợp thất bại (sai username/password, tài khoản bị khóa)

- [ ] **BE-AUTH-002**: Phát triển Lambda function đăng xuất (Medium Priority)
  - POST /api/v1/auth/logout
  - Hủy token phía server
  - Xóa thông tin session

- [ ] **BE-AUTH-003**: Triển khai Lambda function lấy thông tin người dùng hiện tại (High Priority)
  - GET /api/v1/auth/me
  - Lấy thông tin user và quyền của người dùng hiện tại
  - Lọc dữ liệu người dùng theo quyền truy cập

- [ ] **BE-AUTH-004**: Phát triển Lambda function làm mới token (Medium Priority)
  - POST /api/v1/auth/refresh-token
  - Làm mới access token sử dụng refresh token
  - Xử lý các trường hợp token hết hạn

## Module 1: Quản lý Nhân sự (HRM)

- [ ] **BE-HRM-001**: Triển khai Lambda functions quản lý thông tin nhân viên (CRUD) (High Priority)
  - GET /employees (list, filter, search)
  - POST /employees
  - GET /employees/{id}
  - PUT /employees/{id}
  - DELETE /employees/{id}

- [ ] **BE-HRM-002**: Phát triển Lambda functions quản lý skill categories (Medium Priority)
  - GET /skill-categories
  - POST /admin/skill-categories
  - PUT /admin/skill-categories/{id}
  - DELETE /admin/skill-categories/{id}

- [ ] **BE-HRM-003**: Phát triển Lambda functions quản lý skills (Medium Priority)
  - GET /skills
  - POST /admin/skills
  - PUT /admin/skills/{id}
  - DELETE /admin/skills/{id}

- [ ] **BE-HRM-004**: Triển khai Lambda functions quản lý skills của nhân viên (High Priority)
  - GET /employees/{id}/skills
  - POST /employees/{id}/skills
  - DELETE /employees/{id}/skills/{skillId}

- [ ] **BE-HRM-005**: Phát triển Lambda function tìm kiếm nhân viên theo skills (Medium Priority)
  - Implement advanced search functionality
  - Ranking and scoring based on skills matching

- [ ] **BE-HRM-006**: Triển khai Lambda function gợi ý nhân sự phù hợp (Medium Priority)
  - Implement recommendation algorithm
  - Calculate matching score

- [ ] **BE-HRM-007**: Phát triển Lambda functions quản lý trạng thái nhân viên (High Priority)
  - PUT /employees/{id}/status
  - Cập nhật trạng thái và phân bổ dự án

- [ ] **BE-HRM-008**: Triển khai Lambda function xem lịch sử dự án của nhân viên (Medium Priority)
  - GET /employees/{id}/project-history
  - Pagination và filtering

- [ ] **BE-HRM-009**: Phát triển Lambda functions import/export danh sách nhân viên (Low Priority)
  - POST /employees/import
  - GET /employees/export

## Module 2: Quản lý Hiệu suất & Margin

- [ ] **BE-MGN-001**: Triển khai Lambda functions quản lý chi phí nhân viên (High Priority)
  - POST /margins/costs/import
  - POST /margins/costs
  - Validate data và xử lý import

- [ ] **BE-MGN-002**: Phát triển Lambda function tính toán revenue (High Priority)
  - Calculate revenue based on project allocation and contract
  - Scheduled task để tính toán tự động định kỳ

- [ ] **BE-MGN-003**: Triển khai Lambda function tính toán margin (High Priority)
  - Calculate margin from cost and revenue
  - Determine Red/Yellow/Green status based on thresholds

- [ ] **BE-MGN-004**: Phát triển Lambda functions xem thông tin margin (High Priority)
  - GET /margins/employee
  - GET /margins/summary
  - Filter theo team, thời gian

## Module 3: Quản lý Cơ hội Kinh doanh

- [ ] **BE-OPP-001**: Triển khai Lambda functions đồng bộ dữ liệu từ Hubspot (High Priority)
  - Tạo service tích hợp với Hubspot API
  - POST /opportunities/sync (manual trigger)
  - Scheduled event cho đồng bộ tự động

- [ ] **BE-OPP-002**: Phát triển Lambda function xem log đồng bộ (Low Priority)
  - GET /opportunities/sync/logs
  - Filtering, pagination

- [ ] **BE-OPP-003**: Triển khai Lambda functions quản lý cơ hội (High Priority)
  - GET /opportunities (list, filter, search)
  - GET /opportunities/{id}
  - Tính toán trạng thái follow-up (Red/Yellow/Green)

- [ ] **BE-OPP-004**: Phát triển Lambda function gán Leader cho cơ hội (High Priority)
  - POST /opportunities/{id}/assign
  - Gửi notification cho người được assign

- [ ] **BE-OPP-005**: Triển khai Lambda functions quản lý ghi chú cơ hội (High Priority)
  - POST /opportunities/{id}/notes
  - GET /opportunities/{id}/notes
  - Cập nhật last_interaction_date

- [ ] **BE-OPP-006**: Phát triển Lambda function đánh dấu ưu tiên onsite (Medium Priority)
  - PUT /opportunities/{id}/onsite
  - Toggle trạng thái onsite priority

## Module 4: Quản lý Hợp đồng & Doanh thu

- [ ] **BE-CTR-001**: Triển khai Lambda functions quản lý hợp đồng (CRUD) (High Priority)
  - GET /contracts (list, filter, search)
  - POST /contracts
  - GET /contracts/{id}
  - PUT /contracts/{id}
  - DELETE /contracts/{id}

- [ ] **BE-CTR-002**: Phát triển Lambda functions quản lý điều khoản thanh toán (High Priority)
  - GET /contracts/{id}/payment-terms
  - PUT /contracts/payment-terms/{id}/status
  - POST /contracts/payment-terms/import-status

- [ ] **BE-CTR-003**: Triển khai Lambda functions quản lý file đính kèm (High Priority)
  - GET /contracts/{id}/files
  - POST /contracts/{id}/files
  - DELETE /contracts/files/{id}
  - Tích hợp với S3

- [ ] **BE-CTR-004**: Phát triển Lambda functions quản lý nhân sự trong hợp đồng (High Priority)
  - GET /contracts/{id}/employees
  - POST /contracts/{id}/employees
  - DELETE /contracts/{id}/employees/{employeeId}

- [ ] **BE-CTR-005**: Triển khai Lambda functions quản lý KPI doanh thu (High Priority)
  - GET /sales-kpis
  - POST /admin/sales-kpis
  - DELETE /admin/sales-kpis/{id}

## Module 5: Dashboard & Báo cáo

- [ ] **BE-RPT-001**: Phát triển Lambda function lấy dữ liệu tổng hợp cho dashboard (High Priority)
  - GET /dashboard/summary
  - Các metrics chính theo module

- [ ] **BE-RPT-002**: Triển khai Lambda functions cho các báo cáo chi tiết (Medium Priority)
  - GET /reports/employee-list
  - GET /reports/margin-detail
  - GET /reports/opportunity-list
  - GET /reports/contract-list
  - GET /reports/payment-status
  - GET /reports/kpi-progress
  - GET /reports/utilization

## Module 6: Quản trị Hệ thống (Admin)

- [ ] **BE-ADM-001**: Phát triển Lambda functions quản lý người dùng (Medium Priority)
  - GET /admin/users
  - POST /admin/users
  - GET /admin/users/{id}
  - PUT /admin/users/{id}
  - DELETE /admin/users/{id}

- [ ] **BE-ADM-002**: Triển khai Lambda functions quản lý vai trò và phân quyền (High Priority)
  - GET /admin/roles
  - POST /admin/roles
  - PUT /admin/roles/{id}
  - DELETE /admin/roles/{id}
  - GET /admin/permissions

- [ ] **BE-ADM-003**: Phát triển Lambda functions quản lý cấu hình hệ thống (Medium Priority)
  - GET /admin/configs
  - PUT /admin/configs/{key}
  - Cấu hình ngưỡng margin, follow-up, tích hợp API...

- [ ] **BE-ADM-004**: Triển khai Lambda function xem log hệ thống (Low Priority)
  - GET /admin/system-logs
  - Filtering, searching

## Testing

- [ ] **BE-TEST-001**: Viết unit tests cho các Lambda functions (High Priority)
  - Tests cho validation logic
  - Tests cho business rules
  - Mocking DynamoDB, S3

- [ ] **BE-TEST-002**: Viết integration tests (Medium Priority)
  - Tests cho end-to-end flows
  - API testing

- [ ] **BE-TEST-003**: Thiết lập môi trường testing (Medium Priority)
  - DynamoDB Local
  - Local API Gateway
  - Mock S3

## Deployment & Documentation

- [ ] **BE-DEPLOY-001**: Tạo script deployment cho các môi trường (High Priority)
  - Staging
  - Production

- [ ] **BE-DOC-001**: Viết tài liệu API (Swagger/OpenAPI) (Medium Priority)
  - Endpoints documentation
  - Request/response schemas
  - Error codes

- [ ] **BE-DOC-002**: Viết hướng dẫn sử dụng và deployment (Medium Priority)
  - Setup guide
  - Configuration guide
  - Troubleshooting

## Kết luận

Danh sách task trên đã chia nhỏ phần backend thành các công việc cụ thể dựa trên kiến trúc AWS SAM serverless. Các task được tổ chức theo module chức năng và được sắp xếp theo độ ưu tiên, mỗi task được gán một mã duy nhất theo định dạng BE-[Module]-[Number] để dễ theo dõi.

Để triển khai hiệu quả, nên bắt đầu với các task infrastructure và core services, sau đó triển khai các module chức năng theo thứ tự ưu tiên từ cao đến thấp. Testing và documentation nên được thực hiện song song với quá trình phát triển. 