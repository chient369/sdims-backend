# API Details: Báo cáo chi tiết danh sách hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API báo cáo chi tiết danh sách hợp đồng | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để tạo báo cáo chi tiết về danh sách hợp đồng và tình trạng thực hiện, cho phép người dùng lọc và truy vấn thông tin hợp đồng theo nhiều tiêu chí khác nhau, hỗ trợ việc phân tích doanh thu, quản lý trạng thái thanh toán và theo dõi hiệu quả kinh doanh từ các hợp đồng.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-005                                  |
| **Tên API**        | Báo cáo chi tiết danh sách hợp đồng           |
| **Mô tả**          | API cung cấp báo cáo chi tiết về danh sách hợp đồng và tình trạng thực hiện |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/reports/contract-list`              |
| **Quyền truy cập** | report:read:all, report:read:team, report:read:own |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên                | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|--------------------|----------------------|----------|-------|
| `customerId`       | Integer              | Không    | ID của khách hàng cần lọc |
| `salesId`          | Integer              | Không    | ID của nhân viên Sales phụ trách |
| `status`           | String               | Không    | Trạng thái hợp đồng: `New`, `InProgress`, `Paused`, `Completed`, `Cancelled` |
| `type`             | String               | Không    | Loại hợp đồng: `FixedPrice`, `TimeAndMaterial` |
| `opportunityId`    | Integer              | Không    | ID của cơ hội liên kết |
| `minValue`         | Double               | Không    | Giá trị hợp đồng tối thiểu |
| `maxValue`         | Double               | Không    | Giá trị hợp đồng tối đa |
| `fromDate`         | Date (yyyy-MM-dd)    | Không    | Ngày ký hợp đồng từ (mặc định: 1 năm trước) |
| `toDate`           | Date (yyyy-MM-dd)    | Không    | Ngày ký hợp đồng đến (mặc định: hiện tại) |
| `expiryFromDate`   | Date (yyyy-MM-dd)    | Không    | Ngày hết hạn từ |
| `expiryToDate`     | Date (yyyy-MM-dd)    | Không    | Ngày hết hạn đến |
| `paymentStatus`    | String               | Không    | Trạng thái thanh toán: `Pending`, `PartiallyPaid`, `FullyPaid`, `Overdue` |
| `keyword`          | String               | Không    | Tìm kiếm theo tên hợp đồng hoặc mã |
| `includePayments`  | Boolean              | Không    | Bao gồm thông tin thanh toán trong kết quả (mặc định: `true`) |
| `includeEmployees` | Boolean              | Không    | Bao gồm thông tin nhân viên được gán (mặc định: `true`) |
| `exportType`       | String               | Không    | Loại xuất báo cáo: `json`, `csv`, `excel` (mặc định: `json`) |
| `page`             | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`             | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `50`) |
| `sortBy`           | String               | Không    | Trường sắp xếp (mặc định: `signedDate`) |
| `sortDir`          | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |


### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 500          |
| `sortDir`         | `asc`, `desc`    |
| `status`          | Một trong: `New`, `InProgress`, `Paused`, `Completed`, `Cancelled` |
| `type`            | Một trong: `FixedPrice`, `TimeAndMaterial` |
| `paymentStatus`   | Một trong: `Pending`, `PartiallyPaid`, `FullyPaid`, `Overdue` |
| `exportType`      | Một trong: `json`, `csv`, `excel` |
| `fromDate`        | Định dạng yyyy-MM-dd, ≤ toDate |
| `toDate`          | Định dạng yyyy-MM-dd, ≥ fromDate |
| `expiryFromDate`  | Định dạng yyyy-MM-dd, ≤ expiryToDate |
| `expiryToDate`    | Định dạng yyyy-MM-dd, ≥ expiryFromDate |
| `minValue`        | ≥ 0, ≤ maxValue (nếu có) |
| `maxValue`        | ≥ 0, ≥ minValue (nếu có) |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được báo cáo hợp đồng có nhân viên thuộc team mình quản lý
- Sales: Chỉ xem được báo cáo của các hợp đồng do mình phụ trách
- Division Manager: Xem được báo cáo của tất cả hợp đồng thuộc bộ phận mình quản lý
- Kế toán: Xem được báo cáo của tất cả hợp đồng
- Admin: Xem được báo cáo của tất cả hợp đồng

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu báo cáo danh sách hợp đồng |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportInfo` | Object | Thông tin tổng quan về báo cáo |
| `summaryMetrics` | Object | Các chỉ số tổng hợp về hợp đồng |
| `content` | Array | Mảng các đối tượng hợp đồng |
| `pageable` | Object | Thông tin phân trang |

#### ReportInfo Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportName` | String | Tên báo cáo |
| `generatedAt` | String | Thời điểm tạo báo cáo (ISO 8601) |
| `fromDate` | String | Ngày bắt đầu kỳ báo cáo (yyyy-MM-dd) |
| `toDate` | String | Ngày kết thúc kỳ báo cáo (yyyy-MM-dd) |
| `filters` | Object | Các bộ lọc đã áp dụng |

#### SummaryMetrics Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalContracts` | Integer | Tổng số hợp đồng |
| `byStatus` | Object | Phân loại theo trạng thái hợp đồng |
| `byType` | Object | Phân loại theo loại hợp đồng |
| `byPaymentStatus` | Object | Phân loại theo trạng thái thanh toán |
| `totalValue` | Long | Tổng giá trị hợp đồng (VND) |
| `totalPaid` | Long | Tổng số tiền đã thanh toán (VND) |
| `totalPending` | Long | Tổng số tiền chưa thanh toán (VND) |
| `byCustomer` | Array | Phân loại hợp đồng theo khách hàng |
| `bySales` | Array | Phân loại hợp đồng theo nhân viên sales |

#### ByStatus Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `New` | Integer | Số hợp đồng mới |
| `InProgress` | Integer | Số hợp đồng đang thực hiện |
| `Paused` | Integer | Số hợp đồng tạm dừng |
| `Completed` | Integer | Số hợp đồng đã hoàn thành |
| `Cancelled` | Integer | Số hợp đồng đã hủy |

#### ByType Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `FixedPrice` | Integer | Số hợp đồng trọn gói |
| `TimeAndMaterial` | Integer | Số hợp đồng theo thời gian và vật liệu |

#### ByPaymentStatus Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `Pending` | Integer | Số hợp đồng chưa thanh toán |
| `PartiallyPaid` | Integer | Số hợp đồng đã thanh toán một phần |
| `FullyPaid` | Integer | Số hợp đồng đã thanh toán đầy đủ |
| `Overdue` | Integer | Số hợp đồng quá hạn thanh toán |

#### CustomerSummary Object (trong mảng byCustomer)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên khách hàng |
| `count` | Integer | Số lượng hợp đồng của khách hàng |
| `value` | Long | Tổng giá trị hợp đồng của khách hàng (VND) |

#### SalesSummary Object (trong mảng bySales)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên nhân viên sales |
| `count` | Integer | Số lượng hợp đồng do nhân viên phụ trách |
| `value` | Long | Tổng giá trị hợp đồng do nhân viên phụ trách (VND) |

#### Contract Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng |
| `code` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `customer` | Object | Thông tin khách hàng |
| `opportunity` | Object | Thông tin cơ hội liên kết |
| `type` | String | Loại hợp đồng (FixedPrice, TimeAndMaterial) |
| `value` | Long | Giá trị hợp đồng (VND) |
| `status` | String | Trạng thái hợp đồng |
| `signedDate` | String | Ngày ký hợp đồng (yyyy-MM-dd) |
| `effectiveDate` | String | Ngày hiệu lực (yyyy-MM-dd) |
| `expiryDate` | String | Ngày hết hạn (yyyy-MM-dd) |
| `sales` | Object | Thông tin nhân viên sales phụ trách |
| `paymentTerms` | Array | Danh sách các đợt thanh toán |
| `paymentSummary` | Object | Tóm tắt tình trạng thanh toán |
| `employees` | Array | Danh sách nhân viên được gán vào hợp đồng |

