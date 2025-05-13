**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function gợi ý nhân sự phù hợp | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function gợi ý nhân sự phù hợp dựa trên yêu cầu kỹ năng của dự án, giúp tối ưu hóa việc phân bổ nhân sự và tăng hiệu quả quản lý dự án.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-HRM-006  
**Task Name:** Triển khai Lambda function gợi ý nhân sự phù hợp  
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
- BE-HRM-005 (Phát triển Lambda function tìm kiếm nhân viên theo skills)

**Các task phụ thuộc vào task này:** 
- BE-CTR-004 (Phát triển Lambda functions quản lý nhân sự trong hợp đồng)

**Các API:**
- POST /api/v1/employees/recommend (API-HRM-018)

## Mô tả

Triển khai Lambda function gợi ý nhân sự phù hợp cho dự án dựa trên yêu cầu kỹ năng và các tiêu chí khác. API sẽ nhận input là danh sách các yêu cầu kỹ năng cùng với các thông số về dự án, và trả về danh sách nhân viên phù hợp nhất, được xếp hạng theo mức độ phù hợp.

Khác với task BE-HRM-005 (tìm kiếm nhân viên theo skills), task này sẽ có cơ chế đề xuất thông minh hơn, xem xét nhiều yếu tố phức tạp như:
- Prioritization của các skills (skills nào quan trọng hơn)
- Thời gian dự án và khả năng sẵn có của nhân viên
- Kinh nghiệm làm việc với các dự án tương tự
- Chi phí nhân viên và hiệu quả kinh tế
- Mức độ phù hợp về vị trí/cấp bậc (position/seniority)

Chức năng này sẽ giúp các Project Manager và HR Manager dễ dàng tìm ra đội ngũ phù hợp nhất cho dự án, dựa trên dữ liệu thực tế về kỹ năng và tình trạng nhân sự.

## Chi tiết công việc

### Phát triển Lambda function gợi ý nhân sự phù hợp

- [ ] Triển khai Lambda function xử lý POST /api/v1/employees/recommend:
  - Location: src/functions/employee_recommendation/recommend_employees.py
  - Triển khai logic gợi ý:
    - Xác thực người dùng đã đăng nhập
    - Phân quyền (Admin, HR Manager, Division Manager, Project Manager)
    - Xử lý các tham số đầu vào từ request body:
      - project_requirements: Danh sách các yêu cầu kỹ năng, mỗi yêu cầu bao gồm:
        - skill_id: ID của skill
        - importance: Mức độ quan trọng (1-5, 5 là quan trọng nhất)
        - min_proficiency: Mức độ thành thạo tối thiểu yêu cầu
        - min_experience: Số năm kinh nghiệm tối thiểu yêu cầu
        - required_certification: Có yêu cầu chứng chỉ hay không
      - project_details:
        - start_date: Ngày bắt đầu dự án
        - end_date: Ngày kết thúc dự án (dự kiến)
        - required_positions: Các vị trí cần (e.g., 2 Senior Developers, 3 Developers)
        - location: Địa điểm dự án
        - project_type: Loại dự án
      - filter_options:
        - team_id: Lọc theo team (optional)
        - max_budget: Ngân sách tối đa cho nhân sự (optional)
        - availability_threshold: Ngưỡng khả dụng tối thiểu (%) (default: 50)
        - consider_project_history: Có tính đến lịch sử dự án tương tự không (default: true)
      - recommendation_options:
        - size: Số lượng kết quả trả về (default: 10)
        - prioritize_by: Ưu tiên xếp hạng theo yếu tố nào (skill_match, cost_efficiency, availability) (default: skill_match)
    - Triển khai thuật toán đề xuất nâng cao:
      - Xác định danh sách nhân viên tiềm năng dựa trên skill matching
      - Tính toán điểm phù hợp tổng hợp (composite score) dựa trên nhiều yếu tố
      - Phân nhóm đề xuất theo vị trí yêu cầu
      - Sắp xếp kết quả theo điểm phù hợp và ưu tiên
    - Tạo báo cáo gợi ý chi tiết
  - Tối ưu hiệu năng xử lý với dataset lớn
  - Xử lý lỗi và logging chi tiết

### Phát triển Advanced Recommendation Algorithm

