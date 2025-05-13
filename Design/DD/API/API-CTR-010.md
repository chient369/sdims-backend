# API Details: Upload file đính kèm cho hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API upload file đính kèm cho hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để tải lên và lưu trữ các tài liệu đính kèm cho một hợp đồng cụ thể, hỗ trợ việc quản lý và theo dõi các tài liệu liên quan đến hợp đồng như văn bản đã ký, phụ lục, hóa đơn, báo giá, và các tài liệu bổ sung khác.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-010                                  |
| **Tên API**        | Upload file đính kèm cho hợp đồng            |
| **Mô tả**          | API cho phép upload file đính kèm cho một hợp đồng cụ thể |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/contracts/{contractId}/files`       |
| **Quyền truy cập** | contract:upload                              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên                | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------------|--------------|----------|-------|
| `Authorization`    | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`     | String       | Có       | Phải là `multipart/form-data` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Long         | Có       | ID của hợp đồng cần upload file |

### 3.3 Request Body (Multipart Form)

| Tên            | Kiểu dữ liệu    | Bắt buộc | Mô tả |
|----------------|-----------------|----------|-------|
| `file`         | File            | Có       | File cần upload |
| `description`  | String          | Không    | Mô tả về file |
| `fileCategory` | String          | Không    | Phân loại file (mặc định: `other`) |

### 3.4 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `contractId`   | Phải tồn tại trong hệ thống         |
| `file`         | Kích thước tối đa 10MB<br>Định dạng được phép: pdf, docx, doc, xlsx, xls, png, jpg, jpeg, gif, zip |
| `description`  | Tối đa 200 ký tự                     |
| `fileCategory` | Một trong các giá trị: `contract`, `invoice`, `proposal`, `attachment`, `other` |

### 3.5 Phân quyền đặc biệt
- Sales: Chỉ upload được file cho hợp đồng do mình phụ trách
- Division Manager: Upload được file cho tất cả hợp đồng thuộc bộ phận mình quản lý
- Kế toán: Upload được file cho tất cả hợp đồng
- Admin: Upload được file cho tất cả hợp đồng

### 3.6 Business Rule

- Tên file sẽ được chuẩn hóa trước khi lưu trữ để tránh xung đột và đảm bảo an toàn
- Hệ thống sẽ tự động phân loại file theo định dạng (pdf, image, doc, excel, other) để phục vụ cho việc hiển thị và lọc
- Hệ thống sẽ ghi nhận thông tin người upload và thời gian upload
- Người dùng có thể chỉ định thêm một phân loại file theo danh mục:
  - `contract`: File hợp đồng chính thức
  - `invoice`: Hóa đơn
  - `proposal`: Đề xuất/Báo giá
  - `attachment`: Phụ lục hợp đồng
  - `other`: Loại file khác

---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `message` | String | Thông báo kết quả: "Upload file thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về file đã upload |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của file vừa upload |
| `fileName` | String | Tên file đã được chuẩn hóa trong hệ thống |
| `originalFileName` | String | Tên file gốc trước khi upload |
| `fileType` | String | Loại file dựa trên định dạng (pdf, image, doc, excel, other) |
| `fileCategory` | String | Phân loại file (contract, invoice, proposal, attachment, other) |
| `fileSize` | Integer | Kích thước file (bytes) |
| `description` | String | Mô tả về file |
| `uploadedBy` | String | Tên người dùng đã upload file |
| `uploadedAt` | String | Thời gian upload (định dạng ISO 8601) |
| `downloadUrl` | String | URL để tải file |
| `contractId` | Integer | ID của hợp đồng liên quan |
| `contractCode` | String | Mã hợp đồng liên quan |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 201,
  "message": "Upload file thành công",
  "data": {
    "id": 4,
    "fileName": "CTR-ABC-Final-20250511.pdf",
    "originalFileName": "Hợp đồng ABC.pdf",
    "fileType": "pdf",
    "fileCategory": "contract",
    "fileSize": 2048576,
    "description": "Hợp đồng chính thức đã ký",
    "uploadedBy": "nguyen.sales",
    "uploadedAt": "2025-05-11T10:30:00Z",
    "downloadUrl": "/api/v1/contracts/files/4/download",
    "contractId": 123,
    "contractCode": "CTR-2025-123"
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
  "message": "Bạn không có quyền upload file cho hợp đồng này"
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
      "field": "file",
      "message": "Kích thước file vượt quá giới hạn cho phép (10MB)"
    }
  ]
}
```

#### 415 Unsupported Media Type
```json
{
  "status": "error",
  "code": "E2003",
  "message": "Định dạng file không được hỗ trợ",
  "errors": [
    {
      "field": "file",
      "message": "Định dạng .exe không được hỗ trợ. Các định dạng được phép: pdf, docx, doc, xlsx, xls, png, jpg, jpeg, gif, zip"
    }
  ]
}
``` 