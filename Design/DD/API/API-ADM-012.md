# API Details: Cập nhật giá trị cấu hình

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-02 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên cập nhật giá trị của các tham số cấu hình hệ thống, giúp điều chỉnh và tùy biến hoạt động của hệ thống mà không cần can thiệp vào mã nguồn.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-012                                  |
| **Tên API**        | Cập nhật giá trị cấu hình                    |
| **Mô tả**          | API cập nhật giá trị của một tham số cấu hình hệ thống |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/admin/configs/{configKey}`          |
| **Quyền truy cập** | config:update                                |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên          | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------|--------------|----------|-------|
| `configKey`  | String       | Có       | Khóa cấu hình cần cập nhật |

### 3.3 Request Body

| Tên       | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------|--------------|----------|-------|
| `value`   | String       | Có       | Giá trị mới của cấu hình |

### 3.4 Validate Rule
| Trường      | Điều kiện hợp lệ |
|-------------|------------------|
| `configKey` | Phải tồn tại trong hệ thống, phải là cấu hình có thể chỉnh sửa (isEditable=true) |
| `value`     | Phải phù hợp với kiểu dữ liệu của cấu hình, không được null hoặc rỗng |
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin cấu hình đã cập nhật |

#### Configuration Object (data)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `key` | String | Khóa định danh cấu hình đã cập nhật |
| `value` | String | Giá trị mới của cấu hình |
| `previousValue` | String | Giá trị trước khi cập nhật |
| `type` | String | Kiểu dữ liệu: STRING, INTEGER, BOOLEAN, SECRET, ... |
| `category` | String | Danh mục cấu hình |
| `description` | String | Mô tả chi tiết về cấu hình |
| `updatedAt` | DateTime | Thời gian cập nhật (ISO 8601) |
| `updatedBy` | Object | Thông tin người cập nhật cấu hình |

#### Updater Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người cập nhật cấu hình |
| `username` | String | Tên đăng nhập của người cập nhật |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "key": "margin.threshold.red",
    "value": "20",
    "previousValue": "25",
    "type": "INTEGER",
    "category": "MARGIN",
    "description": "Ngưỡng margin cảnh báo đỏ (<=)",
    "updatedAt": "2025-05-02T13:45:30Z",
    "updatedBy": {
      "id": 1,
      "username": "admin"
    }
  }
}
```

### 4.2 Error Responses

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1000",
  "message": "Token không hợp lệ hoặc đã hết hạn"
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

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Dữ liệu đầu vào không hợp lệ",
  "errors": [
    {
      "field": "value",
      "message": "Giá trị không hợp lệ cho cấu hình kiểu INTEGER"
    }
  ]
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy cấu hình với khóa: 'unknown.config.key'"
}
```

#### 422 Unprocessable Entity
```json
{
  "status": "error",
  "code": "E4005",
  "message": "Cấu hình này không thể chỉnh sửa"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi cập nhật cấu hình"
}
``` 