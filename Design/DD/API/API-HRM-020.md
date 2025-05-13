# API Details: Cập nhật trạng thái và phân bổ dự án cho nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2023-07-18 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép cập nhật trạng thái làm việc và thông tin phân bổ dự án của nhân viên trong hệ thống quản lý nhân sự.

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-020                                      |
| **Tên API**        | Cập nhật trạng thái và phân bổ dự án cho nhân viên |
| **Mô tả**          | API cho phép cập nhật trạng thái làm việc và thông tin phân bổ dự án của nhân viên |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/employees/{employeeId}/status`      |
| **Quyền truy cập** | employee-status:update:all, employee-status:update:team |

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
| `employeeId` | Integer      | Có       | ID của nhân viên cần cập nhật trạng thái |

### 3.3 Request Body

| Tên               | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-------------------|--------------|----------|-------|
| `status`          | String       | Có       | Trạng thái mới của nhân viên |
| `projectId`       | Integer      | Không    | ID của dự án (nếu status = `Allocated`) |
| `projectName`     | String       | Không    | Tên dự án (nếu projectId không có hoặc là dự án ngoài hệ thống) |
| `clientName`      | String       | Không    | Tên khách hàng |
| `allocation`      | Integer      | Không    | Tỷ lệ phân bổ (%) cho dự án hiện tại (nếu status = `Allocated`) |
| `role`            | String       | Không    | Vai trò trong dự án |
| `startDate`       | String       | Không    | Ngày bắt đầu làm việc trên dự án (định dạng: YYYY-MM-DD) |
| `endDate`         | String       | Không    | Ngày dự kiến kết thúc tham gia dự án (định dạng: YYYY-MM-DD) |
| `billable`        | Boolean      | Không    | Có tính doanh thu không (mặc định: `true`) |
| `notes`           | String       | Không    | Ghi chú thêm về trạng thái/phân bổ |

### 3.4 Validate Rule

| Trường          | Điều kiện hợp lệ |
|-----------------|------------------|
| `employeeId`    | Phải là số nguyên dương và tồn tại trong hệ thống |
| `status`        | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `projectId`     | Phải là số nguyên dương và tồn tại trong hệ thống (nếu có) |
| `projectName`   | Độ dài: 1-100 ký tự (yêu cầu nếu status = `Allocated` và không có projectId) |
| `clientName`    | Độ dài tối đa: 100 ký tự |
| `allocation`    | Số nguyên từ 0 đến 100 (yêu cầu nếu status = `Allocated`) |
| `role`          | Độ dài tối đa: 100 ký tự |
| `startDate`     | Định dạng: YYYY-MM-DD |
| `endDate`       | Định dạng: YYYY-MM-DD, phải sau startDate |
| `notes`         | Độ dài tối đa: 500 ký tự |

### 3.5 Phân quyền đặc biệt

- `team:employee:manage`: Chỉ cập nhật nhân viên trong team của mình
- `employee:manage`: Cập nhật tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả thực hiện |
| `data` | Object | Đối tượng chứa thông tin cập nhật trạng thái nhân viên |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employee` | Object | Thông tin cơ bản của nhân viên |
| `allocation` | Object | Thông tin phân bổ dự án (nếu status = `Allocated`) |
| `previousStatus` | String | Trạng thái trước khi cập nhật |
| `updatedBy` | Object | Thông tin người cập nhật |
| `updatedAt` | String | Thời điểm cập nhật (ISO 8601) |

#### Employee Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `status` | String | Trạng thái hiện tại của nhân viên sau khi cập nhật |

#### Allocation Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `projectId` | Integer | ID của dự án (nếu có) |
| `projectName` | String | Tên dự án |
| `clientName` | String | Tên khách hàng |
| `allocation` | Integer | Tỷ lệ phân bổ (%) |
| `role` | String | Vai trò trong dự án |
| `startDate` | String | Ngày bắt đầu (YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc dự kiến (YYYY-MM-DD) |
| `billable` | Boolean | Có tính doanh thu không |
| `notes` | String | Ghi chú về phân bổ |

#### UpdatedBy Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng thực hiện cập nhật |
| `name` | String | Tên người dùng thực hiện cập nhật |

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "code": 200,
  "message": "Cập nhật trạng thái nhân viên thành công",
  "data": {
    "employee": {
      "id": 12,
      "employeeCode": "NV012",
      "name": "Hoàng Văn F",
      "position": "Developer",
      "status": "Allocated"
    },
    "allocation": {
      "projectId": 5,
      "projectName": "Dự án ABC",
      "clientName": "Công ty XYZ",
      "allocation": 100,
      "role": "Backend Developer",
      "startDate": "2025-05-10",
      "endDate": "2025-08-31",
      "billable": true,
      "notes": "Dự án mới, cần bổ sung resource gấp"
    },
    "previousStatus": "Available",
    "updatedBy": {
      "id": 2,
      "name": "Nguyễn Văn Leader"
    },
    "updatedAt": "2025-05-03T09:15:00Z"
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
      "field": "status",
      "message": "Trạng thái 'InProgress' không hợp lệ. Các trạng thái hợp lệ: Allocated, Available, EndingSoon, OnLeave, Resigned"
    },
    {
      "field": "allocation",
      "message": "Tỷ lệ phân bổ phải là số nguyên từ 0 đến 100"
    }
  ]
}
```

#### 400 Bad Request (Inconsistent Data)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E2002 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "code": "E2002",
  "message": "Dữ liệu không nhất quán",
  "errors": [
    {
      "field": "status",
      "message": "Trạng thái 'Available' không được có thông tin dự án. Hãy bỏ trống các trường projectId, projectName, allocation"
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
| `code` | String | Mã lỗi: E1002 |
| `message` | String | Thông báo lỗi |

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "status": "error",
  "code": "E1002",
  "message": "Không có quyền cập nhật trạng thái của nhân viên này"
}
```

#### 404 Not Found

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3000 hoặc E3003 |
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
  "code": "E3003",
  "message": "Không tìm thấy dự án với ID: 999"
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