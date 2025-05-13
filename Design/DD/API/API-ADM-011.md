# API Details: Lấy danh sách cấu hình hệ thống

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-02 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp danh sách các cấu hình và tham số hệ thống, cho phép quản trị viên xem các giá trị cấu hình hiện tại, phục vụ cho việc quản lý và điều chỉnh hoạt động của hệ thống.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-011                                  |
| **Tên API**        | Lấy danh sách cấu hình hệ thống              |
| **Mô tả**          | API cung cấp danh sách các cấu hình và tham số hệ thống |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/admin/configs`                      |
| **Quyền truy cập** | config:read                                  |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên                | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|--------------------|----------------------|----------|-------|
| `category`         | String               | Không    | Lọc theo danh mục cấu hình |
| `keyword`          | String               | Không    | Tìm kiếm theo tên cấu hình |
| `page`             | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`             | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `50`) |
| `sortBy`           | String               | Không    | Trường sắp xếp (mặc định: `category`) |
| `sortDir`          | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `asc`) |

### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 100          |
| `sortDir`         | `asc`, `desc`    |
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu cấu hình và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Mảng các đối tượng thông tin cấu hình |
| `categories` | Array of String | Danh sách tất cả các danh mục cấu hình có trong hệ thống |
| `pageable` | Object | Thông tin phân trang |

#### Configuration Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `key` | String | Khóa định danh cấu hình (unique) |
| `value` | String | Giá trị hiện tại của cấu hình |
| `type` | String | Kiểu dữ liệu: STRING, INTEGER, BOOLEAN, SECRET, ... |
| `category` | String | Danh mục cấu hình |
| `description` | String | Mô tả chi tiết về cấu hình |
| `isEditable` | Boolean | Cho biết cấu hình có thể chỉnh sửa hay không |
| `updatedAt` | DateTime | Thời gian cập nhật gần nhất (ISO 8601) |

#### Pageable Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `pageNumber` | Integer | Số trang hiện tại |
| `pageSize` | Integer | Kích thước trang (số bản ghi mỗi trang) |
| `totalPages` | Integer | Tổng số trang |
| `totalElements` | Integer | Tổng số bản ghi |
| `sort` | String | Thông tin sắp xếp (trường,hướng) |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "content": [
      {
        "key": "system.app.name",
        "value": "Internal Management System",
        "type": "STRING",
        "category": "SYSTEM",
        "description": "Tên hệ thống",
        "isEditable": false,
        "updatedAt": "2025-01-01T00:00:00Z"
      },
      {
        "key": "system.maintenance.mode",
        "value": "false",
        "type": "BOOLEAN",
        "category": "SYSTEM",
        "description": "Chế độ bảo trì",
        "isEditable": true,
        "updatedAt": "2025-04-01T10:15:30Z"
      },
      {
        "key": "margin.threshold.red",
        "value": "25",
        "type": "INTEGER",
        "category": "MARGIN",
        "description": "Ngưỡng margin cảnh báo đỏ (<=)",
        "isEditable": true,
        "updatedAt": "2025-02-15T09:30:00Z"
      },
      {
        "key": "margin.threshold.yellow",
        "value": "35",
        "type": "INTEGER",
        "category": "MARGIN",
        "description": "Ngưỡng margin cảnh báo vàng (<=)",
        "isEditable": true,
        "updatedAt": "2025-02-15T09:30:00Z"
      },
      {
        "key": "opportunity.followup.red",
        "value": "21",
        "type": "INTEGER",
        "category": "OPPORTUNITY",
        "description": "Ngưỡng số ngày cảnh báo đỏ cho cơ hội không follow-up (>)",
        "isEditable": true,
        "updatedAt": "2025-03-10T14:20:00Z"
      },
      {
        "key": "opportunity.followup.yellow",
        "value": "7",
        "type": "INTEGER",
        "category": "OPPORTUNITY",
        "description": "Ngưỡng số ngày cảnh báo vàng cho cơ hội không follow-up (>)",
        "isEditable": true,
        "updatedAt": "2025-03-10T14:20:00Z"
      },
      {
        "key": "hubspot.api.key",
        "value": "********",
        "type": "SECRET",
        "category": "INTEGRATION",
        "description": "API Key Hubspot",
        "isEditable": true,
        "updatedAt": "2025-01-10T09:00:00Z"
      },
      {
        "key": "hubspot.sync.schedule",
        "value": "0 */3 * * *",
        "type": "STRING",
        "category": "INTEGRATION",
        "description": "Lịch đồng bộ Hubspot (Cron expression)",
        "isEditable": true,
        "updatedAt": "2025-01-10T09:00:00Z"
      }
    ],
    "categories": [
      "SYSTEM",
      "MARGIN",
      "OPPORTUNITY",
      "INTEGRATION",
      "SECURITY"
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 1,
      "totalElements": 15,
      "sort": "category,asc"
    }
  }
}
```

### 4.2 Error Responses

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

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "size",
      "message": "Kích thước trang phải từ 1 đến 100"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi truy vấn danh sách cấu hình"
}
``` 