# API Details: Xóa hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API xóa hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để xóa mềm (soft delete) một hợp đồng không còn cần thiết trong hệ thống, cho phép loại bỏ thông tin hợp đồng khỏi giao diện người dùng nhưng vẫn duy trì dữ liệu trong cơ sở dữ liệu để đảm bảo tính toàn vẹn và khả năng phục hồi khi cần thiết.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-005                                  |
| **Tên API**        | Xóa hợp đồng                                 |
| **Mô tả**          | API cho phép xóa mềm (soft delete) hợp đồng  |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/contracts/{contractId}`             |
| **Quyền truy cập** | contract:delete                              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Integer      | Có       | ID của hợp đồng cần xóa |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `contractId`   | Số nguyên dương, phải tồn tại trong hệ thống |

### 3.4 Phân quyền đặc biệt
- Chỉ Admin và Division Manager mới có quyền xóa hợp đồng
- Không được phép xóa hợp đồng đã có thanh toán (payment term đã thu tiền)
- Sales và Leader không có quyền xóa hợp đồng

### 3.5 Business Rule
- Khi xóa hợp đồng (soft delete), hệ thống sẽ thiết lập cờ `deleted=true` và ghi lại thời điểm xóa và người thực hiện
- Các dữ liệu liên quan (payment terms, nhân sự liên kết) vẫn giữ nguyên để phục vụ việc khôi phục nếu cần
- Các báo cáo doanh thu sẽ không tính các hợp đồng đã bị xóa
- Hợp đồng đã xóa sẽ không hiển thị trong danh sách hợp đồng thông thường, chỉ hiển thị trong chức năng quản trị đặc biệt

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Hợp đồng đã được xóa thành công" |
| `data` | Object | Đối tượng chứa thông tin hợp đồng đã xóa |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `deletedAt` | String | Thời gian xóa (định dạng ISO 8601) |
| `deletedBy` | Object | Thông tin người thực hiện xóa |

#### Deleter Object (deletedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người xóa |
| `name` | String | Họ tên người xóa |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "message": "Hợp đồng đã được xóa thành công",
  "data": {
    "id": 123,
    "contractCode": "CTR-2025-123",
    "name": "Hợp đồng phát triển phần mềm ABC",
    "deletedAt": "2025-05-15T09:30:45Z",
    "deletedBy": {
      "id": 3,
      "name": "Trần Văn Admin"
    }
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Không thể xóa hợp đồng",
  "errors": [
    {
      "field": "contractId",
      "message": "Không thể xóa hợp đồng đã có thanh toán"
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
  "message": "Bạn không có quyền xóa hợp đồng"
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
      "field": "contractId",
      "message": "Không tìm thấy hợp đồng với ID: 999"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Xung đột dữ liệu",
  "errors": [
    {
      "field": "contractId",
      "message": "Hợp đồng có ID 123 đang được sử dụng trong quy trình thanh toán"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi xóa dữ liệu hợp đồng"
}
``` 