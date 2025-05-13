# API Details: Import danh sách nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép người dùng import danh sách nhân viên từ file Excel hoặc CSV, hỗ trợ việc thêm nhiều nhân viên mới một cách nhanh chóng hoặc cập nhật thông tin hàng loạt cho các nhân viên đã tồn tại.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-007                                  |
| **Tên API**        | Import danh sách nhân viên                   |
| **Mô tả**          | API cho phép import danh sách nhân viên từ file Excel/CSV |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/employees/import`                   |
| **Quyền truy cập** | employee:import                              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `multipart/form-data` |

### 3.2 Form Data

| Tên               | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-------------------|--------------|----------|-------|
| `file`            | File         | Có       | File Excel (.xlsx) hoặc CSV (.csv) chứa dữ liệu nhân viên |
| `skip_validation` | Boolean      | Không    | Nếu `true`, bỏ qua kiểm tra dữ liệu, thực hiện import ngay (mặc định: `false`) |
| `update_existing` | Boolean      | Không    | Nếu `true`, cập nhật thông tin nhân viên đã tồn tại (dựa trên mã NV), nếu `false`, bỏ qua những nhân viên đã tồn tại (mặc định: `true`) |

### 3.3 File Format

File import phải có các cột sau:

| Tên cột          | Bắt buộc | Mô tả |
|------------------|----------|-------|
| `EmployeeCode`   | Có       | Mã nhân viên |
| `Name`           | Có       | Họ tên nhân viên |
| `Email`          | Có       | Email công ty |
| `Position`       | Có       | Vị trí công việc |
| `TeamName`       | Có       | Tên team (hệ thống sẽ ánh xạ đến TeamID tương ứng) |
| `Phone`          | Không    | Số điện thoại |
| `Address`        | Không    | Địa chỉ |
| `BirthDate`      | Không    | Ngày sinh (định dạng: YYYY-MM-DD) |
| `JoinDate`       | Có       | Ngày vào công ty (định dạng: YYYY-MM-DD) |
| `Status`         | Có       | Trạng thái nhân viên |
| `EmergencyName`  | Không    | Tên người liên hệ khẩn cấp |
| `EmergencyPhone` | Không    | Số điện thoại người liên hệ khẩn cấp |
| `EmergencyRelation` | Không | Mối quan hệ với người liên hệ khẩn cấp |

### 3.4 Validate Rule

| Trường        | Điều kiện hợp lệ |
|---------------|------------------|
| `file`        | Kích thước tối đa: 10MB, Định dạng: .xlsx, .csv |
| `EmployeeCode`| Độ dài: 3-20 ký tự, Chỉ chứa chữ cái, số và gạch dưới, Không được trùng lặp (trừ khi `update_existing=true`) |
| `Email`       | Định dạng email hợp lệ, Không được trùng lặp (trừ khi `update_existing=true`) |
| `BirthDate`   | Định dạng ngày tháng hợp lệ (YYYY-MM-DD), nhân viên phải trên 18 tuổi |
| `JoinDate`    | Định dạng ngày tháng hợp lệ (YYYY-MM-DD), không được sau ngày hiện tại |
| `Status`      | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `TeamName`    | Phải tồn tại trong hệ thống |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Import danh sách nhân viên thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về kết quả import |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `total` | Integer | Tổng số bản ghi trong file import |
| `success` | Integer | Số bản ghi được import thành công |
| `failed` | Integer | Số bản ghi import thất bại |
| `created` | Integer | Số nhân viên mới được tạo |
| `updated` | Integer | Số nhân viên đã được cập nhật |
| `skipped` | Integer | Số bản ghi bị bỏ qua |
| `errors` | Array | Mảng chứa thông tin lỗi cho các bản ghi import thất bại |
| `created_employees` | Array | Mảng chứa thông tin cơ bản về nhân viên mới được tạo |

#### Error Object (trong mảng errors)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `row` | Integer | Số thứ tự hàng trong file excel/csv (bắt đầu từ 1) |
| `employeeCode` | String | Mã nhân viên trong bản ghi lỗi |
| `errors` | Array | Mảng các lỗi cụ thể cho bản ghi này |

#### Error Detail Object (trong mảng errors của Error Object)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `field` | String | Tên trường dữ liệu gặp lỗi |
| `message` | String | Thông báo lỗi chi tiết |

#### Employee Summary Object (trong mảng created_employees)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên mới được tạo |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên nhân viên |

```json
{
  "status": "success",
  "code": 200,
  "message": "Import danh sách nhân viên thành công",
  "data": {
    "total": 10,
    "success": 8,
    "failed": 2,
    "created": 5,
    "updated": 3,
    "skipped": 2,
    "errors": [
      {
        "row": 3,
        "employeeCode": "NV011",
        "errors": [
          {
            "field": "Email",
            "message": "Email đã tồn tại trong hệ thống"
          }
        ]
      },
      {
        "row": 8,
        "employeeCode": "NV016",
        "errors": [
          {
            "field": "TeamName",
            "message": "Team 'ABC' không tồn tại trong hệ thống"
          }
        ]
      }
    ],
    "created_employees": [
      {
        "id": 46,
        "employeeCode": "NV046",
        "name": "Lê Văn C"
      },
      {
        "id": 47,
        "employeeCode": "NV047",
        "name": "Trần Thị D"
      },
      {
        "id": 48,
        "employeeCode": "NV048",
        "name": "Nguyễn Văn E"
      },
      {
        "id": 49,
        "employeeCode": "NV049",
        "name": "Phạm Thị F"
      },
      {
        "id": 50,
        "employeeCode": "NV050",
        "name": "Hoàng Văn G"
      }
    ]
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request (Invalid File)
```json
{
  "status": "error",
  "code": "E7000",
  "message": "File import không hợp lệ",
  "errors": [
    {
      "field": "file",
      "message": "Định dạng file không được hỗ trợ. Chỉ hỗ trợ .xlsx và .csv"
    }
  ]
}
```

#### 400 Bad Request (Data Validation)
```json
{
  "status": "error",
  "code": "E7001",
  "message": "Dữ liệu trong file import không hợp lệ",
  "errors": [
    {
      "row": 2,
      "employeeCode": "NV010",
      "errors": [
        {
          "field": "JoinDate",
          "message": "Ngày vào công ty không được sau ngày hiện tại"
        }
      ]
    },
    {
      "row": 5,
      "employeeCode": "NV013",
      "errors": [
        {
          "field": "Email",
          "message": "Email không đúng định dạng"
        },
        {
          "field": "Status",
          "message": "Trạng thái không hợp lệ. Phải là một trong: Allocated, Available, EndingSoon, OnLeave, Resigned"
        }
      ]
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
  "code": "E7002",
  "message": "Lỗi xử lý file import",
  "traceId": "abc-xyz-123"
}
```