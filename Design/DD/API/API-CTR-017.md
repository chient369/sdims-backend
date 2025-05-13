# API Details: Xóa KPI doanh thu

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API xóa KPI doanh thu | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để xóa một chỉ tiêu KPI doanh thu đã thiết lập nhưng không còn phù hợp, cho phép quản lý viên loại bỏ các mục tiêu không chính xác hoặc không còn phù hợp với kế hoạch kinh doanh, đồng thời ghi nhận lịch sử thay đổi để đảm bảo tính minh bạch.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-017                                  |
| **Tên API**        | Xóa KPI doanh thu                           |
| **Mô tả**          | API cho phép Admin xóa một KPI doanh thu đã thiết lập |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/admin/sales-kpis/{kpiId}`           |
| **Quyền truy cập** | sales:kpi:delete                            |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `kpiId`        | Long         | Có       | ID của KPI cần xóa |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `kpiId`        | Phải tồn tại trong hệ thống         |

### 3.4 Phân quyền đặc biệt
- Team Leader: Chỉ xóa được KPI của nhân viên Sales thuộc team mình quản lý
- Division Manager: Xóa được KPI của tất cả nhân viên Sales thuộc bộ phận mình quản lý
- Admin: Xóa được KPI của tất cả nhân viên Sales
- Sales không có quyền xóa KPI

### 3.5 Business Rule

- Không được phép xóa KPI đã có doanh thu thực tế (actualRevenue > 0)
- Không được phép xóa KPI của chu kỳ đã đóng/kết thúc
- Hệ thống ghi nhận thông tin người xóa và thời gian xóa
- Khi xóa KPI, hệ thống ghi nhận vào lịch sử để theo dõi

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Đã xóa KPI doanh thu thành công" |
| `data` | Object | Đối tượng chứa thông tin cơ bản về KPI đã xóa |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi KPI đã xóa |
| `year` | Integer | Năm áp dụng KPI |
| `quarter` | Integer/null | Quý áp dụng KPI (1-4, null nếu là KPI theo năm) |
| `month` | Integer/null | Tháng áp dụng KPI (1-12, null nếu là KPI theo năm hoặc quý) |
| `salesId` | Integer | ID của nhân viên Sales |
| `salesCode` | String | Mã nhân viên Sales |
| `salesName` | String | Tên nhân viên Sales |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "message": "Đã xóa KPI doanh thu thành công",
  "data": {
    "id": 5,
    "year": 2025,
    "quarter": 3,
    "month": null,
    "salesId": 201,
    "salesCode": "SL001",
    "salesName": "Nguyễn Văn Sales"
  }
}
```

### 4.2 Error Responses

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
  "message": "Bạn không có quyền xóa KPI doanh thu"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy KPI với ID: 5"
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4004",
  "message": "Không thể xóa KPI đã có doanh thu thực tế"
}
```

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Không thể xóa KPI của chu kỳ đã kết thúc"
}
``` 