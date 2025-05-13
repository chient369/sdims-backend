# API Details: Xóa nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép xóa logic (soft delete) nhân viên khỏi hệ thống, đảm bảo dữ liệu được giữ nguyên nhưng không hiển thị trong các truy vấn thông thường.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-005                                  |
| **Tên API**        | Xóa nhân viên                                |
| **Mô tả**          | API cho phép xóa mềm (soft delete) một nhân viên theo ID |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/employees/{employeeId}`             |
| **Quyền truy cập** | employee:delete                              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên           | Kiểu dữ liệu | Bắt buộc | Mô tả |
|---------------|--------------|----------|-------|
| `employeeId`  | Integer      | Có       | ID của nhân viên cần xóa |

### 3.3 Validate Rule

| Trường        | Điều kiện hợp lệ |
|---------------|------------------|
| `employeeId`  | Phải là số nguyên dương |

### 3.4 Phân quyền đặc biệt
- employee:delete:department - Chỉ xóa được nhân viên thuộc bộ phận mình quản lý
- employee:delete - Xóa được tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Xóa nhân viên thành công" |
| `data` | Object | Đối tượng chứa thông tin cơ bản về nhân viên đã xóa |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên đã xóa |
| `employeeCode` | String | Mã nhân viên đã xóa |
| `name` | String | Họ tên của nhân viên đã xóa |
| `deletedAt` | String | Thời gian xóa (định dạng ISO 8601) |
| `deletedBy` | String | Người thực hiện xóa nhân viên |

```json
{
  "status": "success",
  "code": 200,
  "message": "Xóa nhân viên thành công",
  "data": {
    "id": 5,
    "employeeCode": "NV005",
    "name": "Phan Văn E",
    "deletedAt": "2025-05-01T16:30:00Z",
    "deletedBy": "admin"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "ID không hợp lệ"
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
  "message": "Không có quyền xóa nhân viên"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3001",
  "message": "Không tìm thấy nhân viên với ID: 999"
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4003",
  "message": "Không thể xóa do nhân viên này đang tham gia dự án hoặc có dữ liệu liên quan"
}
``` 