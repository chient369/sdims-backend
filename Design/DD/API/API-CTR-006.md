# API Details: Lấy các điều khoản thanh toán của hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API lấy điều khoản thanh toán | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để truy vấn thông tin về các điều khoản thanh toán của một hợp đồng cụ thể, bao gồm thông tin về số tiền, thời hạn thanh toán và trạng thái thanh toán, hỗ trợ cho việc theo dõi kế hoạch thu tiền và tình trạng thanh toán của khách hàng.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-006                                  |
| **Tên API**        | Lấy các điều khoản thanh toán của hợp đồng   |
| **Mô tả**          | API cho phép lấy danh sách các điều khoản thanh toán của một hợp đồng cụ thể |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/contracts/{contractId}/payment-terms` |
| **Quyền truy cập** | contract:read:own, contract:read:all, contract:read:team, payment-term:read:own, payment-term:read:all |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Integer      | Có       | ID của hợp đồng cần lấy điều khoản thanh toán |

### 3.3 Query Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `status`       | String       | Không    | Lọc theo trạng thái thanh toán (`unpaid`, `paid`, `partial`, `overdue`) |
| `fromDate`     | String       | Không    | Lọc từ ngày dự kiến thanh toán (định dạng yyyy-MM-dd) |
| `toDate`       | String       | Không    | Lọc đến ngày dự kiến thanh toán (định dạng yyyy-MM-dd) |

### 3.4 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `contractId`   | Số nguyên dương, phải tồn tại trong hệ thống |
| `status`       | Một trong các giá trị: `unpaid`, `paid`, `partial`, `overdue` |
| `fromDate`     | Định dạng yyyy-MM-dd               |
| `toDate`       | Định dạng yyyy-MM-dd và >= fromDate (nếu có) |

### 3.5 Phân quyền đặc biệt
- Admin: Có thể xem tất cả điều khoản thanh toán của tất cả hợp đồng
- Division Manager: Có thể xem điều khoản thanh toán của tất cả hợp đồng trong bộ phận
- Sales: Chỉ có thể xem điều khoản thanh toán của hợp đồng do mình phụ trách
- Leader: Có thể xem điều khoản thanh toán của hợp đồng có liên quan đến team mình
- Kế toán: Có thể xem tất cả điều khoản thanh toán nhưng chỉ cập nhật trạng thái thanh toán

### 3.6 Business Rule
- Trạng thái thanh toán `overdue` được xác định tự động dựa trên `dueDate` và ngày hiện tại
- Dữ liệu trả về được sắp xếp theo thứ tự tăng dần của `dueDate` (đợt thanh toán sớm nhất lên đầu)
- Hệ thống sẽ tự động gửi thông báo cho những người liên quan khi đợt thanh toán sắp đến hạn

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin về điều khoản thanh toán và hợp đồng |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contractId` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `totalValue` | Number | Tổng giá trị hợp đồng (VND) |
| `paymentTerms` | Array | Danh sách các điều khoản thanh toán |
| `summary` | Object | Thông tin tóm tắt về tình trạng thanh toán |

#### Payment Term Object (trong mảng paymentTerms)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của đợt thanh toán |
| `name` | String | Tên đợt thanh toán |
| `dueDate` | String | Ngày đến hạn thanh toán (định dạng YYYY-MM-DD) |
| `amount` | Number | Số tiền thanh toán của đợt (VND) |
| `percentage` | Number | Phần trăm so với tổng giá trị hợp đồng |
| `paymentCondition` | String | Điều kiện để thanh toán đợt này |
| `status` | String | Trạng thái thanh toán (paid, unpaid, partial, overdue) |
| `actualPaymentDate` | String/null | Ngày thanh toán thực tế (hoặc null nếu chưa thanh toán) |
| `invoiceInfo` | Object/null | Thông tin hóa đơn (hoặc null nếu chưa xuất hóa đơn) |
| `note` | String/null | Ghi chú đợt thanh toán |

#### Invoice Info Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `invoiceNo` | String | Số hóa đơn |
| `invoiceDate` | String | Ngày xuất hóa đơn (định dạng YYYY-MM-DD) |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalTerms` | Integer | Tổng số đợt thanh toán |
| `totalAmount` | Number | Tổng giá trị hợp đồng (VND) |
| `paidAmount` | Number | Số tiền đã thanh toán (VND) |
| `pendingAmount` | Number | Số tiền chưa thanh toán (VND) |
| `overdueAmount` | Number | Số tiền quá hạn thanh toán (VND) |
| `paidTerms` | Integer | Số đợt đã thanh toán |
| `remainingAmount` | Number | Số tiền còn lại phải thanh toán (VND) |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "contractId": 123,
    "contractCode": "CTR-2025-123",
    "name": "Phát triển ứng dụng quản lý cho Công ty ABC",
    "totalValue": 300000000,
    "paymentTerms": [
      {
        "id": 1,
        "name": "Đợt 1 - Tạm ứng",
        "dueDate": "2025-05-15",
        "amount": 90000000,
        "percentage": 30,
        "paymentCondition": "Sau khi ký hợp đồng 5 ngày",
        "status": "paid",
        "actualPaymentDate": "2025-05-16",
        "invoiceInfo": {
          "invoiceNo": "INV-2025-001",
          "invoiceDate": "2025-05-10"
        },
        "note": "Đã thanh toán đủ"
      },
      {
        "id": 2,
        "name": "Đợt 2 - Nghiệm thu giai đoạn 1",
        "dueDate": "2025-07-15",
        "amount": 120000000,
        "percentage": 40,
        "paymentCondition": "Sau khi nghiệm thu giai đoạn 1",
        "status": "unpaid",
        "actualPaymentDate": null,
        "invoiceInfo": null,
        "note": null
      },
      {
        "id": 3,
        "name": "Đợt 3 - Nghiệm thu cuối",
        "dueDate": "2025-09-30",
        "amount": 90000000,
        "percentage": 30,
        "paymentCondition": "Sau khi nghiệm thu toàn bộ hệ thống",
        "status": "unpaid",
        "actualPaymentDate": null,
        "invoiceInfo": null,
        "note": null
      }
    ],
    "summary": {
      "totalTerms": 3,
      "totalAmount": 300000000,
      "paidAmount": 90000000,
      "pendingAmount": 210000000,
      "overdueAmount": 0,
      "paidTerms": 1,
      "remainingAmount": 210000000
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
      "message": "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu"
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
  "message": "Bạn không có quyền xem điều khoản thanh toán của hợp đồng này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy dữ liệu",
  "errors": [
    {
      "field": "contractId",
      "message": "Không tìm thấy hợp đồng với ID: 999"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi truy vấn dữ liệu điều khoản thanh toán"
}
``` 