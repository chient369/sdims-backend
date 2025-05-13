# API Details: Lấy dữ liệu margin tổng hợp

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-06-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API lấy dữ liệu margin tổng hợp | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để truy xuất dữ liệu tổng hợp về biên lợi nhuận (margin) cho các team và nhân viên, hỗ trợ việc theo dõi, phân tích hiệu quả kinh doanh và lợi nhuận trên dashboard, giúp lãnh đạo ra quyết định về chiến lược phân bổ nguồn lực và cải thiện hiệu suất.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-MGN-002                                  |
| **Tên API**        | Lấy dữ liệu margin tổng hợp                  |
| **Mô tả**          | API lấy dữ liệu margin tổng hợp cho dashboard |
| **Module**         | Quản lý Hiệu suất & Margin                   |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/margins/summary`                    |
| **Quyền truy cập** | margin-summary:read:all, margin-summary:read:team |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|----------------|------------------|----------|-------|
| `teamId`       | Integer          | Không    | ID của team cần lọc |
| `period`       | String           | Không    | Chu kỳ thời gian: `month`, `quarter`, `year` (mặc định: `month`) |
| `fromDate`     | String           | Không    | Lọc từ ngày (định dạng: YYYY-MM-DD) |
| `toDate`       | String           | Không    | Lọc đến ngày (định dạng: YYYY-MM-DD) |
| `yearMonth`    | String           | Không    | Chỉ lấy một tháng cụ thể (định dạng: YYYY-MM) |
| `yearQuarter`  | String           | Không    | Chỉ lấy một quý cụ thể (định dạng: YYYY-Q1, YYYY-Q2, YYYY-Q3, YYYY-Q4) |
| `year`         | Integer          | Không    | Chỉ lấy một năm cụ thể |
| `view`         | String           | Không    | Kiểu hiển thị: `table`, `chart` (mặc định: `table`) |
| `groupBy`      | String           | Không    | Nhóm theo: `team`, `status` (chỉ áp dụng khi không có teamId, mặc định: `team`) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `teamId`       | Phải là số nguyên dương và tồn tại trong hệ thống |
| `period`       | Một trong: `month`, `quarter`, `year` |
| `fromDate`     | Định dạng: YYYY-MM-DD |
| `toDate`       | Định dạng: YYYY-MM-DD, phải sau hoặc bằng fromDate |
| `yearMonth`    | Định dạng: YYYY-MM (VD: 2025-05) |
| `yearQuarter`  | Định dạng: YYYY-Q[1-4] (VD: 2025-Q2) |
| `year`         | Số 4 chữ số (VD: 2025) |
| `view`         | Một trong: `table`, `chart` |
| `groupBy`      | Một trong: `team`, `status` |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được tổng hợp margin của team mình
- Division Manager: Xem được tổng hợp margin của tất cả team thuộc bộ phận mình quản lý
- Admin: Xem được tổng hợp margin của tất cả team

---

## 4. Response

### 4.1 Success - 200 OK (Table View - Group by Team)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu margin tổng hợp |

#### Data Object (Group by Team)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `summary` | Object | Thông tin tổng hợp về dữ liệu margin |
| `teams` | Array | Mảng các đối tượng thông tin margin của từng team |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Chu kỳ thời gian: month, quarter, year |
| `periodLabel` | String | Nhãn hiển thị chu kỳ (vd: "Tháng 5/2025") |
| `totalTeams` | Integer | Tổng số team |
| `totalEmployees` | Integer | Tổng số nhân viên |
| `averageCost` | Number | Chi phí trung bình (VNĐ) |
| `averageRevenue` | Number | Doanh thu trung bình (VNĐ) |
| `averageMargin` | Number | Tỷ lệ margin trung bình (%) |
| `totalStatusCounts` | Object | Số lượng nhân viên theo từng trạng thái (Red, Yellow, Green) |

#### Team Margin Object (trong mảng teams)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |
| `employeeCount` | Integer | Số lượng nhân viên trong team |
| `cost` | Number | Tổng chi phí của team (VNĐ) |
| `revenue` | Number | Tổng doanh thu của team (VNĐ) |
| `margin` | Number | Tỷ lệ margin của team (%) |
| `marginStatus` | String | Trạng thái margin: Red, Yellow, Green |
| `statusCounts` | Object | Số lượng nhân viên theo từng trạng thái trong team |
| `trends` | Object | Xu hướng margin theo thời gian |

#### StatusCounts Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `Red` | Integer | Số lượng nhân viên có margin ở trạng thái Red |
| `Yellow` | Integer | Số lượng nhân viên có margin ở trạng thái Yellow |
| `Green` | Integer | Số lượng nhân viên có margin ở trạng thái Green |

#### Trends Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `margin` | Array | Mảng các giá trị margin theo thời gian |
| `periods` | Array | Mảng các mã chu kỳ tương ứng |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "summary": {
      "period": "month",
      "periodLabel": "Tháng 5/2025",
      "totalTeams": 5,
      "totalEmployees": 45,
      "averageCost": 25000000,
      "averageRevenue": 37500000,
      "averageMargin": 33.33,
      "totalStatusCounts": {
        "Red": 8,
        "Yellow": 12,
        "Green": 25
      }
    },
    "teams": [
      {
        "id": 1,
        "name": "Team Alpha",
        "employeeCount": 10,
        "cost": 250000000,
        "revenue": 412500000,
        "margin": 39.39,
        "marginStatus": "Green",
        "statusCounts": {
          "Red": 1,
          "Yellow": 2,
          "Green": 7
        },
        "trends": {
          "margin": [35.0, 36.5, 37.8, 38.2, 39.39],
          "periods": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
        }
      },
      {
        "id": 2,
        "name": "Team Beta",
        "employeeCount": 8,
        "cost": 200000000,
        "revenue": 280000000,
        "margin": 28.57,
        "marginStatus": "Yellow",
        "statusCounts": {
          "Red": 2,
          "Yellow": 4,
          "Green": 2
        },
        "trends": {
          "margin": [25.0, 26.2, 27.8, 28.0, 28.57],
          "periods": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
        }
      },
      {
        "id": 3,
        "name": "Team Gamma",
        "employeeCount": 12,
        "cost": 300000000,
        "revenue": 360000000,
        "margin": 16.67,
        "marginStatus": "Red",
        "statusCounts": {
          "Red": 5,
          "Yellow": 5,
          "Green": 2
        },
        "trends": {
          "margin": [20.0, 18.5, 17.5, 17.0, 16.67],
          "periods": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
        }
      }
    ]
  }
}
```

