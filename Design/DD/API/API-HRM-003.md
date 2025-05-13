# API Details: Lấy thông tin chi tiết của một nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới               | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để xem thông tin chi tiết của một nhân viên cụ thể.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-003                                  |
| **Tên API**        | Lấy thông tin chi tiết của một nhân viên     |
| **Mô tả**          | API cung cấp thông tin chi tiết về một nhân viên, bao gồm thông tin cá nhân, lịch sử phân công và các kỹ năng |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/employees/{employeeId}`             |
| **Quyền truy cập** | employee:read:all, employee:read:team, employee:read:own |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên          | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------|--------------|----------|-------|
| `employeeId` | Integer      | Có       | ID của nhân viên cần xem chi tiết |

### 3.3 Query Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `include`       | String       | Không    | Các thông tin bổ sung cần lấy về nhân viên, cách nhau bởi dấu phẩy. Hỗ trợ: `skills`, `allocations`, `evaluations` |

### 3.4 Validate Rule

| Trường          | Điều kiện hợp lệ |
|-----------------|------------------|
| `employeeId`    | Phải là số nguyên dương và tồn tại trong hệ thống |
| `include`       | Chỉ chấp nhận các giá trị: `skills`, `allocations`, `evaluations` |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin chi tiết về nhân viên |

#### Data Object (Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `email` | String | Địa chỉ email công ty của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `phone` | String | Số điện thoại của nhân viên |
| `address` | String | Địa chỉ của nhân viên |
| `birthDate` | String | Ngày sinh (định dạng: YYYY-MM-DD) |
| `joinDate` | String | Ngày vào công ty (định dạng: YYYY-MM-DD) |
| `emergencyContact` | Object | Thông tin liên hệ khẩn cấp |
| `status` | String | Trạng thái nhân viên (Allocated, Available, EndingSoon, OnLeave, Resigned) |
| `avatar` | String | URL ảnh đại diện |
| `userId` | Integer | ID người dùng hệ thống |
| `note` | String | Ghi chú về nhân viên |
| `skills` | Array | Mảng các kỹ năng của nhân viên (chỉ có khi include=skills) |
| `allocations` | Array | Mảng thông tin phân bổ dự án (chỉ có khi include=allocations) |
| `evaluations` | Array | Mảng thông tin đánh giá nhân viên (chỉ có khi include=evaluations) |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |
| `updatedAt` | String | Thời gian cập nhật cuối cùng (định dạng ISO 8601) |

#### Team Object (trong employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Emergency Contact Object (trong employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên người liên hệ khẩn cấp |
| `phone` | String | Số điện thoại người liên hệ |
| `relation` | String | Mối quan hệ với nhân viên |

#### Skill Object (trong mảng skills)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `level` | Integer | Cấp độ kỹ năng (1-5, với 5 là cao nhất) |
| `yearsOfExperience` | Integer | Số năm kinh nghiệm với kỹ năng |

#### Allocation Object (trong mảng allocations)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi phân bổ |
| `project` | Object | Thông tin về dự án |
| `startDate` | String | Ngày bắt đầu tham gia dự án (định dạng: YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc dự án (định dạng: YYYY-MM-DD) |
| `allocation` | Integer | Tỷ lệ phân bổ thời gian (%) |
| `position` | String | Vị trí/vai trò trong dự án |
| `status` | String | Trạng thái phân bổ (Active, Completed, Upcoming) |

#### Project Object (trong allocation)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của dự án |
| `name` | String | Tên dự án |

#### Evaluation Object (trong mảng evaluations)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi đánh giá |
| `period` | String | Kỳ đánh giá |
| `performanceScore` | Number | Điểm đánh giá hiệu suất |
| `evaluator` | String | Người thực hiện đánh giá |
| `evaluationDate` | String | Ngày đánh giá (định dạng: YYYY-MM-DD) |
| `summary` | String | Tóm tắt đánh giá |

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "code": 200,
  "data": {
    "id": 12,
    "employeeCode": "NV012",
    "name": "Nguyễn Văn A",
    "email": "a.nguyenvan@company.com",
    "position": "Senior Developer",
    "team": {
      "id": 3,
      "name": "Team Alpha"
    },
    "phone": "0987654321",
    "address": "123 Đường A, Quận B, TP.HCM",
    "birthDate": "1990-05-15",
    "joinDate": "2023-01-01",
    "emergencyContact": {
      "name": "Nguyễn Thị B",
      "phone": "0912345678",
      "relation": "Vợ"
    },
    "status": "Allocated",
    "avatar": "https://example.com/avatars/nguyenvana.jpg",
    "userId": 56,
    "note": "Nhân viên giỏi, có kinh nghiệm với React Native",
    "skills": [
      {
        "id": 1,
        "name": "React",
        "level": 4,
        "yearsOfExperience": 3
      },
      {
        "id": 2,
        "name": "Node.js",
        "level": 3,
        "yearsOfExperience": 2
      },
      {
        "id": 5,
        "name": "React Native",
        "level": 4,
        "yearsOfExperience": 2
      }
    ],
    "allocations": [
      {
        "id": 1,
        "project": {
          "id": 101,
          "name": "Mobile App XYZ"
        },
        "startDate": "2023-03-01",
        "endDate": "2023-08-31",
        "allocation": 100,
        "position": "Mobile Developer",
        "status": "Completed"
      },
      {
        "id": 2,
        "project": {
          "id": 102,
          "name": "Web App ABC"
        },
        "startDate": "2023-09-01",
        "endDate": "2024-03-31",
        "allocation": 100,
        "position": "Frontend Lead",
        "status": "Active"
      }
    ],
    "evaluations": [
      {
        "id": 1,
        "period": "2023 Q1",
        "performanceScore": 4.5,
        "evaluator": "Trần Văn B",
        "evaluationDate": "2023-04-05",
        "summary": "Hoàn thành xuất sắc công việc"
      },
      {
        "id": 2,
        "period": "2023 Q2",
        "performanceScore": 4.7,
        "evaluator": "Trần Văn B",
        "evaluationDate": "2023-07-05",
        "summary": "Đạt hiệu suất cao, chủ động trong công việc"
      }
    ],
    "createdAt": "2023-01-01T08:00:00Z",
    "updatedAt": "2024-01-10T14:30:00Z"
  }
}
```

### 4.2 Error Responses

#### 401 Unauthorized
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
```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "status": "error",
  "code": "E1002",
  "message": "Không có quyền truy cập chức năng này"
}
```

#### 404 Not Found
```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "status": "error",
  "code": "E3001",
  "message": "Không tìm thấy nhân viên với ID: 999"
}
```

#### 400 Bad Request
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "code": "E2000",
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "include",
      "message": "Giá trị 'history' không được hỗ trợ. Các giá trị hợp lệ: skills, allocations, evaluations"
    }
  ]
}
```

#### 500 Internal Server Error
```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống, vui lòng thử lại sau hoặc liên hệ quản trị viên"
}
``` 