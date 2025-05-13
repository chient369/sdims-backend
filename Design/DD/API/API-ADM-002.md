# API Details: Tạo người dùng mới

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để tạo người dùng mới trong hệ thống quản trị.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-002                                  |
| **Tên API**        | Tạo người dùng mới                           |
| **Mô tả**          | API cho phép admin tạo người dùng mới trong hệ thống với quyền và thông tin cơ bản |
| **Module**         | Quản trị Hệ thống (Admin)                    |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/admin/users`                        |
| **Quyền truy cập** | user:create                                  |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

| Tên           | Kiểu dữ liệu | Bắt buộc | Mô tả |
|---------------|--------------|----------|-------|
| `username`    | String       | Có       | Tên đăng nhập của người dùng |
| `email`       | String       | Có       | Email của người dùng |
| `fullname`    | String       | Có       | Họ tên người dùng |
| `password`    | String       | Có       | Mật khẩu (đã mã hóa bằng bcrypt hoặc cơ chế tương tự) |
| `roleId`      | Integer      | Có       | ID của vai trò (role) |
| `employeeId`  | Integer      | Không    | ID của nhân viên liên kết (nếu có) |
| `status`      | String       | Có       | Trạng thái: `Active`, `Inactive` |
| `phoneNumber` | String       | Không    | Số điện thoại liên hệ |
| `note`        | String       | Không    | Ghi chú |

### 3.3 Validate Rule

| Trường          | Điều kiện hợp lệ |
|-----------------|------------------|
| `username`      | Độ dài: 3-50 ký tự, Chỉ chứa chữ cái, số và dấu gạch dưới, Duy nhất trong hệ thống |
| `email`         | Định dạng email hợp lệ, Duy nhất trong hệ thống |
| `fullname`      | Độ dài: 3-100 ký tự |
| `password`      | Độ dài: >= 8 ký tự, Phải chứa ít nhất 1 chữ cái thường, 1 chữ cái hoa, 1 số |
| `roleId`        | Phải là ID của vai trò có trong hệ thống |
| `employeeId`    | Nếu có, phải là ID của nhân viên có trong hệ thống |
| `status`        | Phải là một trong: `Active`, `Inactive` |
| `phoneNumber`   | Nếu có, phải có định dạng số điện thoại hợp lệ |

---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `message` | String | Thông báo kết quả: "Tạo người dùng thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết người dùng vừa tạo |

#### User Object (data)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `username` | String | Tên đăng nhập của người dùng |
| `email` | String | Địa chỉ email của người dùng |
| `fullname` | String | Họ tên đầy đủ của người dùng |
| `role` | Object | Thông tin vai trò của người dùng |
| `employee` | Object/null | Thông tin nhân viên liên kết (null nếu không liên kết) |
| `status` | String | Trạng thái tài khoản: "Active", "Inactive" |
| `phoneNumber` | String | Số điện thoại liên hệ |
| `note` | String | Ghi chú |
| `createdAt` | DateTime | Thời gian tạo tài khoản (ISO 8601) |
| `createdBy` | String | Người tạo tài khoản |
| `updatedAt` | DateTime | Thời gian cập nhật gần nhất (ISO 8601) |

#### Role Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của vai trò |
| `name` | String | Tên vai trò |

#### Employee Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên liên kết |
| `code` | String | Mã nhân viên |
| `name` | String | Tên nhân viên |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 201,
  "message": "Tạo người dùng thành công",
  "data": {
    "id": 23,
    "username": "nguyenvana",
    "email": "a.nguyenvan@company.com",
    "fullname": "Nguyễn Văn A",
    "role": {
      "id": 3,
      "name": "Employee"
    },
    "employee": {
      "id": 45,
      "code": "NV045",
      "name": "Nguyễn Văn A"
    },
    "status": "Active",
    "phoneNumber": "0901234567",
    "note": "Nhân viên mới phòng kỹ thuật",
    "createdAt": "2025-05-01T09:15:30Z",
    "createdBy": "admin",
    "updatedAt": "2025-05-01T09:15:30Z"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request - Thiếu tham số bắt buộc
```json
{
  "status": "error",
  "code": "E2001",
  "message": "Thiếu tham số bắt buộc",
  "errors": [
    {
      "field": "username",
      "message": "Username không được để trống"
    },
    {
      "field": "password",
      "message": "Password không được để trống"
    }
  ]
}
```

#### 400 Bad Request - Dữ liệu không hợp lệ
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "email",
      "message": "Email không đúng định dạng"
    },
    {
      "field": "password",
      "message": "Password phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường và số"
    }
  ]
}
```

#### 400 Bad Request - Dữ liệu đã tồn tại
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Dữ liệu đã tồn tại",
  "errors": [
    {
      "field": "username",
      "message": "Username đã được sử dụng"
    }
  ]
}
```

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

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3004",
  "message": "Không tìm thấy vai trò (role) với ID: 999"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi tạo người dùng"
}
``` 