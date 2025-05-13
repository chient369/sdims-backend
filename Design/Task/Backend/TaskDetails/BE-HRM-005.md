**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task phát triển Lambda function tìm kiếm nhân viên theo skills | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để phát triển Lambda function tìm kiếm nhân viên dựa trên skills, giúp tìm kiếm nhân sự phù hợp cho dự án và tối ưu hóa việc phân bổ nguồn lực.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-005  
**Task Name:** Phát triển Lambda function tìm kiếm nhân viên theo skills  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-HRM-001 (Triển khai Lambda functions quản lý thông tin nhân viên)
- BE-HRM-003 (Phát triển Lambda functions quản lý skills)
- BE-HRM-004 (Triển khai Lambda functions quản lý skills của nhân viên)

**Các task phụ thuộc vào task này:** 
- BE-HRM-006 (Triển khai Lambda function gợi ý nhân sự phù hợp)

**Các API:**
- GET /api/v1/employees/search/skills (API-HRM-017)

## Mô tả

Phát triển Lambda function cho phép tìm kiếm nhân viên dựa trên các yêu cầu về kỹ năng (skills), bao gồm khả năng tìm kiếm nâng cao với các tùy chọn lọc phức tạp. Hệ thống sẽ trả về danh sách nhân viên phù hợp, được xếp hạng theo mức độ phù hợp với các kỹ năng yêu cầu.

Tính năng này đặc biệt hữu ích cho việc tìm kiếm nhân sự phù hợp cho dự án mới, thay thế nhân sự, hoặc phân bổ nguồn lực hiệu quả. Kết quả tìm kiếm sẽ bao gồm thông tin về mức độ phù hợp của mỗi nhân viên với yêu cầu skill, trạng thái hiện tại của họ (đã được phân bổ hay chưa), và thời gian khả dụng.

## Chi tiết công việc

### Phát triển Lambda function tìm kiếm nhân viên theo skills

- [ ] Triển khai Lambda function xử lý GET /api/v1/employees/search/skills:
  - Location: src/functions/employee_search/search_by_skills.py
  - Triển khai logic tìm kiếm:
    - Xác thực người dùng đã đăng nhập
    - Phân quyền (Admin, HR Manager, Division Manager, Project Manager, Team Leader)
    - Xử lý các tham số tìm kiếm:
      - skills: Danh sách ID các skills cần tìm (required)
      - minProficiency: Mức độ thành thạo tối thiểu cho mỗi skill (optional)
      - matchType: ALL (phải có tất cả skills) hoặc ANY (có bất kỳ skill nào) (default: ANY)
      - availability: Trạng thái khả dụng của nhân viên (Available, PartiallyAllocated, All) (default: All)
      - availableFrom: Ngày nhân viên khả dụng từ (optional)
      - minExperience: Số năm kinh nghiệm tối thiểu cho skill (optional)
      - teamId: Lọc theo team (optional)
      - certifiedOnly: Chỉ lấy nhân viên có chứng chỉ (optional, default: false)
    - Triển khai thuật toán tìm kiếm và xếp hạng:
      - Tính điểm phù hợp (matching score) dựa trên các yếu tố:
        - Số lượng skills phù hợp
        - Mức độ thành thạo mỗi skill
        - Số năm kinh nghiệm
        - Chứng chỉ
        - Thời gian sử dụng skill gần nhất
      - Sắp xếp kết quả theo matching score
    - Hỗ trợ phân trang: page, size
  - Tối ưu hiệu năng truy vấn sử dụng Global Secondary Index
  - Xử lý lỗi và logging chi tiết

### Phát triển Matching Algorithm

