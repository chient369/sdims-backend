# API Details: Báo cáo chi tiết tình trạng thanh toán/công nợ

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API báo cáo chi tiết tình trạng thanh toán/công nợ | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để tạo báo cáo chi tiết về tình trạng thanh toán và công nợ của các hợp đồng, giúp người dùng theo dõi các khoản thanh toán đã nhận, đang chờ và quá hạn, hỗ trợ việc quản lý dòng tiền và dự báo tài chính cho doanh nghiệp.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-006                                  |
| **Tên API**        | Báo cáo chi tiết tình trạng thanh toán/công nợ |
| **Mô tả**          | API cung cấp báo cáo chi tiết về tình trạng thanh toán và công nợ của các hợp đồng |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/reports/payment-status`             |
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
| `contractId`       | Integer              | Không    | ID của hợp đồng cần lọc |
| `status`           | String               | Không    | Trạng thái thanh toán: `Pending`, `Paid`, `Overdue`, `UpcomingDue` |
| `fromDate`         | Date (yyyy-MM-dd)    | Không    | Từ ngày đến hạn (mặc định: 6 tháng trước) |
| `toDate`           | Date (yyyy-MM-dd)    | Không    | Đến ngày đến hạn (mặc định: 6 tháng sau) |
| `paidFromDate`     | Date (yyyy-MM-dd)    | Không    | Từ ngày thanh toán thực tế |
| `paidToDate`       | Date (yyyy-MM-dd)    | Không    | Đến ngày thanh toán thực tế |
| `minAmount`        | Double               | Không    | Giá trị tối thiểu |
| `maxAmount`        | Double               | Không    | Giá trị tối đa |
| `includeDetails`   | Boolean              | Không    | Bao gồm chi tiết hợp đồng (mặc định: `true`) |
| `exportType`       | String               | Không    | Loại xuất báo cáo: `json`, `csv`, `excel` (mặc định: `json`) |
| `page`             | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`             | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `50`) |
| `sortBy`           | String               | Không    | Trường sắp xếp (mặc định: `dueDate`) |
| `sortDir`          | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `asc`) |

### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 500          |
| `sortDir`         | `asc`, `desc`    |
| `status`          | Một trong: `Pending`, `Paid`, `Overdue`, `UpcomingDue` |
| `exportType`      | Một trong: `json`, `csv`, `excel` |
| `fromDate`        | Định dạng yyyy-MM-dd, ≤ toDate |
| `toDate`          | Định dạng yyyy-MM-dd, ≥ fromDate |
| `paidFromDate`    | Định dạng yyyy-MM-dd, ≤ paidToDate |
| `paidToDate`      | Định dạng yyyy-MM-dd, ≥ paidFromDate |
| `minAmount`       | ≥ 0, ≤ maxAmount (nếu có) |
| `maxAmount`       | ≥ 0, ≥ minAmount (nếu có) |

