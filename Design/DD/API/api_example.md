# API Details: Lấy danh sách nhân sự

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu mô tả chi tiết về API lấy danh sách nhân sự, bao gồm cách sử dụng, tham số, và định dạng dữ liệu trả về.

---

## 1. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | HRM-001                                      |
| **Tên API**        | Lấy danh sách nhân sự                        |
| **Mô tả**          | API cho phép lấy danh sách nhân sự với các bộ lọc và phân trang |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/employees`                          |
| **Quyền truy cập** | Leader, 課長, Admin                          |

---

## 2. Parameters

### 2.1 Query Parameters

| Tên            | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|----------------|----------------------|----------|-------|
| `keyword`      | String               | Không    | Tìm theo tên hoặc mã nhân viên |
| `teamId`       | Integer              | Không    | ID của team cần lọc |
| `position`     | String               | Không    | Vị trí công việc (Developer, Tester, BA, ...) |
| `status`       | String               | Không    | Trạng thái: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
| `skills`       | Array of Integer     | Không    | Danh sách ID kỹ năng cần lọc |
| `minExperience`| Integer              | Không    | Số năm kinh nghiệm tối thiểu |
| `page`         | Integer              | Không    | Trang cần lấy (mặc định: `1`) |
| `size`         | Integer              | Không    | Số bản ghi mỗi trang (mặc định: `10`) |
| `sortBy`       | String               | Không    | Trường sắp xếp (mặc định: `name`) |
| `sortDir`      | String               | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `asc`) |


### 2.2 Validate Rule
| Trường      | Điều kiện hợp lệ |
|-------------|------------------|
| `page`      | ≥ 1              |
| `size`      | 1 → 100          |
| `sortDir`   | `asc`, `desc`    |
| `status`    | Một trong: `Allocated`, `Available`, `EndingSoon`, `OnLeave`, `Resigned` |
---

## 3. Response

### 3.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu nhân sự và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Mảng các đối tượng nhân sự |
| `pageable` | Object | Thông tin phân trang |

#### Employee Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `employeeCode` | String | Mã nhân viên |
| `name` | String | Họ tên đầy đủ của nhân viên |
| `email` | String | Địa chỉ email công ty của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `status` | String | Trạng thái phân bổ nhân viên (Allocated, Available, EndingSoon, OnLeave, Resigned) |
| `currentProject` | String | Dự án hiện tại nhân viên đang tham gia |
| `utilization` | Integer | Tỷ lệ sử dụng (0-100%) |
| `endDate` | Date | Ngày kết thúc dự án dự kiến (yyyy-MM-dd) |
| `skills` | Array | Mảng các kỹ năng của nhân viên |

#### Team Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Skill Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng |
| `level` | String | Trình độ (Beginner, Intermediate, Advanced, Expert) |
| `years` | Integer | Số năm kinh nghiệm với kỹ năng |

#### Pageable Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `pageNumber` | Integer | Số trang hiện tại |
| `pageSize` | Integer | Kích thước trang (số bản ghi mỗi trang) |
| `totalPages` | Integer | Tổng số trang |
| `totalElements` | Integer | Tổng số bản ghi |
| `sort` | String | Thông tin sắp xếp (trường,hướng) |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "content": [
      {
        "id": 1,
        "employeeCode": "NV001",
        "name": "Nguyễn Văn A",
        "email": "a.nguyenvan@company.com",
        "position": "Developer",
        "team": {
          "id": 1,
          "name": "Team Alpha"
        },
        "status": "Allocated",
        "currentProject": "Project XYZ",
        "utilization": 100,
        "endDate": "2025-12-31",
        "skills": [
          {
            "id": 1,
            "name": "Java",
            "level": "Advanced",
            "years": 5
          },
          {
            "id": 2,
            "name": "Spring Boot",
            "level": "Intermediate",
            "years": 3
          }
        ]
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 10,
      "totalPages": 5,
      "totalElements": 45,
      "sort": "name,asc"
    }
  }
}
```
### 3.2 Error Responses
#### 400 Bad Request
```json
{
  "status": "error",
  "code": 400,
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "size",
      "message": "Kích thước trang phải nhỏ hơn hoặc bằng 100"
    }
  ]
}
```
<Các lỗi còn lại>

####
