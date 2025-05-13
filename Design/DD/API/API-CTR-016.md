# API Details: Thêm/Sửa KPI doanh thu cho Sales

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API thêm/sửa KPI doanh thu cho Sales | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để quản lý viên thiết lập hoặc cập nhật chỉ tiêu KPI doanh thu cho nhân viên Sales theo các chu kỳ khác nhau (năm, quý, tháng), giúp xây dựng và quản lý mục tiêu kinh doanh, phục vụ cho việc đánh giá hiệu suất và khen thưởng nhân viên.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-016                                  |
| **Tên API**        | Thêm/Sửa KPI doanh thu cho Sales            |
| **Mô tả**          | API cho phép Admin thiết lập hoặc cập nhật KPI doanh thu cho nhân viên Sales |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/admin/sales-kpis`                   |
| **Quyền truy cập** | sales:kpi:manage                             |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

| Tên                | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------------|--------------|----------|-------|
| `id`               | Long         | Không    | ID của KPI (nếu là cập nhật KPI đã tồn tại) |
| `salesId`          | Long         | Có       | ID của nhân viên Sales |
| `year`             | Integer      | Có       | Năm áp dụng KPI |
| `quarter`          | Integer      | Không    | Quý áp dụng KPI (từ 1-4) |
| `month`            | Integer      | Không    | Tháng áp dụng KPI (từ 1-12) |
| `targetRevenue`    | Number       | Có       | Giá trị doanh thu mục tiêu |
| `note`             | String       | Không    | Ghi chú về KPI |

### 3.3 Validate Rule

| Trường          | Điều kiện hợp lệ                     |
|-----------------|------------------------------------- |
| `salesId`       | Phải là ID nhân viên Sales tồn tại trong hệ thống |
| `year`          | Năm hợp lệ (VD: 2025, 2026...), không nhỏ hơn năm hiện tại |
| `quarter`       | Số nguyên từ 1 đến 4                |
| `month`         | Số nguyên từ 1 đến 12               |
| `targetRevenue` | Số dương > 0                        |
| `note`          | Tối đa 500 ký tự                     |

### 3.4 Phân quyền đặc biệt
- Team Leader: Chỉ thiết lập/cập nhật KPI cho nhân viên Sales thuộc team mình quản lý
- Division Manager: Thiết lập/cập nhật KPI cho tất cả nhân viên Sales thuộc bộ phận mình quản lý
- Admin: Thiết lập/cập nhật KPI cho tất cả nhân viên Sales
- Sales không có quyền thiết lập/cập nhật KPI

### 3.5 Business Rule

- KPI có thể được thiết lập theo chu kỳ:
  - Nếu chỉ có `year`: KPI áp dụng cho cả năm
  - Nếu có cả `year` và `quarter`: KPI áp dụng cho quý cụ thể trong năm
  - Nếu có cả `year`, `quarter` và `month`: KPI áp dụng cho tháng cụ thể
- Không được phép thiết lập nhiều KPI trùng nhau cho cùng một nhân viên, cùng chu kỳ
- API hỗ trợ cả thêm mới và cập nhật:
  - Nếu có `id` -> cập nhật KPI đã tồn tại
  - Nếu không có `id` -> thêm mới KPI
- Khi cập nhật KPI đã tồn tại, hệ thống ghi nhận lịch sử thay đổi

---

## 4. Request Example

```json
{
  "salesId": 201,
  "year": 2025,
  "quarter": 3,
  "month": null,
  "targetRevenue": 500000000,
  "note": "KPI quý 3/2025 cho Nguyễn Văn Sales"
}
```

## 5. Response

### 5.1 Success - 200 OK (Cập nhật) hoặc 201 Created (Thêm mới)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 (Cập nhật) hoặc 201 (Thêm mới) |
| `message` | String | Thông báo kết quả: "Đã thiết lập KPI doanh thu thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về KPI đã tạo/cập nhật |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi KPI |
| `year` | Integer | Năm áp dụng KPI |
| `quarter` | Integer/null | Quý áp dụng KPI (1-4, null nếu là KPI theo năm) |
| `month` | Integer/null | Tháng áp dụng KPI (1-12, null nếu là KPI theo năm hoặc quý) |
| `salesId` | Integer | ID của nhân viên Sales |
| `salesCode` | String | Mã nhân viên Sales |
| `salesName` | String | Tên nhân viên Sales |
| `teamId` | Integer | ID của team |
| `teamName` | String | Tên team |
| `targetRevenue` | Number | Doanh thu mục tiêu (VND) |
| `actualRevenue` | Number | Doanh thu thực tế hiện tại (0 nếu mới thiết lập) |
| `achievement` | Number | Tỷ lệ hoàn thành hiện tại (%) |
| `status` | String | Trạng thái KPI (NOT_STARTED, IN_PROGRESS, ACHIEVED, MISSED) |
| `note` | String | Ghi chú về KPI |
| `createdBy` | String | Người tạo KPI |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 201,
  "message": "Đã thiết lập KPI doanh thu thành công",
  "data": {
    "id": 5,
    "year": 2025,
    "quarter": 3,
    "month": null,
    "salesId": 201,
    "salesCode": "SL001",
    "salesName": "Nguyễn Văn Sales",
    "teamId": 5,
    "teamName": "Team Sales Alpha",
    "targetRevenue": 500000000,
    "actualRevenue": 0,
    "achievement": 0,
    "status": "NOT_STARTED",
    "note": "KPI quý 3/2025 cho Nguyễn Văn Sales",
    "createdBy": "admin.user",
    "createdAt": "2025-06-15T09:30:00Z"
  }
}
```

### 5.2 Error Responses

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1001",
  "message": "Chưa xác thực hoặc phiên làm việc đã hết hạn"
}
```

#### 403 Forbidden
```json
{
  "status": "error",
  "code": "E1002",
  "message": "Bạn không có quyền thiết lập KPI doanh thu"
}
```

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "targetRevenue",
      "message": "Giá trị doanh thu mục tiêu phải lớn hơn 0"
    }
  ]
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy nhân viên Sales với ID: 999"
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Đã tồn tại KPI cho nhân viên Sales này trong cùng thời gian (năm 2025, quý 3)"
}
``` 