**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda functions quản lý skill categories | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda functions quản lý skill categories (danh mục kỹ năng), hỗ trợ cho việc phân loại và quản lý skills của nhân viên một cách có hệ thống.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-002  
**Task Name:** Phát triển Lambda functions quản lý skill categories 
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)

**Các task phụ thuộc vào task này:** 
- BE-HRM-003 (Phát triển Lambda functions quản lý skills)
- BE-HRM-004 (Triển khai Lambda functions quản lý skills của nhân viên)
- BE-HRM-005 (Phát triển Lambda function tìm kiếm nhân viên theo skills)

**Các API:**
- GET /api/v1/skill-categories (API-HRM-006)
- POST /api/v1/admin/skill-categories (API-HRM-007)
- PUT /api/v1/admin/skill-categories/{id} (API-HRM-008)
- DELETE /api/v1/admin/skill-categories/{id} (API-HRM-009)

## Mô tả

Phát triển các Lambda functions để quản lý skill categories (danh mục kỹ năng) trong hệ thống. Skill categories là các nhóm phân loại kỹ năng như "Programming Languages", "Databases", "Frameworks", "DevOps Tools", v.v. Việc phân loại này giúp cho việc quản lý và tìm kiếm skills trở nên có tổ chức và hiệu quả hơn.

Hệ thống sẽ có hai loại API endpoint:
1. API public (GET /skill-categories): Cho phép tất cả người dùng đã đăng nhập xem danh sách skill categories
2. API admin (POST, PUT, DELETE /admin/skill-categories): Chỉ dành cho Admin và HR Manager quản lý skill categories

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách skill categories

- [ ] Triển khai Lambda function xử lý GET /api/v1/skill-categories:
  - Location: src/functions/skill_categories/list_skill_categories.py
  - Triển khai logic lấy danh sách skill categories:
    - Xác thực người dùng đã đăng nhập
    - Lấy danh sách skill categories từ DynamoDB
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy, sortDirection
    - Hỗ trợ filter: active/inactive
    - Bổ sung thông tin số lượng skills trong mỗi category
  - Tối ưu hiệu năng truy vấn
  - Xử lý lỗi và logging

### Phát triển Lambda function thêm skill category mới

- [ ] Triển khai Lambda function xử lý POST /api/v1/admin/skill-categories:
  - Location: src/functions/skill_categories/create_skill_category.py
  - Triển khai logic thêm skill category mới:
    - Xác thực và phân quyền (chỉ Admin và HR Manager)
    - Validate dữ liệu đầu vào (name, description không được trùng)
    - Tạo ID duy nhất cho skill category
    - Lưu thông tin skill category vào DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: trùng tên category, dữ liệu không hợp lệ

### Phát triển Lambda function cập nhật skill category

- [ ] Triển khai Lambda function xử lý PUT /api/v1/admin/skill-categories/{id}:
  - Location: src/functions/skill_categories/update_skill_category.py
  - Triển khai logic cập nhật skill category:
    - Xác thực và phân quyền (chỉ Admin và HR Manager)
    - Validate dữ liệu đầu vào
    - Lấy thông tin hiện tại của skill category
    - Cập nhật các trường được thay đổi
    - Lưu thông tin đã cập nhật vào DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: category không tồn tại, trùng tên với category khác

