**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda functions quản lý KPI doanh thu | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda functions quản lý KPI doanh thu, phục vụ cho việc theo dõi, đánh giá hiệu quả của nhân viên sales và bộ phận kinh doanh.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-CTR-005  
**Task Name:** Triển khai Lambda functions quản lý KPI doanh thu  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Phát triển service authentication và authorization)
- BE-CTR-001 (Triển khai Lambda functions quản lý hợp đồng)

**Các task phụ thuộc vào task này:** 
- BE-RPT-007 (Lấy báo cáo tiến độ KPI doanh thu Sales)

**Các API:**
- GET /api/v1/sales-kpis (API-CTR-015)
- POST /api/v1/admin/sales-kpis (API-CTR-016)
- DELETE /api/v1/admin/sales-kpis/{kpiId} (API-CTR-017)

## Mô tả

Triển khai các Lambda functions để quản lý KPI (Key Performance Indicator) doanh thu của nhân viên sales và bộ phận kinh doanh. Các chức năng chính bao gồm:

- Lấy danh sách KPI doanh thu đã thiết lập với khả năng lọc theo nhân viên sales, kỳ (năm, quý, tháng)
- Thêm/Cập nhật KPI doanh thu cho nhân viên sales, cho phép thiết lập mục tiêu theo kỳ
- Xóa KPI doanh thu (khi cần điều chỉnh hoặc có sai sót)
- Tính toán tỷ lệ hoàn thành KPI dựa trên doanh thu thực tế từ các hợp đồng

Các API được bảo mật chặt chẽ, chỉ cho phép Admin và Trưởng phòng kinh doanh thực hiện việc thêm/sửa/xóa KPI. Nhân viên sales chỉ được phép xem KPI của bản thân, trong khi quản lý có thể xem KPI của toàn bộ nhân viên thuộc quyền quản lý.

## Chi tiết công việc

### Phát triển Lambda function lấy danh sách KPI doanh thu

- [ ] Triển khai Lambda function xử lý GET /api/v1/sales-kpis:
  - Location: src/functions/sales_kpis/list_sales_kpis.py
  - Triển khai logic lấy danh sách KPI:
    - Xác thực và phân quyền (kiểm tra quyền xem KPI)
    - Hỗ trợ các tham số filter:
      - sales_user_id: Lọc theo nhân viên sales
      - year: Lọc theo năm
      - quarter: Lọc theo quý
      - month: Lọc theo tháng
      - status: Lọc theo trạng thái (active, closed)
    - Hỗ trợ phân trang: page, size
    - Hỗ trợ sắp xếp: sortBy, sortDirection
    - Lọc dữ liệu KPI theo quyền của người dùng (sales chỉ xem KPI của mình)
    - Bổ sung thông tin tên nhân viên sales để hiển thị
  - Triển khai xử lý lỗi và logging chi tiết

### Phát triển Lambda function thêm/cập nhật KPI doanh thu

- [ ] Triển khai Lambda function xử lý POST /api/v1/admin/sales-kpis:
  - Location: src/functions/sales_kpis/create_update_sales_kpi.py
  - Triển khai logic thêm/cập nhật KPI:
    - Xác thực và phân quyền (chỉ Admin và Trưởng phòng kinh doanh)
    - Validate dữ liệu đầu vào:
      - sales_user_id: ID của nhân viên sales (phải tồn tại)
      - year: Năm áp dụng KPI
      - quarter: Quý áp dụng KPI (tùy chọn, 1-4)
      - month: Tháng áp dụng KPI (tùy chọn, 1-12)
      - target_revenue: Mục tiêu doanh thu
      - currency: Đơn vị tiền tệ
      - notes: Ghi chú bổ sung (tùy chọn)
    - Kiểm tra xem KPI đã tồn tại chưa (dựa vào sales_user_id, year, quarter, month)
    - Nếu đã tồn tại: cập nhật thông tin
    - Nếu chưa tồn tại: tạo mới bản ghi KPI
    - Lưu thông tin KPI vào DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi: nhân viên không tồn tại, dữ liệu không hợp lệ, v.v.
  - Triển khai cơ chế cập nhật thông tin actual_revenue tự động khi có hợp đồng mới hoặc cập nhật thanh toán

### Phát triển Lambda function xóa KPI doanh thu

- [ ] Triển khai Lambda function xử lý DELETE /api/v1/admin/sales-kpis/{kpiId}:
  - Location: src/functions/sales_kpis/delete_sales_kpi.py
  - Triển khai logic xóa KPI:
    - Xác thực và phân quyền (chỉ Admin và Trưởng phòng kinh doanh)
    - Kiểm tra KPI tồn tại
    - Xóa bản ghi KPI khỏi DynamoDB
    - Ghi log thay đổi
  - Xử lý các trường hợp lỗi và xung đột dữ liệu

