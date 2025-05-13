# API Details: Tạo vai trò mới

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên tạo vai trò mới trong hệ thống với các quyền được cấu hình cụ thể, giúp xây dựng cấu trúc phân quyền linh hoạt phù hợp với nhu cầu tổ chức.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-007                                  |
| **Tên API**        | Tạo vai trò mới                              |
| **Mô tả**          | API tạo vai trò mới với danh sách quyền được gán |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/admin/roles`                        |
| **Quyền truy cập** | role:create                                  |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

| Tên             | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|-----------------|----------------------|----------|-------|
| `name`          | String               | Có       | Tên vai trò mới |
| `description`   | String               | Không    | Mô tả về vai trò |
| `permissionIds` | Array of Integer     | Có       | Danh sách ID quyền được gán cho vai trò |

### 3.3 Validate Rule
| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `name`         | Độ dài 3-50 ký tự, phải duy nhất trong hệ thống |
| `description`  | Độ dài tối đa 255 ký tự |
| `permissionIds`| Mảng không rỗng, các ID phải tồn tại trong hệ thống |
---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `data` | Object | Đối tượng chứa thông tin chi tiết vai trò vừa tạo |

#### Role Object (data)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của vai trò vừa tạo |
| `name` | String | Tên vai trò |
| `description` | String | Mô tả chi tiết về vai trò |
| `userCount` | Integer | Số lượng người dùng đang được gán vai trò này (mặc định là 0) |
| `isSystem` | Boolean | Đánh dấu vai trò hệ thống (false với vai trò tạo mới) |
| `permissions` | Array | Danh sách các quyền của vai trò |
| `createdAt` | DateTime | Thời gian tạo vai trò (ISO 8601) |
| `updatedAt` | DateTime | Thời gian cập nhật gần nhất (ISO 8601) |
| `createdBy` | Object | Thông tin người tạo vai trò |

#### Permission Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của quyền |
| `code` | String | Mã quyền theo định dạng resource:action |
| `description` | String | Mô tả chi tiết về quyền |
| `group` | String | Nhóm chức năng của quyền |

#### Creator Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người tạo vai trò |
| `username` | String | Tên đăng nhập của người tạo |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "id": 6,
    "name": "Project Manager",
    "description": "Quản lý dự án với các quyền đặc thù",
    "userCount": 0,
    "isSystem": false,
    "permissions": [
      {
        "id": 10,
        "code": "employee:read",
        "description": "Xem thông tin nhân viên",
        "group": "Employee Management"
      },
      {
        "id": 20,
        "code": "project:read",
        "description": "Xem thông tin dự án",
        "group": "Project Management"
      },
      {
        "id": 21,
        "code": "project:update",
        "description": "Cập nhật thông tin dự án",
        "group": "Project Management"
      },
      {
        "id": 22,
        "code": "project:create",
        "description": "Tạo dự án mới",
        "group": "Project Management"
      },
      {
        "id": 40,
        "code": "report:read",
        "description": "Xem báo cáo",
        "group": "Report Management"
      }
    ],
    "createdAt": "2025-05-02T09:15:30Z",
    "updatedAt": "2025-05-02T09:15:30Z",
    "createdBy": {
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
      "field": "name",
      "message": "Tên vai trò đã tồn tại trong hệ thống"
    },
    {
      "field": "permissionIds",
      "message": "Danh sách quyền không được để trống"
    }
  ]
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Một hoặc nhiều quyền không tồn tại trong hệ thống"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi tạo vai trò mới"
}
``` 