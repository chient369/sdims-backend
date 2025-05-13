# API Details: Thêm nhân viên mới

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới  | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp chức năng thêm nhân viên mới vào hệ thống, cho phép người dùng có quyền employee:create tạo và lưu trữ thông tin nhân viên vào cơ sở dữ liệu.

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-002                                  |
| **Tên API**        | Thêm nhân viên mới                           |
| **Mô tả**          | API cho phép thêm một nhân viên mới vào hệ thống |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/employees`                          |
| **Quyền truy cập** | employee:create                              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

| Tên                | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------------|--------------|----------|-------|
| `employeeCode`     | String       | Có       | Mã nhân viên (phải là duy nhất) |
| `name`             | String       | Có       | Họ tên nhân viên |
| `email`            | String       | Có       | Email công ty (phải là duy nhất) |
| `position`         | String       | Có       | Vị trí công việc |
| `teamId`           | Integer      | Có       | ID của team |
| `phone`            | String       | Không    | Số điện thoại |
| `address`          | String       | Không    | Địa chỉ |
| `birthDate`        | String       | Không    | Ngày sinh (định dạng: YYYY-MM-DD) |
| `joinDate`         | String       | Có       | Ngày vào công ty (định dạng: YYYY-MM-DD) |
| `emergencyContact` | Object       | Không    | Thông tin liên hệ khẩn cấp |
| `status`           | String       | Có       | Trạng thái nhân viên  |
| `avatar`           | String       | Không    | URL ảnh đại diện |
| `userId`           | Integer      | Không    | ID người dùng hệ thống (nếu đã có) |
| `note`             | String       | Không    | Ghi chú về nhân viên |

#### Chi tiết Object `emergencyContact`

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `name`     | String       | Có       | Tên người liên hệ khẩn cấp |
| `phone`    | String       | Có       | Số điện thoại người liên hệ |
| `relation` | String       | Không    | Mối quan hệ với nhân viên |

### 3.3 Validate Rule

| Trường          | Điều kiện hợp lệ |
|-----------------|------------------|
| `employeeCode`  | Độ dài: 3-20 ký tự, Chỉ chứa chữ cái, số và gạch dưới |
| `name`          | Độ dài: 3-100 ký tự |
| `email`         | Định dạng email hợp lệ, độ dài 5-100 ký tự |
| `position`      | Không được rỗng |
| `teamId`        | Phải là số nguyên dương và tồn tại trong hệ thống |
| `phone`         | Định dạng số điện thoại hợp lệ (nếu có) |
| `birthDate`     | Định dạng ngày tháng hợp lệ (YYYY-MM-DD), nhân viên phải trên 18 tuổi |
| `joinDate`      | Định dạng ngày tháng hợp lệ (YYYY-MM-DD), không được sau ngày hiện tại |
| `status`        | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned`, `PartiallyAllocated` |

---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `message` | String | Thông báo kết quả: "Tạo nhân viên thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về nhân viên đã tạo |

#### Data Object (Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên mới được tạo |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `email` | String | Địa chỉ email công ty của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `phone` | String | Số điện thoại của nhân viên |
| `address` | String | Địa chỉ của nhân viên |
| `birthDate` | String | Ngày sinh (định dạng: YYYY-MM-DD) |
| `joinDate` | String | Ngày vào công ty (định dạng: YYYY-MM-DD) |
| `emergencyContact` | Object | Thông tin liên hệ khẩn cấp |
| `status` | String | Trạng thái nhân viên (Allocated, Available, EndingSoon, OnLeave, Resigned) |
| `avatar` | String | URL ảnh đại diện |
| `userId` | Integer/null | ID người dùng hệ thống (null nếu chưa liên kết) |
| `note` | String | Ghi chú về nhân viên |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |
| `createdBy` | String | Người tạo nhân viên |

#### Team Object (trong employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Emergency Contact Object (trong employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên người liên hệ khẩn cấp |
| `phone` | String | Số điện thoại người liên hệ |
| `relation` | String | Mối quan hệ với nhân viên |

```json
{
  "status": "success",
  "code": 201,
  "message": "Tạo nhân viên thành công",
  "data": {
    "id": 46,
    "employeeCode": "NV046",
    "name": "Lê Văn C",
    "email": "c.levan@company.com",
    "position": "Developer",
    "team": {
      "id": 2,
      "name": "Team Beta"
    },
    "phone": "0987654321",
    "address": "123 Đường A, Quận B, TP.HCM",
    "birthDate": "1995-05-15",
    "joinDate": "2025-05-01",
    "emergencyContact": {
      "name": "Lê Thị D",
      "phone": "0912345678",
      "relation": "Vợ"
    },
    "status": "Available",
    "avatar": "https://example.com/avatars/default.jpg",
    "userId": null,
    "note": "Nhân viên mới tuyển dụng từ công ty X",
    "createdAt": "2025-05-01T10:30:00Z",
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
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "employeeCode",
      "message": "Mã nhân viên không được để trống"
    },
    {
      "field": "email",
      "message": "Email không đúng định dạng"
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
      "field": "employeeCode",
      "message": "Mã nhân viên đã tồn tại trong hệ thống"
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
  "code": "E3000",
  "message": "Không tìm thấy team với ID: 99"
}
``` 