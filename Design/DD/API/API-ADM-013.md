# API Details: Xem log hệ thống

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-02 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp khả năng xem và lọc log hoạt động và lỗi của hệ thống, giúp quản trị viên theo dõi, kiểm tra và gỡ lỗi một cách hiệu quả, hỗ trợ quá trình vận hành và bảo trì hệ thống.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-013                                  |
| **Tên API**        | Xem log hệ thống                             |
| **Mô tả**          | API cung cấp log hoạt động và lỗi của hệ thống cho mục đích theo dõi và gỡ lỗi |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/admin/system-logs`                  |
| **Quyền truy cập** | system-log:read:all, system-log:read:limited |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên               | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|-------------------|----------------------|----------|-------|
| `level`           | String               | Không    | Lọc theo mức log: `INFO`, `WARNING`, `ERROR`, `DEBUG` |
| `component`       | String               | Không    | Lọc theo thành phần hệ thống (Auth, HRM, OPP, CTR, ...) |
| `startDate`       | String (ISO Date)    | Không    | Lọc từ ngày (YYYY-MM-DD) |
| `endDate`         | String (ISO Date)    | Không    | Lọc đến ngày (YYYY-MM-DD) |
| `userId`          | Integer              | Không    | Lọc theo ID người dùng thực hiện |
| `keyword`         | String               | Không    | Tìm kiếm theo nội dung |
| `page`            | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`            | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `50`) |
| `sortBy`          | String               | Không    | Trường sắp xếp (mặc định: `timestamp`) |
| `sortDir`         | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |

### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 100          |
| `sortDir`         | `asc`, `desc`    |
| `level`           | Một trong: `INFO`, `WARNING`, `ERROR`, `DEBUG` |
| `startDate`       | Định dạng YYYY-MM-DD, phải <= endDate (nếu có) |
| `endDate`         | Định dạng YYYY-MM-DD, phải >= startDate (nếu có) |

### 3.4 Phân quyền đặc biệt
- Admin: Có quyền `system-log:read:all` - xem tất cả log hệ thống không giới hạn
- Division Manager: Có quyền `system-log:read:limited` - xem log hệ thống giới hạn (không bao gồm các log nhạy cảm và chỉ xem được log liên quan đến bộ phận mình)
- API sẽ tự động lọc dữ liệu dựa trên quyền của người dùng trong JWT token

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu log và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Mảng các đối tượng thông tin log |
| `components` | Array of String | Danh sách các thành phần hệ thống có log |
| `levels` | Array of String | Danh sách các mức độ log trong hệ thống |
| `pageable` | Object | Thông tin phân trang |

#### Log Entry Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi log |
| `timestamp` | DateTime | Thời điểm ghi log (ISO 8601 với millisecond) |
| `level` | String | Mức độ log: INFO, WARNING, ERROR, DEBUG |
| `component` | String | Thành phần hệ thống phát sinh log |
| `message` | String | Nội dung chính của log |
| `details` | String | Thông tin chi tiết (stack trace với lỗi) |
| `user` | Object/null | Thông tin người dùng thực hiện hành động (nếu có) |
| `ipAddress` | String | Địa chỉ IP của request |
| `requestId` | String | ID định danh của request liên quan |

#### User Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `username` | String | Tên đăng nhập của người dùng |

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
        "id": 12345,
        "timestamp": "2025-05-02T14:30:15.123Z",
        "level": "ERROR",
        "component": "OPPORTUNITY_SYNC",
        "message": "Không thể đồng bộ cơ hội từ Hubspot: API Key không hợp lệ",
        "details": "java.io.IOException: 401 Unauthorized - API Key không hợp lệ hoặc đã hết hạn",
        "user": {
          "id": 1,
          "username": "admin"
        },
        "ipAddress": "192.168.1.10",
        "requestId": "req-98765-abcde"
      },
      {
        "id": 12344,
        "timestamp": "2025-05-02T14:15:20.456Z",
        "level": "INFO",
        "component": "AUTH",
        "message": "Đăng nhập thành công",
        "details": "Đăng nhập thành công từ IP 192.168.1.25",
        "user": {
          "id": 2,
          "username": "leader1"
        },
        "ipAddress": "192.168.1.25",
        "requestId": "req-98764-fghij"
      },
      {
        "id": 12343,
        "timestamp": "2025-05-02T14:10:05.789Z",
        "level": "WARNING",
        "component": "CONFIG",
        "message": "Cấu hình cập nhật: margin.threshold.red",
        "details": "Giá trị cập nhật từ 25 thành 20 bởi admin",
        "user": {
          "id": 1,
          "username": "admin"
        },
        "ipAddress": "192.168.1.10",
        "requestId": "req-98763-klmno"
      }
    ],
    "components": [
      "AUTH",
      "CONFIG",
      "HRM",
      "OPPORTUNITY",
      "OPPORTUNITY_SYNC",
      "CONTRACT",
      "MARGIN",
      "SCHEDULER"
    ],
    "levels": [
      "INFO",
      "WARNING",
      "ERROR",
      "DEBUG"
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 247,
      "totalElements": 12345,
      "sort": "timestamp,desc"
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
      "field": "startDate",
      "message": "Ngày bắt đầu không được sau ngày kết thúc"
    },
    {
      "field": "level",
      "message": "Giá trị 'FATAL' không hợp lệ. Các giá trị hợp lệ: INFO, WARNING, ERROR, DEBUG"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi truy vấn log"
}
``` 