### Phát triển Data Access Layer

- [ ] Xây dựng lớp truy cập dữ liệu cho KPI doanh thu:
  - Location: src/models/sales_kpi.py
  - Định nghĩa model cho KPI:
    - Các trường cơ bản: id, sales_user_id, year, quarter, month, target_revenue, actual_revenue, achievement_percentage, currency, status, notes, created_at, updated_at, created_by, updated_by
  - Triển khai các method truy vấn DynamoDB:
    - create_sales_kpi(kpi_data)
    - get_sales_kpi(kpi_id)
    - get_sales_kpi_by_period(sales_user_id, year, quarter=None, month=None)
    - get_sales_kpis(filters, pagination)
    - update_sales_kpi(kpi_id, kpi_data)
    - delete_sales_kpi(kpi_id)
    - calculate_achievement_percentage(kpi_id)
    - update_actual_revenue(sales_user_id, year, quarter, month, value)

### Phát triển Service Layer

- [ ] Xây dựng service layer cho tính toán KPI và tích hợp với hợp đồng:
  - Location: src/services/sales_kpi_service.py
  - Implement các phương thức:
    - update_kpi_from_contract(contract_data): Cập nhật KPI khi có hợp đồng mới hoặc cập nhật
    - calculate_actual_revenue(sales_user_id, year, quarter=None, month=None): Tính toán doanh thu thực tế từ hợp đồng
    - close_period_kpis(year, quarter=None, month=None): Đánh dấu KPI là đã đóng khi hết kỳ

### Cấu hình API Gateway

- [ ] Cài đặt API endpoints trong API Gateway:
  - Location: template.yaml (trong phần Resources)
  - Cấu hình route GET /api/v1/sales-kpis:
    - Method: GET
    - Các tham số query: sales_user_id, year, quarter, month, status, page, size, sortBy, sortDirection
    - Liên kết với Lambda function list_sales_kpis
    - Phân quyền: Admin, Trưởng phòng kinh doanh, Nhân viên sales (giới hạn scope)
  - Cấu hình route POST /api/v1/admin/sales-kpis:
    - Method: POST
    - Request body: Thông tin KPI doanh thu
    - Liên kết với Lambda function create_update_sales_kpi
    - Phân quyền: Admin, Trưởng phòng kinh doanh
  - Cấu hình route DELETE /api/v1/admin/sales-kpis/{kpiId}:
    - Method: DELETE
    - Path parameter: kpiId
    - Liên kết với Lambda function delete_sales_kpi
    - Phân quyền: Admin, Trưởng phòng kinh doanh
  - Tích hợp với Lambda Authorizer để xác thực và phân quyền

### Triển khai Lambda Triggers

- [ ] Phát triển Lambda trigger để cập nhật KPI khi có thay đổi hợp đồng:
  - Location: src/functions/triggers/contract_update_trigger.py
  - Triển khai DynamoDB Stream listener cho bảng hợp đồng
  - Khi có hợp đồng mới hoặc cập nhật trạng thái hợp đồng, tự động cập nhật actual_revenue và achievement_percentage cho KPI tương ứng

### Phát triển Unit Tests

- [ ] Viết unit tests:
  - Location: tests/unit/functions/sales_kpis/
  - Test case cho list_sales_kpis.py:
    - Test lấy danh sách với các filter khác nhau
    - Test phân trang và sắp xếp
    - Test phân quyền (Admin, Trưởng phòng, Nhân viên sales)
  - Test case cho create_update_sales_kpi.py:
    - Test tạo KPI mới
    - Test cập nhật KPI đã tồn tại
    - Test với dữ liệu không hợp lệ
    - Test phân quyền
  - Test case cho delete_sales_kpi.py:
    - Test xóa KPI thành công
    - Test xóa KPI không tồn tại
    - Test phân quyền
  - Test case cho sales_kpi_service.py:
    - Test cập nhật KPI từ hợp đồng
    - Test tính toán doanh thu thực tế
    - Test đóng kỳ KPI

### Tạo Documentation

- [ ] Viết tài liệu:
  - Tài liệu API swagger cho các endpoints:
    - GET /api/v1/sales-kpis
    - POST /api/v1/admin/sales-kpis
    - DELETE /api/v1/admin/sales-kpis/{kpiId}
  - Tài liệu quyền truy cập và sử dụng API
  - Tài liệu mô tả cách thiết lập và quản lý KPI doanh thu

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách lấy danh sách KPI doanh thu:

