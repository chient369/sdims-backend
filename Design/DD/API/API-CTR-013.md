# API Details: Liên kết nhân viên vào hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API liên kết nhân viên vào hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để phân bổ và liên kết nhân viên với một hợp đồng cụ thể, cho phép người quản lý phân công nhân sự tham gia dự án với các thông tin chi tiết về thời gian, tỷ lệ tham gia, vai trò và đơn giá, hỗ trợ việc lập kế hoạch nguồn lực và tính toán doanh thu dự án.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-013                                  |
| **Tên API**        | Liên kết nhân viên vào hợp đồng              |
| **Mô tả**          | API cho phép thêm mới hoặc cập nhật nhân viên tham gia hợp đồng |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/contracts/{contractId}/employees`   |
| **Quyền truy cập** | contract:employee:assign                     |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Long         | Có       | ID của hợp đồng cần liên kết nhân viên |

### 3.3 Request Body

| Tên                   | Kiểu dữ liệu       | Bắt buộc | Mô tả |
|-----------------------|--------------------|----------|-------|
| `employeeAllocations` | Array of Object    | Có       | Danh sách các phân bổ nhân viên cho hợp đồng |

**Mỗi phần tử trong `employeeAllocations` có cấu trúc:**

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `id`           | Long         | Không    | ID của phân bổ (nếu là cập nhật phân bổ đã tồn tại) |
| `employeeId`   | Long         | Có       | ID của nhân viên |
| `allocation`   | Integer      | Có       | Tỷ lệ phân bổ, từ 1-100 (%) |
| `role`         | String       | Có       | Vai trò trong dự án |
| `startDate`    | Date         | Có       | Ngày bắt đầu tham gia (yyyy-MM-dd) |
| `endDate`      | Date         | Có       | Ngày kết thúc (yyyy-MM-dd) |
| `billingRate`  | Number       | Có       | Đơn giá bán (billing rate) |
| `note`         | String       | Không    | Ghi chú |

### 3.4 Validate Rule

| Trường            | Điều kiện hợp lệ                     |
|-------------------|------------------------------------- |
| `contractId`      | Phải tồn tại trong hệ thống         |
| `employeeId`      | Phải tồn tại trong hệ thống và có trạng thái hoạt động |
| `allocation`      | Số nguyên từ 1 đến 100              |
| `role`            | Không được để trống, tối đa 100 ký tự |
| `startDate`       | Định dạng yyyy-MM-dd, không nhỏ hơn ngày bắt đầu hợp đồng |
| `endDate`         | Định dạng yyyy-MM-dd, phải >= startDate và không lớn hơn ngày kết thúc hợp đồng |
| `billingRate`     | Số dương > 0                        |
| `note`            | Tối đa 500 ký tự                    |

### 3.5 Phân quyền đặc biệt
- Leader: Chỉ được liên kết nhân viên thuộc team mình quản lý
- Division Manager: Được liên kết bất kỳ nhân viên nào thuộc bộ phận mình quản lý
- Admin: Được liên kết bất kỳ nhân viên nào trong hệ thống
- Sales không có quyền liên kết nhân viên vào hợp đồng

### 3.6 Business Rule

- Tổng tỷ lệ phân bổ của một nhân viên tại một thời điểm (tính theo ngày) không được vượt quá 100% trên tất cả các hợp đồng
- Nếu liên kết mới xung đột với phân bổ hiện tại của nhân viên (vượt quá 100%), hệ thống sẽ báo lỗi và cung cấp thông tin về xung đột
- Hệ thống sẽ tự động cập nhật trạng thái nhân viên trong module Quản lý Nhân sự:
  - Cập nhật thành `Allocated` khi được phân bổ
  - Thiết lập `EndingSoon` khi gần đến ngày kết thúc dự án
- Mỗi lần thay đổi phân bổ sẽ được ghi nhận vào lịch sử để theo dõi
- API này cho phép cả thêm mới và cập nhật phân bổ hiện có:
  - Nếu có `id` -> Cập nhật phân bổ hiện có
  - Nếu không có `id` -> Thêm mới phân bổ

---

## 4. Request Example

```json
{
  "employeeAllocations": [
    {
      "employeeId": 101,
      "allocation": 100,
      "role": "Developer",
      "startDate": "2025-05-15",
      "endDate": "2025-09-30",
      "billingRate": 1000,
      "note": "Full-time developer"
    },
    {
      "id": 2,
      "employeeId": 102,
      "allocation": 50,
      "role": "Tester",
      "startDate": "2025-05-15",
      "endDate": "2025-08-30",
      "billingRate": 800,
      "note": "Kéo dài thời gian tham gia từ 07/15 đến 08/30"
    }
  ]
}
```

## 5. Response

### 5.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Đã liên kết nhân viên vào hợp đồng thành công" |
| `data` | Object | Đối tượng chứa thông tin về kết quả liên kết nhân viên |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contractId` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `updatedAllocations` | Array | Danh sách các phân bổ đã được cập nhật hoặc tạo mới |
| `totalAllocations` | Integer | Tổng số phân bổ đã xử lý |

#### Employee Allocation Object (trong mảng updatedAllocations)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi phân bổ |
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên nhân viên |
| `allocation` | Integer | Tỷ lệ phân bổ (%) |
| `role` | String | Vai trò trong dự án |
| `startDate` | String | Ngày bắt đầu tham gia (định dạng: YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc (định dạng: YYYY-MM-DD) |
| `billingRate` | Number | Đơn giá bán ra (billing rate) |
| `status` | String | Trạng thái phân bổ (Active, Ended) |
| `action` | String | Hành động đã thực hiện (CREATED, UPDATED) |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "message": "Đã liên kết nhân viên vào hợp đồng thành công",
  "data": {
    "contractId": 123,
    "contractCode": "HD-2025-123",
    "updatedAllocations": [
      {
        "id": 1,
        "employeeId": 101,
        "employeeCode": "NV001",
        "name": "Nguyễn Văn A",
        "allocation": 100,
        "role": "Developer",
        "startDate": "2025-05-15",
        "endDate": "2025-09-30",
        "billingRate": 1000,
        "status": "Active",
        "action": "CREATED"
      },
      {
        "id": 2,
        "employeeId": 102,
        "employeeCode": "NV002",
        "name": "Trần Thị B",
        "allocation": 50,
        "role": "Tester",
        "startDate": "2025-05-15",
        "endDate": "2025-08-30",
        "billingRate": 800,
        "status": "Active",
        "action": "UPDATED"
      }
    ],
    "totalAllocations": 2
  }
}
```

### 5.2 Error Responses

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
  "message": "Bạn không có quyền liên kết nhân viên vào hợp đồng này"
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
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "employeeAllocations[0].allocation",
      "message": "Tỷ lệ phân bổ phải từ 1 đến 100"
    },
    {
      "field": "employeeAllocations[1].endDate",
      "message": "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4004",
  "message": "Xung đột phân bổ nhân viên",
  "errors": [
    {
      "field": "employeeAllocations[0]",
      "message": "Nhân viên Nguyễn Văn A (NV001) đã được phân bổ 80% vào hợp đồng HD-2025-124 trong khoảng thời gian từ 2025-05-01 đến 2025-06-30. Tổng phân bổ sẽ vượt quá 100%."
    }
  ]
} 