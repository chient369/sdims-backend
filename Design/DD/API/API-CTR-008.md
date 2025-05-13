# API Details: Import trạng thái thanh toán từ file

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API import trạng thái thanh toán | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để cho phép bộ phận Kế toán import và cập nhật hàng loạt trạng thái thanh toán của các điều khoản hợp đồng từ file Excel hoặc CSV, giúp tiết kiệm thời gian và đảm bảo tính chính xác trong việc theo dõi doanh thu và tình hình công nợ của công ty.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-008                                  |
| **Tên API**        | Import trạng thái thanh toán từ file         |
| **Mô tả**          | API cho phép Kế toán import trạng thái thanh toán hàng loạt từ file Excel/CSV |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/contracts/payment-terms/import-status` |
| **Quyền truy cập** | payment-status:import                         |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `multipart/form-data` |

### 3.2 Form Data Parameters

| Tên             | Kiểu dữ liệu    | Bắt buộc | Mô tả |
|-----------------|-----------------|----------|-------|
| `file`          | File            | Có       | File Excel (.xlsx, .xls) hoặc CSV (.csv) chứa dữ liệu trạng thái thanh toán |
| `updateMode`    | String          | Không    | Chế độ cập nhật: `ALL` (mặc định) hoặc `ONLY_PENDING` |
| `notifyOwners`  | Boolean         | Không    | Có gửi thông báo đến người phụ trách hợp đồng không (mặc định: `true`) |

### 3.3 Validate Rule

| Trường          | Điều kiện hợp lệ                     |
|-----------------|------------------------------------- |
| `file`          | - Phải là định dạng .xlsx, .xls hoặc .csv<br>- Kích thước tối đa 5MB<br>- Phải đúng cấu trúc template |
| `updateMode`    | Một trong các giá trị: `ALL`, `ONLY_PENDING` |
| `notifyOwners`  | Giá trị boolean: `true` hoặc `false` |

### 3.4 Yêu cầu về cấu trúc file

1. **Định dạng cột trong file Excel/CSV**:
   - Cột A (bắt buộc): Mã hợp đồng (Contract Code)
   - Cột B (bắt buộc): ID điều khoản thanh toán (Term ID) hoặc Tên điều khoản (Term Name)
   - Cột C (bắt buộc): Trạng thái (Status) - "Pending", "Paid", hoặc "PartiallyPaid"
   - Cột D (có điều kiện): Ngày thanh toán thực tế (Actual Payment Date) - bắt buộc nếu Status là "Paid" hoặc "PartiallyPaid"
   - Cột E (có điều kiện): Phương thức thanh toán (Payment Method) - bắt buộc nếu Status là "Paid" hoặc "PartiallyPaid"
   - Cột F (có điều kiện): Số tiền thực tế (Actual Amount) - bắt buộc nếu Status là "PartiallyPaid"
   - Cột G (không bắt buộc): Số hóa đơn (Invoice No.)
   - Cột H (không bắt buộc): Ngày xuất hóa đơn (Invoice Date)
   - Cột I (không bắt buộc): Ghi chú (Note)

2. **Dòng đầu tiên phải là tiêu đề các cột**.

3. **Định dạng ngày tháng**: YYYY-MM-DD (ví dụ: 2025-07-20).

### 3.5 Phân quyền đặc biệt
- Kế toán: Có quyền import trạng thái thanh toán cho tất cả hợp đồng
- Admin và Division Manager: Có quyền import trạng thái thanh toán cho tất cả hợp đồng
- Sales và các vai trò khác không có quyền import trạng thái thanh toán hàng loạt

### 3.6 Business Rule
- Chế độ cập nhật:
  - `ALL`: Cập nhật tất cả các điều khoản trong file, bất kể trạng thái hiện tại
  - `ONLY_PENDING`: Chỉ cập nhật các điều khoản có trạng thái hiện tại là `Pending`
- Hệ thống sẽ tự động cập nhật doanh thu thực tế khi các khoản thanh toán được cập nhật thành `Paid` hoặc `PartiallyPaid`
- Không cho phép cập nhật trạng thái từ `Paid` về `Pending` nếu đã ghi nhận trong báo cáo doanh thu đóng kỳ
- Nếu `notifyOwners` được đặt là `true`, hệ thống sẽ gửi thông báo cho người phụ trách hợp đồng (contract owner) khi trạng thái thanh toán được cập nhật
- Tất cả các thao tác import sẽ được ghi lại trong lịch sử hoạt động hệ thống
- File template mới nhất có thể được tải từ hệ thống thông qua API `/api/v1/contracts/payment-terms/export-template`

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Đã import trạng thái thanh toán thành công" |
| `data` | Object | Đối tượng chứa thông tin kết quả import |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `importId` | String | Mã định danh của thao tác import |
| `totalRecords` | Integer | Tổng số bản ghi trong file |
| `successCount` | Integer | Số bản ghi được cập nhật thành công |
| `failureCount` | Integer | Số bản ghi không thể cập nhật |
| `updatedTerms` | Array | Danh sách các điều khoản đã được cập nhật thành công |
| `errors` | Array | Danh sách lỗi gặp phải trong quá trình import |
| `summary` | Object | Thông tin tóm tắt về thao tác import |

#### Updated Term Object (trong mảng updatedTerms)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của điều khoản thanh toán |
| `contractId` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `name` | String | Tên đợt thanh toán |
| `oldStatus` | String | Trạng thái thanh toán trước khi cập nhật |
| `newStatus` | String | Trạng thái thanh toán sau khi cập nhật |
| `actualPaymentDate` | String | Ngày thanh toán thực tế (định dạng: YYYY-MM-DD) |
| `paymentMethod` | String | Phương thức thanh toán |
| `amount` | Number | Số tiền thanh toán (VND) |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `row` | Integer | Số thứ tự dòng trong file |
| `contractCode` | String | Mã hợp đồng |
| `termName` | String | Tên đợt thanh toán |
| `errorType` | String | Loại lỗi (NOT_FOUND, VALIDATION_ERROR, BUSINESS_RULE_VIOLATION, etc.) |
| `message` | String | Thông báo lỗi chi tiết |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalAmount` | Number | Tổng số tiền đã thanh toán (VND) |
| `totalContracts` | Integer | Số lượng hợp đồng đã được cập nhật |
| `importedBy` | Object | Thông tin người thực hiện import |
| `importedAt` | String | Thời gian import (định dạng ISO 8601) |

