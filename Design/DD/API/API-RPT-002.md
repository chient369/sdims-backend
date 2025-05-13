# API Details: Báo cáo chi tiết danh sách nhân viên

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-06-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để Leader, Trưởng bộ phận hoặc Admin có thể truy xuất báo cáo chi tiết về danh sách nhân viên, kèm theo các thông tin về kỹ năng, trạng thái phân bổ dự án và các chỉ số tổng hợp khác, hỗ trợ cho việc quản lý và phân bổ nguồn lực nhân sự.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-RPT-002                                  |
| **Tên API**        | Báo cáo chi tiết danh sách nhân viên         |
| **Mô tả**          | API cung cấp báo cáo chi tiết danh sách nhân viên kèm theo thông tin kỹ năng và trạng thái |
| **Module**         | Dashboard & Báo cáo                          |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/reports/employee-list`              |
| **Quyền truy cập** | report:read:all, report:read:team, report:read:own |

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
| `position`     | String               | Không    | Vị trí công việc (Developer, Tester, BA, ...) |
| `status`       | String               | Không    | Trạng thái: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `skills`       | Array of Integer     | Không    | Danh sách ID kỹ năng cần lọc |
| `minExperience`| Integer              | Không    | Số năm kinh nghiệm tối thiểu |
| `projectId`    | Integer              | Không    | Lọc theo dự án hiện tại |
| `utilization`  | String               | Không    | Lọc theo mức độ sử dụng (>80%, <50% etc.) |
| `includeSkills`| Boolean              | Không    | Bao gồm chi tiết kỹ năng trong kết quả (mặc định: `true`) |
| `includeProjects`| Boolean            | Không    | Bao gồm chi tiết dự án hiện tại trong kết quả (mặc định: `true`) |
| `exportType`   | String               | Không    | Loại xuất báo cáo: `json`, `csv`, `excel` (mặc định: `json`) |
| `page`         | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`         | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `50`) |
| `sortBy`       | String               | Không    | Trường sắp xếp (mặc định: `name`) |
| `sortDir`      | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `asc`) |

### 3.3 Validate Rule
| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `teamId`       | Phải tồn tại trong hệ thống (nếu có) |
| `projectId`    | Phải tồn tại trong hệ thống (nếu có) |
| `page`         | ≥ 1              |
| `size`         | 1 → 500          |
| `sortBy`       | Một trong các trường của đối tượng employee |
| `sortDir`      | `asc`, `desc`    |
| `status`       | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `exportType`   | Một trong: `json`, `csv`, `excel` |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được báo cáo nhân viên thuộc team mình quản lý
- Division Manager: Xem được báo cáo nhân viên thuộc bộ phận mình quản lý, bao gồm tất cả các team
- Admin: Xem được báo cáo của tất cả nhân viên trong hệ thống

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu báo cáo nhân viên |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportInfo` | Object | Thông tin tổng quan về báo cáo |
| `content` | Array | Mảng các đối tượng nhân viên |
| `summaryMetrics` | Object | Các chỉ số tổng hợp |
| `pageable` | Object | Thông tin phân trang |

#### ReportInfo Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `reportName` | String | Tên báo cáo |
| `generatedAt` | String | Thời điểm tạo báo cáo (ISO 8601) |
| `filters` | Object | Các bộ lọc đã áp dụng |

#### Employee Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `email` | String | Địa chỉ email công ty của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `status` | String | Trạng thái phân bổ nhân viên |
| `currentProject` | Object | Thông tin dự án hiện tại |
| `utilization` | Integer | Tỷ lệ sử dụng (0-100%) |
| `skills` | Array | Mảng các kỹ năng của nhân viên |
| `joinDate` | String | Ngày tham gia công ty (yyyy-MM-dd) |
| `totalExperience` | Integer | Tổng số năm kinh nghiệm |

#### Team Object (trong Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |
| `leader` | Object | Thông tin người quản lý team |

#### Leader Object (trong Team)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của leader |
| `name` | String | Tên leader |

#### Project Object (trong Employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của dự án |
| `name` | String | Tên dự án |
| `customer` | String | Tên khách hàng |
| `allocation` | Integer | Tỷ lệ phân bổ nhân viên cho dự án (%) |
| `startDate` | String | Ngày bắt đầu tham gia dự án (yyyy-MM-dd) |
| `endDate` | String | Ngày kết thúc dự án dự kiến (yyyy-MM-dd) |

#### Skill Object (trong mảng skills)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `category` | String | Danh mục kỹ năng |
| `level` | String | Trình độ (Beginner, Intermediate, Advanced, Expert) |
| `years` | Integer | Số năm kinh nghiệm với kỹ năng |

#### SummaryMetrics Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalEmployees` | Integer | Tổng số nhân viên |
| `allocatedCount` | Integer | Số nhân viên đã được phân bổ dự án |
| `availableCount` | Integer | Số nhân viên đang sẵn sàng |
| `endingSoonCount` | Integer | Số nhân viên sắp kết thúc dự án |
| `utilizationRate` | Double | Tỷ lệ sử dụng trung bình (%) |
| `topSkills` | Array | Danh sách kỹ năng phổ biến nhất |

