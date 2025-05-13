# API Details: Lấy danh sách file đính kèm của hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API lấy danh sách file đính kèm của hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để truy xuất danh sách các file đã được đính kèm vào một hợp đồng cụ thể, cho phép người dùng dễ dàng xem các tài liệu liên quan và tải xuống khi cần thiết, hỗ trợ việc quản lý tài liệu hợp đồng một cách hiệu quả.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-009                                  |
| **Tên API**        | Lấy danh sách file đính kèm của hợp đồng     |
| **Mô tả**          | API cho phép lấy danh sách các file đã đính kèm vào một hợp đồng cụ thể |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/contracts/{contractId}/files`       |
| **Quyền truy cập** | contract:read                                |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Long         | Có       | ID của hợp đồng cần lấy danh sách file |

### 3.3 Query Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `fileType`     | String       | Không    | Loại file cần lọc (pdf, image, doc, excel, other) |

### 3.4 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `contractId`   | Phải tồn tại trong hệ thống         |
| `fileType`     | Một trong các giá trị: `pdf`, `image`, `doc`, `excel`, `other` |

### 3.5 Phân quyền đặc biệt
- Leader: Chỉ xem được các hợp đồng có liên kết với nhân viên thuộc team mình quản lý
- Sales: Xem được các hợp đồng do mình phụ trách
- Division Manager: Xem được tất cả hợp đồng thuộc bộ phận mình quản lý
- Kế toán: Xem được tất cả hợp đồng
- Admin: Xem được tất cả hợp đồng

### 3.6 Business Rule

- File đính kèm được phân loại thành các nhóm: 
  - `pdf`: Các file PDF
  - `image`: Các file hình ảnh (png, jpg, jpeg, gif)
  - `doc`: Các file Word (doc, docx)
  - `excel`: Các file Excel (xls, xlsx)
  - `other`: Các loại file khác
- Dữ liệu trả về được sắp xếp theo thứ tự thời gian upload giảm dần (mới nhất lên đầu)

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin về hợp đồng và danh sách file đính kèm |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contractId` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `files` | Array | Danh sách các file đính kèm của hợp đồng |
| `totalFiles` | Integer | Tổng số file đính kèm |

#### File Object (trong mảng files)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của file |
| `fileName` | String | Tên file đính kèm |
| `fileType` | String | Loại file (pdf, image, doc, excel, other) |
| `fileSize` | Integer | Kích thước file (bytes) |
| `description` | String | Mô tả về file |
| `uploadedBy` | String | Người upload file |
| `uploadedAt` | String | Thời gian upload (định dạng ISO 8601) |
| `downloadUrl` | String | URL để tải file |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "contractId": 123,
    "contractCode": "CTR-2025-123",
    "name": "Phát triển ứng dụng quản lý cho Công ty ABC",
    "files": [
      {
        "id": 1,
        "fileName": "HD-ABC-Signed.pdf",
        "fileType": "pdf",
        "fileSize": 2048576,
        "description": "Hợp đồng đã ký",
        "uploadedBy": "nguyen.sales",
        "uploadedAt": "2025-05-10T14:30:00Z",
        "downloadUrl": "/api/v1/contracts/files/1/download"
      },
      {
        "id": 2,
        "fileName": "Phu-luc-1.pdf",
        "fileType": "pdf",
        "fileSize": 1048576,
        "description": "Phụ lục 1 - Danh mục yêu cầu",
        "uploadedBy": "nguyen.sales",
        "uploadedAt": "2025-05-10T14:35:00Z",
        "downloadUrl": "/api/v1/contracts/files/2/download"
      },
      {
        "id": 3,
        "fileName": "Invoice-Dot1.xlsx",
        "fileType": "excel",
        "fileSize": 524288,
        "description": "Hóa đơn đợt 1",
        "uploadedBy": "tran.ketoan",
        "uploadedAt": "2025-05-20T09:15:00Z",
        "downloadUrl": "/api/v1/contracts/files/3/download"
      }
    ],
    "totalFiles": 3
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
  "message": "Bạn không có quyền xem file đính kèm của hợp đồng này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3003",
  "message": "Không tìm thấy hợp đồng với ID: 123"
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
      "field": "fileType",
      "message": "Loại file không hợp lệ"
    }
  ]
}
``` 