# API Details: Cập nhật vai trò

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-02 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên cập nhật thông tin và các quyền được gán cho vai trò trong hệ thống, giúp quản lý cấu trúc phân quyền một cách linh hoạt và phù hợp với sự thay đổi của tổ chức.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-008                                  |
| **Tên API**        | Cập nhật vai trò                             |
| **Mô tả**          | API cập nhật thông tin và quyền của vai trò  |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/admin/roles/{roleId}`               |
| **Quyền truy cập** | role:update                                  |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `roleId`   | Integer      | Có       | ID của vai trò cần cập nhật |

### 3.3 Request Body

| Tên             | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|-----------------|----------------------|----------|-------|
| `name`          | String               | Không    | Tên mới của vai trò |
| `description`   | String               | Không    | Mô tả mới về vai trò |
| `permissionIds` | Array of Integer     | Không    | Danh sách ID quyền được gán cho vai trò (thay thế hoàn toàn danh sách cũ) |

### 3.4 Validate Rule
| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `roleId`       | Số nguyên dương, phải tồn tại trong hệ thống, không phải là vai trò hệ thống (isSystem=true) |
| `name`         | Độ dài 3-50 ký tự, phải duy nhất trong hệ thống |
| `description`  | Độ dài tối đa 255 ký tự |
| `permissionIds`| Mảng không rỗng, các ID phải tồn tại trong hệ thống |
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin chi tiết vai trò sau khi cập nhật |

#### Role Object (data)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của vai trò |
| `name` | String | Tên vai trò đã cập nhật |
| `description` | String | Mô tả chi tiết về vai trò đã cập nhật |
| `userCount` | Integer | Số lượng người dùng đang được gán vai trò này |
| `isSystem` | Boolean | Đánh dấu vai trò hệ thống (không thể xóa) |
| `permissions` | Array | Danh sách các quyền mới của vai trò |
| `createdAt` | DateTime | Thời gian tạo vai trò ban đầu (ISO 8601) |
| `updatedAt` | DateTime | Thời gian cập nhật gần nhất (ISO 8601) |
| `updatedBy` | Object | Thông tin người cập nhật vai trò |

#### Permission Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của quyền |
| `code` | String | Mã quyền theo định dạng resource:action |
| `description` | String | Mô tả chi tiết về quyền |
| `group` | String | Nhóm chức năng của quyền |

#### Updater Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người cập nhật vai trò |
| `username` | String | Tên đăng nhập của người cập nhật |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": 3,
    "name": "Employee Updated",
    "description": "Nhân viên thông thường với quyền cập nhật",
    "userCount": 38,
    "isSystem": false,
    "permissions": [
      {
        "id": 10,
        "code": "employee:read",
        "description": "Xem thông tin nhân viên (giới hạn)",
        "group": "Employee Management"
      },
      {
        "id": 12,
        "code": "employee:self-update",
        "description": "Cập nhật thông tin cá nhân",
        "group": "Employee Management"
      },
      {
        "id": 40,
        "code": "report:read",
        "description": "Xem báo cáo",
        "group": "Report Management"
      }
    ],
    "createdAt": "2025-01-01T10:15:00Z",
    "updatedAt": "2025-05-02T10:30:45Z",
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
  "code": "E3004",
  "message": "Không tìm thấy vai trò với ID: 999"
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4004",
  "message": "Không thể cập nhật vai trò hệ thống"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi cập nhật vai trò"
}
``` 