#### Importer Object (importedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người import |
| `name` | String | Họ tên người import |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "message": "Đã import trạng thái thanh toán thành công",
  "data": {
    "importId": "IMPORT-20250601-123456",
    "totalRecords": 15,
    "successCount": 12,
    "failureCount": 3,
    "updatedTerms": [
      {
        "id": 2,
        "contractId": 123,
        "contractCode": "CTR-2025-123",
        "name": "Đợt 2 - Nghiệm thu giai đoạn 1",
        "oldStatus": "Pending",
        "newStatus": "Paid",
        "actualPaymentDate": "2025-07-20",
        "paymentMethod": "BankTransfer",
        "amount": 120000000
      },
      {
        "id": 5,
        "contractId": 124,
        "contractCode": "CTR-2025-124",
        "name": "Đợt 1 - Tạm ứng",
        "oldStatus": "Pending",
        "newStatus": "Paid",
        "actualPaymentDate": "2025-06-15",
        "paymentMethod": "BankTransfer",
        "amount": 90000000
      }
    ],
    "errors": [
      {
        "row": 4,
        "contractCode": "CTR-2025-125",
        "termName": "Đợt 3",
        "errorType": "NOT_FOUND",
        "message": "Không tìm thấy hợp đồng hoặc điều khoản thanh toán"
      },
      {
        "row": 7,
        "contractCode": "CTR-2025-126",
        "termName": "Đợt 1",
        "errorType": "VALIDATION_ERROR",
        "message": "Thiếu ngày thanh toán thực tế cho trạng thái Paid"
      },
      {
        "row": 11,
        "contractCode": "CTR-2025-127",
        "termName": "Đợt 2",
        "errorType": "BUSINESS_RULE_VIOLATION",
        "message": "Điều khoản đã được ghi nhận trong báo cáo doanh thu đóng kỳ"
      }
    ],
    "summary": {
      "totalAmount": 210000000,
      "totalContracts": 2,
      "importedBy": {
        "id": 8,
        "name": "Nguyễn Thị Kế Toán"
      },
      "importedAt": "2025-06-01T11:30:45Z"
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
      "field": "file",
      "message": "Định dạng file không được hỗ trợ. Vui lòng sử dụng file Excel (.xlsx, .xls) hoặc CSV (.csv)"
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
  "message": "Bạn không có quyền import trạng thái thanh toán"
}
```

#### 422 Unprocessable Entity
```json
{
  "status": "error",
  "code": "E3002",
  "message": "Không thể xử lý file",
  "errors": [
    {
      "field": "file",
      "message": "Cấu trúc file không đúng mẫu. Vui lòng tải template mới và thử lại"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi xử lý file import"
}
``` 