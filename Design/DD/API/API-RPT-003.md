# API Details: Báo cáo chi tiết margin theo nhân viên/team

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-06-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API báo cáo chi tiết margin theo nhân viên/team | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API cho lãnh đạo và quản lý để phân tích chi tiết biên lợi nhuận (margin) theo từng nhân viên hoặc team, hỗ trợ việc đánh giá hiệu quả kinh doanh và đưa ra các quyết định về chiến lược kinh doanh, phân bổ nguồn lực và chính sách giá.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-003                                  |
| **Tên API**        | Báo cáo chi tiết margin theo nhân viên/team   |
| **Mô tả**          | API cung cấp báo cáo chi tiết về margin của nhân viên và team |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/reports/margin-detail`              |
| **Quyền truy cập** | report:read:all, report:read:team           |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|----------------|----------------------|----------|-------|
| `teamId`       | Integer              | Không    | ID của team cần lọc |
| `employeeId`   | Integer              | Không    | ID của nhân viên cần xem chi tiết |
| `period`       | String               | Không    | Kỳ báo cáo: `month`, `quarter`, `year` (mặc định: `month`) |
| `fromDate`     | Date (yyyy-MM-dd)    | Không    | Ngày bắt đầu kỳ báo cáo (mặc định: 1 năm trước) |
| `toDate`       | Date (yyyy-MM-dd)    | Không    | Ngày kết thúc kỳ báo cáo (mặc định: hiện tại) |
| `marginThreshold` | String            | Không    | Lọc theo ngưỡng margin: `red` (<=25%), `yellow` (25-35%), `green` (>35%) |
| `groupBy`      | String               | Không    | Nhóm kết quả theo: `employee`, `team` (mặc định: `employee`) |
| `includeDetails` | Boolean            | Không    | Bao gồm chi tiết cost/revenue trong kết quả (mặc định: `true`) |
| `exportType`   | String               | Không    | Loại xuất báo cáo: `json`, `csv`, `excel` (mặc định: `json`) |
| `page`         | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`         | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `50`) |
| `sortBy`       | String               | Không    | Trường sắp xếp (mặc định: `margin`) |
| `sortDir`      | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |


### 3.3 Validate Rule
| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `teamId`       | Phải tồn tại trong hệ thống (nếu có) |
| `employeeId`   | Phải tồn tại trong hệ thống (nếu có) |
| `page`         | ≥ 1              |
| `size`         | 1 → 500          |
| `sortBy`       | Một trong: `margin`, `employeeName`, `teamName`, `cost`, `revenue` |
| `sortDir`      | `asc`, `desc`    |
| `period`       | Một trong: `month`, `quarter`, `year` |
| `groupBy`      | Một trong: `employee`, `team` |
| `marginThreshold` | Một trong: `red`, `yellow`, `green` |
| `exportType`   | Một trong: `json`, `csv`, `excel` |
| `fromDate`     | Định dạng yyyy-MM-dd, ≤ toDate |
| `toDate`       | Định dạng yyyy-MM-dd, ≥ fromDate |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được báo cáo margin cho team mình quản lý
- Division Manager: Xem được báo cáo margin cho tất cả team thuộc bộ phận mình quản lý
- Admin: Xem được báo cáo margin của toàn bộ công ty
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu báo cáo margin |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportInfo` | Object | Thông tin tổng quan về báo cáo |
| `summaryMetrics` | Object | Các chỉ số tổng hợp về margin |
| `content` | Array | Mảng các đối tượng nhân viên/team (tùy theo groupBy) |
| `pageable` | Object | Thông tin phân trang |

#### ReportInfo Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportName` | String | Tên báo cáo |
| `generatedAt` | String | Thời điểm tạo báo cáo (ISO 8601) |
| `period` | String | Kỳ báo cáo (month, quarter, year) |
| `fromDate` | String | Ngày bắt đầu kỳ báo cáo (yyyy-MM-dd) |
| `toDate` | String | Ngày kết thúc kỳ báo cáo (yyyy-MM-dd) |
| `filters` | Object | Các bộ lọc đã áp dụng |