### 4.2 Success - 200 OK (Chart View)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu cho biểu đồ margin |

#### Data Object (Chart View)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `summary` | Object | Thông tin tổng quát về dữ liệu biểu đồ |
| `chartData` | Object | Dữ liệu cho việc vẽ biểu đồ |
| `thresholds` | Object | Ngưỡng đánh giá trạng thái margin |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `period` | String | Chu kỳ thời gian |
| `fromDate` | String | Ngày bắt đầu khoảng thời gian (YYYY-MM-DD) |
| `toDate` | String | Ngày kết thúc khoảng thời gian (YYYY-MM-DD) |
| `totalTeams` | Integer | Tổng số team |
| `totalEmployees` | Integer | Tổng số nhân viên |
| `overallMargin` | Number | Tỷ lệ margin tổng thể (%) |
| `marginStatus` | String | Trạng thái margin tổng thể: Red, Yellow, Green |

#### ChartData Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `labels` | Array | Mảng các nhãn thời gian trên trục x |
| `labelFormat` | String | Định dạng nhãn: month, quarter, year |
| `datasets` | Array | Mảng các bộ dữ liệu cho từng đường trên biểu đồ |
| `average` | Array | Mảng giá trị margin trung bình theo thời gian |

#### Dataset Object (trong mảng datasets)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `teamId` | Integer | ID của team |
| `teamName` | String | Tên team |
| `color` | String | Mã màu hiển thị (HEX) |
| `data` | Array | Mảng dữ liệu margin theo thời gian |

