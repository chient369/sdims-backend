**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý skills của nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý skills của nhân viên, cho phép gán, cập nhật và xóa các kỹ năng của nhân viên, phục vụ cho việc tìm kiếm nhân sự phù hợp và phát triển nghề nghiệp.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-004  
**Task Name:** Triển khai Lambda functions quản lý skills của nhân viên  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)
- BE-HRM-003 (Phát triển Lambda functions quản lý skills)

**Các task phụ thuộc vào task này:** 
- BE-HRM-005 (Phát triển Lambda function tìm kiếm nhân viên theo skills)
- BE-HRM-006 (Triển khai Lambda function gợi ý nhân sự phù hợp)

**Các API:**
- GET /api/v1/employees/{id}/skills (API-HRM-014)
- POST /api/v1/employees/{id}/skills (API-HRM-015)
- DELETE /api/v1/employees/{id}/skills/{skillId} (API-HRM-016)

## Mô tả

Triển khai các Lambda functions để quản lý skills của nhân viên trong hệ thống. Cho phép các chức năng:
- Xem danh sách skills của một nhân viên cụ thể
- Thêm hoặc cập nhật skills cho nhân viên, bao gồm mức độ thành thạo và các thông tin liên quan
- Xóa skill khỏi hồ sơ của nhân viên

Việc quản lý skills của nhân viên là cơ sở để thực hiện các chức năng tìm kiếm, đề xuất nhân sự phù hợp cho dự án, và theo dõi sự phát triển nghề nghiệp của nhân viên.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách skills của nhân viên

- [ ] Triển khai Lambda function xử lý GET /api/v1/employees/{id}/skills:
  - Location: src/functions/employee_skills/list_employee_skills.py
  - Triển khai logic lấy danh sách skills của nhân viên:
    - Xác thực người dùng đã đăng nhập
    - Kiểm tra quyền xem thông tin nhân viên
    - Lấy danh sách skills của nhân viên từ DynamoDB
    - Hỗ trợ các tham số filter:
      - categoryId: Lọc theo danh mục skill
      - proficiencyLevel: Lọc theo mức độ thành thạo
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy (name, proficiency, updatedAt), sortDirection
    - Bổ sung thông tin chi tiết về mỗi skill
  - Tối ưu hiệu năng truy vấn sử dụng Global Secondary Index
  - Xử lý lỗi và logging

### Phát triển Lambda function thêm/cập nhật skills cho nhân viên

- [ ] Triển khai Lambda function xử lý POST /api/v1/employees/{id}/skills:
  - Location: src/functions/employee_skills/add_employee_skills.py
  - Triển khai logic thêm/cập nhật skills:
    - Xác thực và phân quyền (Admin, HR Manager, Team Leader của nhân viên đó, hoặc chính nhân viên)
    - Validate dữ liệu đầu vào:
      - skillId: ID của skill đã tồn tại trong hệ thống
      - proficiencyLevel: Mức độ thành thạo (1-5 hoặc Beginner/Intermediate/Advanced/Expert)
      - yearsOfExperience: Số năm kinh nghiệm với skill
      - notes: Ghi chú thêm về skill
      - isCertified: Có chứng chỉ hay không
      - certificationDetails: Chi tiết về chứng chỉ (nếu có)
    - Kiểm tra skill đã tồn tại cho nhân viên chưa (để update hoặc insert)
    - Lưu thông tin skill vào bảng EMPLOYEE_SKILLS trong DynamoDB
    - Hỗ trợ cập nhật hàng loạt nhiều skills (batch update)
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: skill không tồn tại, nhân viên không tồn tại

