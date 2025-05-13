# API Details: Báo cáo tiến độ KPI doanh thu Sales

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API báo cáo tiến độ KPI doanh thu Sales | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để tạo báo cáo về tiến độ thực hiện KPI doanh thu của các nhân viên Sales, cho phép người quản lý theo dõi và đánh giá hiệu quả hoạt động kinh doanh, phân tích mức độ hoàn thành mục tiêu và dự báo khả năng đạt KPI trong tương lai.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-007                                  |
| **Tên API**        | Báo cáo tiến độ KPI doanh thu Sales          |
| **Mô tả**          | API cung cấp báo cáo chi tiết về tiến độ thực hiện KPI doanh thu của đội Sales |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/reports/kpi-progress`               |
| **Quyền truy cập** | report:read:all, report:read:own              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên                | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|--------------------|----------------------|----------|-------|
| `salesId`          | Integer              | Không    | ID của nhân viên Sales cần lọc (nếu không cung cấp, lấy dữ liệu của tất cả Sales) |
| `year`             | Integer              | Không    | Năm cần xem báo cáo (mặc định: năm hiện tại) |
| `quarter`          | Integer              | Không    | Quý cần xem báo cáo (1-4, nếu không cung cấp, lấy dữ liệu cả năm) |
| `month`            | Integer              | Không    | Tháng cần xem báo cáo (1-12, nếu không cung cấp, lấy dữ liệu theo quý hoặc cả năm) |
| `minAchievement`   | Double               | Không    | Tỷ lệ % hoàn thành KPI tối thiểu cần lọc |
| `maxAchievement`   | Double               | Không    | Tỷ lệ % hoàn thành KPI tối đa cần lọc |
| `includeDetails`   | Boolean              | Không    | Bao gồm chi tiết hợp đồng đóng góp vào KPI (mặc định: `true`) |
| `exportType`       | String               | Không    | Loại xuất báo cáo: `json`, `csv`, `excel` (mặc định: `json`) |
| `page`             | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`             | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `20`) |
| `sortBy`           | String               | Không    | Trường sắp xếp (mặc định: `achievementPercentage`) |
| `sortDir`          | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |

### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 100          |
| `sortDir`         | `asc`, `desc`    |
| `year`            | 2020 → 2030      |
| `quarter`         | 1 → 4            |
| `month`           | 1 → 12           |
| `minAchievement`  | 0 → 1000         |
| `maxAchievement`  | 0 → 1000, ≥ minAchievement (nếu có) |
| `exportType`      | Một trong: `json`, `csv`, `excel` |

### 3.4 Phân quyền đặc biệt
- Sales: Chỉ xem được báo cáo KPI của chính mình
- Division Manager: Xem được báo cáo KPI của tất cả nhân viên Sales thuộc bộ phận mình quản lý
- Admin: Xem được báo cáo KPI của tất cả nhân viên Sales

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu báo cáo tiến độ KPI |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportInfo` | Object | Thông tin tổng quan về báo cáo |
| `summaryMetrics` | Object | Các chỉ số tổng hợp về KPI |
| `content` | Array | Mảng các đối tượng nhân viên Sales với thông tin KPI |
| `pageable` | Object | Thông tin phân trang |

#### ReportInfo Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportName` | String | Tên báo cáo |
| `generatedAt` | String | Thời điểm tạo báo cáo (ISO 8601) |
| `period` | Object | Thông tin kỳ báo cáo |
| `filters` | Object | Các bộ lọc đã áp dụng |

#### Period Object (trong ReportInfo)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `year` | Integer | Năm báo cáo |
| `quarter` | Integer | Quý báo cáo (nếu có) |
| `month` | Integer | Tháng báo cáo (nếu có) |
| `description` | String | Mô tả kỳ báo cáo dưới dạng text |

#### SummaryMetrics Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalSales` | Integer | Tổng số nhân viên Sales |
| `averageAchievement` | Double | Tỷ lệ hoàn thành KPI trung bình (%) |
| `byAchievementRange` | Object | Phân loại theo mức độ hoàn thành KPI |
| `totalKpiTarget` | Long | Tổng chỉ tiêu KPI (VND) |
| `totalActualRevenue` | Long | Tổng doanh thu đã đạt được (VND) |
| `totalPendingRevenue` | Long | Tổng doanh thu tiềm năng (VND) |
| `periodProgress` | Object | Tiến độ thời gian của kỳ báo cáo |

