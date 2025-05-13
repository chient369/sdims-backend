# API Details: Cập nhật trạng thái thu tiền

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API cập nhật trạng thái thu tiền | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để cho phép Kế toán và Sales cập nhật trạng thái thanh toán của các điều khoản thanh toán trong hợp đồng, ghi nhận thông tin về ngày thanh toán thực tế và các ghi chú liên quan, phục vụ cho việc theo dõi dòng tiền và tình hình thu hồi công nợ.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-007                                  |
| **Tên API**        | Cập nhật trạng thái thu tiền                 |
| **Mô tả**          | API cho phép Kế toán/Sales cập nhật trạng thái thu tiền cho một điều khoản thanh toán |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/contracts/payment-terms/{termId}/status` |
| **Quyền truy cập** | payment-status:update:all, payment-status:update:own |

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
| `termId`       | Integer      | Có       | ID của điều khoản thanh toán cần cập nhật |

### 3.3 Request Body

```json
{
  "status": "Paid",
  "actualPaymentDate": "2025-07-20",
  "paymentMethod": "BankTransfer",
  "invoiceInfo": {
    "invoiceNo": "INV-2025-002",
    "invoiceDate": "2025-07-15"
  },
  "note": "Khách hàng đã thanh toán đủ đợt 2 qua chuyển khoản ngân hàng"
}
```

### 3.4 Body Parameters

| Tên                   | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------------|--------------|----------|-------|
| `status`              | String       | Có       | Trạng thái mới (`Pending`, `Paid`, `PartiallyPaid`) |
| `actualPaymentDate`   | String       | Không    | Ngày thanh toán thực tế (định dạng: YYYY-MM-DD, bắt buộc nếu status=Paid) |
| `paymentMethod`       | String       | Không    | Phương thức thanh toán (bắt buộc nếu status=Paid hoặc PartiallyPaid) |
| `actualAmount`        | Number       | Không    | Số tiền thực tế đã thanh toán (bắt buộc nếu status=PartiallyPaid) |
| `invoiceInfo`         | Object       | Không    | Thông tin hóa đơn |
| `note`                | String       | Không    | Ghi chú về việc thanh toán |

#### Chi tiết Object `invoiceInfo`

| Tên           | Kiểu dữ liệu | Bắt buộc | Mô tả |
|---------------|--------------|----------|-------|
| `invoiceNo`   | String       | Có       | Số hóa đơn |
| `invoiceDate` | String       | Có       | Ngày xuất hóa đơn (định dạng: YYYY-MM-DD) |

### 3.5 Validate Rule

| Trường                | Điều kiện hợp lệ                     |
|-----------------------|------------------------------------- |
| `termId`              | Số nguyên dương, phải tồn tại trong hệ thống |
| `status`              | Một trong các giá trị: `Pending`, `Paid`, `PartiallyPaid` |
| `actualPaymentDate`   | Định dạng YYYY-MM-DD và <= ngày hiện tại<br>Bắt buộc nếu status=Paid hoặc PartiallyPaid |
| `paymentMethod`       | Một trong các giá trị: `Cash`, `BankTransfer`, `Credit`, `Other`<br>Bắt buộc nếu status=Paid hoặc PartiallyPaid |
| `actualAmount`        | > 0 và < tổng số tiền của điều khoản<br>Bắt buộc nếu status=PartiallyPaid |
| `note`                | Tối đa 500 ký tự                    |

### 3.6 Phân quyền đặc biệt
- Kế toán: Có quyền cập nhật trạng thái thanh toán của tất cả hợp đồng
- Admin và Division Manager: Có quyền cập nhật trạng thái thanh toán của tất cả hợp đồng
- Sales: Chỉ có quyền cập nhật trạng thái thanh toán của hợp đồng do mình phụ trách
- Leader và Nhân viên khác không có quyền cập nhật trạng thái thanh toán

### 3.7 Business Rule
- Khi chuyển từ `Pending` sang `Paid`, phải cung cấp `actualPaymentDate` và `paymentMethod`
- Khi chuyển từ `Pending` sang `PartiallyPaid`, phải cung cấp `actualPaymentDate`, `paymentMethod` và `actualAmount`
- Hệ thống sẽ tự động cập nhật doanh thu thực tế khi một khoản thanh toán được đánh dấu là `Paid` hoặc `PartiallyPaid`
- Không cho phép chuyển trạng thái từ `Paid` về `Pending` nếu đã ghi nhận trong báo cáo doanh thu đóng kỳ
- Hệ thống sẽ tự động gửi thông báo cho các bên liên quan khi trạng thái thanh toán được cập nhật
- Tất cả các thay đổi trạng thái thanh toán đều được ghi lại trong lịch sử hoạt động của hợp đồng

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Cập nhật trạng thái thanh toán thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về điều khoản thanh toán sau khi cập nhật |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của điều khoản thanh toán |
| `contractId` | Integer | ID của hợp đồng liên quan |
| `contractCode` | String | Mã hợp đồng |
| `contractTitle` | String | Tên hợp đồng |
| `name` | String | Tên đợt thanh toán |
| `amount` | Number | Số tiền cần thanh toán (VND) |
| `percentage` | Number | Phần trăm so với tổng giá trị hợp đồng |
| `dueDate` | String | Ngày đến hạn thanh toán (định dạng: YYYY-MM-DD) |
| `status` | String | Trạng thái thanh toán mới |
| `actualPaymentDate` | String/null | Ngày thanh toán thực tế (định dạng: YYYY-MM-DD) |
| `paymentMethod` | String/null | Phương thức thanh toán |
| `invoiceInfo` | Object/null | Thông tin hóa đơn |
| `note` | String | Ghi chú về việc thanh toán |
| `updatedBy` | Object | Thông tin người cập nhật |
| `updatedAt` | String | Thời gian cập nhật (định dạng ISO 8601) |

#### Invoice Info Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `invoiceNo` | String | Số hóa đơn |
| `invoiceDate` | String | Ngày xuất hóa đơn (định dạng: YYYY-MM-DD) |

#### Updater Object (updatedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người cập nhật |
| `name` | String | Họ tên người cập nhật |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "message": "Cập nhật trạng thái thanh toán thành công",
  "data": {
    "id": 2,
    "contractId": 123,
    "contractCode": "CTR-2025-123",
    "contractTitle": "Phát triển ứng dụng quản lý cho Công ty ABC",
    "name": "Đợt 2 - Nghiệm thu giai đoạn 1",
    "amount": 120000000,
    "percentage": 40,
    "dueDate": "2025-07-15",
    "status": "Paid",
    "actualPaymentDate": "2025-07-20",
    "paymentMethod": "BankTransfer",
    "invoiceInfo": {
      "invoiceNo": "INV-2025-002",
      "invoiceDate": "2025-07-15"
    },
    "note": "Khách hàng đã thanh toán đủ đợt 2 qua chuyển khoản ngân hàng",
    "updatedBy": {
      "id": 8,
      "name": "Nguyễn Thị Kế Toán"
    },
    "updatedAt": "2025-07-20T10:15:30Z"
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
      "field": "actualPaymentDate",
      "message": "Ngày thanh toán thực tế là bắt buộc khi trạng thái là 'Paid'"
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
  "message": "Bạn không có quyền cập nhật trạng thái thanh toán"
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
      "field": "termId",
      "message": "Không tìm thấy điều khoản thanh toán với ID: 999"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Xung đột dữ liệu",
  "errors": [
    {
      "field": "status",
      "message": "Không thể thay đổi trạng thái vì đã được ghi nhận trong báo cáo doanh thu đóng kỳ"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi cập nhật trạng thái thanh toán"
}
``` 