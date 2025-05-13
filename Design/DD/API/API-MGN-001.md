# API Details: Lấy dữ liệu margin của nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo tài liệu API lấy dữ liệu margin | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để truy vấn và theo dõi dữ liệu margin của nhân viên, hỗ trợ cho việc quản lý hiệu suất tài chính.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-MGN-001                                  |
| **Tên API**        | Lấy dữ liệu margin của nhân viên             |
| **Mô tả**          | API lấy dữ liệu margin của nhân viên với các bộ lọc |
| **Module**         | Quản lý Hiệu suất & Margin                   |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/margins/employee`                   |
| **Quyền truy cập** | margin:read:all, margin:read:team                                  |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|----------------|------------------|----------|-------|
| `employeeId`   | Integer          | Không    | ID của nhân viên cụ thể cần xem margin, bỏ trống nếu muốn xem nhiều nhân viên |
| `teamId`       | Integer          | Không    | ID của team cần lọc |
| `period`       | String           | Không    | Chu kỳ thời gian: `month`, `quarter`, `year` (mặc định: `month`) |
| `fromDate`     | String           | Không    | Lọc từ ngày (định dạng: YYYY-MM-DD) |
| `toDate`       | String           | Không    | Lọc đến ngày (định dạng: YYYY-MM-DD) |
| `yearMonth`    | String           | Không    | Chỉ lấy một tháng cụ thể (định dạng: YYYY-MM) |
| `yearQuarter`  | String           | Không    | Chỉ lấy một quý cụ thể (định dạng: YYYY-Q1, YYYY-Q2, YYYY-Q3, YYYY-Q4) |
| `year`         | Integer          | Không    | Chỉ lấy một năm cụ thể |
| `status`       | String           | Không    | Lọc theo trạng thái margin: `Red`, `Yellow`, `Green` |
| `sortBy`       | String           | Không    | Trường sắp xếp (mặc định: `margin`) |
| `sortDir`      | String           | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |
| `page`         | Integer          | Không    | Trang cần lấy (mặc định: `1`) |
| `size`         | Integer          | Không    | Số bản ghi mỗi trang (mặc định: `20`) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `employeeId`   | Phải là số nguyên dương và tồn tại trong hệ thống |
| `teamId`       | Phải là số nguyên dương và tồn tại trong hệ thống |
| `period`       | Một trong: `month`, `quarter`, `year` |
| `fromDate`     | Định dạng: YYYY-MM-DD |
| `toDate`       | Định dạng: YYYY-MM-DD, phải sau hoặc bằng fromDate |
| `yearMonth`    | Định dạng: YYYY-MM (VD: 2025-05) |
| `yearQuarter`  | Định dạng: YYYY-Q[1-4] (VD: 2025-Q2) |
| `year`         | Số 4 chữ số (VD: 2025) |
| `status`       | Một trong: `Red`, `Yellow`, `Green` |
| `sortBy`       | Một trong: `name`, `cost`, `revenue`, `margin`, `status` |
| `sortDir`      | Một trong: `asc`, `desc` |
| `page`         | ≥ 1 |
| `size`         | 1 → 100 |

### 3.4 Phân quyền đặc biệt
- Người dùng có quyền `margin:read:team`: Chỉ xem được margin của nhân viên trong team của mình
- Người dùng có quyền `margin:read:department`: Xem được margin của tất cả nhân viên thuộc bộ phận mình quản lý
- Người dùng có quyền `margin:read:all`: Xem được margin của tất cả nhân viên

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu margin và thông tin phân trang |

#### Data Object (khi truy vấn nhiều nhân viên)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `summary` | Object | Thông tin tổng hợp về dữ liệu margin |
| `content` | Array | Mảng các đối tượng nhân viên và margin |
| `pageable` | Object | Thông tin phân trang |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Chu kỳ thời gian: month, quarter, year |
| `periodLabel` | String | Nhãn hiển thị chu kỳ (vd: "Tháng 5/2025") |
| `totalEmployees` | Integer | Tổng số nhân viên |
| `averageCost` | Number | Chi phí trung bình (VNĐ) |
| `averageRevenue` | Number | Doanh thu trung bình (VNĐ) |
| `averageMargin` | Number | Tỷ lệ margin trung bình (%) |
| `statusCounts` | Object | Số lượng nhân viên theo từng trạng thái (Red, Yellow, Green) |

#### Employee Margin Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `status` | String | Trạng thái phân bổ nhân viên |
| `currentProject` | String | Dự án hiện tại nhân viên đang tham gia |
| `allocation` | Integer | Tỷ lệ phân bổ (0-100%) |
| `periods` | Array | Mảng các chu kỳ thời gian có dữ liệu margin |

#### Team Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Period Object (trong mảng periods)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Mã chu kỳ (vd: "2025-05") |
| `periodLabel` | String | Nhãn hiển thị chu kỳ (vd: "Tháng 5/2025") |
| `cost` | Number | Chi phí nhân viên (VNĐ) |
| `revenue` | Number | Doanh thu từ nhân viên (VNĐ) |
| `margin` | Number | Tỷ lệ margin (%) |
| `marginStatus` | String | Trạng thái margin: Red, Yellow, Green |

#### Pageable Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `pageNumber` | Integer | Số trang hiện tại |
| `pageSize` | Integer | Kích thước trang (số bản ghi mỗi trang) |
| `totalPages` | Integer | Tổng số trang |
| `totalElements` | Integer | Tổng số bản ghi |
| `sort` | String | Thông tin sắp xếp (trường,hướng) |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "summary": {
      "period": "month",
      "periodLabel": "Tháng 5/2025",
      "totalEmployees": 45,
      "averageCost": 25000000,
      "averageRevenue": 37500000,
      "averageMargin": 33.33,
      "statusCounts": {
        "Red": 8,
        "Yellow": 12,
        "Green": 25
      }
    },
    "content": [
      {
        "employeeId": 12,
        "employeeCode": "NV012",
        "name": "Hoàng Văn F",
        "position": "Developer",
        "team": {
          "id": 2,
          "name": "Team Beta"
        },
        "status": "Allocated",
        "currentProject": "Dự án ABC",
        "allocation": 100,
        "periods": [
          {
            "period": "2025-05",
            "periodLabel": "Tháng 5/2025",
            "cost": 30000000,
            "revenue": 52500000,
            "margin": 42.86,
            "marginStatus": "Green"
          }
        ]
      },
      {
        "employeeId": 8,
        "employeeCode": "NV008",
        "name": "Lý Thị G",
        "position": "Developer",
        "team": {
          "id": 1,
          "name": "Team Alpha"
        },
        "status": "EndingSoon",
        "currentProject": "Dự án XYZ",
        "allocation": 100,
        "periods": [
          {
            "period": "2025-05",
            "periodLabel": "Tháng 5/2025",
            "cost": 20000000,
            "revenue": 24000000,
            "margin": 16.67,
            "marginStatus": "Red"
          }
        ]
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 2,
      "totalPages": 23,
      "totalElements": 45,
      "sort": "margin,desc"
    }
  }
}
```

