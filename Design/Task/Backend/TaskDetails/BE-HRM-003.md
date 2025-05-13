**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda functions quản lý skills | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions quản lý skills (kỹ năng), phục vụ cho việc quản lý danh mục kỹ năng và hỗ trợ tìm kiếm, đề xuất nhân sự phù hợp dựa trên kỹ năng.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-003  
**Task Name:** Phát triển Lambda functions quản lý skills  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-002 (Phát triển Lambda functions quản lý skill categories)

**Các task phụ thuộc vào task này:** 
- BE-HRM-004 (Triển khai Lambda functions quản lý skills của nhân viên)
- BE-HRM-005 (Phát triển Lambda function tìm kiếm nhân viên theo skills)
- BE-HRM-006 (Triển khai Lambda function gợi ý nhân sự phù hợp)

**Các API:**
- GET /api/v1/skills (API-HRM-010)
- POST /api/v1/admin/skills (API-HRM-011)
- PUT /api/v1/admin/skills/{id} (API-HRM-012)
- DELETE /api/v1/admin/skills/{id} (API-HRM-013)

## Mô tả

Phát triển các Lambda functions để quản lý skills (kỹ năng) trong hệ thống. Skills là các kỹ năng cụ thể như "Java", "Python", "PostgreSQL", "AWS", "React", v.v. Mỗi skill sẽ thuộc về một skill category đã được định nghĩa trong task BE-HRM-002.

Hệ thống sẽ có hai loại API endpoint:
1. API public (GET /skills): Cho phép tất cả người dùng đã đăng nhập xem danh sách skills
2. API admin (POST, PUT, DELETE /admin/skills): Chỉ dành cho Admin và HR Manager quản lý skills

Các skills được định nghĩa sẽ là cơ sở để gán kỹ năng cho nhân viên, tìm kiếm nhân viên theo kỹ năng, và đề xuất nhân viên phù hợp cho dự án dựa trên yêu cầu kỹ năng.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách skills

- [ ] Triển khai Lambda function xử lý GET /api/v1/skills:
  - Location: src/functions/skills/list_skills.py
  - Triển khai logic lấy danh sách skills:
    - Xác thực người dùng đã đăng nhập
    - Lấy danh sách skills từ DynamoDB
    - Hỗ trợ các tham số filter:
      - categoryId: Lọc theo danh mục
      - searchText: Tìm kiếm theo tên skill
      - isActive: Lọc theo trạng thái active/inactive
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy, sortDirection
    - Bổ sung thông tin về danh mục của mỗi skill
    - Bổ sung thông tin số lượng nhân viên có skill
  - Tối ưu hiệu năng truy vấn sử dụng Global Secondary Index
  - Xử lý lỗi và logging

### Phát triển Lambda function thêm skill mới

- [ ] Triển khai Lambda function xử lý POST /api/v1/admin/skills:
  - Location: src/functions/skills/create_skill.py
  - Triển khai logic thêm skill mới:
    - Xác thực và phân quyền (chỉ Admin và HR Manager)
    - Validate dữ liệu đầu vào:
      - name: không được trùng với skills hiện có
      - category_id: phải tồn tại trong hệ thống
      - description: mô tả về skill
      - keywords: các từ khóa liên quan (để hỗ trợ tìm kiếm)
    - Tạo ID duy nhất cho skill
    - Lưu thông tin skill vào DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: trùng tên skill, category không tồn tại

### Phát triển Lambda function cập nhật skill

- [ ] Triển khai Lambda function xử lý PUT /api/v1/admin/skills/{id}:
  - Location: src/functions/skills/update_skill.py
  - Triển khai logic cập nhật skill:
    - Xác thực và phân quyền (chỉ Admin và HR Manager)
    - Validate dữ liệu đầu vào
    - Lấy thông tin hiện tại của skill
    - Cập nhật các trường được thay đổi
    - Lưu thông tin đã cập nhật vào DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: skill không tồn tại, trùng tên với skill khác, category mới không tồn tại

