# API Details: Cập nhật thông tin nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp khả năng cập nhật thông tin của nhân viên trong hệ thống, với cơ chế phân quyền chi tiết đảm bảo người dùng chỉ có thể cập nhật các thông tin họ được phép.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-004                                  |
| **Tên API**        | Cập nhật thông tin nhân viên                 |
| **Mô tả**          | API cho phép cập nhật thông tin của một nhân viên theo ID |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/employees/{employeeId}`             |
| **Quyền truy cập** | employee:update:all, employee:update:team, employee:update:own |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên           | Kiểu dữ liệu | Bắt buộc | Mô tả |
|---------------|--------------|----------|-------|
| `employeeId`  | Integer      | Có       | ID của nhân viên cần cập nhật |

### 3.3 Request Body

| Tên                | Kiểu dữ liệu | Bắt buộc | Mô tả | Quyền cần thiết |
|--------------------|--------------|----------|-------|-----------------|
| `name`             | String       | Không    | Họ tên nhân viên | employee:update:all |
| `email`            | String       | Không    | Email công ty | employee:update:all |
| `phone`            | String       | Không    | Số điện thoại | employee:update:self, employee:update:team, employee:update:all |
| `address`          | String       | Không    | Địa chỉ | employee:update:self, employee:update:team, employee:update:all |
| `birthDate`        | String       | Không    | Ngày sinh (định dạng: YYYY-MM-DD) | employee:update:all |
| `joinDate`         | String       | Không    | Ngày vào công ty (định dạng: YYYY-MM-DD) | employee:update:all |
| `position`         | String       | Không    | Vị trí công việc | employee:update:team, employee:update:all |
| `teamId`           | Integer      | Không    | ID của team | employee:update:all |
| `status`           | String       | Không    | Trạng thái nhân viên | employee:update:team, employee:update:all |
| `currentProject`   | String       | Không    | Dự án hiện tại | employee:update:team, employee:update:all |
| `utilization`      | Integer      | Không    | Tỷ lệ sử dụng (0-100) | employee:update:team, employee:update:all |
| `endDate`          | String       | Không    | Ngày kết thúc dự hiện tại (định dạng: YYYY-MM-DD) | employee:update:team, employee:update:all |
| `emergencyContact` | Object       | Không    | Thông tin liên hệ khẩn cấp | employee:update:self, employee:update:team, employee:update:all |
| `note`             | String       | Không    | Ghi chú về nhân viên | employee:update:team, employee:update:all |

#### Chi tiết Object `emergencyContact`

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `name`     | String       | Có       | Tên người liên hệ khẩn cấp |
| `phone`    | String       | Có       | Số điện thoại người liên hệ |
| `relation` | String       | Không    | Mối quan hệ với nhân viên |

### 3.4 Validate Rule

| Trường          | Điều kiện hợp lệ |
|-----------------|------------------|
| `employeeId`    | Phải là số nguyên dương |
| `email`         | Định dạng email hợp lệ, độ dài 5-100 ký tự |
| `phone`         | Định dạng số điện thoại hợp lệ |
| `birthDate`     | Định dạng ngày tháng hợp lệ (YYYY-MM-DD), nhân viên phải trên 18 tuổi |
| `joinDate`      | Định dạng ngày tháng hợp lệ (YYYY-MM-DD), không được sau ngày hiện tại |
| `status`        | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `utilization`   | Số nguyên từ 0 đến 100 |

### 3.5 Phân quyền đặc biệt
- employee:update:self - Chỉ cập nhật được một số thông tin cá nhân của bản thân (phone, address, emergencyContact)
- employee:update:team - Cập nhật được thông tin cá nhân của mình và một số thông tin chuyên môn của thành viên trong team (position, status, currentProject, utilization, endDate, note)
- employee:update:department - Cập nhật được hầu hết thông tin của nhân viên thuộc bộ phận mình quản lý
- employee:update:all - Cập nhật được tất cả thông tin của tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Cập nhật thông tin nhân viên thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về nhân viên sau khi đã cập nhật |

#### Data Object (Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `email` | String | Địa chỉ email công ty của nhân viên |
| `phone` | String | Số điện thoại của nhân viên |
| `address` | String | Địa chỉ của nhân viên |
| `birthDate` | String | Ngày sinh (định dạng: YYYY-MM-DD) |
| `joinDate` | String | Ngày vào công ty (định dạng: YYYY-MM-DD) |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `status` | String | Trạng thái nhân viên (Allocated, Available, EndingSoon, OnLeave, Resigned) |
| `currentProject` | String | Dự án hiện tại nhân viên đang tham gia |
| `utilization` | Integer | Tỷ lệ sử dụng (0-100%) |
| `endDate` | String | Ngày kết thúc dự án dự kiến (định dạng: YYYY-MM-DD) |
| `emergencyContact` | Object | Thông tin liên hệ khẩn cấp |
| `note` | String | Ghi chú về nhân viên |
| `updatedAt` | String | Thời gian cập nhật (định dạng ISO 8601) |
| `updatedBy` | String | Người thực hiện cập nhật |

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

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "code": 200,
  "message": "Cập nhật thông tin nhân viên thành công",
  "data": {
    "id": 1,
    "employeeCode": "NV001",
    "name": "Nguyễn Văn A",
    "email": "a.nguyenvan@company.com",
    "phone": "0912345678",
    "address": "123 Đường ABC, Quận XYZ, Thành phố HCM (Đã cập nhật)",
    "birthDate": "1990-01-15",
    "joinDate": "2020-03-01",
    "position": "Senior Developer",
    "team": {
      "id": 1,
      "name": "Team Alpha"
    },
    "status": "Allocated",
    "currentProject": "Project XYZ",
    "utilization": 100,
    "endDate": "2025-12-31",
    "emergencyContact": {
      "name": "Nguyễn Thị C",
      "phone": "0987654321",
      "relation": "Vợ"
    },
    "note": "Cập nhật từ Developer lên Senior Developer",
    "updatedAt": "2025-05-01T15:30:00Z",
    "updatedBy": "admin"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "code": "E2000",
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "email",
      "message": "Email không đúng định dạng"
    }
  ]
}
```

#### 400 Bad Request (Duplicate)
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "code": "E4000",
  "message": "Dữ liệu đã tồn tại",
  "errors": [
    {
      "field": "email",
      "message": "Email đã tồn tại trong hệ thống"
    }
  ]
}
```

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
  "code": "E1003",
  "message": "Không có quyền cập nhật thông tin của nhân viên này"
}
```

#### 403 Forbidden (Field Level)
```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "status": "error",
  "code": "E1003",
  "message": "Không có quyền cập nhật một số trường thông tin",
  "errors": [
    {
      "field": "position",
      "message": "Bạn không có quyền cập nhật vị trí công việc"
    }
  ]
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