### Phát triển Lambda function xóa skill category

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/admin/skill-categories/{id}:
  - Location: src/functions/skill_categories/delete_skill_category.py
  - Triển khai logic xóa skill category:
    - Xác thực và phân quyền (chỉ Admin và HR Manager)
    - Kiểm tra ràng buộc dữ liệu (category có chứa skills không?)
    - Xóa skill category khỏi DynamoDB (hoặc đánh dấu là inactive)
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột dữ liệu
  - Cung cấp tùy chọn force delete (xóa bỏ cả các skills thuộc category) cho Admin

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho skill category:
  - Location: src/models/skill_category.py
  - Định nghĩa model cho skill category:
    - Các trường cơ bản: id, name, description, created_at, updated_at, is_active, v.v.
  - Triển khai các method truy vấn DynamoDB:
    - create_skill_category(category_data)
    - get_skill_category(category_id)
    - get_skill_categories(filters, pagination)
    - update_skill_category(category_id, category_data)
    - delete_skill_category(category_id)
    - get_category_skills_count(category_id)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/skill-categories:
    - Method: GET
    - Các tham số query: page, size, sortBy, sortDirection, isActive
    - Liên kết với Lambda function list_skill_categories
    - Phân quyền: Authenticated Users
  - Cấu hình route POST /api/v1/admin/skill-categories:
    - Method: POST
    - Request body: Thông tin skill category
    - Liên kết với Lambda function create_skill_category
    - Phân quyền: Admin, HR Manager
  - Cấu hình route PUT /api/v1/admin/skill-categories/{id}:
    - Method: PUT
    - Path parameter: id
    - Request body: Thông tin cập nhật
    - Liên kết với Lambda function update_skill_category
    - Phân quyền: Admin, HR Manager
  - Cấu hình route DELETE /api/v1/admin/skill-categories/{id}:
    - Method: DELETE
    - Path parameter: id
    - Query parameter: force (boolean)
    - Liên kết với Lambda function delete_skill_category
    - Phân quyền: Admin, HR Manager
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/skill_categories/
  - Test case cho list_skill_categories.py:
    - Test lấy danh sách đầy đủ
    - Test phân trang
    - Test sắp xếp
    - Test filter theo active/inactive
  - Test case cho create_skill_category.py:
    - Test tạo category thành công
    - Test với dữ liệu không hợp lệ
    - Test trùng tên category
    - Test phân quyền
  - Test case cho update_skill_category.py:
    - Test cập nhật thành công
    - Test với category không tồn tại
    - Test trùng tên với category khác
    - Test phân quyền
  - Test case cho delete_skill_category.py:
    - Test xóa thành công
    - Test xóa category có chứa skills
    - Test force delete
    - Test phân quyền

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/skill-categories
    - POST /api/v1/admin/skill-categories
    - PUT /api/v1/admin/skill-categories/{id}
    - DELETE /api/v1/admin/skill-categories/{id}
  - Tài liệu quyền truy cập và sử dụng API
  - Tài liệu về cấu trúc dữ liệu skill category

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách skill categories:

```python
# Lấy danh sách skill categories
import requests

def get_skill_categories(api_base_url, token, is_active=True, page=1, size=10, sort_by='name', sort_direction='asc'):
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
    
    if is_active is not None:
        params['isActive'] = str(is_active).lower()
    
    response = requests.get(
        f"{api_base_url}/api/v1/skill-categories",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "categories": [
#       {
#         "id": "cat123",
#         "name": "Programming Languages",
#         "description": "Languages used for software development",
#         "skills_count": 15,
#         "is_active": true,
#         "created_at": "2025-01-15T08:30:00Z",
#         "updated_at": "2025-04-20T14:45:00Z"
#       },
#       {
#         "id": "cat456",
#         "name": "Databases",
#         "description": "Database technologies and systems",
#         "skills_count": 8,
#         "is_active": true,
#         "created_at": "2025-01-15T09:15:00Z",
#         "updated_at": "2025-03-10T11:20:00Z"
#       },
#       // ... more categories
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 10,
#       "total_items": 12,
#       "total_pages": 2
#     }
#   }
# }
```

Ví dụ về cách thêm skill category mới:

```python
# Thêm skill category mới
import requests

def create_skill_category(api_base_url, token, category_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/admin/skill-categories",
        headers=headers,
        json=category_data
    )
    
    return response.json()

# Dữ liệu đầu vào:
# category_data = {
#   "name": "Cloud Technologies",
#   "description": "Skills related to cloud platforms and services",
#   "is_active": true
# }

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 201,
#   "message": "Skill category đã được tạo thành công",
#   "data": {
#     "id": "cat789",
#     "name": "Cloud Technologies",
#     "description": "Skills related to cloud platforms and services",
#     "skills_count": 0,
#     "is_active": true,
#     "created_at": "2025-05-13T11:45:00Z",
#     "updated_at": "2025-05-13T11:45:00Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách skill categories hoạt động chính xác với khả năng phân trang, sắp xếp và lọc
2. Lambda function thêm skill category mới hoạt động chính xác với validation đầy đủ
3. Lambda function cập nhật skill category hoạt động chính xác
4. Lambda function xóa skill category hoạt động chính xác, bao gồm xử lý các ràng buộc dữ liệu
5. API endpoints được cấu hình đúng với phân quyền phù hợp
6. Unit tests đạt coverage > 80%
7. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- Nên thiết kế hệ thống skill categories có tính mở rộng để dễ dàng thêm các loại kỹ năng mới trong tương lai
- Cân nhắc việc hỗ trợ phân cấp (hierarchical) cho skill categories (ví dụ: Programming Languages > OOP Languages > Java)
- Đảm bảo bảo mật và phân quyền chặt chẽ cho các API admin
- Cần có cơ chế xử lý khi xóa một category có chứa skills (ví dụ: di chuyển skills sang Uncategorized) 