```python
# Lấy danh sách KPI doanh thu
import requests

def get_sales_kpis(api_base_url, token, sales_user_id=None, year=None, quarter=None, month=None, status='active', page=1, size=10):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'page': page,
        'size': size,
        'status': status
    }
    
    if sales_user_id:
        params['sales_user_id'] = sales_user_id
    
    if year:
        params['year'] = year
    
    if quarter:
        params['quarter'] = quarter
    
    if month:
        params['month'] = month
    
    response = requests.get(
        f"{api_base_url}/api/v1/sales-kpis",
        headers=headers,
        params=params
    )
    
    return response.json()

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 200,
#   "data": {
#     "kpis": [
#       {
#         "id": "kpi123",
#         "sales_user": {
#           "id": "user456",
#           "full_name": "Nguyễn Văn A"
#         },
#         "year": 2025,
#         "quarter": 2,
#         "month": null,
#         "target_revenue": 500000000,
#         "actual_revenue": 380000000,
#         "achievement_percentage": 76,
#         "currency": "VND",
#         "status": "active",
#         "notes": "KPI Q2/2025 cho nhân viên A",
#         "created_at": "2025-03-20T08:30:00Z",
#         "updated_at": "2025-05-12T14:15:00Z"
#       },
#       // ... more KPIs
#     ],
#     "pagination": {
#       "page": 1,
#       "size": 10,
#       "total_items": 25,
#       "total_pages": 3
#     }
#   }
# }
```

Ví dụ về cách thêm/cập nhật KPI doanh thu:

```python
# Thêm/Cập nhật KPI doanh thu
import requests

def create_update_sales_kpi(api_base_url, token, kpi_data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{api_base_url}/api/v1/admin/sales-kpis",
        headers=headers,
        json=kpi_data
    )
    
    return response.json()

# Dữ liệu đầu vào:
# kpi_data = {
#   "sales_user_id": "user456",
#   "year": 2025,
#   "quarter": 3,
#   "month": null,  # Null cho KPI theo quý
#   "target_revenue": 600000000,
#   "currency": "VND",
#   "notes": "KPI Q3/2025 cho nhân viên A"
# }

# Kết quả mong đợi:
# {
#   "status": "success",
#   "code": 201,
#   "message": "KPI doanh thu đã được tạo thành công",
#   "data": {
#     "id": "kpi789",
#     "sales_user": {
#       "id": "user456",
#       "full_name": "Nguyễn Văn A"
#     },
#     "year": 2025,
#     "quarter": 3,
#     "month": null,
#     "target_revenue": 600000000,
#     "actual_revenue": 0,
#     "achievement_percentage": 0,
#     "currency": "VND",
#     "status": "active",
#     "notes": "KPI Q3/2025 cho nhân viên A",
#     "created_at": "2025-05-13T10:20:00Z",
#     "updated_at": "2025-05-13T10:20:00Z"
#   }
# }
```

## Tiêu chí hoàn thành

1. Lambda function lấy danh sách KPI doanh thu hoạt động chính xác với đầy đủ chức năng filter, phân trang
2. Lambda function thêm/cập nhật KPI doanh thu hoạt động chính xác với validation đầy đủ
3. Lambda function xóa KPI doanh thu hoạt động chính xác
4. Lambda trigger tự động cập nhật actual_revenue và achievement_percentage khi có thay đổi hợp đồng
5. API endpoints được cấu hình đúng với phân quyền phù hợp
6. Cơ chế tính toán doanh thu thực tế và tỷ lệ hoàn thành hoạt động chính xác
7. Unit tests đạt coverage > 80%
8. Tài liệu API đầy đủ và chính xác

## Ước tính thời gian

- 4-5 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý đến vấn đề phân quyền, đảm bảo nhân viên sales chỉ xem được KPI của họ
- KPI có thể được thiết lập theo năm, quý hoặc tháng, cần thiết kế cơ chế lưu trữ linh hoạt
- Cơ chế tính toán doanh thu thực tế cần tính đến các hợp đồng được ký, không phụ thuộc vào việc đã thanh toán hay chưa
- Cần cân nhắc các trường hợp đặc biệt như hợp đồng được ký bởi nhiều sales, hoặc chuyển đổi sales trong quá trình đàm phán
- Nên có cơ chế đánh dấu KPI là đã đóng (closed) khi kết thúc kỳ đánh giá để tránh cập nhật không cần thiết 