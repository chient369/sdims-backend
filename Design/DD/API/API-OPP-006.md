# API Details: Thêm ghi chú/log hoạt động cho cơ hội

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-31 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để Sales hoặc Leader được assign vào cơ hội có thể thêm ghi chú hoặc log hoạt động liên quan đến cơ hội, bao gồm khả năng đính kèm tài liệu và cập nhật trạng thái cơ hội.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-OPP-006                                  |
| **Tên API**        | Thêm ghi chú/log hoạt động cho cơ hội        |
| **Mô tả**          | API cho phép Sales/Leader được assign thêm ghi chú hoặc log hoạt động cho cơ hội |
| **Module**         | Quản lý Cơ hội Kinh doanh                    |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/opportunities/{oppId}/notes`        |
| **Quyền truy cập** | opportunity-note:create:all, opportunity-note:create:assigned |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `multipart/form-data` hoặc `application/json` tùy vào có đính kèm file hay không |

### 3.2 Path Parameters

| Tên         | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-------------|--------------|----------|-------|
| `oppId`     | Integer      | Có       | ID của cơ hội kinh doanh cần thêm ghi chú |

### 3.3 Request Body

**Nếu không có file đính kèm** (`Content-Type: application/json`):

```json
{
  "content": "Đã họp với khách hàng vào ngày 16/05/2025. Khách hàng quan tâm đến giải pháp của chúng ta và muốn xem demo trong tuần sau.",
  "activityType": "meeting",
  "meetingDate": "2025-05-16T14:30:00Z",
  "updateStatus": true,
  "newStatus": "proposal"
}
```

**Nếu có file đính kèm** (`Content-Type: multipart/form-data`):

```
// Trường data chứa JSON mô tả ở trên
content: "Đã gửi đề xuất chi tiết cho khách hàng"
activityType: "document_sent"
updateStatus: false

// File đính kèm (có thể có nhiều file)
files: [File 1]
files: [File 2]
```

### 3.4 Body Parameters

| Tên             | Kiểu dữ liệu  | Bắt buộc | Mô tả |
|-----------------|---------------|----------|-------|
| `content`       | String        | Có       | Nội dung ghi chú |
| `activityType`  | String        | Không    | Loại hoạt động: `note`, `email`, `call`, `meeting`, `document_sent`, `other` (mặc định: `note`) |
| `meetingDate`   | String (Date) | Không    | Ngày họp/gọi điện/gửi email... nếu có (định dạng ISO: YYYY-MM-DDTHH:MM:SSZ) |
| `updateStatus`  | Boolean       | Không    | Có cập nhật trạng thái cơ hội không (mặc định: `false`) |
| `newStatus`     | String        | Không*   | Trạng thái mới của cơ hội (*Bắt buộc nếu `updateStatus` là `true`) |
| `files`         | Array of File | Không    | Các file đính kèm |

### 3.5 Validate Rule

| Trường           | Điều kiện hợp lệ |
|------------------|------------------|
| `oppId`          | Số nguyên dương, phải tồn tại trong hệ thống |
| `content`        | Không được để trống, tối đa 2000 ký tự |
| `activityType`   | Một trong: `note`, `email`, `call`, `meeting`, `document_sent`, `other` |
| `meetingDate`    | Định dạng ISO: YYYY-MM-DDTHH:MM:SSZ, không được là thời gian trong tương lai |
| `updateStatus`   | Boolean: `true` hoặc `false` |
| `newStatus`      | Một trong: `new`, `contacted`, `qualified`, `proposal`, `negotiation`, `won`, `lost`, `closed` |
| `files`          | - Tối đa 5 file<br>- Mỗi file tối đa 10MB<br>- Định dạng cho phép: pdf, doc, docx, xls, xlsx, ppt, pptx, txt, png, jpg, jpeg |

### 3.6 Phân quyền đặc biệt
- Leader: Chỉ thêm được ghi chú cho các cơ hội được gán cho mình
- Sales: Thêm được ghi chú cho các cơ hội do mình tạo hoặc phụ trách
- General Manager: Thêm được ghi chú cho tất cả cơ hội thuộc bộ phận mình quản lý
- Admin: Thêm được ghi chú cho tất cả cơ hội

---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `data` | Object | Đối tượng chứa thông tin chi tiết về ghi chú đã được tạo |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `note` | Object | Thông tin chi tiết về ghi chú đã tạo |
| `statusUpdated` | Boolean | Trạng thái cơ hội đã được cập nhật hay chưa |
| `previousStatus` | String | Trạng thái trước của cơ hội (nếu đã thay đổi) |
| `newStatus` | String | Trạng thái mới của cơ hội (nếu đã thay đổi) |
| `lastInteractionDate` | String | Thời điểm tương tác mới nhất với cơ hội (ISO 8601) |

#### Note Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của ghi chú |
| `content` | String | Nội dung ghi chú |
| `activityType` | String | Loại hoạt động |
| `meetingDate` | String | Ngày họp/gọi điện/gửi email (ISO 8601) nếu có |
| `opportunity` | Object | Thông tin cơ hội liên quan |
| `attachments` | Array | Danh sách file đính kèm |
| `createdBy` | Object | Thông tin người tạo ghi chú |
| `createdAt` | String | Thời điểm tạo ghi chú (ISO 8601) |

#### Opportunity Object (trong note)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội kinh doanh |
| `code` | String | Mã cơ hội (tự động sinh) |
| `name` | String | Tên cơ hội kinh doanh |

#### User Object (trong createdBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `name` | String | Tên đầy đủ của người dùng |

#### Attachment Object (trong mảng attachments)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của tài liệu đính kèm |
| `name` | String | Tên file |
| `type` | String | Loại MIME của file |
| `size` | Integer | Kích thước file (bytes) |
| `url` | String | Đường dẫn để tải file |

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "note": {
      "id": 35,
      "content": "Đã họp với khách hàng vào ngày 16/05/2025. Khách hàng quan tâm đến giải pháp của chúng ta và muốn xem demo trong tuần sau.",
      "activityType": "meeting",
      "meetingDate": "2025-05-16T14:30:00Z",
      "opportunity": {
        "id": 134,
        "code": "OPP-2025050134",
        "name": "Hệ thống CRM cho công ty ABC"
      },
      "attachments": [],
      "createdBy": {
        "id": 8,
        "name": "Lê Thị Leader"
      },
      "createdAt": "2025-05-16T16:45:20Z"
    },
    "statusUpdated": true,
    "previousStatus": "qualified",
    "newStatus": "proposal",
    "lastInteractionDate": "2025-05-16T16:45:20Z"
  }
}
```

