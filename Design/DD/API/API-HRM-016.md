# API Details: Xóa kỹ năng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-03 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên xóa một kỹ năng (skill) khỏi hệ thống, giúp duy trì danh sách kỹ năng gọn gàng và phù hợp với nhu cầu thực tế của tổ chức, đồng thời kiểm tra các ràng buộc liên quan đến việc sử dụng kỹ năng của nhân viên.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-016                                  |
| **Tên API**        | Xóa kỹ năng                                  |
| **Mô tả**          | API cho phép xóa một kỹ năng (cần kiểm tra ràng buộc) |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/admin/skills/{id}`                  |
| **Quyền truy cập** | skill:delete                                 |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên  | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------|--------------|----------|-------|
| `id` | Integer      | Có       | ID của kỹ năng cần xóa |

### 3.3 Query Parameters

| Tên          | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------|--------------|----------|-------|
| `force`      | Boolean      | Không    | Nếu `true`, xóa kỹ năng kể cả khi có nhân viên đang sử dụng (xóa cả các bản ghi kỹ năng của nhân viên); nếu `false`, chỉ xóa khi không có nhân viên nào sử dụng kỹ năng này (mặc định: `false`) |

### 3.4 Validate Rule

| Trường     | Điều kiện hợp lệ |
|------------|------------------|
| `id`       | Phải là số nguyên dương và tồn tại trong hệ thống |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả thực hiện |
| `data` | Object | Đối tượng chứa thông tin kỹ năng đã xóa |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng đã xóa |
| `name` | String | Tên kỹ năng đã xóa |
| `employeeCount` | Integer | Số lượng nhân viên đã có kỹ năng này (trước khi xóa) |

```json
{
  "status": "success",
  "code": 200,
  "message": "Xóa kỹ năng thành công",
  "data": {
    "id": 51,
    "name": "Docker & Kubernetes",
    "employeeCount": 0
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
      "field": "id",
      "message": "ID kỹ năng phải là số nguyên dương"
    }
  ]
}
```

#### 401 Unauthorized

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E1000 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E1000",
  "message": "Token không hợp lệ hoặc đã hết hạn"
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
  "message": "Không có quyền truy cập chức năng này"
}
```

#### 404 Not Found

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3000 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy kỹ năng với ID: 99"
}
```

#### 409 Conflict

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E4001 |
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
  "code": "E4001",
  "message": "Không thể xóa kỹ năng",
  "errors": [
    {
      "field": "id",
      "message": "Kỹ năng này đang được sử dụng bởi 15 nhân viên. Hãy sử dụng tham số 'force=true' nếu muốn xóa kỹ năng và tất cả dữ liệu liên quan."
    }
  ]
}
```

#### 500 Internal Server Error

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E6000 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi xóa kỹ năng"
}
``` 