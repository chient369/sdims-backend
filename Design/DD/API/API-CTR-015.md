# API Details: Lấy danh sách KPI doanh thu

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API lấy danh sách KPI doanh thu | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để truy xuất danh sách các chỉ tiêu KPI doanh thu đã được thiết lập cho nhân viên Sales, cho phép theo dõi và so sánh mục tiêu với kết quả thực tế theo các kỳ báo cáo khác nhau (năm, quý, tháng), hỗ trợ việc đánh giá hiệu suất kinh doanh.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-015                                  |
| **Tên API**        | Lấy danh sách KPI doanh thu                  |
| **Mô tả**          | API cho phép lấy danh sách KPI doanh thu đã thiết lập với khả năng lọc theo Sales và kỳ báo cáo |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/sales-kpis`                         |
| **Quyền truy cập** | sales-kpi:read:all, sales-kpi:read:own       |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `year`         | Integer      | Không    | Năm cần lấy KPI (mặc định: năm hiện tại) |
| `quarter`      | Integer      | Không    | Quý cần lấy KPI (từ 1-4) |
| `month`        | Integer      | Không    | Tháng cần lấy KPI (từ 1-12) |
| `salesId`      | Long         | Không    | ID của nhân viên Sales cần lấy KPI |
| `teamId`       | Long         | Không    | ID của team cần lấy KPI |
| `page`         | Integer      | Không    | Trang cần lấy (mặc định: 1) |
| `size`         | Integer      | Không    | Số bản ghi mỗi trang (mặc định: 10) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ                     |
|----------------|------------------------------------- |
| `year`         | Năm hợp lệ (VD: 2025, 2026...)      |
| `quarter`      | Số nguyên từ 1 đến 4                |
| `month`        | Số nguyên từ 1 đến 12               |
| `salesId`      | Phải là ID nhân viên Sales tồn tại trong hệ thống |
| `page`         | Số nguyên dương                     |
| `size`         | Số nguyên từ 1 đến 100              |

### 3.4 Phân quyền đặc biệt
- Sales: Chỉ xem được KPI của chính mình
- Team Leader: Xem được KPI của tất cả Sales trong team mình quản lý
- Division Manager: Xem được KPI của tất cả Sales thuộc bộ phận mình quản lý
- Admin: Xem được KPI của tất cả Sales

### 3.5 Business Rule

- Nếu không chỉ định `year`, hệ thống sẽ lấy KPI của năm hiện tại
- Nếu chỉ định cả `quarter` và `month`, hệ thống sẽ ưu tiên lọc theo `quarter`
- Hệ thống hỗ trợ KPI theo nhiều chu kỳ:
  - KPI theo năm
  - KPI theo quý
  - KPI theo tháng
- Ngoài KPI mục tiêu, hệ thống cũng trả về doanh thu thực tế đã đạt được trong kỳ

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin về danh sách KPI doanh thu |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `kpis` | Array | Danh sách các KPI doanh thu |
| `summary` | Object | Thông tin tóm tắt về KPI doanh thu |
| `pageable` | Object | Thông tin phân trang |

#### KPI Object (trong mảng kpis)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi KPI |
| `year` | Integer | Năm áp dụng KPI |
| `quarter` | Integer/null | Quý áp dụng KPI (1-4, null nếu là KPI theo năm) |
| `month` | Integer/null | Tháng áp dụng KPI (1-12, null nếu là KPI theo năm hoặc quý) |
| `salesId` | Integer | ID của nhân viên Sales |
| `salesCode` | String | Mã nhân viên Sales |
| `salesName` | String | Tên nhân viên Sales |
| `teamId` | Integer | ID của team |
| `teamName` | String | Tên team |
| `targetRevenue` | Number | Doanh thu mục tiêu (VND) |
| `actualRevenue` | Number | Doanh thu thực tế đạt được (VND) |
| `achievement` | Number | Tỷ lệ hoàn thành (%, được tính bằng actualRevenue/targetRevenue*100) |
| `status` | String | Trạng thái KPI (IN_PROGRESS, ACHIEVED, MISSED) |
| `note` | String | Ghi chú về KPI |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalKPIs` | Integer | Tổng số KPI được trả về |
| `totalTargetRevenue` | Number | Tổng doanh thu mục tiêu (VND) |
| `totalActualRevenue` | Number | Tổng doanh thu thực tế (VND) |
| `overallAchievement` | Number | Tỷ lệ hoàn thành tổng thể (%) |

#### Pageable Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `pageNumber` | Integer | Số trang hiện tại |
| `pageSize` | Integer | Số bản ghi mỗi trang |
| `totalPages` | Integer | Tổng số trang |
| `totalElements` | Integer | Tổng số bản ghi |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "kpis": [
      {
        "id": 1,
        "year": 2025,
        "quarter": 2,
        "month": null,
        "salesId": 201,
        "salesCode": "SL001",
        "salesName": "Nguyễn Văn Sales",
        "teamId": 5,
        "teamName": "Team Sales Alpha",
        "targetRevenue": 500000000,
        "actualRevenue": 420000000,
        "achievement": 84,
        "status": "IN_PROGRESS",
        "note": "KPI quý 2/2025"
      },
      {
        "id": 2,
        "year": 2025,
        "quarter": 2,
        "month": 4,
        "salesId": 201,
        "salesCode": "SL001",
        "salesName": "Nguyễn Văn Sales",
        "teamId": 5,
        "teamName": "Team Sales Alpha",
        "targetRevenue": 150000000,
        "actualRevenue": 160000000,
        "achievement": 106.67,
        "status": "ACHIEVED",
        "note": "KPI tháng 4/2025"
      },
      {
        "id": 3,
        "year": 2025,
        "quarter": 2,
        "month": 5,
        "salesId": 201,
        "salesCode": "SL001",
        "salesName": "Nguyễn Văn Sales",
        "teamId": 5,
        "teamName": "Team Sales Alpha",
        "targetRevenue": 170000000,
        "actualRevenue": 150000000,
        "achievement": 88.24,
        "status": "IN_PROGRESS",
        "note": "KPI tháng 5/2025"
      }
    ],
    "summary": {
      "totalKPIs": 3,
      "totalTargetRevenue": 820000000,
      "totalActualRevenue": 730000000,
      "overallAchievement": 89.02
    },
    "pageable": {
      "pageNumber": 1,
      "pageSize": 10,
      "totalPages": 1,
      "totalElements": 3
    }
  }
}
```

### 4.2 Error Responses

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
  "message": "Bạn không có quyền xem KPI của nhân viên Sales khác"
}
```

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "quarter",
      "message": "Quý phải là số nguyên từ 1 đến 4"
    }
  ]
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3000",
  "message": "Không tìm thấy nhân viên Sales với ID: 999"
}
``` 