### 3.4 Phân quyền đặc biệt
- Sales: Chỉ xem được báo cáo thanh toán của các hợp đồng do mình phụ trách
- Division Manager: Xem được báo cáo thanh toán của tất cả hợp đồng thuộc bộ phận mình quản lý
- Kế toán: Xem được báo cáo thanh toán của tất cả hợp đồng với đầy đủ thông tin
- Admin: Xem được báo cáo thanh toán của tất cả hợp đồng

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu báo cáo thanh toán và công nợ |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportInfo` | Object | Thông tin tổng quan về báo cáo |
| `summaryMetrics` | Object | Các chỉ số tổng hợp về thanh toán |
| `content` | Array | Mảng các đối tượng kỳ thanh toán |
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
| `totalPaymentTerms` | Integer | Tổng số kỳ thanh toán |
| `byStatus` | Object | Phân loại theo trạng thái thanh toán |
| `totalAmount` | Long | Tổng giá trị các khoản thanh toán (VND) |
| `totalPaid` | Long | Tổng số tiền đã thanh toán (VND) |
| `totalPending` | Long | Tổng số tiền đang chờ thanh toán (VND) |
| `totalOverdue` | Long | Tổng số tiền quá hạn thanh toán (VND) |
| `overdueDays` | Object | Phân loại theo số ngày quá hạn |
| `byCustomer` | Array | Phân loại công nợ theo khách hàng |
| `bySales` | Array | Phân loại công nợ theo nhân viên sales |

#### ByStatus Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `Pending` | Integer | Số kỳ thanh toán đang chờ |
| `Paid` | Integer | Số kỳ thanh toán đã hoàn thành |
| `Overdue` | Integer | Số kỳ thanh toán quá hạn |
| `UpcomingDue` | Integer | Số kỳ thanh toán sắp đến hạn |

#### OverdueDays Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `1-15` | Integer | Số kỳ thanh toán quá hạn 1-15 ngày |
| `16-30` | Integer | Số kỳ thanh toán quá hạn 16-30 ngày |
| `31-60` | Integer | Số kỳ thanh toán quá hạn 31-60 ngày |
| `60+` | Integer | Số kỳ thanh toán quá hạn trên 60 ngày |

#### CustomerSummary Object (trong mảng byCustomer)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên khách hàng |
| `pending` | Long | Số tiền đang chờ thanh toán của khách hàng (VND) |
| `overdue` | Long | Số tiền quá hạn thanh toán của khách hàng (VND) |

#### SalesSummary Object (trong mảng bySales)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên nhân viên sales |
| `pending` | Long | Số tiền đang chờ thanh toán của hợp đồng do nhân viên phụ trách (VND) |
| `overdue` | Long | Số tiền quá hạn thanh toán của hợp đồng do nhân viên phụ trách (VND) |

#### PaymentTerm Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỳ thanh toán |
| `contract` | Object | Thông tin hợp đồng liên quan |
| `termNumber` | Integer | Số thứ tự kỳ thanh toán |
| `description` | String | Mô tả kỳ thanh toán |
| `amount` | Long | Số tiền cần thanh toán (VND) |
| `dueDate` | String | Ngày đến hạn (yyyy-MM-dd) |
| `status` | String | Trạng thái thanh toán |
| `daysUntilDue` | Integer | Số ngày còn lại đến khi đến hạn (đối với trạng thái Pending) |
| `daysOverdue` | Integer | Số ngày quá hạn (đối với trạng thái Overdue) |
| `paidAmount` | Long | Số tiền đã thanh toán (VND) |
| `paidDate` | String | Ngày đã thanh toán (yyyy-MM-dd) |
| `note` | String | Ghi chú về kỳ thanh toán |

#### Contract Object (trong PaymentTerm)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng |
| `code` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `customer` | Object | Thông tin khách hàng |
| `sales` | Object | Thông tin nhân viên sales phụ trách |

#### Customer Object (trong Contract)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của khách hàng |
| `name` | String | Tên khách hàng |

#### Sales Object (trong Contract)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên sales |
| `name` | String | Tên nhân viên sales |

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
      "reportName": "Báo cáo tình trạng thanh toán/công nợ",
      "generatedAt": "2025-05-01T15:30:45Z",
      "fromDate": "2024-11-01",
      "toDate": "2025-11-30",
      "filters": {
        "status": "Pending,Overdue"
      }
    },
    "summaryMetrics": {
      "totalPaymentTerms": 95,
      "byStatus": {
        "Pending": 35,
        "Paid": 45,
        "Overdue": 10,
        "UpcomingDue": 5
      },
      "totalAmount": 8500000000,
      "totalPaid": 5000000000,
      "totalPending": 2800000000,
      "totalOverdue": 700000000,
      "overdueDays": {
        "1-15": 4,
        "16-30": 3,
        "31-60": 2,
        "60+": 1
      },
      "byCustomer": [
        {"name": "ABC Corporation", "pending": 1000000000, "overdue": 300000000},
        {"name": "XYZ Inc", "pending": 800000000, "overdue": 200000000},
        {"name": "DEF Limited", "pending": 600000000, "overdue": 0}
      ],
      "bySales": [
        {"name": "Nguyễn Văn X", "pending": 1200000000, "overdue": 400000000},
        {"name": "Trần Thị Y", "pending": 1000000000, "overdue": 200000000},
        {"name": "Lê Anh Z", "pending": 800000000, "overdue": 100000000}
      ]
    },
    "content": [
      {
        "id": 201,
        "contract": {
          "id": 101,
          "code": "HD-2025-001",
          "name": "Phát triển phần mềm quản lý nhân sự",
          "customer": {
            "id": 15,
            "name": "ABC Corporation"
          },
          "sales": {
            "id": 20,
            "name": "Nguyễn Văn X"
          }
        },
        "termNumber": 3,
        "description": "Thanh toán đợt 3 (40%)",
        "amount": 200000000,
        "dueDate": "2025-12-15",
        "status": "Pending",
        "daysUntilDue": 229,
        "paidAmount": 0,
        "paidDate": null,
        "note": null
      },
      {
        "id": 208,
        "contract": {
          "id": 102,
          "code": "HD-2025-002",
          "name": "Bảo trì hệ thống kế toán",
          "customer": {
            "id": 16,
            "name": "XYZ Inc"
          },
          "sales": {
            "id": 21,
            "name": "Trần Thị Y"
          }
        },
        "termNumber": 3,
        "description": "Thanh toán tháng 4/2025",
        "amount": 80000000,
        "dueDate": "2025-05-15",
        "status": "Pending",
        "daysUntilDue": 14,
        "paidAmount": 0,
        "paidDate": null,
        "note": null
      },
      {
        "id": 195,
        "contract": {
          "id": 95,
          "code": "HD-2024-095",
          "name": "Tư vấn triển khai CRM",
          "customer": {
            "id": 22,
            "name": "PQR Group"
          },
          "sales": {
            "id": 22,
            "name": "Lê Anh Z"
          }
        },
        "termNumber": 2,
        "description": "Thanh toán đợt 2 (50%)",
        "amount": 150000000,
        "dueDate": "2025-04-15",
        "status": "Overdue",
        "daysOverdue": 16,
        "paidAmount": 0,
        "paidDate": null,
        "note": "Đã liên hệ khách hàng, hứa sẽ thanh toán trước 10/5"
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 2,
      "totalElements": 95,
      "sort": "dueDate,asc"
    }
  }
}
```

#### 4.1.1 Response khi exportType=excel hoặc csv - 200 OK

```
Content-Disposition: attachment; filename="payment_report_20250501.xlsx"
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
      "message": "Giá trị không hợp lệ. Các giá trị hợp lệ: Pending, Paid, Overdue, UpcomingDue"
    },
    {
      "field": "fromDate",
      "message": "Định dạng phải là yyyy-MM-dd"
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
  "message": "Bạn không có quyền xem báo cáo thanh toán này"
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