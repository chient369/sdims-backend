# API Details: Nhập chi phí thủ công cho nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API nhập chi phí thủ công cho nhân viên | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để nhập thủ công hoặc cập nhật chi phí của một hoặc nhiều nhân viên trong hệ thống, cho phép người quản lý cập nhật chi phí cơ bản, phụ cấp, chi phí tăng ca và các chi phí khác của nhân viên, giúp tính toán chính xác margin và hiệu suất kinh doanh.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-MGN-004                                  |
| **Tên API**        | Nhập chi phí thủ công cho nhân viên          |
| **Mô tả**          | API cho phép nhập thủ công hoặc cập nhật chi phí của một hoặc nhiều nhân viên |
| **Module**         | Quản lý Hiệu suất & Margin                   |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/margins/costs`                      |
| **Quyền truy cập** | employee-cost:update:all                           |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

```json
{
  "month": "2025-05",
  "overwrite": false,
  "employees": [
    {
      "employeeId": 12,
      "employeeCode": "NV012",
      "basicCost": 25000000,
      "allowance": 2000000,
      "overtime": 0,
      "otherCosts": 500000,
      "note": "Điều chỉnh phụ cấp tháng 5"
    },
    {
      "employeeId": 15,
      "employeeCode": "NV015",
      "basicCost": 20000000,
      "allowance": 1500000,
      "overtime": 1000000,
      "otherCosts": 0,
      "note": "Tăng ca dự án XYZ"
    }
  ]
}
```

### 3.3 Body Parameters

| Tên                      | Kiểu dữ liệu | Bắt buộc | Mô tả |
|--------------------------|--------------|----------|-------|
| `month`                  | String       | Có       | Tháng cần cập nhật chi phí (định dạng: YYYY-MM) |
| `overwrite`              | Boolean      | Không    | Có ghi đè dữ liệu đã tồn tại không (mặc định: `false`) |
| `employees`              | Array        | Có       | Mảng thông tin chi phí của nhân viên |
| `employees[].employeeId` | Integer      | Có*      | ID của nhân viên (*Có thể bỏ qua nếu cung cấp employeeCode) |
| `employees[].employeeCode` | String     | Có*      | Mã nhân viên (*Có thể bỏ qua nếu cung cấp employeeId) |
| `employees[].basicCost`  | Number       | Có       | Chi phí cơ bản (VNĐ) |
| `employees[].allowance`  | Number       | Không    | Chi phí phụ cấp (VNĐ) |
| `employees[].overtime`   | Number       | Không    | Chi phí tăng ca (VNĐ) |
| `employees[].otherCosts` | Number       | Không    | Chi phí khác (VNĐ) |
| `employees[].note`       | String       | Không    | Ghi chú về chi phí |

### 3.4 Validate Rule

| Trường                   | Điều kiện hợp lệ |
|--------------------------|------------------|
| `month`                  | - Định dạng: YYYY-MM<br>- Không được là tháng trong tương lai |
| `overwrite`              | - Phải là giá trị boolean: `true` hoặc `false` |
| `employees`              | - Mảng không được rỗng<br>- Tối đa 50 nhân viên trong một request |
| `employees[].employeeId`/`employeeCode` | - Phải cung cấp ít nhất một trong hai trường<br>- Phải tồn tại trong hệ thống<br>- Người dùng phải có quyền quản lý nhân viên này |
| `employees[].basicCost`  | - Phải là số không âm<br>- Tối đa 1.000.000.000 VND |
| `employees[].allowance`  | - Phải là số không âm<br>- Tối đa 100.000.000 VND |
| `employees[].overtime`   | - Phải là số không âm<br>- Tối đa 100.000.000 VND |
| `employees[].otherCosts` | - Phải là số không âm<br>- Tối đa 100.000.000 VND |
| `employees[].note`       | - Tối đa 255 ký tự |

### 3.5 Phân quyền đặc biệt
- Leader: Chỉ cập nhật được chi phí của nhân viên trong team của mình
- Division Manager: Cập nhật được chi phí của tất cả nhân viên thuộc bộ phận mình quản lý
- Admin: Cập nhật được chi phí của tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa kết quả cập nhật chi phí nhân viên |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `month` | String | Tháng đã cập nhật chi phí (YYYY-MM) |
| `totalEmployees` | Integer | Tổng số nhân viên trong request |
| `successCount` | Integer | Số nhân viên cập nhật thành công |
| `errorCount` | Integer | Số nhân viên cập nhật thất bại |
| `results` | Array | Mảng kết quả cập nhật cho từng nhân viên thành công |
| `errors` | Array | Mảng thông tin lỗi khi cập nhật nhân viên thất bại |

#### Employee Result Object (trong mảng results)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `totalCost` | Number | Tổng chi phí của nhân viên (VNĐ) |
| `status` | String | Trạng thái cập nhật: "created" (tạo mới) hoặc "updated" (cập nhật) |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên gây lỗi (có thể null) |
| `employeeCode` | String | Mã nhân viên gây lỗi (có thể null) |
| `errorType` | String | Loại lỗi: NOT_FOUND, ACCESS_DENIED, INVALID_FORMAT, etc. |
| `message` | String | Thông báo chi tiết về lỗi |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "month": "2025-05",
    "totalEmployees": 2,
    "successCount": 2,
    "errorCount": 0,
    "results": [
      {
        "employeeId": 12,
        "employeeCode": "NV012",
        "name": "Hoàng Văn F",
        "totalCost": 27500000,
        "status": "updated"
      },
      {
        "employeeId": 15,
        "employeeCode": "NV015",
        "name": "Nguyễn Thị H",
        "totalCost": 22500000,
        "status": "created"
      }
    ],
    "errors": []
  }
}
```

### 4.2 Partial Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "partial_success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa kết quả cập nhật chi phí nhân viên |

```json
{
  "status": "partial_success",
  "code": 200,
  "data": {
    "month": "2025-05",
    "totalEmployees": 2,
    "successCount": 1,
    "errorCount": 1,
    "results": [
      {
        "employeeId": 12,
        "employeeCode": "NV012",
        "name": "Hoàng Văn F",
        "totalCost": 27500000,
        "status": "updated"
      }
    ],
    "errors": [
      {
        "employeeId": null,
        "employeeCode": "NV099",
        "errorType": "NOT_FOUND",
        "message": "Không tìm thấy nhân viên với mã NV099"
      }
    ]
  }
}
```

### 4.3 Error Responses

#### 400 Bad Request

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
      "field": "month",
      "message": "Định dạng tháng không hợp lệ. Yêu cầu định dạng YYYY-MM"
    },
    {
      "field": "employees",
      "message": "Danh sách nhân viên không được để trống"
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
  "message": "Bạn không có quyền thực hiện chức năng này"
}
```

#### 409 Conflict

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3005 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên gây lỗi |
| `employeeCode` | String | Mã nhân viên gây lỗi |
| `message` | String | Thông báo chi tiết về lỗi |

```json
{
  "status": "error",
  "code": "E3005",
  "message": "Dữ liệu chi phí đã tồn tại",
  "errors": [
    {
      "employeeId": 12,
      "employeeCode": "NV012",
      "message": "Chi phí của nhân viên này đã tồn tại cho tháng 2025-05. Sử dụng tham số 'overwrite=true' để ghi đè."
    }
  ]
}
``` 