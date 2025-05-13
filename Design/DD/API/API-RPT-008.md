# API Details: Báo cáo tỷ lệ sử dụng nguồn lực

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API báo cáo tỷ lệ sử dụng nguồn lực | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để tạo báo cáo về tỷ lệ sử dụng nguồn lực nhân sự, giúp người quản lý theo dõi hiệu suất phân bổ nhân viên vào các dự án, phân tích tỷ lệ nhân viên đang làm việc trong các dự án so với tổng số nhân viên sẵn có, hỗ trợ việc tối ưu hóa việc sử dụng nguồn lực.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-008                                  |
| **Tên API**        | Báo cáo tỷ lệ sử dụng nguồn lực              |
| **Mô tả**          | API cung cấp báo cáo chi tiết về tỷ lệ sử dụng nguồn lực nhân sự |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/reports/utilization`                |
| **Quyền truy cập** | report:read:all, report:read:team            |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên                | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|--------------------|----------------------|----------|-------|
| `teamId`           | Integer              | Không    | ID của team cần lọc |
| `leaderId`         | Integer              | Không    | ID của leader cần lọc |
| `employeeId`       | Integer              | Không    | ID của nhân viên cụ thể cần lọc |
| `positionId`       | Integer              | Không    | ID của vị trí/chức danh cần lọc |
| `skillId`          | Integer              | Không    | ID của kỹ năng cần lọc |
| `status`           | String               | Không    | Trạng thái nhân viên: `Allocated`, `PartiallyAllocated`, `Available`, `EndingSoon` |
| `minUtilization`   | Double               | Không    | Tỷ lệ % sử dụng tối thiểu cần lọc |
| `maxUtilization`   | Double               | Không    | Tỷ lệ % sử dụng tối đa cần lọc |
| `periodType`       | String               | Không    | Loại kỳ báo cáo: `currentMonth`, `nextMonth`, `custom` (mặc định: `currentMonth`) |
| `fromDate`         | Date (yyyy-MM-dd)    | Không    | Từ ngày (bắt buộc nếu periodType=`custom`) |
| `toDate`           | Date (yyyy-MM-dd)    | Không    | Đến ngày (bắt buộc nếu periodType=`custom`) |
| `groupBy`          | String               | Không    | Nhóm theo: `team`, `leader`, `position`, `skill` (mặc định: `team`) |
| `includeDetails`   | Boolean              | Không    | Bao gồm chi tiết phân bổ dự án (mặc định: `true`) |
| `exportType`       | String               | Không    | Loại xuất báo cáo: `json`, `csv`, `excel` (mặc định: `json`) |
| `page`             | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`             | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `20`) |
| `sortBy`           | String               | Không    | Trường sắp xếp (mặc định: `utilizationRate`) |
| `sortDir`          | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |

### 3.3 Validate Rule
| Trường            | Điều kiện hợp lệ |
|-------------------|------------------|
| `page`            | ≥ 1              |
| `size`            | 1 → 100          |
| `sortDir`         | `asc`, `desc`    |
| `status`          | Một trong: `Allocated`, `PartiallyAllocated`, `Available`, `EndingSoon` |
| `periodType`      | Một trong: `currentMonth`, `nextMonth`, `custom` |
| `groupBy`         | Một trong: `team`, `leader`, `position`, `skill` |
| `fromDate`        | Định dạng yyyy-MM-dd, ≤ toDate |
| `toDate`          | Định dạng yyyy-MM-dd, ≥ fromDate |
| `minUtilization`  | 0 → 100          |
| `maxUtilization`  | 0 → 100, ≥ minUtilization (nếu có) |
| `exportType`      | Một trong: `json`, `csv`, `excel` |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được báo cáo sử dụng nguồn lực của team mình quản lý
- Division Manager: Xem được báo cáo sử dụng nguồn lực của tất cả team thuộc bộ phận mình quản lý
- Admin: Xem được báo cáo sử dụng nguồn lực của tất cả team

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu báo cáo tỷ lệ sử dụng nguồn lực |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportInfo` | Object | Thông tin tổng quan về báo cáo |
| `summaryMetrics` | Object | Các chỉ số tổng hợp về sử dụng nguồn lực |
| `groups` | Array | Mảng các nhóm (theo team, leader, position hoặc skill) |
| `content` | Array | Mảng các đối tượng nhân viên với thông tin phân bổ |
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
| `type` | String | Loại kỳ báo cáo (currentMonth, nextMonth, custom) |
| `fromDate` | String | Ngày bắt đầu kỳ báo cáo (yyyy-MM-dd) |
| `toDate` | String | Ngày kết thúc kỳ báo cáo (yyyy-MM-dd) |
| `description` | String | Mô tả kỳ báo cáo dưới dạng text |

#### SummaryMetrics Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalEmployees` | Integer | Tổng số nhân viên |
| `fullyAllocated` | Integer | Số nhân viên được phân bổ 100% |
| `partiallyAllocated` | Integer | Số nhân viên được phân bổ một phần |
| `available` | Integer | Số nhân viên sẵn sàng phân bổ (0%) |
| `endingSoon` | Integer | Số nhân viên sắp kết thúc dự án |
| `averageUtilization` | Double | Tỷ lệ sử dụng nguồn lực trung bình (%) |
| `byUtilizationRange` | Object | Phân loại theo mức độ sử dụng |

