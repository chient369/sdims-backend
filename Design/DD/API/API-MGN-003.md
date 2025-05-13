# API Details: Import chi phí nhân viên hàng tháng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API import chi phí nhân viên | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để import dữ liệu chi phí nhân viên hàng tháng từ file Excel hoặc CSV, hỗ trợ việc cập nhật nhanh và đồng bộ thông tin chi phí cho nhiều nhân viên, giúp tính toán chính xác margin và các báo cáo hiệu suất tài chính.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-MGN-003                                  |
| **Tên API**        | Import chi phí nhân viên hàng tháng từ file  |
| **Mô tả**          | API cho phép import chi phí của nhân viên từ file Excel hoặc CSV |
| **Module**         | Quản lý Hiệu suất & Margin                   |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/margins/costs/import`               |
| **Quyền truy cập** | employee-cost:import                          |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `multipart/form-data` |

### 3.2 Form Data Parameters

| Tên         | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-------------|--------------|----------|-------|
| `file`      | File         | Có       | File Excel (.xlsx) hoặc CSV (.csv) chứa dữ liệu chi phí nhân viên |
| `month`     | String       | Có       | Tháng cần import dữ liệu (định dạng: YYYY-MM) |
| `teamId`    | Integer      | Không    | ID của team (nếu là Leader và muốn import cho team cụ thể) |
| `overwrite` | Boolean      | Không    | Có ghi đè dữ liệu đã tồn tại không (mặc định: `false`) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `file`         | - Định dạng phải là .xlsx hoặc .csv<br>- Dung lượng tối đa 5MB<br>- Cấu trúc file phải đúng theo template hệ thống |
| `month`        | - Định dạng: YYYY-MM<br>- Không được là tháng trong tương lai |
| `teamId`       | - Nếu cung cấp, phải là số nguyên dương và tồn tại trong hệ thống<br>- Người dùng phải có quyền quản lý team này |
| `overwrite`    | - Phải là giá trị boolean: `true` hoặc `false` |

### 3.4 Yêu cầu về cấu trúc file

1. **Định dạng cột trong file Excel/CSV**:
   - Cột A (bắt buộc): Mã nhân viên (Employee Code)
   - Cột B (bắt buộc): Tên nhân viên (Employee Name)
   - Cột C (bắt buộc): Chi phí cơ bản (Basic Cost) - VNĐ
   - Cột D (không bắt buộc): Chi phí phụ cấp (Allowance) - VNĐ
   - Cột E (không bắt buộc): Chi phí tăng ca (Overtime) - VNĐ
   - Cột F (không bắt buộc): Chi phí khác (Other Costs) - VNĐ

2. **Dòng đầu tiên phải là tiêu đề các cột**.

3. **Mã nhân viên phải tồn tại** trong hệ thống và thuộc quyền quản lý của người dùng hiện tại.

### 3.5 Phân quyền đặc biệt
- Leader: Chỉ import được chi phí của nhân viên trong team của mình
- Division Manager: Import được chi phí của tất cả nhân viên thuộc bộ phận mình quản lý
- Admin: Import được chi phí của tất cả nhân viên
- Người dùng thông thường không có quyền import chi phí

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa kết quả import chi phí |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `importId` | String | Mã định danh của lần import |
| `month` | String | Tháng import dữ liệu (YYYY-MM) |
| `totalRecords` | Integer | Tổng số bản ghi trong file |
| `successCount` | Integer | Số bản ghi import thành công |
| `errorCount` | Integer | Số bản ghi lỗi |
| `summary` | Object | Thông tin tổng hợp về dữ liệu đã import |
| `errors` | Array | Mảng các lỗi gặp phải khi import |
| `importedBy` | Object | Thông tin người thực hiện import |
| `importedAt` | String | Thời điểm thực hiện import (ISO 8601) |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `teamId` | Integer | ID của team (nếu import cho một team cụ thể) |
| `teamName` | String | Tên team (nếu import cho một team cụ thể) |
| `totalEmployees` | Integer | Số lượng nhân viên đã import thành công |
| `totalCost` | Number | Tổng chi phí đã import (VNĐ) |
| `averageCost` | Number | Chi phí trung bình (VNĐ) |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `rowNumber` | Integer | Số thứ tự dòng trong file gặp lỗi |
| `employeeCode` | String | Mã nhân viên gây lỗi |
| `errorType` | String | Loại lỗi: NOT_FOUND, ACCESS_DENIED, INVALID_FORMAT, etc. |
| `message` | String | Thông báo chi tiết về lỗi |

#### ImportedBy Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng thực hiện import |
| `name` | String | Tên người dùng thực hiện import |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "importId": "IMPORT-20250531-123456",
    "month": "2025-05",
    "totalRecords": 32,
    "successCount": 30,
    "errorCount": 2,
    "summary": {
      "teamId": 1,
      "teamName": "Team Alpha",
      "totalEmployees": 30,
      "totalCost": 750000000,
      "averageCost": 25000000
    },
    "errors": [
      {
        "rowNumber": 12,
        "employeeCode": "NV099",
        "errorType": "NOT_FOUND",
        "message": "Không tìm thấy nhân viên với mã NV099"
      },
      {
        "rowNumber": 25,
        "employeeCode": "NV034",
        "errorType": "ACCESS_DENIED",
        "message": "Bạn không có quyền cập nhật chi phí cho nhân viên này"
      }
    ],
    "importedBy": {
      "id": 5,
      "name": "Nguyễn Văn Leader"
    },
    "importedAt": "2025-05-31T10:15:30Z"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request - Lỗi định dạng file

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E2000 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `field` | String | Tên trường dữ liệu gây lỗi |
| `message` | String | Thông báo chi tiết về lỗi |

```json
{
  "status": "error",
  "code": "E2000",
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "file",
      "message": "Định dạng file không hợp lệ. Chỉ chấp nhận file .xlsx hoặc .csv"
    }
  ]
}
```

#### 400 Bad Request - Lỗi cấu trúc file

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

```json
{
  "status": "error",
  "code": "E2001",
  "message": "Cấu trúc file không hợp lệ",
  "errors": [
    {
      "field": "file",
      "message": "Cột 'Mã nhân viên' bắt buộc nhưng không tìm thấy trong file"
    }
  ]
}
```

#### 401 Unauthorized

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E1001 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E1001",
  "message": "Chưa xác thực hoặc phiên làm việc đã hết hạn"
}
```

#### 403 Forbidden

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E1002 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E1002",
  "message": "Bạn không có quyền import chi phí nhân viên"
}
```

#### 413 Payload Too Large

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E2002 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E2002",
  "message": "File quá lớn. Kích thước tối đa cho phép là 5MB"
}
```

#### 500 Internal Server Error

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E5000 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi import chi phí nhân viên"
}
``` 