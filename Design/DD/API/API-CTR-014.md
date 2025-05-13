# API Details: Gỡ liên kết nhân viên khỏi hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API gỡ liên kết nhân viên khỏi hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để gỡ bỏ liên kết một nhân viên khỏi hợp đồng hoặc kết thúc sớm thời gian tham gia của họ, giúp quản lý linh hoạt việc phân bổ nguồn lực khi có sự thay đổi về nhu cầu nhân sự hoặc khi nhân viên kết thúc công việc sớm hơn dự kiến.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-014                                  |
| **Tên API**        | Gỡ liên kết nhân viên khỏi hợp đồng         |
| **Mô tả**          | API cho phép xóa phân bổ của một nhân viên khỏi hợp đồng |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/contracts/{contractId}/employees/{employeeId}` |
| **Quyền truy cập** | contract:employee:remove                     |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Long         | Có       | ID của hợp đồng |
| `employeeId`   | Long         | Có       | ID của nhân viên cần gỡ khỏi hợp đồng |

### 3.3 Query Parameters

| Tên              | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------------|--------------|----------|-------|
| `endDate`        | Date         | Không    | Ngày kết thúc phân bổ (yyyy-MM-dd), nếu muốn chỉ kết thúc phân bổ sớm thay vì xóa hoàn toàn |

### 3.4 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `contractId`   | Phải tồn tại trong hệ thống         |
| `employeeId`   | Phải tồn tại và đang được phân bổ cho hợp đồng này |
| `endDate`      | Định dạng yyyy-MM-dd, phải >= ngày bắt đầu phân bổ và <= ngày hiện tại (nếu có) |

### 3.5 Phân quyền đặc biệt
- Leader: Chỉ gỡ được nhân viên thuộc team mình quản lý
- Division Manager: Gỡ được bất kỳ nhân viên nào thuộc bộ phận mình quản lý
- Admin: Gỡ được bất kỳ nhân viên nào trong hệ thống
- Sales không có quyền gỡ nhân viên khỏi hợp đồng

### 3.6 Business Rule

- Hệ thống hỗ trợ hai chế độ:
  - **Kết thúc sớm:** Nếu cung cấp `endDate`, hệ thống chỉ cập nhật ngày kết thúc phân bổ mà không xóa hoàn toàn liên kết
  - **Xóa hoàn toàn:** Nếu không cung cấp `endDate`, hệ thống sẽ xóa hoàn toàn liên kết (phù hợp khi thêm nhầm nhân viên)
- Không được phép xóa hoàn toàn phân bổ đã tồn tại quá 30 ngày (chỉ được phép kết thúc sớm)
- Hệ thống sẽ tự động cập nhật trạng thái nhân viên trong module Quản lý Nhân sự nếu cần thiết
- Mỗi lần thay đổi phân bổ sẽ được ghi nhận vào lịch sử để theo dõi

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả tùy theo thao tác: "Đã gỡ nhân viên khỏi hợp đồng thành công" hoặc "Đã cập nhật ngày kết thúc tham gia của nhân viên thành công" |
| `data` | Object | Đối tượng chứa thông tin về kết quả gỡ liên kết nhân viên |

#### Data Object (trường hợp xóa hoàn toàn)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contractId` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `employeeId` | Integer | ID của nhân viên đã gỡ |
| `employeeCode` | String | Mã nhân viên |
| `employeeName` | String | Tên nhân viên |
| `action` | String | Hành động đã thực hiện: "REMOVED" |

#### Data Object (trường hợp kết thúc sớm)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contractId` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `employeeName` | String | Tên nhân viên |
| `originalEndDate` | String | Ngày kết thúc ban đầu (định dạng: YYYY-MM-DD) |
| `newEndDate` | String | Ngày kết thúc mới (định dạng: YYYY-MM-DD) |
| `action` | String | Hành động đã thực hiện: "ENDED_EARLY" |

#### Ví dụ (trường hợp xóa hoàn toàn):

```json
{
  "status": "success",
  "code": 200,
  "message": "Đã gỡ nhân viên khỏi hợp đồng thành công",
  "data": {
    "contractId": 123,
    "contractCode": "HD-2025-123",
    "employeeId": 102,
    "employeeCode": "NV002",
    "employeeName": "Trần Thị B",
    "action": "REMOVED"
  }
}
```

#### Ví dụ (trường hợp kết thúc sớm):

```json
{
  "status": "success",
  "code": 200,
  "message": "Đã cập nhật ngày kết thúc tham gia của nhân viên thành công",
  "data": {
    "contractId": 123,
    "contractCode": "HD-2025-123",
    "employeeId": 102,
    "employeeCode": "NV002",
    "employeeName": "Trần Thị B",
    "originalEndDate": "2025-08-30",
    "newEndDate": "2025-06-30",
    "action": "ENDED_EARLY"
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
  "message": "Bạn không có quyền gỡ nhân viên khỏi hợp đồng này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy phân bổ của nhân viên với ID: 102 trong hợp đồng với ID: 123"
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
      "field": "endDate",
      "message": "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu phân bổ (2025-05-15)"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4004",
  "message": "Không thể xóa hoàn toàn phân bổ đã tồn tại quá 30 ngày. Vui lòng sử dụng tính năng kết thúc sớm bằng cách cung cấp endDate"
}
``` 