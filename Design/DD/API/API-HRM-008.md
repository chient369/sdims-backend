# API Details: Export danh sách nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2025-05-10 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép người dùng xuất danh sách nhân viên ra file Excel hoặc CSV với các tùy chọn lọc và định dạng linh hoạt, phục vụ mục đích báo cáo và phân tích dữ liệu ngoại tuyến.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-008                                  |
| **Tên API**        | Export danh sách nhân viên                   |
| **Mô tả**          | API cho phép export danh sách nhân viên ra file Excel/CSV |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/employees/export`                   |
| **Quyền truy cập** | employee:export                              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu        | Bắt buộc | Mô tả |
|----------------|---------------------|----------|-------|
| `format`       | String              | Không    | Định dạng file xuất: `xlsx` hoặc `csv` (mặc định: `xlsx`) |
| `keyword`      | String              | Không    | Tìm theo tên hoặc mã nhân viên |
| `teamId`       | Integer             | Không    | ID của team cần lọc |
| `position`     | String              | Không    | Vị trí công việc (Developer, Tester, BA, ...) |
| `status`       | String              | Không    | Trạng thái: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `skills`       | Array of Integer    | Không    | Danh sách ID kỹ năng cần lọc |
| `minExperience`| Integer             | Không    | Số năm kinh nghiệm tối thiểu |
| `fields`       | Array of String     | Không    | Danh sách các trường thông tin cần xuất, mặc định là xuất tất cả |
| `include_skills`| Boolean            | Không    | Có xuất kỹ năng của nhân viên không (mặc định: `false`) |
| `include_history`| Boolean           | Không    | Có xuất lịch sử tham gia dự án không (mặc định: `false`) |
| `filename`     | String              | Không    | Tên file khi tải về (không cần đuôi) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `format`       | Một trong: `xlsx`, `csv` |
| `teamId`       | Số nguyên dương |
| `status`       | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `fields`       | Các giá trị hợp lệ: `id`, `employeeCode`, `name`, `email`, `phone`, `address`, `birthDate`, `joinDate`, `position`, `team`, `status`, `currentProject`, `utilization`, `endDate` |

### 3.4 Phân quyền đặc biệt
- employee:export:team - Chỉ export được nhân viên trong team của mình
- employee:export:department - Export được tất cả nhân viên thuộc bộ phận mình quản lý
- employee:export - Export được tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin về file được tạo |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `fileUrl` | String | URL tạm thời để tải file (có hiệu lực trong 15 phút) |
| `fileName` | String | Tên file đã được tạo |
| `fileSize` | Integer | Kích thước file (bytes) |
| `fileType` | String | Loại file (`xlsx` hoặc `csv`) |
| `recordCount` | Integer | Số bản ghi được xuất ra file |
| `expiresAt` | String | Thời gian hết hạn của liên kết tải (ISO 8601) |

Trả về file Excel (.xlsx) hoặc CSV (.csv) chứa danh sách nhân viên.

Headers:
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (cho .xlsx)
Content-Type: text/csv (cho .csv)
Content-Disposition: attachment; filename="employees_export_20250501.xlsx"
```

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "fileUrl": "https://example.com/download/temp/employees_export_20250501.xlsx",
    "fileName": "employees_export_20250501.xlsx",
    "fileSize": 24580,
    "fileType": "xlsx",
    "recordCount": 45,
    "expiresAt": "2025-05-01T15:15:00Z"
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
      "field": "format",
      "message": "Định dạng không hợp lệ. Chỉ hỗ trợ 'xlsx' và 'csv'"
    }
  ]
}
```

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1000",
  "message": "Token không hợp lệ hoặc đã hết hạn"
}
```

#### 403 Forbidden
```json
{
  "status": "error",
  "code": "E1002",
  "message": "Không có quyền truy cập chức năng này"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E7003",
  "message": "Lỗi tạo file export",
  "traceId": "abc-xyz-123"
}
``` 