**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function xem lịch sử dự án của nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function xem lịch sử dự án của nhân viên, hỗ trợ việc đánh giá kinh nghiệm và theo dõi quá trình phát triển nghề nghiệp của nhân viên.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-008  
**Task Name:** Triển khai Lambda function xem lịch sử dự án của nhân viên  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)
- BE-HRM-007 (Phát triển Lambda functions quản lý trạng thái nhân viên)

**Các task phụ thuộc vào task này:** 
- BE-HRM-006 (Triển khai Lambda function gợi ý nhân sự phù hợp)
- BE-RPT-002 (Triển khai Lambda functions cho các báo cáo chi tiết)

**Các API:**
- GET /api/v1/employees/{id}/project-history (API-HRM-021)

## Mô tả

Triển khai Lambda function cho phép xem lịch sử dự án của nhân viên, bao gồm thông tin chi tiết về các dự án mà nhân viên đã tham gia, vai trò, kỹ năng sử dụng, thời gian tham gia và đánh giá hiệu suất. Chức năng này giúp:
- Theo dõi lộ trình sự nghiệp của nhân viên
- Đánh giá mức độ kinh nghiệm trên các loại dự án và công nghệ khác nhau
- Hỗ trợ việc đánh giá hiệu suất và phát triển chuyên môn
- Cung cấp dữ liệu cho thuật toán đề xuất nhân sự phù hợp

Dữ liệu lịch sử dự án sẽ được thu thập tự động từ các hoạt động phân bổ nhân viên vào dự án (employee allocation) và thay đổi trạng thái, đồng thời cho phép bổ sung thông tin đánh giá và ghi chú.

## Chi tiết công việc

### Phát triển Lambda function xem lịch sử dự án

- [ ] Triển khai Lambda function xử lý GET /api/v1/employees/{id}/project-history:
  - Location: src/functions/employee_project_history/get_project_history.py
  - Triển khai logic lấy lịch sử dự án:
    - Xác thực người dùng đã đăng nhập
    - Phân quyền (Admin, HR Manager, Division Manager, Team Leader, hoặc chính nhân viên đó)
    - Lấy danh sách lịch sử dự án của nhân viên từ DynamoDB
    - Xử lý các tham số filter:
      - startDate: Lọc theo thời gian bắt đầu (từ ngày)
      - endDate: Lọc theo thời gian kết thúc (đến ngày)
      - projectId: Lọc theo dự án cụ thể
      - projectType: Lọc theo loại dự án
      - role: Lọc theo vai trò trong dự án
      - skillsUsed: Lọc theo kỹ năng đã sử dụng
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy (startDate, endDate, projectName), sortDirection
    - Tổng hợp thông tin phụ (số dự án, tổng thời gian, phân bố theo loại dự án)
  - Tối ưu hiệu năng truy vấn và caching
  - Xử lý lỗi và logging

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho project history:
  - Location: src/models/employee_project_history.py
  - Định nghĩa model cho lịch sử dự án của nhân viên:
    - Các trường cơ bản: employee_id, project_id, project_name, project_type, role, start_date, end_date, allocation_percentage, skills_used, responsibilities, achievements, performance_rating, feedback, client_feedback, notes, v.v.
  - Triển khai các method truy vấn DynamoDB:
    - get_employee_project_history(employee_id, filters, pagination)
    - get_project_history_summary(employee_id)
    - get_project_history_by_id(employee_id, project_history_id)
    - get_active_project(employee_id, date)
    - get_projects_by_skill(employee_id, skill_id)
    - update_project_history_item(employee_id, project_history_id, update_data)

### Phát triển Cơ chế Tự động Cập nhật Lịch sử

- [ ] Triển khai service tự động cập nhật lịch sử dự án:
  - Location: src/services/project_history_updater.py
  - Triển khai các hàm:
    - auto_create_project_history(employee_id, project_id, status_change_data): Tự động tạo bản ghi lịch sử khi nhân viên được phân bổ vào dự án
    - auto_update_project_end_date(employee_id, project_id, end_date): Cập nhật ngày kết thúc khi nhân viên rời dự án
    - auto_update_project_details(employee_id, project_id, project_details): Cập nhật thông tin dự án khi dự án thay đổi
    - notify_for_evaluation(employee_id, project_id): Gửi thông báo để đánh giá khi dự án kết thúc
  - Tích hợp với DynamoDB Streams để phản ứng với thay đổi trạng thái nhân viên

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/employees/{id}/project-history:
    - Method: GET
    - Path parameter: id (employee_id)
    - Các tham số query: startDate, endDate, projectId, projectType, role, skillsUsed, page, size, sortBy, sortDirection
    - Liên kết với Lambda function get_project_history
    - Phân quyền: Admin, HR Manager, Division Manager, Team Leader, Self (chính nhân viên đó)
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/employee_project_history/
  - Test case cho get_project_history.py:
    - Test lấy lịch sử dự án của nhân viên
    - Test phân trang
    - Test sắp xếp
    - Test filter theo các tiêu chí khác nhau
    - Test tính toán thống kê tổng hợp
    - Test phân quyền
  - Test case cho project_history_updater.py:
    - Test tự động tạo bản ghi lịch sử
    - Test cập nhật ngày kết thúc
    - Test cập nhật thông tin dự án

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho endpoint:
    - GET /api/v1/employees/{id}/project-history
  - Tài liệu về cấu trúc dữ liệu lịch sử dự án
  - Tài liệu về cơ chế tự động cập nhật lịch sử
  - Hướng dẫn sử dụng API với các scenarios thực tế

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy lịch sử dự án của nhân viên:

