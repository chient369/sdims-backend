# API Details: Cập nhật loại kỹ năng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-03 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2025-05-10 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để cho phép cập nhật thông tin của một loại kỹ năng hiện có trong hệ thống. Chỉ Admin hoặc người dùng có quyền thích hợp mới được phép thực hiện.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-011                                  |
| **Tên API**        | Cập nhật loại kỹ năng                        |
| **Mô tả**          | API cho phép cập nhật thông tin của một loại kỹ năng |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/admin/skill-categories/{id}`        |
| **Quyền truy cập** | skill:update                                 |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên  | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------|--------------|----------|-------|
| `id` | Integer      | Có       | ID của loại kỹ năng cần cập nhật |

### 3.3 Request Body

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `name`         | String       | Không    | Tên loại kỹ năng |
| `description`  | String       | Không    | Mô tả về loại kỹ năng |
| `active`       | Boolean      | Không    | Trạng thái kích hoạt |
| `sortOrder`    | Integer      | Không    | Thứ tự sắp xếp |

### 3.4 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `id`           | Phải là số nguyên dương và tồn tại trong hệ thống |
| `name`         | Độ dài: 1-100 ký tự, Không được trùng lặp với các loại kỹ năng khác |
| `description`  | Độ dài tối đa: 500 ký tự |
| `sortOrder`    | Số nguyên ≥ 0 |

### 3.5 Phân quyền đặc biệt
- Chỉ người dùng có quyền `skill:update` mới được cập nhật thông tin loại kỹ năng
- Theo ma trận CRUD, chỉ Admin và Division Manager có quyền này

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Cập nhật loại kỹ năng thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về loại kỹ năng sau khi cập nhật |

#### Data Object (SkillCategory)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng |
| `name` | String | Tên loại kỹ năng (đã cập nhật) |
| `description` | String | Mô tả về loại kỹ năng (đã cập nhật) |
| `active` | Boolean | Trạng thái kích hoạt (đã cập nhật) |
| `sortOrder` | Integer | Thứ tự sắp xếp (đã cập nhật) |
| `updatedAt` | String | Thời gian cập nhật (định dạng ISO 8601) |
| `updatedBy` | String | Người thực hiện cập nhật |

```json
{
  "status": "success",
  "code": 200,
  "message": "Cập nhật loại kỹ năng thành công",
  "data": {
    "id": 9,
    "name": "DevOps & CI/CD",
    "description": "Các kỹ năng liên quan đến DevOps và Continuous Integration/Continuous Deployment",
    "active": true,
    "sortOrder": 7,
    "updatedAt": "2025-05-02T11:45:00Z",
    "updatedBy": "admin"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Tham số không hợp lệ",
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
      "message": "Loại kỹ năng 'Cloud' đã tồn tại trong hệ thống"
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