# API Details: Đánh dấu/bỏ đánh dấu ưu tiên Onsite

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-31 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để Sales, Leader hoặc quản lý có thể đánh dấu hoặc bỏ đánh dấu một cơ hội kinh doanh có ưu tiên Onsite, nhằm ưu tiên sắp xếp nhân sự cho các dự án yêu cầu kỹ sư làm việc tại chỗ.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-OPP-008                                  |
| **Tên API**        | Đánh dấu/bỏ đánh dấu ưu tiên Onsite          |
| **Mô tả**          | API cho phép đánh dấu hoặc bỏ đánh dấu một cơ hội kinh doanh có ưu tiên Onsite |
| **Module**         | Quản lý Cơ hội Kinh doanh                    |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/opportunities/{oppId}/onsite`       |
| **Quyền truy cập** | opportunity-onsite:update:all, opportunity-onsite:update:assigned |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên         | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-------------|--------------|----------|-------|
| `oppId`     | Integer      | Có       | ID của cơ hội kinh doanh cần đánh dấu/bỏ đánh dấu ưu tiên Onsite |

### 3.3 Request Body

```json
{
  "priority": true,
  "note": "Khách hàng yêu cầu kỹ sư onsite ít nhất 3 ngày/tuần"
}
```

### 3.4 Body Parameters

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `priority` | Boolean      | Có       | `true` để đánh dấu ưu tiên Onsite, `false` để bỏ đánh dấu |
| `note`     | String       | Không    | Ghi chú về lý do đánh dấu/bỏ đánh dấu ưu tiên Onsite |

### 3.5 Validate Rule

| Trường     | Điều kiện hợp lệ |
|------------|------------------|
| `oppId`    | Số nguyên dương, phải tồn tại trong hệ thống |
| `priority` | Boolean: `true` hoặc `false` |
| `note`     | Tối đa 500 ký tự |

### 3.6 Phân quyền đặc biệt
- Leader: Chỉ đánh dấu/bỏ đánh dấu được cho các cơ hội được gán cho mình
- Sales: Đánh dấu/bỏ đánh dấu được cho các cơ hội do mình tạo hoặc phụ trách
- Division Manager: Đánh dấu/bỏ đánh dấu được cho tất cả cơ hội thuộc bộ phận mình quản lý
- Admin: Đánh dấu/bỏ đánh dấu được cho tất cả cơ hội

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin sau khi đánh dấu/bỏ đánh dấu ưu tiên Onsite |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `opportunity` | Object | Thông tin cơ hội sau khi cập nhật trạng thái ưu tiên |
| `activityLogged` | Boolean | Đã ghi nhật ký hoạt động hay chưa |

#### Opportunity Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội kinh doanh |
| `code` | String | Mã cơ hội (tự động sinh) |
| `name` | String | Tên cơ hội kinh doanh |
| `priority` | Boolean | Trạng thái ưu tiên mới (true/false) |
| `previousPriority` | Boolean | Trạng thái ưu tiên trước khi thay đổi |
| `updatedAt` | String | Thời điểm cập nhật (ISO 8601) |
| `updatedBy` | Object | Thông tin người thực hiện cập nhật |

#### User Object (trong updatedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `name` | String | Tên đầy đủ của người dùng |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "opportunity": {
      "id": 134,
      "code": "OPP-2025050134",
      "name": "Hệ thống CRM cho công ty ABC",
      "priority": true,
      "previousPriority": false,
      "updatedAt": "2025-05-17T09:45:12Z",
      "updatedBy": {
        "id": 8,
        "name": "Lê Thị Leader"
      }
    },
    "activityLogged": true
  }
}
```

### 4.2 Success - 200 OK (Bỏ đánh dấu)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin sau khi bỏ đánh dấu ưu tiên Onsite |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "opportunity": {
      "id": 134,
      "code": "OPP-2025050134",
      "name": "Hệ thống CRM cho công ty ABC",
      "priority": false,
      "previousPriority": true,
      "updatedAt": "2025-05-17T10:30:45Z",
      "updatedBy": {
        "id": 8,
        "name": "Lê Thị Leader"
      }
    },
    "activityLogged": true
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
      "field": "priority",
      "message": "Trường priority là bắt buộc"
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

#### 409 Conflict

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E4004 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

```json
{
  "status": "error",
  "code": "E4004",
  "message": "Xung đột dữ liệu",
  "errors": [
    {
      "field": "status",
      "message": "Không thể thay đổi trạng thái ưu tiên Onsite cho cơ hội đã kết thúc (won/lost/closed)"
    }
  ]
} 