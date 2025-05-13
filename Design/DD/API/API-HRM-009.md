# API Details: Lấy danh sách loại kỹ năng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-2 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2025-05-10 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để lấy danh sách các loại kỹ năng (skill categories) trong hệ thống với các tùy chọn lọc và tìm kiếm.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-009                                  |
| **Tên API**        | Lấy danh sách loại kỹ năng                   |
| **Mô tả**          | API lấy danh sách các loại kỹ năng (skill categories) |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/skill-categories`                   |
| **Quyền truy cập** | skill:read                                   |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `keyword`  | String       | Không    | Tìm kiếm theo tên loại kỹ năng |
| `active`   | Boolean      | Không    | Lọc theo trạng thái: `true` - chỉ lấy loại đang active, `false` - chỉ lấy loại không active, bỏ trống - lấy tất cả (mặc định: `true`) |

### 3.3 Validate Rule

| Trường      | Điều kiện hợp lệ |
|-------------|------------------|
| `keyword`   | Độ dài tối đa: 100 ký tự |

### 3.4 Phân quyền đặc biệt
- Người dùng có quyền `skill:read`: Xem được danh sách loại kỹ năng
- Các vai trò Division Manager, 部長 (Leader) và Nhân viên đều có quyền xem danh sách loại kỹ năng

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu loại kỹ năng và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Mảng các đối tượng loại kỹ năng |
| `pageable` | Object | Thông tin phân trang |

#### Skill Category Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng |
| `name` | String | Tên loại kỹ năng |
| `description` | String | Mô tả về loại kỹ năng |
| `active` | Boolean | Trạng thái kích hoạt của loại kỹ năng |

#### Pageable Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `pageNumber` | Integer | Số trang hiện tại |
| `pageSize` | Integer | Kích thước trang (số bản ghi mỗi trang) |
| `totalPages` | Integer | Tổng số trang |
| `totalElements` | Integer | Tổng số bản ghi |
| `sort` | String | Thông tin sắp xếp (trường,hướng) |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "content": [
      {
        "id": 1,
        "name": "Programming Language",
        "description": "Ngôn ngữ lập trình",
        "active": true        
      },
      {
        "id": 2,
        "name": "Framework",
        "description": "Framework phát triển",
        "active": true
      },
      {
        "id": 3,
        "name": "Database",
        "description": "Hệ quản trị cơ sở dữ liệu",
        "active": true
      },
      {
        "id": 4,
        "name": "Language",
        "description": "Ngoại ngữ",
        "active": true
      },
      {
        "id": 5,
        "name": "Tool",
        "description": "Công cụ phát triển",
        "active": true,     
      },
      {
        "id": 6,
        "name": "Certificate",
        "description": "Chứng chỉ",
        "active": true
        },
      {
        "id": 7,
        "name": "Cloud",
        "description": "Công nghệ Cloud",
        "active": true,     
      },
      {
        "id": 8,
        "name": "Other",
        "description": "Kỹ năng khác",
        "active": true,
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 10,
      "totalPages": 5,
      "totalElements": 45,
      "sort": "name,asc"
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
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "keyword",
      "message": "Độ dài từ khóa tìm kiếm không được vượt quá 100 ký tự"
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
  "message": "Bạn không có quyền truy cập chức năng này"
}
``` 