#### ByUtilizationRange Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `0%` | Integer | Số nhân viên có tỷ lệ sử dụng 0% |
| `1-25%` | Integer | Số nhân viên có tỷ lệ sử dụng 1-25% |
| `26-50%` | Integer | Số nhân viên có tỷ lệ sử dụng 26-50% |
| `51-75%` | Integer | Số nhân viên có tỷ lệ sử dụng 51-75% |
| `76-99%` | Integer | Số nhân viên có tỷ lệ sử dụng 76-99% |
| `100%` | Integer | Số nhân viên có tỷ lệ sử dụng 100% |

#### Group Object (trong mảng groups)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên nhóm (team, leader, position hoặc skill) |
| `id` | Integer | ID của nhóm |
| `totalEmployees` | Integer | Tổng số nhân viên trong nhóm |
| `averageUtilization` | Double | Tỷ lệ sử dụng trung bình trong nhóm (%) |
| `fullyAllocated` | Integer | Số nhân viên được phân bổ 100% trong nhóm |
| `partiallyAllocated` | Integer | Số nhân viên được phân bổ một phần trong nhóm |
| `available` | Integer | Số nhân viên sẵn sàng phân bổ (0%) trong nhóm |
| `endingSoon` | Integer | Số nhân viên sắp kết thúc dự án trong nhóm |

#### EmployeeUtilization Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `employee` | Object | Thông tin nhân viên |
| `utilizationInfo` | Object | Thông tin về sử dụng nguồn lực của nhân viên |

#### Employee Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `code` | String | Mã nhân viên |
| `name` | String | Tên nhân viên |
| `position` | String | Chức danh/vị trí công việc |
| `team` | Object | Thông tin team của nhân viên |
| `leader` | Object | Thông tin leader của nhân viên |

#### Team Object (trong Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Leader Object (trong Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của leader |
| `name` | String | Tên leader |

#### UtilizationInfo Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `utilizationRate` | Double | Tỷ lệ sử dụng tài nguyên (%) |
| `status` | String | Trạng thái phân bổ (Allocated, PartiallyAllocated, Available, EndingSoon) |
| `contracts` | Array | Danh sách hợp đồng/dự án được phân bổ |

