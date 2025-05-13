# API Details: Gợi ý nhân viên theo kỹ năng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp khả năng gợi ý các nhân viên phù hợp dựa trên bộ kỹ năng yêu cầu, giúp quản lý dễ dàng tìm được nguồn lực phù hợp cho các dự án mới.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-006                                  |
| **Tên API**        | Gợi ý nhân viên theo kỹ năng                 |
| **Mô tả**          | API gợi ý nhân viên phù hợp dựa trên yêu cầu về kỹ năng |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/employees/search/suggest`           |
| **Quyền truy cập** | employee-suggest:read                              |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên             | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|-----------------|------------------|----------|-------|
| `skills`        | Array of Integer | Có       | Danh sách ID các kỹ năng yêu cầu |
| `minExperience` | Integer          | Không    | Số năm kinh nghiệm tối thiểu cho các kỹ năng |
| `minLevel`      | String           | Không    | Cấp độ tối thiểu: `Basic`, `Intermediate`, `Advanced` |
| `status`        | String           | Không    | Chỉ tìm nhân viên có trạng thái này (mặc định: `Available`) |
| `limit`         | Integer          | Không    | Số lượng nhân viên tối đa cần gợi ý (mặc định: `5`) |
| `teamId`        | Integer          | Không    | Chỉ tìm nhân viên trong team này |
| `strict`        | Boolean          | Không    | Nếu `true`, chỉ lấy nhân viên có tất cả kỹ năng yêu cầu; nếu `false`, lấy cả nhân viên có một phần kỹ năng yêu cầu (mặc định: `false`) |

### 3.3 Validate Rule

| Trường          | Điều kiện hợp lệ |
|-----------------|------------------|
| `skills`        | Phải có ít nhất 1 kỹ năng |
| `minExperience` | ≥ 0 |
| `minLevel`      | Một trong: `Basic`, `Intermediate`, `Advanced` |
| `status`        | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `limit`         | 1 → 20 |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa kết quả gợi ý nhân viên |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `suggestions` | Array | Mảng các đối tượng nhân viên được gợi ý |

#### Suggestion Object (trong mảng suggestions)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `email` | String | Địa chỉ email công ty của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `status` | String | Trạng thái phân bổ nhân viên (Allocated, Available, EndingSoon, OnLeave, Resigned) |
| `endDate` | String | Ngày kết thúc dự án (nếu status = EndingSoon, định dạng: YYYY-MM-DD) |
| `matchingScore` | Integer | Điểm phù hợp với yêu cầu (0-100%) |
| `matchingSkills` | Array | Mảng các kỹ năng phù hợp với yêu cầu |
| `missingSkills` | Array | Mảng các kỹ năng còn thiếu so với yêu cầu |

#### Team Object (trong suggestion)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Matching Skill Object (trong mảng matchingSkills)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `level` | String | Trình độ (Basic, Intermediate, Advanced) |
| `years` | Integer | Số năm kinh nghiệm với kỹ năng |
| `required` | Boolean | Cờ đánh dấu kỹ năng có nằm trong yêu cầu hay không |

#### Missing Skill Object (trong mảng missingSkills)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `required` | Boolean | Cờ đánh dấu kỹ năng yêu cầu |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "suggestions": [
      {
        "id": 12,
        "employeeCode": "NV012",
        "name": "Hoàng Văn F",
        "email": "f.hoangvan@company.com",
        "position": "Developer",
        "team": {
          "id": 2,
          "name": "Team Beta"
        },
        "status": "Available",
        "matchingScore": 95,
        "matchingSkills": [
          {
            "id": 1,
            "name": "Java",
            "level": "Advanced",
            "years": 5,
            "required": true
          },
          {
            "id": 2,
            "name": "Spring Boot",
            "level": "Advanced",
            "years": 4,
            "required": true
          },
          {
            "id": 3,
            "name": "MySQL",
            "level": "Intermediate",
            "years": 3,
            "required": true
          }
        ],
        "missingSkills": []
      },
      {
        "id": 8,
        "employeeCode": "NV008",
        "name": "Lý Thị G",
        "email": "g.lythi@company.com",
        "position": "Developer",
        "team": {
          "id": 1,
          "name": "Team Alpha"
        },
        "status": "EndingSoon",
        "endDate": "2025-06-15",
        "matchingScore": 85,
        "matchingSkills": [
          {
            "id": 1,
            "name": "Java",
            "level": "Advanced",
            "years": 6,
            "required": true
          },
          {
            "id": 2,
            "name": "Spring Boot",
            "level": "Intermediate",
            "years": 3,
            "required": true
          }
        ],
        "missingSkills": [
          {
            "id": 3,
            "name": "MySQL",
            "required": true
          }
        ]
      }
    ]
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2001",
  "message": "Thiếu tham số bắt buộc",
  "errors": [
    {
      "field": "skills",
      "message": "Phải có ít nhất một kỹ năng yêu cầu"
    }
  ]
}
```

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1000",
  "message": "Token không hợp lệ hoặc đã hết hạn"
}
```

#### 403 Forbidden
```json
{
  "status": "error",
  "code": "E1002",
  "message": "Không có quyền truy cập chức năng này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3006",
  "message": "Không tìm thấy kỹ năng với ID: 999"
}
``` 