# API Details: Gán Leader vào cơ hội

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API gán Leader vào cơ hội | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để Sales hoặc Trưởng bộ phận có thể gán một Leader vào cơ hội kinh doanh, nhằm bắt đầu quá trình hỗ trợ presales và theo dõi cơ hội theo quy trình nội bộ.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-OPP-005                                  |
| **Tên API**        | Gán Leader vào cơ hội                        |
| **Mô tả**          | API cho phép gán Leader vào cơ hội kinh doanh để hỗ trợ presales |
| **Module**         | Quản lý Cơ hội Kinh doanh                    |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/opportunities/{oppId}/assign`       |
| **Quyền truy cập** | opportunity-assign:update:all                           |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên         | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-------------|--------------|----------|-------|
| `oppId`     | Integer      | Có       | ID của cơ hội kinh doanh cần gán Leader |

### 3.3 Request Body

```json
{
  "leaderId": 8,
  "note": "Yêu cầu hỗ trợ presales cho khách hàng Công ty ABC. Có kinh nghiệm CRM và Java là lợi thế.",
  "notifyLeader": true,
  "notifySales": true
}
```

### 3.4 Body Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `leaderId`      | Integer      | Có       | ID của Leader được gán vào cơ hội |
| `note`          | String       | Không    | Ghi chú kèm theo khi gán Leader |
| `notifyLeader`  | Boolean      | Không    | Có gửi thông báo cho Leader không (mặc định: `true`) |
| `notifySales`   | Boolean      | Không    | Có gửi thông báo cho Sales không (mặc định: `true`) |

### 3.5 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `oppId`        | Số nguyên dương, phải tồn tại trong hệ thống |
| `leaderId`     | Số nguyên dương, phải là ID của người dùng có vai trò Leader và tồn tại trong hệ thống |
| `note`         | Tối đa 500 ký tự |
| `notifyLeader` | Boolean: `true` hoặc `false` |
| `notifySales`  | Boolean: `true` hoặc `false` |

### 3.6 Phân quyền đặc biệt
- Theo ma trận CRUD, người dùng có quyền `opportunity:assign` là Sales, Division Manager và Admin
- Sales: Chỉ có thể gán Leader vào các cơ hội do mình tạo hoặc phụ trách
- Division Manager: Có thể gán Leader vào bất kỳ cơ hội nào thuộc bộ phận mình quản lý

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin sau khi gán Leader cho cơ hội |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `opportunity` | Object | Thông tin cơ hội sau khi được gán Leader |
| `notification` | Object | Thông tin về trạng thái gửi thông báo |
| `activityLogged` | Boolean | Đã ghi nhật ký hoạt động hay chưa |

#### Opportunity Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội kinh doanh |
| `code` | String | Mã cơ hội (tự động sinh) |
| `name` | String | Tên cơ hội kinh doanh |
| `assignedTo` | Object | Thông tin Leader được gán vào cơ hội |
| `previouslyAssignedTo` | Object | Thông tin Leader trước đó (null nếu chưa từng gán) |
| `assignedAt` | String | Thời điểm gán Leader (ISO 8601) |
| `assignedBy` | Object | Thông tin người thực hiện gán Leader |

#### User Object (trong assignedTo, previouslyAssignedTo, assignedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `name` | String | Tên đầy đủ của người dùng |
| `email` | String | Địa chỉ email của người dùng (chỉ có trong assignedTo) |
| `position` | String | Vị trí công việc (chỉ có trong assignedTo) |

#### Notification Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `leaderNotified` | Boolean | Đã gửi thông báo cho Leader hay chưa |
| `salesNotified` | Boolean | Đã gửi thông báo cho Sales hay chưa |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "opportunity": {
      "id": 134,
      "code": "OPP-2025050134",
      "name": "Hệ thống CRM cho công ty ABC",
      "assignedTo": {
        "id": 8,
        "name": "Lê Thị Leader",
        "email": "leader@company.com",
        "position": "Team Leader"
      },
      "previouslyAssignedTo": null,
      "assignedAt": "2025-05-16T10:30:45Z",
      "assignedBy": {
        "id": 5,
        "name": "Trần Văn Sales"
      }
    },
    "notification": {
      "leaderNotified": true,
      "salesNotified": true
    },
    "activityLogged": true
  }
}
```

### 4.2 Error Responses

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
      "field": "leaderId",
      "message": "Leader không tồn tại trong hệ thống"
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
  "message": "Bạn không có quyền truy cập chức năng này"
}
```

#### 404 Not Found

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E3002 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

```json
{
  "status": "error",
  "code": "E3002",
  "message": "Không tìm thấy cơ hội kinh doanh",
  "errors": [
    {
      "field": "oppId",
      "message": "Không tìm thấy cơ hội với ID: 999"
    }
  ]
}
```

#### 409 Conflict

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E4004 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |
| `data` | Object | Đối tượng chứa thông tin bổ sung về xung đột |

#### Conflict Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `assignedAt` | String | Thời điểm gán Leader trước đó (ISO 8601) |
| `assignedBy` | Object | Thông tin người gán Leader trước đó |

```json
{
  "status": "error",
  "code": "E4004",
  "message": "Xung đột dữ liệu",
  "errors": [
    {
      "field": "leaderId",
      "message": "Leader này đã được gán vào cơ hội"
    }
  ],
  "data": {
    "assignedAt": "2025-05-15T14:22:45Z",
    "assignedBy": {
      "id": 3,
      "name": "Trưởng Phòng Lê"
    }
  }
}
``` 