### Phát triển Lambda function xóa skill của nhân viên

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/employees/{id}/skills/{skillId}:
  - Location: src/functions/employee_skills/remove_employee_skill.py
  - Triển khai logic xóa skill:
    - Xác thực và phân quyền (Admin, HR Manager, Team Leader của nhân viên đó)
    - Kiểm tra skill có tồn tại cho nhân viên không
    - Xóa liên kết skill với nhân viên khỏi DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và ngoại lệ

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho employee skills:
  - Location: src/models/employee_skill.py
  - Định nghĩa model cho liên kết employee-skill:
    - Các trường cơ bản: employee_id, skill_id, proficiency_level, years_of_experience, is_certified, certification_details, notes, last_used_date, created_at, updated_at, v.v.
  - Triển khai các method truy vấn DynamoDB:
    - create_employee_skill(employee_id, skill_data)
    - update_employee_skill(employee_id, skill_id, skill_data)
    - get_employee_skill(employee_id, skill_id)
    - get_employee_skills(employee_id, filters, pagination)
    - delete_employee_skill(employee_id, skill_id)
    - batch_add_employee_skills(employee_id, skills_data)
    - get_employees_by_skill(skill_id, filters)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/employees/{id}/skills:
    - Method: GET
    - Path parameter: id (employee_id)
    - Các tham số query: categoryId, proficiencyLevel, page, size, sortBy, sortDirection
    - Liên kết với Lambda function list_employee_skills
    - Phân quyền: Authenticated Users (với ràng buộc quyền xem)
  - Cấu hình route POST /api/v1/employees/{id}/skills:
    - Method: POST
    - Path parameter: id (employee_id)
    - Request body: Thông tin skill hoặc mảng skills
    - Liên kết với Lambda function add_employee_skills
    - Phân quyền: Admin, HR Manager, Team Leader, Self (chính nhân viên đó)
  - Cấu hình route DELETE /api/v1/employees/{id}/skills/{skillId}:
    - Method: DELETE
    - Path parameters: id (employee_id), skillId
    - Liên kết với Lambda function remove_employee_skill
    - Phân quyền: Admin, HR Manager, Team Leader
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/employee_skills/
  - Test case cho list_employee_skills.py:
    - Test lấy danh sách skills của nhân viên
    - Test phân trang
    - Test sắp xếp
    - Test filter theo category
    - Test filter theo proficiency
    - Test phân quyền
  - Test case cho add_employee_skills.py:
    - Test thêm skill mới cho nhân viên
    - Test cập nhật skill hiện có
    - Test thêm hàng loạt nhiều skills
    - Test với dữ liệu không hợp lệ
    - Test với skill không tồn tại
    - Test phân quyền
  - Test case cho remove_employee_skill.py:
    - Test xóa skill thành công
    - Test xóa skill không tồn tại
    - Test phân quyền

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/employees/{id}/skills
    - POST /api/v1/employees/{id}/skills
    - DELETE /api/v1/employees/{id}/skills/{skillId}
  - Tài liệu quyền truy cập và sử dụng API
  - Tài liệu về cấu trúc dữ liệu và mức độ thành thạo (proficiency levels)

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách skills của nhân viên:

```python
# Lấy danh sách skills của nhân viên
import requests

def get_employee_skills(api_base_url, token, employee_id, category_id=None, proficiency_level=None, page=1, size=20):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page': page,
        'size': size
    }
    
    if category_id:
        params['categoryId'] = category_id
    
    if proficiency_level:
        params['proficiencyLevel'] = proficiency_level
    
    response = requests.get(
        f"{api_base_url}/api/v1/employees/{employee_id}/skills",
        headers=headers,
        params=params
    )
    
    return response.json()

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
#     "skills": [
#       {
#         "skill": {
#           "id": "skill123",
#           "name": "Java",
#           "description": "Java programming language and ecosystem",
#           "category": {
#             "id": "cat456",
#             "name": "Programming Languages"
#           }
#         },
#         "proficiency_level": 4,
#         "proficiency_text": "Advanced",
#         "years_of_experience": 5,
#         "is_certified": true,
#         "certification_details": "Oracle Certified Professional Java SE 11 Developer",
#         "notes": "Chuyên gia Spring Boot, có kinh nghiệm với microservices",
#         "last_used_date": "2025-04-30",
#         "created_at": "2024-02-15T10:30:00Z",
#         "updated_at": "2025-01-10T15:45:00Z"
#       },
#       {
#         "skill": {
#           "id": "skill456",
#           "name": "AWS",
#           "description": "Amazon Web Services cloud platform",
#           "category": {
#             "id": "cat789",
#             "name": "Cloud Technologies"
#           }
#         },
#         "proficiency_level": 3,
#         "proficiency_text": "Intermediate",
#         "years_of_experience": 2,
#         "is_certified": true,
#         "certification_details": "AWS Certified Solutions Architect - Associate",
#         "notes": "Kinh nghiệm với EC2, S3, Lambda, DynamoDB",
#         "last_used_date": "2025-05-01",
#         "created_at": "2024-06-20T09:15:00Z",
#         "updated_at": "2025-03-05T11:30:00Z"
#       },
#       // ... more skills
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 20,
#       "total_items": 8,
#       "total_pages": 1
#     }
#   }
# }
```