#### SummaryMetrics Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `averageMargin` | Double | Tỷ lệ margin trung bình (%) |
| `redCount` | Integer | Số nhân viên/team có margin thấp (<=25%) |
| `yellowCount` | Integer | Số nhân viên/team có margin trung bình (25-35%) |
| `greenCount` | Integer | Số nhân viên/team có margin cao (>35%) |
| `marginDistribution` | Object | Phân bố margin theo ngưỡng |
| `marginTrend` | Array | Xu hướng margin theo thời gian |

#### MarginDistribution Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `labels` | Array | Mảng các nhãn ngưỡng margin |
| `values` | Array | Mảng số lượng tương ứng với mỗi ngưỡng |

#### MarginTrend Object (trong mảng marginTrend)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Kỳ báo cáo (YYYY-MM cho tháng, YYYY-QQ cho quý, YYYY cho năm) |
| `value` | Double | Giá trị margin trung bình (%) |

#### Employee Object (trong mảng content khi groupBy=employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employeeId` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `employeeName` | String | Tên nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `position` | String | Vị trí công việc |
| `marginData` | Array | Dữ liệu margin theo các kỳ |
| `averageMargin` | Double | Margin trung bình (%) |
| `status` | String | Trạng thái margin (red, yellow, green) |

#### Team Object (trong Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### MarginData Object (trong mảng marginData của Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Kỳ báo cáo |
| `cost` | Long | Chi phí nhân viên (VND) |
| `revenue` | Long | Doanh thu từ nhân viên (VND) |
| `margin` | Double | Tỷ lệ margin (%) |
| `status` | String | Trạng thái margin (red, yellow, green) |

#### Team Object (trong mảng content khi groupBy=team)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `teamId` | Integer | ID của team |
| `teamName` | String | Tên team |
| `leader` | Object | Thông tin leader của team |
| `employeeCount` | Integer | Số lượng nhân viên trong team |
| `marginData` | Array | Dữ liệu margin theo các kỳ |
| `averageMargin` | Double | Margin trung bình (%) |
| `status` | String | Trạng thái margin (red, yellow, green) |

#### Leader Object (trong Team)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của leader |
| `name` | String | Tên leader |

