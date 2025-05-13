# API Details: Xóa loại kỹ năng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-03 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2025-05-10 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên xóa một loại kỹ năng (skill category) khỏi hệ thống, giúp duy trì cấu trúc phân loại kỹ năng gọn gàng và phù hợp với nhu cầu của tổ chức.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-012                                  |
| **Tên API**        | Xóa loại kỹ năng                             |
| **Mô tả**          | API cho phép xóa một loại kỹ năng (cần kiểm tra ràng buộc) |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/admin/skill-categories/{id}`        |
| **Quyền truy cập** | skill:delete                                 |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên  | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------|--------------|----------|-------|
| `id` | Integer      | Có       | ID của loại kỹ năng cần xóa |

### 3.3 Query Parameters

| Tên          | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------|--------------|----------|-------|
| `force`      | Boolean      | Không    | Nếu `true`, xóa loại kỹ năng và tất cả kỹ năng liên quan; nếu `false`, chỉ xóa khi không có kỹ năng nào trong loại này (mặc định: `false`) |

### 3.4 Validate Rule

| Trường     | Điều kiện hợp lệ |
|------------|------------------|
| `id`       | Phải là số nguyên dương và tồn tại trong hệ thống |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Xóa loại kỹ năng thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về loại kỹ năng đã xóa |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng đã xóa |
| `name` | String | Tên loại kỹ năng đã xóa |
| `skillCount` | Integer | Số lượng kỹ năng thuộc loại này (và đã bị xóa nếu force=true) |

```json
{
  "status": "success",
  "code": 200,
  "message": "Xóa loại kỹ năng thành công",
  "data": {
    "id": 9,
    "name": "DevOps & CI/CD",
    "skillCount": 0
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E4003",
  "message": "Không thể xóa do có dữ liệu liên quan",
  "errors": [
    {
      "field": "id",
      "message": "Loại kỹ năng này đang chứa 5 kỹ năng. Hãy sử dụng tham số 'force=true' nếu muốn xóa cả loại và kỹ năng."
    }
  ]
}
```

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
  "message": "Không có quyền truy cập chức năng này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy dữ liệu",
  "errors": [
    {
      "field": "id",
      "message": "Không tìm thấy loại kỹ năng với ID: 99"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4002",
  "message": "Dữ liệu vi phạm ràng buộc",
  "errors": [
    {
      "field": "id",
      "message": "Có 8 nhân viên đang sử dụng các kỹ năng trong loại này"
    }
  ]
}
``` 