### 4.2 Success - 200 OK (Employee Detail)

#### Response Structure (khi truy vấn chi tiết một nhân viên)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu chi tiết margin của nhân viên |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employee` | Object | Thông tin cơ bản của nhân viên |
| `summary` | Object | Thông tin tổng hợp về dữ liệu margin của nhân viên |
| `margins` | Array | Mảng chứa dữ liệu margin theo từng chu kỳ |

#### Employee Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `status` | String | Trạng thái phân bổ nhân viên |
| `currentProject` | String | Dự án hiện tại nhân viên đang tham gia |
| `allocation` | Integer | Tỷ lệ phân bổ (0-100%) |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Chu kỳ thời gian đang xem (month, quarter, year) |
| `periodRange` | String | Phạm vi thời gian (vd: "Tháng 1/2025 - Tháng 5/2025") |
| `averageCost` | Number | Chi phí trung bình (VNĐ) |
| `averageRevenue` | Number | Doanh thu trung bình (VNĐ) |
| `averageMargin` | Number | Tỷ lệ margin trung bình (%) |
| `trend` | String | Xu hướng margin: Increasing, Decreasing, Stable |

#### Margin Object (trong mảng margins)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Mã chu kỳ (vd: "2025-05") |
| `periodLabel` | String | Nhãn hiển thị chu kỳ (vd: "Tháng 5/2025") |
| `basicCost` | Number | Chi phí cơ bản (VNĐ) |
| `allowance` | Number | Chi phí phụ cấp (VNĐ) |
| `overtime` | Number | Chi phí tăng ca (VNĐ) |
| `otherCosts` | Number | Chi phí khác (VNĐ) |
| `totalCost` | Number | Tổng chi phí (VNĐ) |
| `revenue` | Number | Doanh thu (VNĐ) |
| `profit` | Number | Lợi nhuận (VNĐ) |
| `margin` | Number | Tỷ lệ margin (%) |
| `marginStatus` | String | Trạng thái margin: Red, Yellow, Green |
| `billRate` | Number | Giá trị thanh toán theo giờ (VNĐ) |
| `workingDays` | Number | Số ngày làm việc trong chu kỳ |
| `notes` | String | Ghi chú về chi phí/doanh thu |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "employee": {
      "id": 12,
      "employeeCode": "NV012",
      "name": "Hoàng Văn F",
      "position": "Developer",
      "team": {
        "id": 2,
        "name": "Team Beta"
      },
      "status": "Allocated",
      "currentProject": "Dự án ABC",
      "allocation": 100
    },
    "summary": {
      "period": "month",
      "periodRange": "Tháng 1/2025 - Tháng 5/2025",
      "averageCost": 28500000,
      "averageRevenue": 50400000,
      "averageMargin": 43.45,
      "trend": "Increasing"
    },
    "margins": [
      {
        "period": "2025-05",
        "periodLabel": "Tháng 5/2025",
        "basicCost": 25000000,
        "allowance": 2000000,
        "overtime": 0,
        "otherCosts": 3000000,
        "totalCost": 30000000,
        "revenue": 52500000,
        "profit": 22500000,
        "margin": 42.86,
        "marginStatus": "Green",
        "billRate": 350000,
        "workingDays": 20,
        "notes": "Dự án ABC - Full-time"
      },
      {
        "period": "2025-04",
        "periodLabel": "Tháng 4/2025",
        "basicCost": 25000000,
        "allowance": 2000000,
        "overtime": 0,
        "otherCosts": 2500000,
        "totalCost": 29500000,
        "revenue": 52500000,
        "profit": 23000000,
        "margin": 43.81,
        "marginStatus": "Green",
        "billRate": 350000,
        "workingDays": 21,
        "notes": "Dự án ABC - Full-time"
      },
      {
        "period": "2025-03",
        "periodLabel": "Tháng 3/2025",
        "basicCost": 25000000,
        "allowance": 2000000,
        "overtime": 0,
        "otherCosts": 2000000,
        "totalCost": 29000000,
        "revenue": 50400000,
        "profit": 21400000,
        "margin": 42.46,
        "marginStatus": "Green",
        "billRate": 350000,
        "workingDays": 18,
        "notes": "Dự án ABC - Full-time"
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
      "field": "yearMonth",
      "message": "Định dạng tháng không hợp lệ. Yêu cầu định dạng YYYY-MM"
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
  "message": "Bạn không có quyền xem dữ liệu margin của nhân viên này"
}
```

#### 404 Not Found

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3000 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy nhân viên với ID: 999"
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
  "message": "Lỗi hệ thống khi lấy dữ liệu margin của nhân viên"
}
``` 