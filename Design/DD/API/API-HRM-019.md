# API Details: Xóa kỹ năng khỏi hồ sơ nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-06-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API xóa kỹ năng khỏi hồ sơ nhân viên | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để xóa một kỹ năng không còn phù hợp khỏi hồ sơ của nhân viên, giúp duy trì tính chính xác của hồ sơ kỹ năng và đảm bảo thông tin được cập nhật khi nhân viên không còn sử dụng hoặc không còn thành thạo một kỹ năng cụ thể.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-019                                  |
| **Tên API**        | Xóa kỹ năng khỏi hồ sơ nhân viên             |
| **Mô tả**          | API cho phép xóa một kỹ năng khỏi hồ sơ của nhân viên |
| **Module**         | Quản lý Nhân sự                              |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/employees/{employeeId}/skills/{skillId}` |
| **Quyền truy cập** | employee:profile:update                      |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên          | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------|--------------|----------|-------|
| `employeeId` | Integer      | Có       | ID của nhân viên cần xóa kỹ năng |
| `skillId`    | Integer      | Có       | ID của kỹ năng cần xóa khỏi hồ sơ nhân viên |

### 3.3 Validate Rule

| Trường        | Điều kiện hợp lệ |
|---------------|------------------|
| `employeeId`  | Số nguyên dương, phải tồn tại trong hệ thống |
| `skillId`     | Số nguyên dương, phải tồn tại trong hồ sơ của nhân viên |

### 3.4 Phân quyền đặc biệt

- Nhân viên: Chỉ xóa kỹ năng của chính mình
- Leader: Xóa kỹ năng của nhân viên trong team của mình
- Division Manager: Xóa kỹ năng của nhân viên thuộc bộ phận mình quản lý
- Admin: Xóa kỹ năng của tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả thực hiện |
| `data` | Object | Đối tượng chứa thông tin về kỹ năng đã xóa khỏi hồ sơ nhân viên |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `deletedSkill` | Object | Thông tin kỹ năng đã xóa |

#### DeletedSkill Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `category` | Object | Thông tin về loại kỹ năng |

#### Category Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng |
| `name` | String | Tên loại kỹ năng |

```json
{
  "status": "success",
  "code": 200,
  "message": "Xóa kỹ năng khỏi hồ sơ nhân viên thành công",
  "data": {
    "employeeId": 12,
    "employeeCode": "NV012",
    "name": "Hoàng Văn F",
    "deletedSkill": {
      "id": 1,
      "name": "Java",
      "category": {
        "id": 1,
        "name": "Programming Language"
      }
    }
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E2000 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `field` | String | Tên trường dữ liệu gây lỗi |
| `message` | String | Thông báo chi tiết về lỗi |

```json
{
  "status": "error",
  "code": "E2000",
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "employeeId",
      "message": "ID nhân viên phải là số nguyên dương"
    }
  ]
}
```

#### 401 Unauthorized

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E1001 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E1001",
  "message": "Chưa xác thực hoặc phiên làm việc đã hết hạn"
}
```

#### 403 Forbidden

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E1002 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E1002",
  "message": "Bạn không có quyền xóa kỹ năng khỏi hồ sơ nhân viên này"
}
```

#### 404 Not Found

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3000 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `field` | String | Tên trường dữ liệu gây lỗi |
| `message` | String | Thông báo chi tiết về lỗi |

```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy dữ liệu",
  "errors": [
    {
      "field": "employeeId",
      "message": "Không tìm thấy nhân viên với ID: 999"
    }
  ]
}
```

```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy dữ liệu",
  "errors": [
    {
      "field": "skillId",
      "message": "Không tìm thấy kỹ năng với ID: 5 trong hồ sơ của nhân viên này"
    }
  ]
}
``` 