#### ByAchievementRange Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `0-25%` | Integer | Số nhân viên hoàn thành dưới 25% KPI |
| `26-50%` | Integer | Số nhân viên hoàn thành từ 26-50% KPI |
| `51-75%` | Integer | Số nhân viên hoàn thành từ 51-75% KPI |
| `76-100%` | Integer | Số nhân viên hoàn thành từ 76-100% KPI |
| `100%+` | Integer | Số nhân viên hoàn thành trên 100% KPI |

#### PeriodProgress Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalDays` | Integer | Tổng số ngày trong kỳ báo cáo |
| `elapsedDays` | Integer | Số ngày đã trôi qua trong kỳ báo cáo |
| `progressPercentage` | Double | Phần trăm thời gian đã trôi qua (%) |

#### SalesKPIInfo Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `salesPerson` | Object | Thông tin nhân viên Sales |
| `kpiInfo` | Object | Thông tin KPI của nhân viên |
| `contracts` | Array | Danh sách hợp đồng đóng góp vào KPI |

#### SalesPerson Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên Sales |
| `code` | String | Mã nhân viên |
| `name` | String | Tên nhân viên |
| `team` | String | Tên team của nhân viên |

#### KPIInfo Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi KPI |
| `year` | Integer | Năm KPI |
| `quarter` | Integer | Quý KPI |
| `month` | Integer | Tháng KPI (nếu có) |
| `target` | Long | Chỉ tiêu doanh thu (VND) |
| `achievedRevenue` | Long | Doanh thu đã đạt được (VND) |
| `pendingRevenue` | Long | Doanh thu tiềm năng (VND) |
| `achievementPercentage` | Double | Tỷ lệ hoàn thành KPI hiện tại (%) |
| `forecastPercentage` | Double | Tỷ lệ dự báo hoàn thành KPI cuối kỳ (%) |
| `lastUpdated` | String | Thời điểm cập nhật gần nhất (ISO 8601) |