#### TeamMarginData Object (trong mảng marginData của Team)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Kỳ báo cáo |
| `totalCost` | Long | Tổng chi phí team (VND) |
| `totalRevenue` | Long | Tổng doanh thu từ team (VND) |
| `margin` | Double | Tỷ lệ margin (%) |
| `status` | String | Trạng thái margin (red, yellow, green) |

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
      "reportName": "Báo cáo chi tiết margin",
      "generatedAt": "2025-05-01T10:45:30Z",
      "period": "month",
      "fromDate": "2024-05-01",
      "toDate": "2025-04-30",
      "filters": {
        "teamId": 1,
        "groupBy": "employee"
      }
    },
    "summaryMetrics": {
      "averageMargin": 42.5,
      "redCount": 3,
      "yellowCount": 5,
      "greenCount": 37,
      "marginDistribution": {
        "labels": ["<=25%", "25-35%", ">35%"],
        "values": [3, 5, 37]
      },
      "marginTrend": [
        {"period": "2024-05", "value": 39.2},
        {"period": "2024-06", "value": 40.1},
        {"period": "2024-07", "value": 41.5},
        {"period": "2024-08", "value": 40.8},
        {"period": "2024-09", "value": 41.2},
        {"period": "2024-10", "value": 41.5},
        {"period": "2024-11", "value": 42.0},
        {"period": "2024-12", "value": 41.8},
        {"period": "2025-01", "value": 41.9},
        {"period": "2025-02", "value": 42.2},
        {"period": "2025-03", "value": 42.3},
        {"period": "2025-04", "value": 42.5}
      ]
    },
    "content": [
      {
        "employeeId": 1,
        "employeeCode": "NV001",
        "employeeName": "Nguyễn Văn A",
        "team": {
          "id": 1,
          "name": "Team Alpha"
        },
        "position": "Developer",
        "marginData": [
          {
            "period": "2024-05",
            "cost": 25000000,
            "revenue": 45000000,
            "margin": 44.4,
            "status": "green"
          },
          {
            "period": "2024-06",
            "cost": 25000000,
            "revenue": 45000000,
            "margin": 44.4,
            "status": "green"
          },
          {
            "period": "2025-04",
            "cost": 27000000,
            "revenue": 50000000,
            "margin": 46.0,
            "status": "green"
          }
        ],
        "averageMargin": 45.2,
        "status": "green"
      },
      {
        "employeeId": 2,
        "employeeCode": "NV002",
        "employeeName": "Lê Thị C",
        "team": {
          "id": 1,
          "name": "Team Alpha"
        },
        "position": "Developer",
        "marginData": [
          {
            "period": "2024-05",
            "cost": 22000000,
            "revenue": 30000000,
            "margin": 26.7,
            "status": "yellow"
          },
          {
            "period": "2025-04",
            "cost": 23000000,
            "revenue": 35000000,
            "margin": 34.3,
            "status": "yellow"
          }
        ],
        "averageMargin": 31.5,
        "status": "yellow"
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 1,
      "totalElements": 45,
      "sort": "margin,desc"
    }
  }
}
```

#### 4.1.1 Response khi groupBy=team - 200 OK

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "reportInfo": {
      "reportName": "Báo cáo chi tiết margin theo team",
      "generatedAt": "2025-05-01T10:45:30Z",
      "period": "month",
      "fromDate": "2024-05-01",
      "toDate": "2025-04-30",
      "filters": {
        "groupBy": "team"
      }
    },
    "summaryMetrics": {
      "averageMargin": 42.5,
      "redCount": 0,
      "yellowCount": 1,
      "greenCount": 4,
      "marginDistribution": {
        "labels": ["<=25%", "25-35%", ">35%"],
        "values": [0, 1, 4]
      },
      "marginTrend": [
        {"period": "2024-05", "value": 39.2},
        {"period": "2025-04", "value": 42.5}
      ]
    },
    "content": [
      {
        "teamId": 1,
        "teamName": "Team Alpha",
        "leader": {
          "id": 5,
          "name": "Trần Văn B"
        },
        "employeeCount": 12,
        "marginData": [
          {
            "period": "2024-05",
            "totalCost": 280000000,
            "totalRevenue": 490000000,
            "margin": 42.9,
            "status": "green"
          },
          {
            "period": "2025-04",
            "totalCost": 300000000,
            "totalRevenue": 540000000,
            "margin": 44.4,
            "status": "green"
          }
        ],
        "averageMargin": 43.5,
        "status": "green"
      },
      {
        "teamId": 2,
        "teamName": "Team Beta",
        "leader": {
          "id": 8,
          "name": "Phạm Thị D"
        },
        "employeeCount": 10,
        "marginData": [
          {
            "period": "2024-05",
            "totalCost": 220000000,
            "totalRevenue": 310000000,
            "margin": 29.0,
            "status": "yellow"
          },
          {
            "period": "2025-04",
            "totalCost": 230000000,
            "totalRevenue": 350000000,
            "margin": 34.3,
            "status": "yellow"
          }
        ],
        "averageMargin": 32.5,
        "employeeMarginDistribution": {
          "red": 1,
          "yellow": 3,
          "green": 6
        },
        "status": "yellow"
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 1,
      "totalElements": 5,
      "sort": "margin,desc"
    }
  }
}
```

#### 4.1.2 Response khi exportType=excel hoặc csv - 200 OK

```
Content-Disposition: attachment; filename="margin_report_20250501.xlsx"
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
      "field": "exportType",
      "message": "Giá trị 'pdf' không được hỗ trợ. Các giá trị hợp lệ: json, csv, excel"
    },
    {
      "field": "toDate",
      "message": "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu"
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
  "message": "Bạn không có quyền truy cập chức năng này"
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
      "field": "teamId",
      "message": "Không tìm thấy team với ID: 999"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi tạo báo cáo"
}
``` 