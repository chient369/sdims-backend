# API Details: Lấy danh sách kỹ năng của nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-03 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp danh sách các kỹ năng (skills) đã được khai báo cho một nhân viên cụ thể, giúp người dùng xem và đánh giá các kỹ năng chuyên môn của nhân viên để phục vụ cho việc phân công công việc, tìm kiếm nhân sự phù hợp cho dự án, và phát triển nghề nghiệp của nhân viên.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-017                                  |
| **Tên API**        | Lấy danh sách kỹ năng của nhân viên          |
| **Mô tả**          | API lấy danh sách các kỹ năng đã được khai báo của một nhân viên |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/employees/{employeeId}/skills`      |
| **Quyền truy cập** | employee-skill:read:all, employee-skill:read:team, employee-skill:read:own |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên          | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------|--------------|----------|-------|
| `employeeId` | Integer      | Có       | ID của nhân viên cần lấy danh sách kỹ năng |

### 3.3 Query Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `categoryId`   | Integer      | Không    | Lọc theo ID loại kỹ năng |
| `keyword`      | String       | Không    | Tìm kiếm theo tên kỹ năng |
| `sortBy`       | String       | Không    | Trường sắp xếp (mặc định: `level`) |
| `sortDir`      | String       | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |

### 3.4 Validate Rule

| Trường        | Điều kiện hợp lệ |
|---------------|------------------|
| `employeeId`  | Phải là số nguyên dương và tồn tại trong hệ thống |
| `categoryId`  | Phải là số nguyên dương |
| `keyword`     | Độ dài tối đa: 100 ký tự |
| `sortBy`      | Một trong: `skill`, `level`, `years`, `lastUpdated` |
| `sortDir`     | Một trong: `asc`, `desc` |

### 3.5 Phân quyền đặc biệt
- Người dùng chỉ có quyền `employee.skill:read` trên tài khoản của chính mình
- Người dùng có quyền `team.skill:read` có thể xem kỹ năng của nhân viên trong team mình quản lý
- Người dùng có quyền `department.skill:read` có thể xem kỹ năng của tất cả nhân viên thuộc bộ phận mình quản lý
- Người dùng có quyền `system.skill:read` có thể xem kỹ năng của tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin nhân viên và danh sách kỹ năng |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `skills` | Array | Mảng các đối tượng kỹ năng của nhân viên |

#### Skill Object (trong mảng skills)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `category` | Object | Thông tin về loại kỹ năng |
| `level` | String | Trình độ (Beginner, Intermediate, Advanced, Expert) |
| `years` | Integer | Số năm kinh nghiệm với kỹ năng |
| `description` | String | Mô tả chi tiết về kinh nghiệm với kỹ năng |
| `isVerified` | Boolean | Trạng thái xác nhận kỹ năng |
| `verifiedBy` | Object | Thông tin người xác nhận kỹ năng (null nếu chưa được xác nhận) |
| `lastUpdated` | String | Thời điểm cập nhật kỹ năng gần nhất (ISO 8601) |

#### Category Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng |
| `name` | String | Tên loại kỹ năng |

#### VerifiedBy Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người xác nhận kỹ năng |
| `name` | String | Tên người xác nhận kỹ năng |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "employeeId": 12,
    "employeeCode": "NV012",
    "name": "Hoàng Văn F",
    "position": "Developer",
    "skills": [
      {
        "id": 1,
        "name": "Java",
        "category": {
          "id": 1,
          "name": "Programming Language"
        },
        "level": "Advanced",
        "years": 5,
        "description": "Có kinh nghiệm phát triển ứng dụng enterprise với Java",
        "isVerified": true,
        "verifiedBy": {
          "id": 2,
          "name": "Nguyễn Văn Leader"
        },
        "lastUpdated": "2025-03-15T10:30:00Z"
      },
      {
        "id": 2,
        "name": "Spring Boot",
        "category": {
          "id": 2,
          "name": "Framework"
        },
        "level": "Advanced",
        "years": 4,
        "description": "Có kinh nghiệm phát triển RESTful API và microservices với Spring Boot",
        "isVerified": true,
        "verifiedBy": {
          "id": 2,
          "name": "Nguyễn Văn Leader"
        },
        "lastUpdated": "2025-03-15T10:30:00Z"
      },
      {
        "id": 4,
        "name": "MySQL",
        "category": {
          "id": 3,
          "name": "Database"
        },
        "level": "Intermediate",
        "years": 3,
        "description": "Có kinh nghiệm thiết kế database và viết các truy vấn phức tạp",
        "isVerified": false,
        "verifiedBy": null,
        "lastUpdated": "2025-04-10T14:45:00Z"
      }
    ]
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
      "field": "employeeId",
      "message": "ID nhân viên phải là số nguyên dương"
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
  "message": "Không có quyền truy cập thông tin kỹ năng của nhân viên này"
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
  "message": "Không tìm thấy nhân viên với ID: 999"
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
  "message": "Lỗi hệ thống khi lấy danh sách kỹ năng của nhân viên"
}
``` 