#### Contract Object (trong mảng contracts)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng (null nếu là cơ hội) |
| `code` | String | Mã hợp đồng hoặc mã cơ hội |
| `name` | String | Tên hợp đồng hoặc tên cơ hội |
| `customer` | String | Tên khách hàng |
| `signedDate` | String | Ngày ký hợp đồng (yyyy-MM-dd) |
| `expectedSignDate` | String | Ngày dự kiến ký (đối với cơ hội) |
| `value` | Long | Giá trị hợp đồng (VND) |
| `estimatedValue` | Long | Giá trị ước tính (đối với cơ hội) (VND) |
| `status` | String | Trạng thái hợp đồng hoặc cơ hội |
| `probability` | Integer | Xác suất thành công (%) (đối với cơ hội) |
| `kpiContribution` | Long | Giá trị đóng góp vào KPI (VND) |

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
      "reportName": "Báo cáo tiến độ KPI doanh thu Sales",
      "generatedAt": "2025-05-01T16:45:20Z",
      "period": {
        "year": 2025,
        "quarter": 2,
        "description": "Quý 2/2025 (Tháng 4-6)"
      },
      "filters": {
        "minAchievement": 30
      }
    },
    "summaryMetrics": {
      "totalSales": 5,
      "averageAchievement": 68.4,
      "byAchievementRange": {
        "0-25%": 0,
        "26-50%": 1,
        "51-75%": 2,
        "76-100%": 1,
        "100%+": 1
      },
      "totalKpiTarget": 5000000000,
      "totalActualRevenue": 3420000000,
      "totalPendingRevenue": 1250000000,
      "periodProgress": {
        "totalDays": 91,
        "elapsedDays": 31,
        "progressPercentage": 34.1
      }
    },
    "content": [
      {
        "salesPerson": {
          "id": 20,
          "code": "NV020",
          "name": "Nguyễn Văn X",
          "team": "Sales Team A"
        },
        "kpiInfo": {
          "id": 125,
          "year": 2025,
          "quarter": 2,
          "target": 1500000000,
          "achievedRevenue": 1200000000,
          "pendingRevenue": 400000000,
          "achievementPercentage": 80.0,
          "forecastPercentage": 106.7,
          "lastUpdated": "2025-05-01T10:00:00Z"
        },
        "contracts": [
          {
            "id": 101,
            "code": "HD-2025-001",
            "name": "Phát triển phần mềm quản lý nhân sự",
            "customer": "ABC Corporation",
            "signedDate": "2025-04-15",
            "value": 500000000,
            "status": "InProgress",
            "kpiContribution": 500000000
          },
          {
            "id": 105,
            "code": "HD-2025-005",
            "name": "Bảo trì hệ thống ERP",
            "customer": "GHI Ltd",
            "signedDate": "2025-04-22",
            "value": 700000000,
            "status": "InProgress",
            "kpiContribution": 700000000
          },
          {
            "id": null,
            "code": "Pending-X01",
            "name": "Triển khai hệ thống BI",
            "customer": "JKL Group",
            "expectedSignDate": "2025-05-20",
            "estimatedValue": 400000000,
            "status": "Pending",
            "probability": 80,
            "kpiContribution": 0
          }
        ]
      },
      {
        "salesPerson": {
          "id": 21,
          "code": "NV021",
          "name": "Trần Thị Y",
          "team": "Sales Team A"
        },
        "kpiInfo": {
          "id": 126,
          "year": 2025,
          "quarter": 2,
          "target": 1200000000,
          "achievedRevenue": 820000000,
          "pendingRevenue": 300000000,
          "achievementPercentage": 68.3,
          "forecastPercentage": 93.3,
          "lastUpdated": "2025-05-01T10:00:00Z"
        },
        "contracts": [
          {
            "id": 102,
            "code": "HD-2025-002",
            "name": "Bảo trì hệ thống kế toán",
            "customer": "XYZ Inc",
            "signedDate": "2025-04-05",
            "value": 320000000,
            "status": "InProgress",
            "kpiContribution": 320000000
          },
          {
            "id": 110,
            "code": "HD-2025-010",
            "name": "Phát triển ứng dụng di động",
            "customer": "MNO Corporation",
            "signedDate": "2025-04-30",
            "value": 500000000,
            "status": "New",
            "kpiContribution": 500000000
          }
        ]
      },
      {
        "salesPerson": {
          "id": 22,
          "code": "NV022",
          "name": "Lê Anh Z",
          "team": "Sales Team B"
        },
        "kpiInfo": {
          "id": 127,
          "year": 2025,
          "quarter": 2,
          "target": 800000000,
          "achievedRevenue": 1050000000,
          "pendingRevenue": 0,
          "achievementPercentage": 131.3,
          "forecastPercentage": 131.3,
          "lastUpdated": "2025-05-01T10:00:00Z"
        },
        "contracts": [
          {
            "id": 115,
            "code": "HD-2025-015",
            "name": "Xây dựng cổng thông tin nội bộ",
            "customer": "PQR Group",
            "signedDate": "2025-04-10",
            "value": 800000000,
            "status": "InProgress",
            "kpiContribution": 800000000
          },
          {
            "id": 120,
            "code": "HD-2025-020",
            "name": "Dịch vụ đào tạo CNTT",
            "customer": "STU Academy",
            "signedDate": "2025-04-25",
            "value": 250000000,
            "status": "InProgress",
            "kpiContribution": 250000000
          }
        ]
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 20,
      "totalPages": 1,
      "totalElements": 3,
      "sort": "achievementPercentage,desc"
    }
  }
}
```

#### 4.1.1 Response khi exportType=excel hoặc csv - 200 OK

```
Content-Disposition: attachment; filename="kpi_report_20250501.xlsx"
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
      "field": "quarter",
      "message": "Giá trị phải trong khoảng từ 1 đến 4"
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
  "message": "Bạn không có quyền xem báo cáo KPI này"
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
      "field": "salesId",
      "message": "Không tìm thấy nhân viên Sales với ID: 999"
    }
  ]
}
``` 