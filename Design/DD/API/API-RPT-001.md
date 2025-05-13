# API Details: Lấy dữ liệu tổng hợp cho dashboard

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo tài liệu API dashboard tổng hợp | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để lấy dữ liệu tổng hợp từ nhiều module khác nhau nhằm hiển thị trên dashboard chính của hệ thống, tùy theo phân quyền và vai trò của người dùng, giúp người dùng có cái nhìn tổng quan về tình hình kinh doanh và hoạt động của công ty.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-001                                  |
| **Tên API**        | Lấy dữ liệu tổng hợp cho dashboard          |
| **Mô tả**          | API cho phép lấy dữ liệu tổng hợp từ nhiều module để hiển thị trên dashboard chính |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/dashboard/summary`                  |
| **Quyền truy cập** | dashboard:read:all, dashboard:read:team, dashboard:read:own |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `fromDate`     | Date         | Không    | Ngày bắt đầu dữ liệu (yyyy-MM-dd, mặc định: đầu tháng hiện tại) |
| `toDate`       | Date         | Không    | Ngày kết thúc dữ liệu (yyyy-MM-dd, mặc định: ngày hiện tại) |
| `teamId`       | Long         | Không    | ID của team cần lọc dữ liệu |
| `widgets`      | Array[String]| Không    | Danh sách các widget cần lấy dữ liệu, nếu không có sẽ lấy tất cả |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `fromDate`     | Định dạng yyyy-MM-dd                |
| `toDate`       | Định dạng yyyy-MM-dd và >= fromDate |
| `teamId`       | Phải tồn tại trong hệ thống (nếu có) |
| `widgets`      | Các giá trị có thể: `opportunity_status`, `margin_distribution`, `revenue_summary`, `employee_status`, `utilization_rate` |

### 3.4 Phân quyền đặc biệt
- Mỗi người dùng chỉ nhận được dữ liệu dựa trên quyền truy cập của họ:
  - Admin và Division Manager: Xem tất cả dữ liệu
  - Leader: Chỉ xem dữ liệu của team mình và các nhân viên trong team
  - Sales: Chỉ xem dữ liệu cơ hội và doanh thu liên quan đến mình
- Phạm vi dữ liệu mặc định là từ đầu tháng hiện tại đến ngày hiện tại
- Widget `margin_distribution` chỉ hiển thị cho Admin và Division Manager

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu tổng hợp cho dashboard |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `dateRange` | Object | Thông tin về khoảng thời gian dữ liệu |
| `widgets` | Object | Đối tượng chứa dữ liệu của các widget |

#### DateRange Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `fromDate` | String | Ngày bắt đầu khoảng thời gian (yyyy-MM-dd) |
| `toDate` | String | Ngày kết thúc khoảng thời gian (yyyy-MM-dd) |

#### Widgets Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `opportunity_status` | Object | Dữ liệu tổng quan về tình trạng cơ hội kinh doanh |
| `margin_distribution` | Object | Dữ liệu về phân bố biên lợi nhuận |
| `revenue_summary` | Object | Tóm tắt doanh thu |
| `employee_status` | Object | Dữ liệu trạng thái nhân viên |
| `utilization_rate` | Object | Tỷ lệ sử dụng nhân sự |

#### OpportunityStatus Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalOpportunities` | Integer | Tổng số cơ hội |
| `byStatus` | Object | Số lượng cơ hội theo trạng thái đèn hiệu |
| `byDealStage` | Array | Phân bố cơ hội theo giai đoạn |
| `topOpportunities` | Array | Danh sách cơ hội tiềm năng hàng đầu |

#### ByStatus Object (trong OpportunityStatus)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `green` | Integer | Số cơ hội có trạng thái tốt |
| `yellow` | Integer | Số cơ hội cần theo dõi |
| `red` | Integer | Số cơ hội có rủi ro cao |

#### DealStage Object (trong mảng byDealStage)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `stage` | String | Tên giai đoạn |
| `count` | Integer | Số lượng cơ hội ở giai đoạn này |

#### Opportunity Object (trong mảng topOpportunities)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội |
| `name` | String | Tên cơ hội |
| `customer` | String | Tên khách hàng |
| `value` | Long | Giá trị dự án (VND) |
| `stage` | String | Giai đoạn của cơ hội |
| `lastInteraction` | String | Ngày tương tác gần nhất (yyyy-MM-dd) |

#### MarginDistribution Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalEmployees` | Integer | Tổng số nhân viên |
| `distribution` | Object | Phân bố nhân viên theo biên lợi nhuận |
| `trend` | Array | Xu hướng biên lợi nhuận theo thời gian |

#### Distribution Object (trong MarginDistribution)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `green` | Object | Thông tin nhân viên có biên lợi nhuận tốt |
| `yellow` | Object | Thông tin nhân viên có biên lợi nhuận trung bình |
| `red` | Object | Thông tin nhân viên có biên lợi nhuận thấp |

#### DistributionCategory Object (trong Distribution - green, yellow, red)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `count` | Integer | Số lượng nhân viên trong nhóm này |
| `percentage` | Double | Tỷ lệ phần trăm |

#### TrendItem Object (trong mảng trend)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `month` | String | Tháng (yyyy-MM) |
| `value` | Double | Giá trị biên lợi nhuận trung bình |

#### RevenueSummary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `currentMonth` | Object | Dữ liệu doanh thu tháng hiện tại |
| `currentQuarter` | Object | Dữ liệu doanh thu quý hiện tại |
| `ytd` | Object | Dữ liệu doanh thu từ đầu năm đến hiện tại |
| `contracts` | Object | Thông tin về hợp đồng |
| `payment` | Object | Thông tin về thanh toán |

