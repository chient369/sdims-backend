# API Details: Lấy danh sách nhân viên liên kết với hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API lấy danh sách nhân viên liên kết với hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để truy xuất danh sách nhân viên được phân bổ tham gia vào một hợp đồng cụ thể, giúp theo dõi việc phân bổ nguồn lực cho dự án, tỷ lệ tham gia và thời gian làm việc của từng nhân viên, hỗ trợ cho việc quản lý nhân sự và tính toán doanh thu dự án.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-012                                  |
| **Tên API**        | Lấy danh sách nhân viên liên kết với hợp đồng |
| **Mô tả**          | API cho phép lấy danh sách nhân viên được phân bổ tham gia vào một hợp đồng cụ thể |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/contracts/{contractId}/employees`   |
| **Quyền truy cập** | contract:employee:read                       |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Long         | Có       | ID của hợp đồng cần lấy danh sách nhân viên |

### 3.3 Query Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `status`       | String       | Không    | Lọc theo trạng thái phân bổ: `Active`, `Ended` |
| `teamId`       | Long         | Không    | Lọc theo ID của team |
| `keyword`      | String       | Không    | Tìm kiếm theo tên hoặc mã nhân viên |

### 3.4 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `contractId`   | Phải tồn tại trong hệ thống         |
| `status`       | Một trong các giá trị: `Active`, `Ended` |

### 3.5 Phân quyền đặc biệt
- Leader: Chỉ xem được phân bổ nhân viên cho hợp đồng có nhân viên thuộc team mình quản lý
- Sales: Xem được phân bổ nhân viên của hợp đồng do mình phụ trách
- Division Manager: Xem được phân bổ nhân viên của tất cả hợp đồng thuộc bộ phận mình quản lý
- Admin: Xem được phân bổ nhân viên của tất cả hợp đồng

### 3.6 Business Rule

- Mỗi nhân viên được phân bổ tham gia hợp đồng cần có các thông tin liên quan:
  - Tỷ lệ phân bổ (% allocation): thời gian tham gia dự án, tính theo tỷ lệ phần trăm
  - Ngày bắt đầu và kết thúc tham gia
  - Vai trò trong dự án
  - Đơn giá bán (billing rate): giá trị được tính cho doanh thu
- Dữ liệu trả về mặc định bao gồm cả nhân viên đang tham gia (`Active`) và đã kết thúc (`Ended`), có thể lọc theo trạng thái

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin về hợp đồng và danh sách nhân viên liên kết |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contractId` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `contractName` | String | Tên hợp đồng |
| `employees` | Array | Danh sách các nhân viên được phân bổ cho hợp đồng |
| `totalEmployees` | Integer | Tổng số nhân viên liên kết với hợp đồng |
| `activeEmployees` | Integer | Số nhân viên đang tham gia (trạng thái Active) |

#### Employee Assignment Object (trong mảng employees)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi phân bổ nhân viên |
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `allocation` | Integer | Tỷ lệ phân bổ thời gian (%) |
| `role` | String | Vai trò của nhân viên trong dự án |
| `startDate` | String | Ngày bắt đầu tham gia (định dạng: YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc tham gia (định dạng: YYYY-MM-DD) |
| `status` | String | Trạng thái phân bổ (Active, Ended) |
| `billingRate` | Number | Đơn giá bán ra (đơn vị: USD hoặc theo cấu hình) |
| `allocatedBy` | String | Người phân bổ nhân viên |
| `allocatedAt` | String | Thời gian phân bổ (định dạng ISO 8601) |

#### Team Object (trong employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "contractId": 123,
    "contractCode": "HD-2025-123",
    "contractName": "Phát triển ứng dụng quản lý cho Công ty ABC",
    "employees": [
      {
        "id": 1,
        "employeeId": 101,
        "employeeCode": "NV001",
        "name": "Nguyễn Văn A",
        "team": {
          "id": 1,
          "name": "Team Alpha"
        },
        "allocation": 100,
        "role": "Developer",
        "startDate": "2025-05-15",
        "endDate": "2025-09-30",
        "status": "Active",
        "billingRate": 1000,
        "allocatedBy": "tran.leader",
        "allocatedAt": "2025-05-10T10:30:00Z"
      },
      {
        "id": 2,
        "employeeId": 102,
        "employeeCode": "NV002",
        "name": "Trần Thị B",
        "team": {
          "id": 1,
          "name": "Team Alpha"
        },
        "allocation": 50,
        "role": "Tester",
        "startDate": "2025-05-15",
        "endDate": "2025-07-15",
        "status": "Ended",
        "billingRate": 800,
        "allocatedBy": "tran.leader",
        "allocatedAt": "2025-05-10T10:35:00Z"
      },
      {
        "id": 3,
        "employeeId": 103,
        "employeeCode": "NV003",
        "name": "Lê Văn C",
        "team": {
          "id": 2,
          "name": "Team Beta"
        },
        "allocation": 80,
        "role": "Tech Lead",
        "startDate": "2025-05-15",
        "endDate": "2025-09-30",
        "status": "Active",
        "billingRate": 1500,
        "allocatedBy": "nguyen.ka",
        "allocatedAt": "2025-05-10T11:00:00Z"
      }
    ],
    "totalEmployees": 3,
    "activeEmployees": 2
  }
}
```

### 4.2 Error Responses

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
  "message": "Bạn không có quyền xem danh sách nhân viên của hợp đồng này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3003",
  "message": "Không tìm thấy hợp đồng với ID: 123"
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
      "field": "status",
      "message": "Trạng thái không hợp lệ"
    }
  ]
}
``` 