# API Details: Lấy danh sách các quyền

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo tài liệu API lấy danh sách quyền | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để lấy danh sách tất cả các quyền có sẵn trong hệ thống, phục vụ cho việc quản lý phân quyền người dùng.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-010                                  |
| **Tên API**        | Lấy danh sách các quyền                      |
| **Mô tả**          | API cung cấp danh sách tất cả các quyền có sẵn trong hệ thống |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/admin/permissions`                  |
| **Quyền truy cập** | permission:read                              |

---

## 3. Parameters

### 3.1 Query Parameters

| Tên               | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|-------------------|----------------------|----------|-------|
| `keyword`         | String               | Không    | Tìm kiếm theo tên hoặc mã quyền |
| `group`           | String               | Không    | Lọc theo nhóm quyền |
| `roleId`          | Integer              | Không    | Nếu được chỉ định, API sẽ đánh dấu quyền nào đã được gán cho vai trò này |
| `page`            | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`            | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `100`) |
| `sortBy`          | String               | Không    | Trường sắp xếp (mặc định: `group`) |
| `sortDir`         | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `asc`) |

### 3.2 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 200          |
| `sortDir`         | `asc`, `desc`    |
| `roleId`          | Số nguyên dương, phải tồn tại trong hệ thống |
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu quyền và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Mảng các đối tượng thông tin quyền |
| `groups` | Array of String | Danh sách tất cả các nhóm quyền có trong hệ thống |
| `pageable` | Object | Thông tin phân trang |

#### Permission Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của quyền |
| `code` | String | Mã quyền theo định dạng resource:action |
| `description` | String | Mô tả chi tiết về quyền |
| `group` | String | Nhóm chức năng của quyền |
| `isAssigned` | Boolean | Đánh dấu quyền đã được gán cho vai trò (chỉ có khi tham số roleId được chỉ định) |

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
        "code": "user:create",
        "description": "Tạo người dùng mới",
        "group": "User Management",
        "isAssigned": false
      },
      {
        "id": 2,
        "code": "user:read",
        "description": "Xem thông tin người dùng",
        "group": "User Management",
        "isAssigned": true
      },
      {
        "id": 3,
        "code": "user:update",
        "description": "Cập nhật thông tin người dùng",
        "group": "User Management",
        "isAssigned": true
      },
      {
        "id": 4,
        "code": "user:delete",
        "description": "Xóa người dùng",
        "group": "User Management",
        "isAssigned": false
      },
      {
        "id": 5,
        "code": "role:create",
        "description": "Tạo vai trò mới",
        "group": "Role Management",
        "isAssigned": false
      },
      {
        "id": 6,
        "code": "role:read",
        "description": "Xem thông tin vai trò",
        "group": "Role Management",
        "isAssigned": true
      },
      {
        "id": 30,
        "code": "margin:read",
        "description": "Xem thông tin margin",
        "group": "Margin Management",
        "isAssigned": false
      }
    ],
    "groups": [
      "User Management",
      "Role Management",
      "Employee Management",
      "Project Management",
      "Margin Management",
      "Report Management",
      "Contract Management"
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 100,
      "totalPages": 1,
      "totalElements": 45,
      "sort": "group,asc"
    }
  }
}
```

### 4.2 Error Responses

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1001",
  "message": "Chưa đăng nhập"
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
      "message": "Kích thước trang phải từ 1 đến 200"
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

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi truy vấn danh sách quyền"
}
``` 