# API Details: Xóa file đính kèm

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API xóa file đính kèm | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để xóa một file đính kèm không còn cần thiết khỏi hợp đồng, cho phép người dùng có thẩm quyền quản lý linh hoạt các tài liệu liên quan đến hợp đồng, loại bỏ những file không phù hợp, lỗi thời hoặc đã tải lên nhầm.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-011                                  |
| **Tên API**        | Xóa file đính kèm                            |
| **Mô tả**          | API cho phép xóa một file đính kèm đã upload |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/contracts/files/{fileId}`           |
| **Quyền truy cập** | contract:file:delete                         |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `fileId`       | Long         | Có       | ID của file cần xóa |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `fileId`       | Phải tồn tại trong hệ thống         |

### 3.4 Phân quyền đặc biệt
- Sales: Chỉ xóa được file do chính mình đã upload
- Division Manager: Xóa được file của hợp đồng thuộc bộ phận mình quản lý
- Kế toán: Chỉ xóa được file do chính mình đã upload
- Admin: Xóa được tất cả file đính kèm

### 3.5 Business Rule

- Hệ thống sẽ ghi nhận thông tin người xóa và thời gian xóa
- File bị xóa sẽ được đánh dấu là đã xóa (soft delete) trong CSDL và không hiển thị trong danh sách
- Đối với file thuộc loại `contract` (hợp đồng chính thức) hoặc `invoice` (hóa đơn) đã tồn tại trên 30 ngày, chỉ Admin mới có quyền xóa

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Đã xóa file thành công" |
| `data` | Object | Đối tượng chứa thông tin cơ bản về file đã xóa |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của file đã xóa |
| `fileName` | String | Tên file đã xóa |
| `contractId` | Integer | ID của hợp đồng liên quan |
| `contractCode` | String | Mã hợp đồng liên quan |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "message": "Đã xóa file thành công",
  "data": {
    "id": 4,
    "fileName": "HD-ABC-Final-20250511.pdf",
    "contractId": 123,
    "contractCode": "HD-2025-123"
  }
}
```

### 4.2 Error Responses

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
  "message": "Bạn không có quyền xóa file này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3007",
  "message": "Không tìm thấy file với ID: 4"
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4004",
  "message": "Không thể xóa file hợp đồng chính thức đã tồn tại trên 30 ngày, vui lòng liên hệ Admin"
}
``` 