#### Thresholds Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `red` | Number | Ngưỡng dưới (margin <= red được đánh dấu đỏ) |
| `yellow` | Number | Ngưỡng trung bình (red < margin <= yellow được đánh dấu vàng) |
| `green` | Number | Ngưỡng trên (margin > yellow được đánh dấu xanh) |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "summary": {
      "period": "month",
      "fromDate": "2025-01-01",
      "toDate": "2025-05-31",
      "totalTeams": 5,
      "totalEmployees": 45,
      "overallMargin": 33.33,
      "marginStatus": "Yellow"
    },
    "chartData": {
      "labels": ["Tháng 1/2025", "Tháng 2/2025", "Tháng 3/2025", "Tháng 4/2025", "Tháng 5/2025"],
      "labelFormat": "month",
      "datasets": [
        {
          "teamId": 1,
          "teamName": "Team Alpha",
          "color": "#4CAF50",
          "data": [35.0, 36.5, 37.8, 38.2, 39.39]
        },
        {
          "teamId": 2,
          "teamName": "Team Beta",
          "color": "#FFC107",
          "data": [25.0, 26.2, 27.8, 28.0, 28.57]
        },
        {
          "teamId": 3,
          "teamName": "Team Gamma",
          "color": "#F44336",
          "data": [20.0, 18.5, 17.5, 17.0, 16.67]
        }
      ],
      "average": [30.0, 30.5, 31.2, 32.1, 33.33]
    },
    "thresholds": {
      "red": 20.0,
      "yellow": 30.0,
      "green": 30.0
    }
  }
}
```

### 4.3 Success - 200 OK (Group by Status)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu margin tổng hợp theo trạng thái |

#### Data Object (Group by Status)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `summary` | Object | Thông tin tổng hợp về dữ liệu margin |
| `groupedByStatus` | Object | Đối tượng chứa dữ liệu được nhóm theo trạng thái margin |

#### GroupedByStatus Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `Red` | Object | Thông tin về nhóm có margin trạng thái Red |
| `Yellow` | Object | Thông tin về nhóm có margin trạng thái Yellow |
| `Green` | Object | Thông tin về nhóm có margin trạng thái Green |

#### Status Group Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `count` | Integer | Số lượng nhân viên thuộc nhóm này |
| `percentage` | Number | Tỷ lệ phần trăm trong tổng số nhân viên |
| `averageCost` | Number | Chi phí trung bình của nhóm (VNĐ) |
| `averageRevenue` | Number | Doanh thu trung bình của nhóm (VNĐ) |
| `averageMargin` | Number | Tỷ lệ margin trung bình của nhóm (%) |
| `teamDistribution` | Object | Phân bố theo team trong nhóm này |

#### TeamDistribution Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `[teamId]` | Object | Key là ID của team, value là thông tin về team |

#### Team Info Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên team |
| `count` | Integer | Số lượng nhân viên thuộc team này trong nhóm |
| `percentage` | Number | Tỷ lệ phần trăm trong nhóm |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "summary": {
      "period": "month",
      "periodLabel": "Tháng 5/2025",
      "totalTeams": 5,
      "totalEmployees": 45,
      "averageCost": 25000000,
      "averageRevenue": 37500000,
      "averageMargin": 33.33
    },
    "groupedByStatus": {
      "Green": {
        "count": 25,
        "percentage": 55.56,
        "averageCost": 26000000,
        "averageRevenue": 45500000,
        "averageMargin": 42.86,
        "teamDistribution": {
          "1": {
            "name": "Team Alpha",
            "count": 7,
            "percentage": 28.0
          },
          "2": {
            "name": "Team Beta",
            "count": 2,
            "percentage": 8.0
          },
          "3": {
            "name": "Team Gamma",
            "count": 2,
            "percentage": 8.0
          },
          "4": {
            "name": "Team Delta",
            "count": 8,
            "percentage": 32.0
          },
          "5": {
            "name": "Team Epsilon",
            "count": 6,
            "percentage": 24.0
          }
        }
      },
      "Yellow": {
        "count": 12,
        "percentage": 26.67,
        "averageCost": 24000000,
        "averageRevenue": 31200000,
        "averageMargin": 23.08,
        "teamDistribution": {
          "1": {
            "name": "Team Alpha",
            "count": 2,
            "percentage": 16.67
          },
          "2": {
            "name": "Team Beta",
            "count": 4,
            "percentage": 33.33
          },
          "3": {
            "name": "Team Gamma",
            "count": 5,
            "percentage": 41.67
          },
          "5": {
            "name": "Team Epsilon",
            "count": 1,
            "percentage": 8.33
          }
        }
      },
      "Red": {
        "count": 8,
        "percentage": 17.78,
        "averageCost": 23000000,
        "averageRevenue": 18400000,
        "averageMargin": -25.0,
        "teamDistribution": {
          "1": {
            "name": "Team Alpha",
            "count": 1,
            "percentage": 12.5
          },
          "2": {
            "name": "Team Beta",
            "count": 2,
            "percentage": 25.0
          },
          "3": {
            "name": "Team Gamma",
            "count": 5,
            "percentage": 62.5
          }
        }
      }
    }
  }
}
```

### 4.4 Error Responses

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
      "field": "view",
      "message": "Giá trị 'grid' không hợp lệ. Các giá trị hợp lệ cho tham số view: table, chart"
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
  "message": "Bạn không có quyền xem dữ liệu margin tổng hợp"
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
  "message": "Không tìm thấy team với ID: 999"
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
  "message": "Lỗi hệ thống khi lấy dữ liệu margin tổng hợp"
}
``` 