### Phát triển Lambda function xóa skill

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/admin/skills/{id}:
  - Location: src/functions/skills/delete_skill.py
  - Triển khai logic xóa skill:
    - Xác thực và phân quyền (chỉ Admin và HR Manager)
    - Kiểm tra ràng buộc dữ liệu (skill đã được gán cho nhân viên nào chưa?)
    - Xóa skill khỏi DynamoDB (hoặc đánh dấu là inactive)
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột dữ liệu
  - Cung cấp tùy chọn force delete (xóa bỏ cả các liên kết với nhân viên) cho Admin

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho skill:
  - Location: src/models/skill.py
  - Định nghĩa model cho skill:
    - Các trường cơ bản: id, name, description, category_id, keywords, difficulty_level, is_active, created_at, updated_at, v.v.
  - Triển khai các method truy vấn DynamoDB:
    - create_skill(skill_data)
    - get_skill(skill_id)
    - get_skills(filters, pagination)
    - update_skill(skill_id, skill_data)
    - delete_skill(skill_id)
    - get_skills_by_category(category_id)
    - search_skills(search_text)
    - get_skill_employee_count(skill_id)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/skills:
    - Method: GET
    - Các tham số query: categoryId, searchText, isActive, page, size, sortBy, sortDirection
    - Liên kết với Lambda function list_skills
    - Phân quyền: Authenticated Users
  - Cấu hình route POST /api/v1/admin/skills:
    - Method: POST
    - Request body: Thông tin skill
    - Liên kết với Lambda function create_skill
    - Phân quyền: Admin, HR Manager
  - Cấu hình route PUT /api/v1/admin/skills/{id}:
    - Method: PUT
    - Path parameter: id
    - Request body: Thông tin cập nhật
    - Liên kết với Lambda function update_skill
    - Phân quyền: Admin, HR Manager
  - Cấu hình route DELETE /api/v1/admin/skills/{id}:
    - Method: DELETE
    - Path parameter: id
    - Query parameter: force (boolean)
    - Liên kết với Lambda function delete_skill
    - Phân quyền: Admin, HR Manager
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/skills/
  - Test case cho list_skills.py:
    - Test lấy danh sách đầy đủ
    - Test phân trang
    - Test sắp xếp
    - Test filter theo category
    - Test tìm kiếm theo tên
    - Test filter theo active/inactive
  - Test case cho create_skill.py:
    - Test tạo skill thành công
    - Test với dữ liệu không hợp lệ
    - Test trùng tên skill
    - Test với category không tồn tại
    - Test phân quyền
  - Test case cho update_skill.py:
    - Test cập nhật thành công
    - Test với skill không tồn tại
    - Test trùng tên với skill khác
    - Test chuyển sang category không tồn tại
    - Test phân quyền
  - Test case cho delete_skill.py:
    - Test xóa thành công
    - Test xóa skill đã được gán cho nhân viên
    - Test force delete
    - Test phân quyền

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/skills
    - POST /api/v1/admin/skills
    - PUT /api/v1/admin/skills/{id}
    - DELETE /api/v1/admin/skills/{id}
  - Tài liệu quyền truy cập và sử dụng API
  - Tài liệu về cấu trúc dữ liệu skill

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách skills với các tham số filter:

```python
# Lấy danh sách skills theo category và tìm kiếm
import requests

def get_skills(api_base_url, token, category_id=None, search_text=None, is_active=True, page=1, size=20):
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
    
    if search_text:
        params['searchText'] = search_text
    
    if is_active is not None:
        params['isActive'] = str(is_active).lower()
    
    response = requests.get(
        f"{api_base_url}/api/v1/skills",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "skills": [
#       {
#         "id": "skill123",
#         "name": "Java",
#         "description": "Java programming language and ecosystem",
#         "keywords": ["Java SE", "J2EE", "Spring", "JVM"],
#         "difficulty_level": "Medium",
#         "category": {
#           "id": "cat456",
#           "name": "Programming Languages"
#         },
#         "employee_count": 12,
#         "is_active": true,
#         "created_at": "2025-01-20T10:15:00Z",
#         "updated_at": "2025-03-15T14:30:00Z"
#       },
#       {
#         "id": "skill124",
#         "name": "Python",
#         "description": "Python programming language and libraries",
#         "keywords": ["Python 3", "Django", "Flask", "Data Science"],
#         "difficulty_level": "Easy",
#         "category": {
#           "id": "cat456",
#           "name": "Programming Languages"
#         },
#         "employee_count": 8,
#         "is_active": true,
#         "created_at": "2025-01-22T09:45:00Z",
#         "updated_at": "2025-04-10T16:20:00Z"
#       },
#       // ... more skills
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 20,
#       "total_items": 45,
#       "total_pages": 3
#     }
#   }
# }
```

Ví dụ về cách thêm skill mới:

```python
# Thêm skill mới
import requests

def create_skill(api_base_url, token, skill_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/admin/skills",
        headers=headers,
        json=skill_data
    )
    
    return response.json()

# Dữ liệu đầu vào:
# skill_data = {
#   "name": "AWS Lambda",
#   "description": "Serverless compute service by AWS",
#   "category_id": "cat789",  # Cloud Technologies
#   "keywords": ["Serverless", "AWS", "FaaS", "Cloud Computing"],
#   "difficulty_level": "Medium",
#   "is_active": true
# }

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 201,
#   "message": "Skill đã được tạo thành công",
#   "data": {
#     "id": "skill125",
#     "name": "AWS Lambda",
#     "description": "Serverless compute service by AWS",
#     "keywords": ["Serverless", "AWS", "FaaS", "Cloud Computing"],
#     "difficulty_level": "Medium",
#     "category": {
#       "id": "cat789",
#       "name": "Cloud Technologies"
#     },
#     "employee_count": 0,
#     "is_active": true,
#     "created_at": "2025-05-13T15:20:00Z",
#     "updated_at": "2025-05-13T15:20:00Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách skills hoạt động chính xác với khả năng phân trang, sắp xếp, lọc và tìm kiếm
2. Lambda function thêm skill mới hoạt động chính xác với validation đầy đủ
3. Lambda function cập nhật skill hoạt động chính xác
4. Lambda function xóa skill hoạt động chính xác, bao gồm xử lý các ràng buộc dữ liệu
5. API endpoints được cấu hình đúng với phân quyền phù hợp
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 3 ngày làm việc

## Ghi chú

- Cấu trúc skill nên hỗ trợ các mức độ khó (difficulty levels) để giúp đánh giá năng lực nhân viên chính xác hơn
- Cần thiết kế cơ chế search hiệu quả, bao gồm full-text search và tìm kiếm qua từ khóa (keywords)
- Xem xét việc thêm trường weight hoặc importance cho skill để sử dụng trong thuật toán gợi ý nhân sự
- Khi xóa skill, cần cẩn thận với các tham chiếu đang tồn tại trong hệ thống
- Nên có khả năng import skills hàng loạt từ file (có thể phát triển trong tương lai) 