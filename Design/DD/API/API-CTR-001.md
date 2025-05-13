# API Details: Lấy danh sách hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API lấy danh sách hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để lấy danh sách tất cả các hợp đồng trong hệ thống, hỗ trợ phân trang và lọc theo nhiều tiêu chí khác nhau, giúp người dùng dễ dàng tra cứu và quản lý danh sách hợp đồng.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-001                                  |
| **Tên API**        | Lấy danh sách hợp đồng                       |
| **Mô tả**          | API cho phép lấy danh sách các hợp đồng trong hệ thống với nhiều tiêu chí lọc |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/contracts`                          |
| **Quyền truy cập** | contract:read                                |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên                | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------------|--------------|----------|-------|
| `customerName`     | String       | Không    | Lọc theo tên khách hàng |
| `contractCode`     | String       | Không    | Lọc theo mã hợp đồng |
| `status`           | String       | Không    | Lọc theo trạng thái hợp đồng |
| `contractType`     | String       | Không    | Lọc theo loại hợp đồng |
| `salesId`          | Integer      | Không    | Lọc theo ID nhân viên Sales phụ trách |
| `minAmount`        | Number       | Không    | Giá trị hợp đồng tối thiểu |
| `maxAmount`        | Number       | Không    | Giá trị hợp đồng tối đa |
| `fromDate`         | String       | Không    | Ngày bắt đầu (định dạng: YYYY-MM-DD) |
| `toDate`           | String       | Không    | Ngày kết thúc (định dạng: YYYY-MM-DD) |
| `paymentStatus`    | String       | Không    | Lọc theo trạng thái thanh toán |
| `page`             | Integer      | Không    | Trang cần lấy (mặc định: 1) |
| `size`             | Integer      | Không    | Số hợp đồng trên mỗi trang (mặc định: 20) |
| `sortBy`           | String       | Không    | Trường sắp xếp (mặc định: 'updatedAt') |
| `sortDirection`    | String       | Không    | Hướng sắp xếp: 'asc' hoặc 'desc' (mặc định: 'desc') |

### 3.3 Validate Rule

| Trường             | Điều kiện hợp lệ |
|--------------------|------------------|
| `status`           | Một trong: `Draft`, `InReview`, `Approved`, `Active`, `InProgress`, `OnHold`, `Completed`, `Terminated`, `Expired`, `Cancelled` |
| `contractType`     | Một trong: `FixedPrice`, `TimeAndMaterial`, `Retainer`, `Maintenance`, `Other` |
| `paymentStatus`    | Một trong: `unpaid`, `partial`, `paid`, `overdue` |
| `fromDate`         | Định dạng ngày tháng hợp lệ (YYYY-MM-DD) |
| `toDate`           | Định dạng ngày tháng hợp lệ (YYYY-MM-DD), phải sau fromDate |
| `page`             | Số nguyên > 0 |
| `size`             | Số nguyên > 0 và <= 100 |
| `sortBy`           | Tên trường hợp lệ trong đối tượng hợp đồng |
| `sortDirection`    | Một trong: `asc`, `desc` |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được các hợp đồng có liên kết với nhân viên thuộc team mình quản lý
- Sales: Xem được các hợp đồng do mình phụ trách
- Division Manager: Xem được tất cả hợp đồng thuộc bộ phận mình quản lý
- Kế toán: Xem được tất cả hợp đồng nhưng chỉ tập trung vào thông tin thanh toán
- Admin: Xem được tất cả hợp đồng

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa danh sách hợp đồng và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Danh sách các hợp đồng |
| `pageable` | Object | Thông tin phân trang |

#### Contract Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `customerName` | String | Tên khách hàng |
| `amount` | Number | Tổng giá trị hợp đồng (VND) |
| `contractType` | String | Loại hợp đồng: `FixedPrice`, `TimeAndMaterial`, `Retainer`, `Maintenance`, `Other` |
| `status` | String | Trạng thái hợp đồng: `Draft`, `InReview`, `Approved`, `Active`, `InProgress`, `OnHold`, `Completed`, `Terminated`, `Expired`, `Cancelled` |
| `signDate` | String | Ngày ký hợp đồng (định dạng: YYYY-MM-DD) |
| `startDate` | String | Ngày bắt đầu hiệu lực (định dạng: YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `salesPerson` | Object | Thông tin người phụ trách Sales |
| `relatedOpportunity` | Object | Thông tin cơ hội liên quan (nếu có) |
| `paymentStatus` | Object | Tóm tắt trạng thái thanh toán |
| `employeeCount` | Integer | Số nhân viên đang được phân bổ vào hợp đồng |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |
| `updatedAt` | String | Thời gian cập nhật gần nhất (định dạng ISO 8601) |

#### Sales Person Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên Sales |
| `name` | String | Họ tên nhân viên Sales |

#### Related Opportunity Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội |
| `code` | String | Mã cơ hội |
| `name` | String | Tên cơ hội |

#### Payment Status Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái thanh toán (unpaid, partial, paid, overdue) |
| `paidAmount` | Number | Số tiền đã thanh toán (VND) |
| `totalAmount` | Number | Tổng số tiền cần thanh toán (VND) |
| `paidPercentage` | Number | Tỷ lệ đã thanh toán (%) |
| `nextDueDate` | String/null | Ngày đến hạn thanh toán tiếp theo (YYYY-MM-DD) |
| `nextDueAmount` | Number | Số tiền phải thanh toán ở đợt tiếp theo (VND) |
| `totalTerms` | Integer | Tổng số đợt thanh toán |
| `paidTerms` | Integer | Số đợt đã thanh toán |
| `remainingAmount` | Number | Số tiền còn lại phải thanh toán (VND) |

#### Pageable Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `pageNumber` | Integer | Số trang hiện tại |
| `pageSize` | Integer | Kích thước trang |
| `totalElements` | Integer | Tổng số hợp đồng thỏa mãn điều kiện lọc |
| `totalPages` | Integer | Tổng số trang |
| `first` | Boolean | Có phải là trang đầu tiên không |
| `last` | Boolean | Có phải là trang cuối cùng không |
| `sort` | String | Thông tin sắp xếp |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "content": [
      {
        "id": 45,
        "contractCode": "CTR-2025-045",
        "name": "Hợp đồng phát triển phần mềm XYZ",
        "customerName": "Công ty ABC",
        "amount": 1200000,
        "contractType": "FixedPrice",
        "status": "Active",
        "signDate": "2025-05-30",
        "startDate": "2025-06-01",
        "endDate": "2026-05-31",
        "salesPerson": {
          "id": 5,
          "name": "Trần Văn A"
        },
        "relatedOpportunity": {
          "id": 10,
          "code": "OP-2025-010",
          "name": "Cơ hội phát triển thị trường mới"
        },
        "paymentStatus": {
          "status": "partial",
          "paidAmount": 400000,
          "totalAmount": 1200000,
          "paidPercentage": 33.33,
          "nextDueDate": "2025-09-30",
          "nextDueAmount": 400000,
          "totalTerms": 3,
          "paidTerms": 1,
          "remainingAmount": 800000
        },
        "employeeCount": 5,
        "createdAt": "2025-05-30T09:45:20Z",
        "updatedAt": "2025-06-15T14:30:15Z"
      },
      {
        "id": 44,
        "contractCode": "CTR-2025-044",
        "name": "Hợp đồng bảo trì hệ thống LMN",
        "customerName": "Công ty DEF",
        "amount": 500000,
        "contractType": "Maintenance",
        "status": "Active",
        "signDate": "2025-05-10",
        "startDate": "2025-05-15",
        "endDate": "2026-05-14",
        "salesPerson": {
          "id": 8,
          "name": "Nguyễn Thị B"
        },
        "relatedOpportunity": null,
        "paymentStatus": {
          "status": "paid",
          "paidAmount": 500000,
          "totalAmount": 500000,
          "paidPercentage": 100,
          "nextDueDate": null,
          "nextDueAmount": 0,
          "totalTerms": 1,
          "paidTerms": 1,
          "remainingAmount": 0
        },
        "employeeCount": 2,
        "createdAt": "2025-05-10T11:30:45Z",
        "updatedAt": "2025-05-20T10:15:30Z"
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 20,
      "totalElements": 45,
      "totalPages": 3,
      "first": true,
      "last": false,
      "sort": "updatedAt,desc"
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
      "field": "toDate",
      "message": "Ngày kết thúc phải sau ngày bắt đầu"
    },
    {
      "field": "size",
      "message": "Kích thước trang phải nhỏ hơn hoặc bằng 100"
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
  "message": "Bạn không có quyền xem danh sách hợp đồng"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi truy vấn dữ liệu hợp đồng"
}
``` 