Ví dụ về cách thêm/cập nhật skills cho nhân viên:

```python
# Thêm/cập nhật skills cho nhân viên
import requests

def add_employee_skills(api_base_url, token, employee_id, skills_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/employees/{employee_id}/skills",
        headers=headers,
        json=skills_data
    )
    
    return response.json()

# Dữ liệu đầu vào (một skill):
# skill_data = {
#   "skill_id": "skill789",
#   "proficiency_level": 3,
#   "years_of_experience": 2,
#   "is_certified": false,
#   "notes": "Đang học và phát triển dự án với React"
# }

# Dữ liệu đầu vào (nhiều skills - batch update):
# skills_data = [
#   {
#     "skill_id": "skill789",
#     "proficiency_level": 3,
#     "years_of_experience": 2,
#     "is_certified": false,
#     "notes": "Đang học và phát triển dự án với React"
#   },
#   {
#     "skill_id": "skill567",
#     "proficiency_level": 4,
#     "years_of_experience": 4,
#     "is_certified": true,
#     "certification_details": "Microsoft Certified: Azure Developer Associate",
#     "notes": "Chuyên sâu về Azure Functions và Cosmos DB"
#   }
# ]

# Kết quả mong đợi (cập nhật một skill):
# {
#   "status": "success",
#   "code": 200,
#   "message": "Skill đã được thêm/cập nhật thành công",
#   "data": {
#     "employee_id": "emp123",
#     "skill": {
#       "id": "skill789",
#       "name": "React",
#       "category": {
#         "id": "cat012",
#         "name": "Frontend Technologies"
#       }
#     },
#     "proficiency_level": 3,
#     "proficiency_text": "Intermediate",
#     "years_of_experience": 2,
#     "is_certified": false,
#     "updated_at": "2025-05-13T16:30:00Z"
#   }
# }

# Kết quả mong đợi (cập nhật nhiều skills):
# {
#   "status": "success",
#   "code": 200,
#   "message": "Skills đã được thêm/cập nhật thành công",
#   "data": {
#     "employee_id": "emp123",
#     "total_updated": 2,
#     "updated_skills": [
#       {
#         "id": "skill789",
#         "name": "React"
#       },
#       {
#         "id": "skill567",
#         "name": "Azure"
#       }
#     ],
#     "updated_at": "2025-05-13T16:30:00Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách skills của nhân viên hoạt động chính xác với khả năng phân trang, sắp xếp và lọc
2. Lambda function thêm/cập nhật skills cho nhân viên hoạt động chính xác, bao gồm cả chức năng cập nhật hàng loạt
3. Lambda function xóa skill của nhân viên hoạt động chính xác
4. API endpoints được cấu hình đúng với phân quyền phù hợp
5. Unit tests đạt coverage > 80%
6. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Cần thiết kế mô hình dữ liệu linh hoạt để hỗ trợ các mức độ thành thạo và chi tiết khác nhau cho mỗi skill
- Có thể xem xét việc thêm tính năng tự đánh giá định kỳ của nhân viên về các kỹ năng của họ
- Cân nhắc việc triển khai tính năng xác thực kỹ năng bởi đồng nghiệp hoặc quản lý
- Các mức độ thành thạo nên được chuẩn hóa (ví dụ: 1=Beginner, 2=Elementary, 3=Intermediate, 4=Advanced, 5=Expert)
- API cần hỗ trợ cả scenario người dùng tự cập nhật kỹ năng và HR/quản lý cập nhật kỹ năng 