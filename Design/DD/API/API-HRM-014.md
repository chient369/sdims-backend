# API Details: Thêm kỹ năng mới

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-03 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2025-05-10 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên thêm mới một kỹ năng (skill) vào hệ thống, giúp mở rộng danh sách kỹ năng có thể gán cho nhân viên, phục vụ cho việc quản lý và tìm kiếm nhân viên theo yêu cầu kỹ năng của dự án.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-014                                  |
| **Tên API**        | Thêm kỹ năng mới                             |
| **Mô tả**          | API cho phép thêm một kỹ năng mới vào hệ thống |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/admin/skills`                       |
| **Quyền truy cập** | skill:create                                 |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `name`         | String       | Có       | Tên kỹ năng |
| `description`  | String       | Không    | Mô tả về kỹ năng |
| `categoryId`   | Integer      | Có       | ID của loại kỹ năng |
| `active`       | Boolean      | Không    | Trạng thái kích hoạt (mặc định: `true`) |
| `levels`       | Array        | Không    | Mảng các cấp độ kỹ năng (nếu có) |

#### Chi tiết Object `levels`

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `name`         | String       | Có       | Tên cấp độ kỹ năng |
| `description`  | String       | Không    | Mô tả về cấp độ |
| `sortOrder`    | Integer      | Không    | Thứ tự sắp xếp |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `name`         | Độ dài: 1-100 ký tự, Không được trùng lặp với các kỹ năng đã có |
| `description`  | Độ dài tối đa: 500 ký tự |
| `categoryId`   | Phải là số nguyên dương và tồn tại trong hệ thống |
| `levels.name`  | Độ dài: 1-50 ký tự |

---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `message` | String | Thông báo kết quả: "Thêm kỹ năng thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về kỹ năng mới |

#### Data Object (Skill)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng mới được tạo |
| `name` | String | Tên kỹ năng |
| `description` | String | Mô tả về kỹ năng |
| `category` | Object | Thông tin về loại kỹ năng |
| `active` | Boolean | Trạng thái kích hoạt |
| `levels` | Array | Mảng các cấp độ kỹ năng |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |
| `createdBy` | String | Người tạo kỹ năng |

#### Category Object (trong Skill)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng |
| `name` | String | Tên loại kỹ năng |

#### Level Object (trong mảng levels)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cấp độ kỹ năng |
| `name` | String | Tên cấp độ kỹ năng |
| `description` | String | Mô tả về cấp độ |
| `sortOrder` | Integer | Thứ tự sắp xếp |

```json
{
  "status": "success",
  "code": 201,
  "message": "Thêm kỹ năng thành công",
  "data": {
    "id": 51,
    "name": "Docker",
    "description": "Công nghệ container Docker",
    "category": {
      "id": 9,
      "name": "DevOps & CI/CD"
    },
    "active": true,
    "levels": [
      {
        "id": 1,
        "name": "Basic",
        "description": "Hiểu biết cơ bản về Docker, có thể sử dụng các lệnh cơ bản",
        "sortOrder": 1
      },
      {
        "id": 2,
        "name": "Intermediate",
        "description": "Có thể tạo Dockerfile, hiểu về docker-compose",
        "sortOrder": 2
      },
      {
        "id": 3,
        "name": "Advanced",
        "description": "Có kinh nghiệm triển khai hệ thống phức tạp với Docker, hiểu về network, volume, security",
        "sortOrder": 3
      }
    ],
    "createdAt": "2025-05-02T14:30:00Z",
    "createdBy": "admin"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "name",
      "message": "Tên kỹ năng không được để trống"
    },
    {
      "field": "categoryId",
      "message": "Loại kỹ năng là bắt buộc"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Dữ liệu đã tồn tại",
  "errors": [
    {
      "field": "name",
      "message": "Kỹ năng 'Docker' đã tồn tại trong hệ thống"
    }
  ]
}
```

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

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy loại kỹ năng với ID: 99"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi thêm kỹ năng mới"
}
``` 