#### RevenuePeriod Object (currentMonth, currentQuarter, ytd)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `target` | Long | Mục tiêu doanh thu (VND) |
| `actual` | Long | Doanh thu thực tế (VND) |
| `achievement` | Double | Tỷ lệ hoàn thành mục tiêu (%) |

#### Contracts Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `total` | Integer | Tổng số hợp đồng |
| `newlyAdded` | Integer | Số hợp đồng mới ký |

#### Payment Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalDue` | Long | Tổng số tiền phải thu (VND) |
| `overdue` | Long | Số tiền quá hạn thanh toán (VND) |
| `upcoming` | Long | Số tiền sắp đến hạn thanh toán (VND) |

#### EmployeeStatus Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalEmployees` | Integer | Tổng số nhân viên |
| `byStatus` | Object | Phân bố nhân viên theo trạng thái |
| `endingSoonList` | Array | Danh sách nhân viên sắp kết thúc dự án |

#### ByStatus Object (trong EmployeeStatus)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `allocated` | Integer | Số nhân viên đã được phân bổ |
| `available` | Integer | Số nhân viên đang sẵn sàng |
| `endingSoon` | Integer | Số nhân viên sắp kết thúc dự án |
| `onLeave` | Integer | Số nhân viên đang nghỉ phép |

#### Employee Object (trong mảng endingSoonList)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `name` | String | Tên nhân viên |
| `projectEndDate` | String | Ngày kết thúc dự án (yyyy-MM-dd) |

#### UtilizationRate Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `overall` | Double | Tỷ lệ sử dụng tổng thể (%) |
| `byTeam` | Array | Tỷ lệ sử dụng theo từng team |
| `trend` | Array | Xu hướng tỷ lệ sử dụng theo thời gian |

#### TeamUtilization Object (trong mảng byTeam)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `team` | String | Tên team |
| `rate` | Double | Tỷ lệ sử dụng nhân sự (%) |

#### UtilizationTrend Object (trong mảng trend)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `month` | String | Tháng (yyyy-MM) |
| `value` | Double | Tỷ lệ sử dụng trung bình (%) |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "dateRange": {
      "fromDate": "2025-06-01",
      "toDate": "2025-06-15"
    },
    "widgets": {
      "opportunity_status": {
        "totalOpportunities": 28,
        "byStatus": {
          "green": 15,
          "yellow": 8,
          "red": 5
        },
        "byDealStage": [
          { "stage": "Prospecting", "count": 10 },
          { "stage": "Needs Analysis", "count": 5 },
          { "stage": "Proposal", "count": 8 },
          { "stage": "Negotiation", "count": 3 },
          { "stage": "Closed Won", "count": 2 }
        ],
        "topOpportunities": [
          {
            "id": 45,
            "name": "Dự án quản lý bán hàng ABC Corp",
            "customer": "ABC Corporation",
            "value": 500000000,
            "stage": "Proposal",
            "lastInteraction": "2025-06-10"
          },
          {
            "id": 48,
            "name": "Nâng cấp hệ thống XYZ",
            "customer": "XYZ Company",
            "value": 350000000,
            "stage": "Negotiation",
            "lastInteraction": "2025-06-12"
          }
        ]
      },
      "margin_distribution": {
        "totalEmployees": 45,
        "distribution": {
          "green": { "count": 28, "percentage": 62.2 },
          "yellow": { "count": 12, "percentage": 26.7 },
          "red": { "count": 5, "percentage": 11.1 }
        },
        "trend": [
          { "month": "2025-01", "value": 38.5 },
          { "month": "2025-02", "value": 39.2 },
          { "month": "2025-03", "value": 40.1 },
          { "month": "2025-04", "value": 38.7 },
          { "month": "2025-05", "value": 40.5 },
          { "month": "2025-06", "value": 41.2 }
        ]
      },
      "revenue_summary": {
        "currentMonth": {
          "target": 1500000000,
          "actual": 1250000000,
          "achievement": 83.3
        },
        "currentQuarter": {
          "target": 4000000000,
          "actual": 3200000000,
          "achievement": 80.0
        },
        "ytd": {
          "target": 15000000000,
          "actual": 13800000000,
          "achievement": 92.0
        },
        "contracts": {
          "total": 15,
          "newlyAdded": 2
        },
        "payment": {
          "totalDue": 2500000000,
          "overdue": 500000000,
          "upcoming": 1000000000
        }
      },
      "employee_status": {
        "totalEmployees": 45,
        "byStatus": {
          "allocated": 35,
          "available": 5,
          "endingSoon": 4,
          "onLeave": 1
        },
        "endingSoonList": [
          {
            "id": 102,
            "name": "Trần Thị B",
            "projectEndDate": "2025-07-15"
          },
          {
            "id": 105,
            "name": "Lê Văn E",
            "projectEndDate": "2025-07-30"
          }
        ]
      },
      "utilization_rate": {
        "overall": 85.5,
        "byTeam": [
          { "team": "Team Alpha", "rate": 92.0 },
          { "team": "Team Beta", "rate": 87.5 },
          { "team": "Team Gamma", "rate": 78.0 }
        ],
        "trend": [
          { "month": "2025-01", "value": 82.5 },
          { "month": "2025-02", "value": 84.0 },
          { "month": "2025-03", "value": 83.5 },
          { "month": "2025-04", "value": 84.5 },
          { "month": "2025-05", "value": 86.0 },
          { "month": "2025-06", "value": 85.5 }
        ]
      }
    }
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
      "field": "toDate",
      "message": "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu"
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
  "message": "Bạn không có quyền xem dữ liệu dashboard này"
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