### 4.2 Success - 201 Created (Với file đính kèm)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `data` | Object | Đối tượng chứa thông tin chi tiết về ghi chú có đính kèm file |

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "note": {
      "id": 36,
      "content": "Đã gửi đề xuất chi tiết cho khách hàng",
      "activityType": "document_sent",
      "meetingDate": null,
      "opportunity": {
        "id": 134,
        "code": "OPP-2025050134",
        "name": "Hệ thống CRM cho công ty ABC"
      },
      "attachments": [
        {
          "id": 12,
          "name": "proposal_abc_v1.pdf",
          "type": "application/pdf",
          "size": 2400000,
          "url": "/api/v1/files/12"
        },
        {
          "id": 13,
          "name": "timeline.xlsx",
          "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "size": 1500000,
          "url": "/api/v1/files/13"
        }
      ],
      "createdBy": {
        "id": 8,
        "name": "Lê Thị Leader"
      },
      "createdAt": "2025-05-16T17:30:45Z"
    },
    "statusUpdated": false,
    "lastInteractionDate": "2025-05-16T17:30:45Z"
  }
}
```

### 4.3 Error Responses

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
      "field": "content",
      "message": "Nội dung ghi chú không được để trống"
    },
    {
      "field": "newStatus",
      "message": "Trạng thái 'ongoing' không hợp lệ. Các giá trị hợp lệ: new, contacted, qualified, proposal, negotiation, won, lost, closed"
    }
  ]
}
```

#### 400 Bad Request - Lỗi file

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3003 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

```json
{
  "status": "error",
  "code": "E3003",
  "message": "Lỗi file đính kèm",
  "errors": [
    {
      "field": "files",
      "message": "File 'malware.exe' có định dạng không được hỗ trợ"
    },
    {
      "field": "files",
      "message": "Vượt quá số lượng file tối đa cho phép (tối đa: 5)"
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
  "message": "Bạn không có quyền thực hiện hành động này trên cơ hội này"
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

```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy dữ liệu",
  "errors": [
    {
      "field": "oppId",
      "message": "Không tìm thấy cơ hội với ID: 999"
    }
  ]
}
``` 