- [ ] Triển khai thuật toán đánh giá mức độ phù hợp (matching):
  - Location: src/services/skill_matching.py
  - Triển khai các hàm tính toán matching score:
    - calculate_skill_match(required_skills, employee_skills): Tính điểm phù hợp tổng thể
    - calculate_individual_skill_match(required_skill, employee_skill): Tính điểm cho từng skill
    - normalize_scores(scores): Chuẩn hóa điểm về thang 0-100
    - rank_employees(employees, scores): Xếp hạng nhân viên theo điểm
  - Triển khai các hàm lọc kết quả:
    - filter_by_availability(employees, availability_date)
    - filter_by_team(employees, team_id)
    - filter_by_certification(employees, required_certification)
  - Xử lý các trường hợp đặc biệt và tối ưu thuật toán

### Phát triển Data Access Layer

- [ ] Mở rộng lớp truy cập dữ liệu cho employee skills:
  - Location: src/models/employee_skill.py
  - Triển khai các method truy vấn nâng cao:
    - find_employees_by_skills(skill_ids, match_type)
    - get_employees_with_skill_details(employee_ids)
    - filter_employees_by_availability(employee_ids, availability_type, available_from)
    - get_employee_matching_data(employee_id, skill_ids)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/employees/search/skills:
    - Method: GET
    - Các tham số query: skills, minProficiency, matchType, availability, availableFrom, minExperience, teamId, certifiedOnly, page, size
    - Liên kết với Lambda function search_by_skills
    - Phân quyền: Admin, HR Manager, Division Manager, Project Manager, Team Leader
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Caching Mechanism

- [ ] Triển khai cơ chế cache cho tìm kiếm thường xuyên:
  - Location: src/common/cache_utils.py
  - Triển khai các hàm xử lý cache:
    - generate_cache_key(search_params): Tạo key cho cache dựa vào tham số tìm kiếm
    - get_cached_results(cache_key): Lấy kết quả từ cache
    - store_results_in_cache(cache_key, results): Lưu kết quả vào cache
    - invalidate_cache(employee_id): Xóa cache khi thông tin skill của nhân viên thay đổi
  - Tích hợp với ElastiCache hoặc DynamoDB để lưu cache

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/employee_search/
  - Test case cho search_by_skills.py:
    - Test tìm kiếm với match type ALL
    - Test tìm kiếm với match type ANY
    - Test với các filter khác nhau
    - Test xếp hạng kết quả
    - Test phân trang
    - Test phân quyền
  - Test case cho skill_matching.py:
    - Test tính matching score
    - Test xếp hạng nhân viên
    - Test các trường hợp đặc biệt

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho endpoint:
    - GET /api/v1/employees/search/skills
  - Tài liệu giải thích thuật toán matching và cách tính điểm
  - Hướng dẫn sử dụng API với các tham số khác nhau
  - Ví dụ tìm kiếm với các kịch bản khác nhau

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách tìm kiếm nhân viên theo skills:

```python
# Tìm kiếm nhân viên theo skills
import requests

def search_employees_by_skills(api_base_url, token, skill_ids, min_proficiency=None, match_type='ANY', 
                              availability=None, available_from=None, team_id=None, certified_only=False, 
                              page=1, size=10):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'skills': ','.join(skill_ids),
        'matchType': match_type,
        'page': page,
        'size': size
    }
    
    if min_proficiency:
        params['minProficiency'] = min_proficiency
    
    if availability:
        params['availability'] = availability
    
    if available_from:
        params['availableFrom'] = available_from
    
    if team_id:
        params['teamId'] = team_id
    
    if certified_only:
        params['certifiedOnly'] = 'true'
    
    response = requests.get(
        f"{api_base_url}/api/v1/employees/search/skills",
        headers=headers,
        params=params
    )
    
    return response.json()

# Ví dụ gọi hàm:
# skill_ids = ["skill123", "skill456"]  # Java và AWS
# result = search_employees_by_skills(
#     api_base_url="https://api.example.com",
#     token="your_auth_token",
#     skill_ids=skill_ids,
#     min_proficiency=3,  # Intermediate trở lên
#     match_type="ALL",   # Phải có cả Java và AWS
#     availability="PartiallyAllocated",  # Nhân viên còn thời gian rảnh
#     available_from="2025-06-01",  # Khả dụng từ 1/6/2025
#     certified_only=True  # Có chứng chỉ
# )

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "search_criteria": {
#       "skills": [
#         {
#           "id": "skill123",
#           "name": "Java"
#         },
#         {
#           "id": "skill456",
#           "name": "AWS"
#         }
#       ],
#       "match_type": "ALL",
#       "min_proficiency": 3,
#       "availability": "PartiallyAllocated",
#       "available_from": "2025-06-01",
#       "certified_only": true
#     },
#     "employees": [
#       {
#         "id": "emp123",
#         "employee_code": "E001",
#         "full_name": "Nguyễn Văn A",
#         "position": "Senior Developer",
#         "team": {
#           "id": "team456",
#           "name": "Java Team"
#         },
#         "matching_score": 92.5,
#         "current_status": "Allocated",
#         "availability_date": "2025-06-15",
#         "allocation_percentage": 70,
#         "skill_matches": [
#           {
#             "skill": {
#               "id": "skill123",
#               "name": "Java"
#             },
#             "proficiency_level": 4,
#             "proficiency_text": "Advanced",
#             "years_of_experience": 5,
#             "is_certified": true,
#             "certification_details": "Oracle Certified Professional Java SE 11 Developer"
#           },
#           {
#             "skill": {
#               "id": "skill456",
#               "name": "AWS"
#             },
#             "proficiency_level": 3,
#             "proficiency_text": "Intermediate",
#             "years_of_experience": 2,
#             "is_certified": true,
#             "certification_details": "AWS Certified Solutions Architect - Associate"
#           }
#         ]
#       },
#       {
#         "id": "emp456",
#         "employee_code": "E002",
#         "full_name": "Trần Thị B",
#         "position": "Developer",
#         "team": {
#           "id": "team789",
#           "name": "Cloud Team"
#         },
#         "matching_score": 85.0,
#         "current_status": "PartiallyAllocated",
#         "availability_date": "2025-06-01",
#         "allocation_percentage": 50,
#         "skill_matches": [
#           {
#             "skill": {
#               "id": "skill123",
#               "name": "Java"
#             },
#             "proficiency_level": 3,
#             "proficiency_text": "Intermediate",
#             "years_of_experience": 3,
#             "is_certified": true,
#             "certification_details": "Oracle Certified Associate Java Programmer"
#           },
#           {
#             "skill": {
#               "id": "skill456",
#               "name": "AWS"
#             },
#             "proficiency_level": 4,
#             "proficiency_text": "Advanced",
#             "years_of_experience": 3,
#             "is_certified": true,
#             "certification_details": "AWS Certified Developer - Associate"
#           }
#         ]
#       },
#       // ... more matching employees
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

1. Lambda function tìm kiếm nhân viên theo skills hoạt động chính xác với đầy đủ các tham số tìm kiếm
2. Thuật toán matching và ranking hoạt động chính xác, đánh giá đúng mức độ phù hợp của nhân viên
3. Kết quả tìm kiếm được trả về với các thông tin chi tiết về mức độ phù hợp
4. Hiệu năng tìm kiếm nhanh, ngay cả với dataset lớn
5. Cơ chế cache hoạt động hiệu quả cho các tìm kiếm lặp lại
6. API endpoint được cấu hình đúng với phân quyền phù hợp
7. Unit tests đạt coverage > 80%
8. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 4-5 ngày làm việc

## Ghi chú

- Thuật toán matching cần được tối ưu để có thể xử lý nhanh với số lượng lớn nhân viên và skills
- Cần cẩn thận với hiệu năng khi tìm kiếm trên nhiều skills và với nhiều điều kiện, có thể cần phân trang hoặc giới hạn số lượng kết quả
- Cấu trúc điểm matching score nên được thiết kế linh hoạt để có thể điều chỉnh trọng số của các yếu tố (proficiency, experience, certification, etc.)
- Xem xét việc lưu cache kết quả tìm kiếm thường xuyên để tăng hiệu năng
- Cân nhắc việc cho phép điều chỉnh trọng số của các yếu tố trong thuật toán matching qua tham số tìm kiếm 