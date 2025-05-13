# API Details: Thêm/Cập nhật kỹ năng cho nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2023-07-18 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép thêm mới hoặc cập nhật một kỹ năng cho nhân viên trong hệ thống quản lý nhân sự.

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-018                                      |
| **Tên API**        | Thêm/Cập nhật kỹ năng cho nhân viên          |
| **Mô tả**          | API cho phép thêm mới hoặc cập nhật một kỹ năng cho nhân viên |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/employees/{employeeId}/skills`      |
| **Quyền truy cập** | `employee:skill:add` (bản thân), `team:skill:manage` (team mình), `skill:manage` (tất cả) |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên          | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------|--------------|----------|-------|
| `employeeId` | Integer      | Có       | ID của nhân viên cần thêm/cập nhật kỹ năng |

### 3.3 Request Body

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `employeeSkillId` | Integer   | Không    | ID kỹ năng nhân viên (nếu là cập nhật), bỏ trống nếu thêm mới |
| `skillId`      | Integer      | Có       | ID của kỹ năng cần thêm/cập nhật |
| `level`        | String       | Có       | Cấp độ kỹ năng |
| `years`        | Number       | Có       | Số năm kinh nghiệm |
| `description`  | String       | Không    | Mô tả chi tiết về kỹ năng/kinh nghiệm của nhân viên |
| `isVerified`   | Boolean      | Không    | (Yêu cầu quyền `team:skill:manage` hoặc `skill:manage`) Đánh dấu đã xác minh kỹ năng này |

### 3.4 Validate Rule

| Trường           | Điều kiện hợp lệ |
|------------------|------------------|
| `employeeId`     | Phải là số nguyên dương và tồn tại trong hệ thống |
| `employeeSkillId`| Nếu có, phải là số nguyên dương và tồn tại trong hệ thống |
| `skillId`        | Phải là số nguyên dương và tồn tại trong hệ thống |
| `level`          | Phải nằm trong danh sách cấp độ của kỹ năng, hoặc một trong các giá trị mặc định: `Basic`, `Intermediate`, `Advanced`, `Expert` |
| `years`          | Phải là số dương, tối đa 50 |
| `description`    | Độ dài tối đa: 1000 ký tự |
| `isVerified`     | Chỉ người dùng có quyền `team:skill:manage` hoặc `skill:manage` được phép đặt giá trị này |

### 3.5 Phân quyền đặc biệt

- `employee:skill:add`: Chỉ thêm/cập nhật kỹ năng cho chính mình, không được chỉnh sửa trường `isVerified`
- `team:skill:manage`: Thêm/cập nhật kỹ năng cho nhân viên trong team của mình, được chỉnh sửa trường `isVerified`
- `skill:manage`: Thêm/cập nhật kỹ năng cho tất cả nhân viên, được chỉnh sửa tất cả trường

---

## 4. Response

### 4.1 Success - 200 OK (Cập nhật) hoặc 201 Created (Thêm mới)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 hoặc 201 |
| `message` | String | Thông báo kết quả thực hiện |
| `data` | Object | Đối tượng chứa thông tin kỹ năng của nhân viên đã thêm/cập nhật |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `employeeSkillId` | Integer | ID của bản ghi kỹ năng nhân viên |
| `skill` | Object | Thông tin kỹ năng |
| `level` | String | Trình độ kỹ năng |
| `years` | Integer | Số năm kinh nghiệm với kỹ năng |
| `description` | String | Mô tả chi tiết về kinh nghiệm với kỹ năng |
| `isVerified` | Boolean | Trạng thái xác nhận kỹ năng |
| `verifiedBy` | Object | Thông tin người xác nhận kỹ năng (null nếu chưa được xác nhận) |
| `createdAt` | String | Thời điểm tạo bản ghi kỹ năng (ISO 8601) |
| `updatedAt` | String | Thời điểm cập nhật gần nhất (ISO 8601) |

#### Skill Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `category` | Object | Thông tin về loại kỹ năng |

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

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "success",
  "code": 200,
  "message": "Cập nhật kỹ năng cho nhân viên thành công",
  "data": {
    "employeeId": 12,
    "employeeCode": "NV012",
    "name": "Hoàng Văn F",
    "employeeSkillId": 101,
    "skill": {
      "id": 1,
      "name": "Java",
      "category": {
        "id": 1,
        "name": "Programming Language"
      }
    },
    "level": "Advanced",
    "years": 5,
    "description": "Có kinh nghiệm phát triển ứng dụng enterprise với Java, Spring Boot, và microservices",
    "isVerified": true,
    "verifiedBy": {
      "id": 2,
      "name": "Nguyễn Văn Leader"
    },
    "createdAt": "2025-03-15T10:30:00Z",
    "updatedAt": "2025-05-02T16:45:00Z"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E2001 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `field` | String | Tên trường dữ liệu gây lỗi |
| `message` | String | Thông báo chi tiết về lỗi |

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "code": "E2001",
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "level",
      "message": "Cấp độ 'SuperExpert' không hợp lệ. Các cấp độ hợp lệ cho kỹ năng 'Java' là: Basic, Intermediate, Advanced, Expert"
    },
    {
      "field": "years",
      "message": "Số năm kinh nghiệm phải là số dương không quá 50"
    }
  ]
}
```

#### 400 Bad Request (Duplicate)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E4000 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "code": "E4000",
  "message": "Dữ liệu đã tồn tại",
  "errors": [
    {
      "field": "skillId",
      "message": "Nhân viên đã có kỹ năng 'Java' trong hồ sơ"
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

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

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
| `code` | String | Mã lỗi: E1002 hoặc E1003 |
| `message` | String | Thông báo lỗi |
| `errors` | Array | Mảng chứa chi tiết các lỗi (tùy trường hợp) |

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "status": "error",
  "code": "E1002",
  "message": "Không có quyền cập nhật kỹ năng cho nhân viên này"
}
```

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "status": "error",
  "code": "E1003",
  "message": "Không có quyền xác minh kỹ năng",
  "errors": [
    {
      "field": "isVerified",
      "message": "Chỉ người dùng có quyền team:skill:manage hoặc skill:manage mới có quyền xác minh kỹ năng"
    }
  ]
}
```

#### 404 Not Found

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3000, E3001, hoặc E3002 |
| `message` | String | Thông báo lỗi |

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy nhân viên với ID: 999"
}
```

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "status": "error",
  "code": "E3001",
  "message": "Không tìm thấy kỹ năng với ID: 999"
}
```

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "status": "error",
  "code": "E3002",
  "message": "Không tìm thấy bản ghi kỹ năng nhân viên với ID: 999"
}
```

#### 500 Internal Server Error

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E5000 |
| `message` | String | Thông báo lỗi |

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống, vui lòng thử lại sau hoặc liên hệ quản trị viên"
}
``` 