#### Contract Object (trong mảng contracts)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng |
| `code` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `customer` | String | Tên khách hàng |
| `allocation` | Integer | Phần trăm phân bổ vào hợp đồng (%) |
| `fromDate` | String | Ngày bắt đầu phân bổ (yyyy-MM-dd) |
| `toDate` | String | Ngày kết thúc phân bổ (yyyy-MM-dd) |
| `role` | String | Vai trò trong dự án |

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
      "reportName": "Báo cáo tỷ lệ sử dụng nguồn lực",
      "generatedAt": "2025-05-01T17:30:15Z",
      "period": {
        "type": "currentMonth",
        "fromDate": "2025-05-01",
        "toDate": "2025-05-31",
        "description": "Tháng 5/2025"
      },
      "filters": {
        "groupBy": "team"
      }
    },
    "summaryMetrics": {
      "totalEmployees": 50,
      "fullyAllocated": 30,
      "partiallyAllocated": 10,
      "available": 8,
      "endingSoon": 2,
      "averageUtilization": 78.5,
      "byUtilizationRange": {
        "0%": 8,
        "1-25%": 2,
        "26-50%": 5,
        "51-75%": 10,
        "76-99%": 5,
        "100%": 20
      }
    },
    "groups": [
      {
        "name": "Team Alpha",
        "id": 1,
        "totalEmployees": 15,
        "averageUtilization": 85.3,
        "fullyAllocated": 10,
        "partiallyAllocated": 3,
        "available": 2,
        "endingSoon": 0
      },
      {
        "name": "Team Beta",
        "id": 2,
        "totalEmployees": 12,
        "averageUtilization": 75.8,
        "fullyAllocated": 8,
        "partiallyAllocated": 2,
        "available": 1,
        "endingSoon": 1
      },
      {
        "name": "Team Gamma",
        "id": 3,
        "totalEmployees": 10,
        "averageUtilization": 90.0,
        "fullyAllocated": 9,
        "partiallyAllocated": 1,
        "available": 0,
        "endingSoon": 0
      }
    ],
    "content": [
      {
        "employee": {
          "id": 101,
          "code": "NV001",
          "name": "Nguyễn Văn A",
          "position": "Senior Developer",
          "team": {
            "id": 1,
            "name": "Team Alpha"
          },
          "leader": {
            "id": 201,
            "name": "Lê Văn Leader"
          }
        },
        "utilizationInfo": {
          "utilizationRate": 100,
          "status": "Allocated",
          "contracts": [
            {
              "id": 301,
              "code": "HD-2025-001",
              "name": "Phát triển phần mềm quản lý nhân sự",
              "customer": "ABC Corporation",
              "allocation": 100,
              "fromDate": "2025-01-15",
              "toDate": "2025-12-31",
              "role": "Lead Developer"
            }
          ]
        }
      },
      {
        "employee": {
          "id": 102,
          "code": "NV002",
          "name": "Trần Thị B",
          "position": "Developer",
          "team": {
            "id": 1,
            "name": "Team Alpha"
          },
          "leader": {
            "id": 201,
            "name": "Lê Văn Leader"
          }
        },
        "utilizationInfo": {
          "utilizationRate": 80,
          "status": "PartiallyAllocated",
          "contracts": [
            {
              "id": 302,
              "code": "HD-2025-002",
              "name": "Bảo trì hệ thống kế toán",
              "customer": "XYZ Inc",
              "allocation": 50,
              "fromDate": "2025-02-01",
              "toDate": "2026-01-31",
              "role": "Developer"
            },
            {
              "id": 305,
              "code": "HD-2025-005",
              "name": "Phát triển ứng dụng di động",
              "customer": "PQR Corp",
              "allocation": 30,
              "fromDate": "2025-04-01",
              "toDate": "2025-07-31",
              "role": "Mobile Developer"
            }
          ]
        }
      },
      {
        "employee": {
          "id": 103,
          "code": "NV003",
          "name": "Phạm Văn C",
          "position": "Tester",
          "team": {
            "id": 2,
            "name": "Team Beta"
          },
          "leader": {
            "id": 202,
            "name": "Trần Thị Manager"
          }
        },
        "utilizationInfo": {
          "utilizationRate": 50,
          "status": "PartiallyAllocated",
          "contracts": [
            {
              "id": 310,
              "code": "HD-2025-010",
              "name": "Nâng cấp hệ thống ERP",
              "customer": "MNO Ltd",
              "allocation": 50,
              "fromDate": "2025-03-15",
              "toDate": "2025-09-30",
              "role": "Test Lead"
            }
          ]
        }
      },
      {
        "employee": {
          "id": 104,
          "code": "NV004",
          "name": "Lê Thị D",
          "position": "Business Analyst",
          "team": {
            "id": 3,
            "name": "Team Gamma"
          },
          "leader": {
            "id": 203,
            "name": "Hoàng Văn Director"
          }
        },
        "utilizationInfo": {
          "utilizationRate": 0,
          "status": "Available",
          "contracts": []
        }
      },
      {
        "employee": {
          "id": 105,
          "code": "NV005",
          "name": "Hoàng Văn E",
          "position": "Developer",
          "team": {
            "id": 2,
            "name": "Team Beta"
          },
          "leader": {
            "id": 202,
            "name": "Trần Thị Manager"
          }
        },
        "utilizationInfo": {
          "utilizationRate": 100,
          "status": "EndingSoon",
          "contracts": [
            {
              "id": 320,
              "code": "HD-2025-020",
              "name": "Phát triển website bán hàng",
              "customer": "RST Company",
              "allocation": 100,
              "fromDate": "2025-04-01",
              "toDate": "2025-05-15",
              "role": "Frontend Developer"
            }
          ]
        }
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 20,
      "totalPages": 3,
      "totalElements": 50,
      "sort": "utilizationRate,desc"
    }
  }
}
```

#### 4.1.1 Response khi exportType=excel hoặc csv - 200 OK

```
Content-Disposition: attachment; filename="utilization_report_20250501.xlsx"
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
      "field": "periodType",
      "message": "Giá trị 'quartely' không được hỗ trợ. Các giá trị hợp lệ: currentMonth, nextMonth, custom"
    },
    {
      "field": "fromDate",
      "message": "Bắt buộc khi periodType là 'custom'"
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
  "message": "Bạn không có quyền xem báo cáo sử dụng nguồn lực này"
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