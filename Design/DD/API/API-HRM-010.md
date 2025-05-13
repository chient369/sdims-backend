# API Details: Thêm loại kỹ năng mới

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-02 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2025-05-10 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để cho phép thêm một loại kỹ năng mới vào hệ thống. Chỉ Admin hoặc người dùng có quyền thích hợp mới được phép thực hiện.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-010                                  |
| **Tên API**        | Thêm loại kỹ năng mới                        |
| **Mô tả**          | API cho phép thêm một loại kỹ năng mới       |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/admin/skill-categories`             |
| **Quyền truy cập** | skill:create                                 |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `name`         | String       | Có       | Tên loại kỹ năng |
| `description`  | String       | Không    | Mô tả về loại kỹ năng |
| `active`       | Boolean      | Không    | Trạng thái kích hoạt (mặc định: `true`) |
| `sortOrder`    | Integer      | Không    | Thứ tự sắp xếp (mặc định: 999) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `name`         | Độ dài: 1-100 ký tự, Không được trùng lặp với các loại kỹ năng đã có |
| `description`  | Độ dài tối đa: 500 ký tự |
| `sortOrder`    | Số nguyên ≥ 0 |

### 3.4 Phân quyền đặc biệt
- Chỉ người dùng có quyền `skill:create` mới được thêm loại kỹ năng mới
- Theo ma trận CRUD, chỉ Admin và Division Manager có quyền này

---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `message` | String | Thông báo kết quả: "Thêm loại kỹ năng thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về loại kỹ năng mới |

#### Data Object (SkillCategory)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng mới |
| `name` | String | Tên loại kỹ năng |
| `description` | String | Mô tả về loại kỹ năng |
| `active` | Boolean | Trạng thái kích hoạt |
| `sortOrder` | Integer | Thứ tự sắp xếp |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |
| `createdBy` | String | Người tạo |

```json
{
  "status": "success",
  "code": 201,
  "message": "Thêm loại kỹ năng thành công",
  "data": {
    "id": 9,
    "name": "DevOps",
    "description": "Các kỹ năng liên quan đến DevOps",
    "active": true,
    "sortOrder": 8,
    "createdAt": "2025-05-02T10:30:00Z",
    "createdBy": "admin"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2001",
  "message": "Thiếu tham số bắt buộc",
  "errors": [
    {
      "field": "name",
      "message": "Tên loại kỹ năng không được để trống"
    }
  ]
}
```

#### 400 Bad Request (Duplicate)
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Dữ liệu đã tồn tại",
  "errors": [
    {
      "field": "name",
      "message": "Loại kỹ năng 'DevOps' đã tồn tại trong hệ thống"
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
  "message": "Bạn không có quyền truy cập chức năng này"
}
``` 