#### TopSkill Object (trong mảng topSkills)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `name` | String | Tên kỹ năng |
| `count` | Integer | Số nhân viên có kỹ năng |

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
      "reportName": "Báo cáo danh sách nhân viên",
      "generatedAt": "2025-05-01T10:30:45Z",
      "filters": {
        "teamId": 1,
        "position": "Developer"
      }
    },
    "content": [
      {
        "id": 1,
        "employeeCode": "NV001",
        "name": "Nguyễn Văn A",
        "email": "a.nguyenvan@company.com",
        "position": "Developer",
        "team": {
          "id": 1,
          "name": "Team Alpha",
          "leader": {
            "id": 5,
            "name": "Trần Văn B"
          }
        },
        "status": "Allocated",
        "currentProject": {
          "id": 10,
          "name": "Project XYZ",
          "customer": "ABC Corporation",
          "allocation": 100,
          "startDate": "2025-01-15",
          "endDate": "2025-12-31"
        },
        "utilization": 100,
        "skills": [
          {
            "id": 1,
            "name": "Java",
            "category": "Programming Language",
            "level": "Advanced",
            "years": 5
          },
          {
            "id": 2,
            "name": "Spring Boot",
            "category": "Framework",
            "level": "Intermediate",
            "years": 3
          },
          {
            "id": 8,
            "name": "Japanese N2",
            "category": "Language",
            "level": "Intermediate",
            "years": 4
          }
        ],
        "joinDate": "2020-05-10",
        "totalExperience": 5
      },
      {
        "id": 2,
        "employeeCode": "NV002",
        "name": "Lê Thị C",
        "email": "c.lethi@company.com",
        "position": "Developer",
        "team": {
          "id": 1,
          "name": "Team Alpha",
          "leader": {
            "id": 5,
            "name": "Trần Văn B"
          }
        },
        "status": "EndingSoon",
        "currentProject": {
          "id": 11,
          "name": "Project DEF",
          "customer": "DEF Limited",
          "allocation": 100,
          "startDate": "2024-10-01",
          "endDate": "2025-05-31"
        },
        "utilization": 100,
        "skills": [
          {
            "id": 3,
            "name": "React",
            "category": "Framework",
            "level": "Advanced",
            "years": 4
          },
          {
            "id": 4,
            "name": "TypeScript",
            "category": "Programming Language",
            "level": "Advanced",
            "years": 4
          }
        ],
        "joinDate": "2021-02-15",
        "totalExperience": 4
      }
    ],
    "summaryMetrics": {
      "totalEmployees": 45,
      "allocatedCount": 38,
      "availableCount": 3,
      "endingSoonCount": 4,
      "utilizationRate": 84.5,
      "topSkills": [
        {"name": "Java", "count": 20},
        {"name": "React", "count": 15},
        {"name": "Japanese N2+", "count": 12}
      ]
    },
    "pageable": {
      "pageNumber": 1,
      "pageSize": 50,
      "totalPages": 1,
      "totalElements": 45,
      "sort": "name,asc"
    }
  }
}
```

#### 4.1.1 Response khi exportType=excel hoặc csv - 200 OK

```
Content-Disposition: attachment; filename="employee_report_20250501.xlsx"
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
  "message": "Bạn không có quyền xem báo cáo này"
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