#### Customer Object (trong Contract)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của khách hàng |
| `name` | String | Tên khách hàng |
| `industry` | String | Ngành nghề khách hàng |

#### Opportunity Object (trong Contract)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội |
| `name` | String | Tên cơ hội |

#### Sales Object (trong Contract)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên sales |
| `name` | String | Tên nhân viên sales |
| `email` | String | Email của nhân viên sales |

#### PaymentTerm Object (trong mảng paymentTerms)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của đợt thanh toán |
| `description` | String | Mô tả đợt thanh toán |
| `amount` | Long | Số tiền thanh toán (VND) |
| `dueDate` | String | Ngày đến hạn (yyyy-MM-dd) |
| `actualPaidDate` | String | Ngày thực tế thanh toán (yyyy-MM-dd) |
| `status` | String | Trạng thái thanh toán (Paid, Pending, Overdue) |

#### PaymentSummary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalAmount` | Long | Tổng giá trị hợp đồng (VND) |
| `paidAmount` | Long | Số tiền đã thanh toán (VND) |
| `pendingAmount` | Long | Số tiền chưa thanh toán (VND) |
| `percentPaid` | Double | Phần trăm đã thanh toán (%) |
| `status` | String | Trạng thái thanh toán tổng hợp |

#### Employee Object (trong mảng employees)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `name` | String | Tên nhân viên |
| `position` | String | Vị trí công việc |
| `allocation` | Integer | Tỷ lệ phân bổ vào hợp đồng (%) |

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
    "reportInfo": {
      "reportName": "Báo cáo danh sách hợp đồng",
      "generatedAt": "2025-05-01T11:45:30Z",
      "fromDate": "2024-05-01",
      "toDate": "2025-04-30",
      "filters": {
        "status": "InProgress",
        "includePayments": true
      }
    },
    "summaryMetrics": {
      "totalContracts": 85,
      "byStatus": {
        "New": 15,
        "InProgress": 45,
        "Paused": 5,
        "Completed": 15,
        "Cancelled": 5
      },
      "byType": {
        "FixedPrice": 35,
        "TimeAndMaterial": 50
      },
      "byPaymentStatus": {
        "Pending": 20,
        "PartiallyPaid": 40,
        "FullyPaid": 20,
        "Overdue": 5
      },
      "totalValue": 12500000000,
      "totalPaid": 7500000000,
      "totalPending": 5000000000,
      "byCustomer": [
        {"name": "ABC Corporation", "count": 10, "value": 2500000000},
        {"name": "XYZ Inc", "count": 8, "value": 2000000000},
        {"name": "DEF Limited", "count": 6, "value": 1800000000}
      ],
      "bySales": [
        {"name": "Nguyễn Văn X", "count": 25, "value": 5000000000},
        {"name": "Trần Thị Y", "count": 20, "value": 4000000000},
        {"name": "Lê Anh Z", "count": 15, "value": 3500000000}
      ]
    },
    "content": [
      {
        "id": 101,
        "code": "HD-2025-001",
        "name": "Phát triển phần mềm quản lý nhân sự",
        "customer": {
          "id": 15,
          "name": "ABC Corporation",
          "industry": "Manufacturing"
        },
        "opportunity": {
          "id": 50,
          "name": "ABC Corp - Hệ thống quản lý nhân sự"
        },
        "type": "FixedPrice",
        "value": 500000000,
        "status": "InProgress",
        "signedDate": "2025-01-15",
        "effectiveDate": "2025-01-20",
        "expiryDate": "2025-12-31",
        "sales": {
          "id": 20,
          "name": "Nguyễn Văn X",
          "email": "x.nguyenvan@company.com"
        },
        "paymentTerms": [
          {
            "id": 201,
            "description": "Thanh toán đợt 1 (30%)",
            "amount": 150000000,
            "dueDate": "2025-02-15",
            "actualPaidDate": "2025-02-10",
            "status": "Paid"
          },
          {
            "id": 202,
            "description": "Thanh toán đợt 2 (30%)",
            "amount": 150000000,
            "dueDate": "2025-06-15",
            "actualPaidDate": "2025-06-20",
            "status": "Paid"
          },
          {
            "id": 203,
            "description": "Thanh toán đợt 3 (40%)",
            "amount": 200000000,
            "dueDate": "2025-12-15",
            "actualPaidDate": null,
            "status": "Pending"
          }
        ],
        "paymentSummary": {
          "totalAmount": 500000000,
          "paidAmount": 300000000,
          "pendingAmount": 200000000,
          "percentPaid": 60,
          "status": "PartiallyPaid"
        },
        "employees": [
          {
            "id": 1,
            "name": "Nguyễn Văn A",
            "position": "Developer",
            "allocation": 100
          },
          {
            "id": 2,
            "name": "Lê Thị C",
            "position": "Developer",
            "allocation": 100
          },
          {
            "id": 5,
            "name": "Trần Văn B",
            "position": "Leader",
            "allocation": 50
          }
        ]
      },
      {
        "id": 102,
        "code": "HD-2025-002",
        "name": "Bảo trì hệ thống kế toán",
        "customer": {
          "id": 16,
          "name": "XYZ Inc",
          "industry": "Finance"
        },
        "opportunity": {
          "id": 51,
          "name": "XYZ Inc - Bảo trì kế toán 2025"
        },
        "type": "TimeAndMaterial",
        "value": 320000000,
        "status": "InProgress",
        "signedDate": "2025-01-30",
        "effectiveDate": "2025-02-01",
        "expiryDate": "2026-01-31",
        "sales": {
          "id": 21,
          "name": "Trần Thị Y",
          "email": "y.tranthi@company.com"
        },
        "paymentTerms": [
          {
            "id": 205,
            "description": "Thanh toán tháng 2/2025",
            "amount": 80000000,
            "dueDate": "2025-03-15",
            "actualPaidDate": "2025-03-12",
            "status": "Paid"
          },
          {
            "id": 206,
            "description": "Thanh toán tháng 3/2025",
            "amount": 80000000,
            "dueDate": "2025-04-15",
            "actualPaidDate": "2025-04-18",
            "status": "Paid"
          },
          {
            "id": 207,
            "description": "Thanh toán tháng 4/2025",
            "amount": 80000000,
            "dueDate": "2025-05-15",
            "actualPaidDate": null,
            "status": "Pending"
          },
          {
            "id": 208,
            "description": "Thanh toán tháng 5/2025",
            "amount": 80000000,
            "dueDate": "2025-06-15",
            "actualPaidDate": null,
            "status": "Pending"
          }
        ],
        "paymentSummary": {
          "totalAmount": 320000000,
          "paidAmount": 160000000,
          "pendingAmount": 160000000,
          "percentPaid": 50,
          "status": "PartiallyPaid"
        },
        "employees": [
          {
            "id": 8,
            "name": "Phạm Văn D",
            "position": "Developer",
            "allocation": 50
          },
          {
            "id": 10,
            "name": "Hoàng Thị E",
            "position": "Tester",
            "allocation": 30
          }
        ]
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 2,
      "totalElements": 85,
      "sort": "signedDate,desc"
    }
  }
}
```

#### 4.1.1 Response khi exportType=excel hoặc csv - 200 OK

```
Content-Disposition: attachment; filename="contract_report_20250501.xlsx"
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

[Binary Excel File Content]
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
      "field": "status",
      "message": "Giá trị 'Pending' không hợp lệ. Các giá trị hợp lệ: New, InProgress, Paused, Completed, Cancelled"
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
  "message": "Bạn không có quyền xem báo cáo hợp đồng này"
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
      "field": "customerId",
      "message": "Không tìm thấy khách hàng với ID: 999"
    }
  ]
}
``` 