- [ ] Triển khai thuật toán đề xuất nâng cao:
  - Location: src/services/employee_recommendation.py
  - Triển khai các hàm chính:
    - get_potential_employees(project_requirements): Lấy danh sách nhân viên tiềm năng
    - calculate_composite_score(employee, requirements, options): Tính điểm phù hợp tổng hợp
    - calculate_skill_match_score(employee_skills, required_skills): Tính điểm phù hợp về kỹ năng
    - calculate_availability_score(employee, project_dates): Tính điểm phù hợp về thời gian
    - calculate_cost_efficiency(employee, project_requirements): Tính điểm hiệu quả chi phí
    - calculate_experience_relevance(employee, project_type): Tính điểm liên quan về kinh nghiệm
    - group_by_position(recommendations, required_positions): Nhóm kết quả theo vị trí
    - create_optimal_team(grouped_recommendations, requirements): Tạo đội ngũ tối ưu
  - Triển khai các thuật toán phụ:
    - normalize_scores(scores): Chuẩn hóa điểm về thang 0-100
    - apply_weighting(scores, weights): Áp dụng trọng số cho các điểm thành phần
    - handle_special_cases(recommendations): Xử lý các trường hợp đặc biệt
  - Xử lý tối ưu hiệu năng và bộ nhớ

### Phát triển Data Access Layer

- [ ] Mở rộng lớp truy cập dữ liệu:
  - Location: src/models/employee_recommendation.py
  - Triển khai các method truy vấn:
    - get_employees_for_recommendation(skill_ids, filters)
    - get_employee_detailed_info(employee_ids)
    - get_employee_project_history(employee_id, project_type)
    - get_employee_availability(employee_id, date_range)
    - get_employee_cost_data(employee_id)
    - save_recommendation_history(recommendation_data)

### Cấu hình API Gateway

- [ ] Cài đặt API endpoint trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route POST /api/v1/employees/recommend:
    - Method: POST
    - Request body: Cấu trúc JSON với project_requirements, project_details, filter_options, recommendation_options
    - Liên kết với Lambda function recommend_employees
    - Phân quyền: Admin, HR Manager, Division Manager, Project Manager
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Phát triển Caching và Lưu trữ lịch sử

- [ ] Triển khai cơ chế cache cho đề xuất lặp lại và lưu lịch sử đề xuất:
  - Location: src/common/recommendation_utils.py
  - Triển khai các hàm:
    - generate_recommendation_cache_key(request_data): Tạo key cho cache
    - cache_recommendation_results(cache_key, results): Lưu kết quả vào cache
    - get_cached_recommendation(cache_key): Lấy kết quả từ cache
    - save_recommendation_history(user_id, request_data, results): Lưu lịch sử đề xuất
    - get_previous_recommendations(user_id, limit): Lấy lịch sử đề xuất trước đó

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/employee_recommendation/
  - Test case cho recommend_employees.py:
    - Test đề xuất với các yêu cầu khác nhau
    - Test với các tùy chọn filter và recommendation khác nhau
    - Test phân quyền
    - Test xử lý lỗi
  - Test case cho employee_recommendation.py:
    - Test tính điểm phù hợp tổng hợp
    - Test tính điểm skill match
    - Test tính điểm availability
    - Test tính điểm cost efficiency
    - Test nhóm kết quả theo vị trí
    - Test tạo đội ngũ tối ưu

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho endpoint:
    - POST /api/v1/employees/recommend
  - Tài liệu giải thích thuật toán đề xuất và cách tính điểm
  - Tài liệu về cấu trúc request và response
  - Hướng dẫn sử dụng API với các scenarios khác nhau

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng API gợi ý nhân sự:

```python
# Gợi ý nhân sự phù hợp cho dự án
import requests
import json

def recommend_employees(api_base_url, token, project_requirements, project_details, 
                       filter_options=None, recommendation_options=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    request_data = {
        'project_requirements': project_requirements,
        'project_details': project_details
    }
    
    if filter_options:
        request_data['filter_options'] = filter_options
    
    if recommendation_options:
        request_data['recommendation_options'] = recommendation_options
    
    response = requests.post(
        f"{api_base_url}/api/v1/employees/recommend",
        headers=headers,
        json=request_data
    )
    
    return response.json()

# Ví dụ gọi hàm:
# project_requirements = [
#     {
#         "skill_id": "skill123",  # Java
#         "importance": 5,         # Rất quan trọng
#         "min_proficiency": 4,    # Advanced
#         "min_experience": 3,     # Tối thiểu 3 năm
#         "required_certification": True
#     },
#     {
#         "skill_id": "skill456",  # AWS
#         "importance": 4,         # Quan trọng
#         "min_proficiency": 3,    # Intermediate
#         "min_experience": 1,     # Tối thiểu 1 năm
#         "required_certification": False
#     },
#     {
#         "skill_id": "skill789",  # React
#         "importance": 3,         # Tương đối quan trọng
#         "min_proficiency": 2,    # Elementary
#         "min_experience": 1,     # Tối thiểu 1 năm
#         "required_certification": False
#     }
# ]
# 
# project_details = {
#     "start_date": "2025-07-01",
#     "end_date": "2025-12-31",
#     "required_positions": [
#         {"position": "Senior Developer", "count": 2},
#         {"position": "Developer", "count": 3},
#         {"position": "UI/UX Designer", "count": 1}
#     ],
#     "location": "Ho Chi Minh City",
#     "project_type": "Web Application"
# }
# 
# filter_options = {
#     "team_id": None,  # Không lọc theo team
#     "max_budget": 100000000,  # 100 triệu VND/tháng
#     "availability_threshold": 70,  # Nhân viên phải khả dụng ít nhất 70%
#     "consider_project_history": True
# }
# 
# recommendation_options = {
#     "size": 15,  # 15 kết quả hàng đầu
#     "prioritize_by": "skill_match"  # Ưu tiên xếp hạng theo skill match
# }
# 
# result = recommend_employees(
#     api_base_url="https://api.example.com",
#     token="your_auth_token",
#     project_requirements=project_requirements,
#     project_details=project_details,
#     filter_options=filter_options,
#     recommendation_options=recommendation_options
# )

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "request_summary": {
#       "project_requirements": {
#         "skills": [
#           {"id": "skill123", "name": "Java", "importance": 5},
#           {"id": "skill456", "name": "AWS", "importance": 4},
#           {"id": "skill789", "name": "React", "importance": 3}
#         ],
#         "duration": "6 months (Jul 01, 2025 - Dec 31, 2025)",
#         "team_size": 6
#       }
#     },
#     "recommendations": {
#       "optimal_team": [
#         {
#           "position": "Senior Developer",
#           "candidates": [
#             {
#               "id": "emp123",
#               "employee_code": "E001",
#               "full_name": "Nguyễn Văn A",
#               "position": "Senior Developer",
#               "team": {
#                 "id": "team456",
#                 "name": "Java Team"
#               },
#               "composite_score": 94.8,
#               "skill_match_score": 96.5,
#               "availability_score": 90.0,
#               "cost_efficiency_score": 85.0,
#               "experience_relevance_score": 98.0,
#               "availability": {
#                 "status": "PartiallyAllocated",
#                 "available_percentage": 80,
#                 "available_from": "2025-07-01"
#               },
#               "matching_skills": [
#                 {
#                   "skill": {
#                     "id": "skill123",
#                     "name": "Java"
#                   },
#                   "proficiency_level": 5,
#                   "proficiency_text": "Expert",
#                   "years_of_experience": 7,
#                   "is_certified": true,
#                   "match_score": 100
#                 },
#                 {
#                   "skill": {
#                     "id": "skill456",
#                     "name": "AWS"
#                   },
#                   "proficiency_level": 4,
#                   "proficiency_text": "Advanced",
#                   "years_of_experience": 3,
#                   "is_certified": true,
#                   "match_score": 95
#                 },
#                 // ... more skills
#               ],
#               "cost_details": {
#                 "monthly_cost": 35000000,
#                 "relative_efficiency": "High"
#               },
#               "similar_projects": 5
#             },
#             // ... more Senior Developer candidates
#           ]
#         },
#         {
#           "position": "Developer",
#           "candidates": [
#             // ... Developer candidates
#           ]
#         },
#         {
#           "position": "UI/UX Designer",
#           "candidates": [
#             // ... UI/UX Designer candidates
#           ]
#         }
#       ],
#       "alternative_candidates": [
#         // ... other potential candidates not in optimal team
#       ]
#     },
#     "summary_statistics": {
#       "total_candidates_evaluated": 45,
#       "average_skill_match": 82.5,
#       "average_availability": 75.0,
#       "total_estimated_monthly_cost": 95000000
#     },
#     "recommendation_id": "rec-20250513-001",
#     "generated_at": "2025-05-13T17:45:30Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function gợi ý nhân sự hoạt động chính xác với đầy đủ các tùy chọn
2. Thuật toán đề xuất nâng cao hoạt động tốt, xem xét các yếu tố đa chiều
3. Kết quả đề xuất được phân nhóm theo vị trí và được xếp hạng hợp lý
4. Hiệu năng tốt khi xử lý danh sách lớn nhân viên và yêu cầu
5. Cơ chế cache và lưu lịch sử đề xuất hoạt động hiệu quả
6. API endpoint được cấu hình đúng với phân quyền phù hợp
7. Unit tests đạt coverage > 80%
8. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 5-6 ngày làm việc

## Ghi chú

- Thuật toán đề xuất nên có tính linh hoạt, cho phép điều chỉnh trọng số các yếu tố đánh giá
- Cần xem xét nhiều yếu tố ngoài skills, như chi phí, khả năng làm việc nhóm, kinh nghiệm dự án tương tự
- Kết quả đề xuất nên được trình bày theo hướng gợi ý đội ngũ tối ưu, không chỉ là danh sách nhân viên riêng lẻ
- Có thể xem xét lưu lịch sử đề xuất để hỗ trợ phân tích và cải thiện thuật toán
- Hiệu năng là yếu tố quan trọng khi thuật toán phải xử lý lượng lớn dữ liệu nhân viên và skills 