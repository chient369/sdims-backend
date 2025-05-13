# API Details: Báo cáo chi tiết danh sách cơ hội

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-06-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API báo cáo chi tiết danh sách cơ hội | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để truy xuất báo cáo chi tiết về danh sách các cơ hội kinh doanh trong hệ thống, cho phép lọc và phân tích theo nhiều tiêu chí khác nhau như khách hàng, nhân viên sales, trạng thái follow-up và yêu cầu onsite, nhằm hỗ trợ đội Sales và quản lý theo dõi, đánh giá và đưa ra quyết định kinh doanh.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-004                                  |
| **Tên API**        | Báo cáo chi tiết danh sách cơ hội             |
| **Mô tả**          | API cung cấp báo cáo chi tiết về danh sách cơ hội kinh doanh |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/reports/opportunity-list`           |
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
| `leaderId`         | Integer              | Không    | ID của Leader được gán |
| `dealStage`        | String               | Không    | Giai đoạn bán hàng (từ Hubspot): `Appointment`, `Demo`, `Negotiation`, `Closed Won`, `Closed Lost` |
| `followUpStatus`   | String               | Không    | Trạng thái follow-up: `red`, `yellow`, `green` |
| `onsite`           | Boolean              | Không    | Lọc cơ hội đánh dấu ưu tiên onsite |
| `fromDate`         | Date (yyyy-MM-dd)    | Không    | Ngày bắt đầu tạo cơ hội (mặc định: 1 năm trước) |
| `toDate`           | Date (yyyy-MM-dd)    | Không    | Ngày kết thúc tạo cơ hội (mặc định: hiện tại) |
| `keyword`          | String               | Không    | Tìm kiếm theo tên cơ hội hoặc khách hàng |
| `includeNotes`     | Boolean              | Không    | Bao gồm ghi chú trong kết quả (mặc định: `false`) |
| `includeLeaders`   | Boolean              | Không    | Bao gồm thông tin Leaders được assign (mặc định: `true`) |
| `exportType`       | String               | Không    | Loại xuất báo cáo: `json`, `csv`, `excel` (mặc định: `json`) |
| `page`             | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`             | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `50`) |
| `sortBy`           | String               | Không    | Trường sắp xếp (mặc định: `lastInteractionDate`) |
| `sortDir`          | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |


### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `customerId`      | Phải tồn tại trong hệ thống (nếu có) |
| `salesId`         | Phải tồn tại trong hệ thống (nếu có) |
| `leaderId`        | Phải tồn tại trong hệ thống (nếu có) |
| `page`            | ≥ 1              |
| `size`            | 1 → 500          |
| `sortBy`          | Một trong: `createdDate`, `lastInteractionDate`, `dealStage`, `estimatedValue`, `name`, `customerName` |
| `sortDir`         | `asc`, `desc`    |
| `followUpStatus`  | Một trong: `red`, `yellow`, `green` |
| `dealStage`       | Một trong: `Appointment`, `Demo`, `Negotiation`, `Closed Won`, `Closed Lost` |
| `exportType`      | Một trong: `json`, `csv`, `excel` |
| `fromDate`        | Định dạng yyyy-MM-dd, ≤ toDate |
| `toDate`          | Định dạng yyyy-MM-dd, ≥ fromDate |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được báo cáo cơ hội cho các cơ hội được gán cho mình
- Sales: Chỉ xem được báo cáo cơ hội do mình phụ trách
- Division Manager: Xem được báo cáo cơ hội cho tất cả cơ hội thuộc bộ phận mình quản lý
- Admin: Xem được báo cáo cơ hội của toàn bộ công ty
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu báo cáo danh sách cơ hội |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportInfo` | Object | Thông tin tổng quan về báo cáo |
| `summaryMetrics` | Object | Các chỉ số tổng hợp về cơ hội |
| `content` | Array | Mảng các đối tượng cơ hội kinh doanh |
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
| `totalOpportunities` | Integer | Tổng số cơ hội |
| `byFollowUp` | Object | Phân loại theo trạng thái follow-up |
| `byDealStage` | Object | Phân loại theo giai đoạn bán hàng |
| `onsitePriority` | Integer | Số cơ hội đánh dấu ưu tiên onsite |
| `byCustomer` | Array | Phân loại cơ hội theo khách hàng |
| `bySales` | Array | Phân loại cơ hội theo nhân viên sales |

#### ByFollowUp Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `red` | Integer | Số cơ hội có trạng thái follow-up màu đỏ (cần chú ý gấp) |
| `yellow` | Integer | Số cơ hội có trạng thái follow-up màu vàng (cần theo dõi) |
| `green` | Integer | Số cơ hội có trạng thái follow-up màu xanh (bình thường) |

#### ByDealStage Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `Appointment` | Integer | Số cơ hội ở giai đoạn hẹn gặp |
| `Demo` | Integer | Số cơ hội ở giai đoạn demo sản phẩm |
| `Negotiation` | Integer | Số cơ hội ở giai đoạn thương lượng |
| `Closed Won` | Integer | Số cơ hội thành công |
| `Closed Lost` | Integer | Số cơ hội thất bại |

#### CustomerSummary Object (trong mảng byCustomer)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên khách hàng |
| `count` | Integer | Số lượng cơ hội liên quan đến khách hàng |

#### SalesSummary Object (trong mảng bySales)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên nhân viên sales |
| `count` | Integer | Số lượng cơ hội do nhân viên phụ trách |

#### Opportunity Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội |
| `hubspotId` | String | ID của cơ hội trong Hubspot |
| `name` | String | Tên cơ hội |
| `customer` | Object | Thông tin khách hàng |
| `dealStage` | String | Giai đoạn bán hàng |
| `estimatedValue` | Long | Giá trị ước tính của cơ hội (VND) |
| `createdDate` | String | Ngày tạo cơ hội (ISO 8601) |
| `lastInteractionDate` | String | Ngày tương tác gần nhất (ISO 8601) |
| `followUpStatus` | String | Trạng thái follow-up (red, yellow, green) |
| `sales` | Object | Thông tin nhân viên sales phụ trách |
| `leaders` | Array | Danh sách leaders được gán |
| `onsite` | Boolean | Đánh dấu ưu tiên onsite |
| `notes` | Array | Danh sách ghi chú (nếu includeNotes=true) |

#### Customer Object (trong Opportunity)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của khách hàng |
| `name` | String | Tên khách hàng |
| `industry` | String | Ngành nghề khách hàng |

#### Sales Object (trong Opportunity)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên sales |
| `name` | String | Tên nhân viên sales |
| `email` | String | Email của nhân viên sales |

#### Leader Object (trong mảng leaders)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của leader |
| `name` | String | Tên leader |
| `assignDate` | String | Ngày được gán vào cơ hội (ISO 8601) |

#### Note Object (trong mảng notes)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của ghi chú |
| `content` | String | Nội dung ghi chú |
| `createdBy` | Object | Thông tin người tạo ghi chú |
| `createdAt` | String | Thời điểm tạo ghi chú (ISO 8601) |

#### CreatedBy Object (trong Note)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `name` | String | Tên người dùng |

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
      "reportName": "Báo cáo danh sách cơ hội",
      "generatedAt": "2025-05-01T11:15:20Z",
      "fromDate": "2024-05-01",
      "toDate": "2025-04-30",
      "filters": {
        "followUpStatus": "red",
        "onsite": true
      }
    },
    "summaryMetrics": {
      "totalOpportunities": 120,
      "byFollowUp": {
        "red": 25,
        "yellow": 35,
        "green": 60
      },
      "byDealStage": {
        "Appointment": 30,
        "Demo": 35,
        "Negotiation": 20,
        "Closed Won": 25,
        "Closed Lost": 10
      },
      "onsitePriority": 45,
      "byCustomer": [
        {"name": "ABC Corporation", "count": 15},
        {"name": "XYZ Inc", "count": 12},
        {"name": "DEF Limited", "count": 10}
      ],
      "bySales": [
        {"name": "Nguyễn Văn X", "count": 30},
        {"name": "Trần Thị Y", "count": 25},
        {"name": "Lê Anh Z", "count": 20}
      ]
    },
    "content": [
      {
        "id": 101,
        "hubspotId": "12345",
        "name": "ABC Corp - Hệ thống quản lý nhân sự",
        "customer": {
          "id": 15,
          "name": "ABC Corporation",
          "industry": "Manufacturing"
        },
        "dealStage": "Negotiation",
        "estimatedValue": 250000000,
        "createdDate": "2025-01-15T08:30:00Z",
        "lastInteractionDate": "2025-03-01T14:20:00Z",
        "followUpStatus": "red",
        "sales": {
          "id": 20,
          "name": "Nguyễn Văn X",
          "email": "x.nguyenvan@company.com"
        },
        "leaders": [
          {
            "id": 5,
            "name": "Trần Văn B",
            "assignDate": "2025-01-20T09:15:00Z"
          }
        ],
        "onsite": true,
        "notes": [
          {
            "id": 201,
            "content": "Khách hàng yêu cầu demo bổ sung tính năng quản lý đào tạo",
            "createdBy": {
              "id": 20,
              "name": "Nguyễn Văn X"
            },
            "createdAt": "2025-03-01T14:20:00Z"
          },
          {
            "id": 200,
            "content": "Gặp khách hàng trao đổi yêu cầu ban đầu",
            "createdBy": {
              "id": 5,
              "name": "Trần Văn B"
            },
            "createdAt": "2025-01-20T15:30:00Z"
          }
        ]
      },
      {
        "id": 102,
        "hubspotId": "12346",
        "name": "XYZ Inc - Phần mềm kế toán",
        "customer": {
          "id": 16,
          "name": "XYZ Inc",
          "industry": "Finance"
        },
        "dealStage": "Demo",
        "estimatedValue": 180000000,
        "createdDate": "2025-02-10T09:45:00Z",
        "lastInteractionDate": "2025-03-05T10:30:00Z",
        "followUpStatus": "red",
        "sales": {
          "id": 21,
          "name": "Trần Thị Y",
          "email": "y.tranthi@company.com"
        },
        "leaders": [
          {
            "id": 8,
            "name": "Phạm Thị D",
            "assignDate": "2025-02-15T14:20:00Z"
          }
        ],
        "onsite": true,
        "notes": [
          {
            "id": 205,
            "content": "Demo phần mềm kế toán phiên bản 1.0",
            "createdBy": {
              "id": 8,
              "name": "Phạm Thị D"
            },
            "createdAt": "2025-03-05T10:30:00Z"
          }
        ]
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 1,
      "totalElements": 25,
      "sort": "lastInteractionDate,desc"
    }
  }
}
```

#### 4.1.1 Response khi exportType=excel hoặc csv - 200 OK

```
Content-Disposition: attachment; filename="opportunity_report_20250501.xlsx"
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
      "field": "dealStage",
      "message": "Giá trị 'Active' không hợp lệ. Các giá trị hợp lệ: Appointment, Demo, Negotiation, Closed Won, Closed Lost"
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
  "message": "Bạn không có quyền xem báo cáo cơ hội này"
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