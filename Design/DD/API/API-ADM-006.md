# API Details: Lấy danh sách các vai trò

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp danh sách các vai trò trong hệ thống cùng với thông tin chi tiết về các quyền tương ứng của từng vai trò, giúp quản trị viên quản lý và phân quyền người dùng một cách hiệu quả.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-006                                  |
| **Tên API**        | Lấy danh sách các vai trò                    |
| **Mô tả**          | API cung cấp danh sách các vai trò (role) trong hệ thống, kèm theo quyền của từng vai trò |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/admin/roles`                        |
| **Quyền truy cập** | role:read                                    |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên               | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|-------------------|----------------------|----------|-------|
| `includePermissions` | Boolean           | Không    | Bao gồm danh sách quyền chi tiết của mỗi vai trò (mặc định: `true`) |
| `keyword`         | String               | Không    | Tìm kiếm theo tên vai trò |
| `page`            | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`            | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `20`) |
| `sortBy`          | String               | Không    | Trường sắp xếp (mặc định: `name`) |
| `sortDir`         | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `asc`) |

### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 100          |
| `sortDir`         | `asc`, `desc`    |
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu vai trò và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Mảng các đối tượng thông tin vai trò |
| `pageable` | Object | Thông tin phân trang |

#### Role Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của vai trò |
| `name` | String | Tên vai trò |
| `description` | String | Mô tả chi tiết về vai trò |
| `userCount` | Integer | Số lượng người dùng đang được gán vai trò này |
| `isSystem` | Boolean | Đánh dấu vai trò hệ thống (không thể xóa) |
| `permissions` | Array | Danh sách các quyền của vai trò (chỉ có khi includePermissions=true) |
| `createdAt` | DateTime | Thời gian tạo vai trò (ISO 8601) |
| `updatedAt` | DateTime | Thời gian cập nhật gần nhất (ISO 8601) |

#### Permission Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của quyền |
| `code` | String | Mã quyền theo định dạng resource:action |
| `description` | String | Mô tả chi tiết về quyền |
| `group` | String | Nhóm chức năng của quyền |

#### Pageable Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `pageNumber` | Integer | Số trang hiện tại |
| `pageSize` | Integer | Kích thước trang (số bản ghi mỗi trang) |
| `totalPages` | Integer | Tổng số trang |
| `totalElements` | Integer | Tổng số bản ghi |
| `sort` | String | Thông tin sắp xếp (trường,hướng) |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "content": [
      {
        "id": 1,
        "name": "Admin",
        "description": "Quản trị viên hệ thống",
        "userCount": 2,
        "isSystem": true,
        "permissions": [
          {
            "id": 1,
            "code": "user:create",
            "description": "Tạo người dùng mới",
            "group": "User Management"
          },
          {
            "id": 2,
            "code": "user:read",
            "description": "Xem thông tin người dùng",
            "group": "User Management"
          },
          {
            "id": 3,
            "code": "user:update",
            "description": "Cập nhật thông tin người dùng",
            "group": "User Management"
          },
          {
            "id": 4,
            "code": "user:delete",
            "description": "Xóa người dùng",
            "group": "User Management"
          },
          {
            "id": 5,
            "code": "role:create",
            "description": "Tạo vai trò mới",
            "group": "Role Management"
          }
          // ... more permissions
        ],
        "createdAt": "2025-01-01T08:00:00Z",
        "updatedAt": "2025-01-01T08:00:00Z"
      },
      {
        "id": 2,
        "name": "Leader",
        "description": "Leader quản lý team",
        "userCount": 5,
        "isSystem": false,
        "permissions": [
          {
            "id": 10,
            "code": "employee:read",
            "description": "Xem thông tin nhân viên",
            "group": "Employee Management"
          },
          {
            "id": 11,
            "code": "employee:update",
            "description": "Cập nhật thông tin nhân viên",
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
            "id": 30,
            "code": "margin:read",
            "description": "Xem thông tin margin",
            "group": "Margin Management"
          },
          {
            "id": 40,
            "code": "report:read",
            "description": "Xem báo cáo",
            "group": "Report Management"
          }
        ],
        "createdAt": "2025-01-01T09:30:00Z",
        "updatedAt": "2025-03-15T14:20:00Z"
      },
      {
        "id": 3,
        "name": "Employee",
        "description": "Nhân viên thông thường",
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
          }
        ],
        "createdAt": "2025-01-01T10:15:00Z",
        "updatedAt": "2025-02-20T09:45:00Z"
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 20,
      "totalPages": 1,
      "totalElements": 5,
      "sort": "name,asc"
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
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "size",
      "message": "Kích thước trang phải từ 1 đến 100"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi truy vấn danh sách vai trò"
}
``` 