```python
# Lấy lịch sử dự án của nhân viên
import requests

def get_employee_project_history(api_base_url, token, employee_id, start_date=None, 
                               end_date=None, project_type=None, role=None, 
                               page=1, size=10, sort_by="startDate", sort_direction="desc"):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page': page,
        'size': size,
        'sortBy': sort_by,
        'sortDirection': sort_direction
    }
    
    if start_date:
        params['startDate'] = start_date
    
    if end_date:
        params['endDate'] = end_date
    
    if project_type:
        params['projectType'] = project_type
    
    if role:
        params['role'] = role
    
    response = requests.get(
        f"{api_base_url}/api/v1/employees/{employee_id}/project-history",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ gọi hàm:
# result = get_employee_project_history(
#     api_base_url="https://api.example.com",
#     token="your_auth_token",
#     employee_id="emp123",
#     start_date="2023-01-01",
#     project_type="Web Application",
#     sort_by="endDate",
#     sort_direction="desc"
# )

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "employee": {
#       "id": "emp123",
#       "employee_code": "E001",
#       "full_name": "Nguyễn Văn A"
#     },
#     "summary": {
#       "total_projects": 5,
#       "total_duration_months": 24,
#       "project_types_distribution": {
#         "Web Application": 3,
#         "Mobile Application": 1,
#         "System Integration": 1
#       },
#       "roles_distribution": {
#         "Developer": 2,
#         "Technical Lead": 2,
#         "Architect": 1
#       },
#       "most_used_skills": [
#         {"name": "Java", "count": 4},
#         {"name": "AWS", "count": 3},
#         {"name": "React", "count": 2}
#       ]
#     },
#     "project_history": [
#       {
#         "id": "ph001",
#         "project": {
#           "id": "proj123",
#           "name": "Banking System",
#           "type": "Web Application",
#           "client": "ABC Bank",
#           "description": "Hệ thống ngân hàng điện tử với đầy đủ tính năng giao dịch và quản lý"
#         },
#         "role": "Technical Lead",
#         "start_date": "2024-10-01",
#         "end_date": "2025-03-15",
#         "duration_months": 5.5,
#         "allocation_percentage": 100,
#         "skills_used": [
#           {"id": "skill123", "name": "Java"},
#           {"id": "skill456", "name": "AWS"},
#           {"id": "skill789", "name": "React"}
#         ],
#         "responsibilities": [
#           "Thiết kế kiến trúc hệ thống",
#           "Hướng dẫn đội phát triển",
#           "Code review và đảm bảo chất lượng"
#         ],
#         "achievements": [
#           "Hoàn thành dự án trước deadline 2 tuần",
#           "Cải thiện hiệu năng hệ thống tăng 40%"
#         ],
#         "performance_rating": 4.8,
#         "feedback": "Thể hiện khả năng lãnh đạo và kỹ thuật xuất sắc trong dự án phức tạp",
#         "client_feedback": "Rất hài lòng với chất lượng sản phẩm và tinh thần làm việc"
#       },
#       {
#         "id": "ph002",
#         "project": {
#           "id": "proj456",
#           "name": "E-commerce Platform",
#           "type": "Web Application",
#           "client": "XYZ Retail",
#           "description": "Nền tảng thương mại điện tử tích hợp với hệ thống quản lý kho và thanh toán"
#         },
#         "role": "Architect",
#         "start_date": "2024-03-01",
#         "end_date": "2024-09-30",
#         "duration_months": 7,
#         "allocation_percentage": 80,
#         "skills_used": [
#           {"id": "skill123", "name": "Java"},
#           {"id": "skill456", "name": "AWS"},
#           {"id": "skill321", "name": "Microservices"}
#         ],
#         "responsibilities": [
#           "Thiết kế kiến trúc microservices",
#           "Xây dựng CI/CD pipeline",
#           "Đảm bảo khả năng mở rộng hệ thống"
#         ],
#         "achievements": [
#           "Xây dựng hệ thống có khả năng xử lý 10,000 giao dịch/phút",
#           "Đạt AWS Well-Architected Framework"
#         ],
#         "performance_rating": 4.9,
#         "feedback": "Đóng góp xuất sắc vào việc xây dựng kiến trúc bền vững, khả năng mở rộng cao",
#         "client_feedback": "Ấn tượng với khả năng thiết kế hệ thống mạnh mẽ và linh hoạt"
#       },
#       // ... more project history items
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 10,
#       "total_items": 5,
#       "total_pages": 1
#     }
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function xem lịch sử dự án hoạt động chính xác với khả năng phân trang, sắp xếp và lọc
2. Có thể hiển thị đầy đủ thông tin chi tiết về các dự án mà nhân viên đã tham gia
3. Thống kê tổng hợp về lịch sử dự án chính xác và đầy đủ
4. Cơ chế tự động cập nhật lịch sử dự án hoạt động đúng
5. API endpoint được cấu hình đúng với phân quyền phù hợp
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Dữ liệu lịch sử dự án nên được thiết kế để dễ dàng mở rộng thêm các thông tin trong tương lai
- Cần có cơ chế tự động ghi nhận khi nhân viên được phân bổ vào dự án mới hoặc kết thúc dự án
- Xem xét việc cho phép Team Leader hoặc Project Manager bổ sung thông tin đánh giá và feedback sau khi dự án kết thúc
- Thông tin về lịch sử dự án rất quan trọng cho việc đánh giá hiệu suất và phát triển nghề nghiệp, cần đảm bảo tính chính xác
- Cần lưu ý về quyền riêng tư khi hiển thị thông tin đánh giá và feedback chi tiết 