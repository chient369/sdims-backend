**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý cơ hội kinh doanh | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý cơ hội kinh doanh, bao gồm xem danh sách, lọc, tìm kiếm và xem chi tiết cơ hội.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-OPP-003  
**Task Name:** Triển khai Lambda functions quản lý cơ hội  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-OPP-001 (Triển khai Lambda functions đồng bộ dữ liệu từ Hubspot)

**Các task phụ thuộc vào task này:** 
- BE-OPP-004 (Phát triển Lambda function gán Leader cho cơ hội)
- BE-OPP-005 (Triển khai Lambda functions quản lý ghi chú cơ hội)
- BE-OPP-006 (Phát triển Lambda function đánh dấu ưu tiên onsite)

**Các API:**
- GET /api/v1/opportunities (API-OPP-001)
- GET /api/v1/opportunities/{id} (API-OPP-002)

## Mô tả

Triển khai các Lambda functions cho phép người dùng xem danh sách cơ hội kinh doanh, tìm kiếm, lọc và xem chi tiết cơ hội. Các chức năng này là nền tảng cho các hoạt động quản lý cơ hội tiếp theo như gán leader, quản lý ghi chú và đánh dấu ưu tiên onsite.

Đặc biệt quan trọng, hệ thống cần tính toán tự động trạng thái follow-up (Red/Yellow/Green) dựa trên thời gian tương tác cuối cùng và trạng thái của cơ hội, giúp người dùng dễ dàng xác định các cơ hội cần được ưu tiên xử lý.

## Chi tiết công việc

### Phát triển Lambda function xem danh sách cơ hội

- [ ] Triển khai Lambda function xử lý GET /api/v1/opportunities:
  - Triển khai logic lấy dữ liệu cơ hội:
    - Truy vấn dữ liệu từ bảng OPPORTUNITIES trên DynamoDB
    - Hỗ trợ phân trang với tokenization (DynamoDB pagination)
    - Hỗ trợ lọc theo:
      - Trạng thái cơ hội (status)
      - Trạng thái follow-up (follow_up_status)
      - Leader được gán (assigned_to)
      - Khách hàng (customer_name)
      - Khoảng thời gian (tạo/cập nhật/tương tác cuối)
      - Giá trị dự kiến (potential_value range)
    - Hỗ trợ tìm kiếm text (full-text search) trên các trường:
      - Tên cơ hội (opportunity_name)
      - Mô tả (description)
      - Tên khách hàng (customer_name)
    - Hỗ trợ sắp xếp theo các trường phổ biến:
      - Ngày tạo (created_at)
      - Ngày cập nhật (updated_at)
      - Ngày tương tác cuối (last_interaction_date)
      - Giá trị dự kiến (potential_value)
  - Triển khai tính toán trạng thái follow-up (Red/Yellow/Green):
    - Red: quá thời hạn follow-up và không có tương tác trong thời gian X ngày (mặc định 7 ngày)
    - Yellow: sắp đến thời hạn follow-up (còn 2 ngày)
    - Green: đã có tương tác gần đây hoặc không yêu cầu follow-up

### Phát triển Lambda function xem chi tiết cơ hội

- [ ] Triển khai Lambda function xử lý GET /api/v1/opportunities/{id}:
  - Triển khai logic lấy chi tiết cơ hội:
    - Truy vấn dữ liệu từ bảng OPPORTUNITIES trên DynamoDB theo opportunity_id
    - Kết hợp với dữ liệu từ các bảng liên quan (nếu cần):
      - Thông tin leader được gán
      - Thông tin notes gần đây (3-5 notes mới nhất)
      - Thông tin trạng thái đồng bộ
  - Triển khai logic xử lý lỗi khi không tìm thấy cơ hội

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho cơ hội:
  - Location: src/models/opportunity.py
  - Định nghĩa model cho cơ hội kinh doanh:
    - Các trường cơ bản: id, name, description, status, value, etc.
    - Các trường tính toán: follow_up_status, days_since_last_interaction, etc.
  - Triển khai các method truy vấn DynamoDB:
    - list_opportunities(limit, next_token, filters, search_term, sort_by, sort_order)
    - get_opportunity_by_id(opportunity_id)
    - calculate_follow_up_status(opportunity)
  - Xử lý chuyển đổi giữa DynamoDB Item và model object

### Tích hợp với API Gateway

- [ ] Cấu hình API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/opportunities:
    - Các tham số query: page_size, next_token, các tham số filter và search
    - Liên kết với Lambda function list_opportunities
    - Phân quyền phù hợp
  - Cấu hình route GET /api/v1/opportunities/{id}:
    - Path parameter: id
    - Liên kết với Lambda function get_opportunity
    - Phân quyền phù hợp
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền


## Tiêu chí hoàn thành

1. Lambda function xem danh sách cơ hội hoạt động chính xác với đầy đủ chức năng filter, search và sort
2. Lambda function xem chi tiết cơ hội hoạt động chính xác
3. Tính toán chính xác trạng thái follow-up (Red/Yellow/Green)
4. API endpoints được cấu hình đúng với phân trang và phân quyền

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Cân nhắc sử dụng GSI (Global Secondary Indexes) trong DynamoDB để hỗ trợ các query pattern phức tạp
- Đảm bảo hiệu suất cao khi tìm kiếm và lọc trên dataset lớn
- Tính toán follow-up status có thể được thực hiện on-the-fly hoặc được lưu trữ và cập nhật định kỳ, tùy thuộc vào yêu cầu hiệu suất
- Cân nhắc việc sử dụng caching (như ElastiCache) cho các truy vấn phổ biến 