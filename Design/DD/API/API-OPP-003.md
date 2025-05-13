# API Details: Kích hoạt đồng bộ thủ công từ Hubspot

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn |Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để Admin hoặc Trưởng bộ phận có thể kích hoạt thủ công quá trình đồng bộ dữ liệu cơ hội kinh doanh từ Hubspot vào hệ thống, với các tùy chọn về chế độ và phạm vi đồng bộ.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-OPP-003                                  |
| **Tên API**        | Kích hoạt đồng bộ thủ công từ Hubspot        |
| **Mô tả**          | API cho phép kích hoạt thủ công việc đồng bộ dữ liệu cơ hội từ Hubspot |
| **Module**         | Quản lý Cơ hội Kinh doanh                    |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/opportunities/sync`                 |
| **Quyền truy cập** | opportunities:sync                           |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Request Body

```json
{
  "syncMode": "incremental",
  "fromDate": "2025-05-01",
  "toDate": "2025-05-31",
  "dealStage": "all",
  "overwriteExisting": false
}
```

### 3.3 Body Parameters

| Tên                  | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------------|--------------|----------|-------|
| `syncMode`           | String       | Không    | Chế độ đồng bộ: `incremental` (mặc định) hoặc `full` |
| `fromDate`           | String       | Không    | Ngày bắt đầu khoảng thời gian cần đồng bộ (định dạng: YYYY-MM-DD) |
| `toDate`             | String       | Không    | Ngày kết thúc khoảng thời gian cần đồng bộ (định dạng: YYYY-MM-DD) |
| `dealStage`          | String       | Không    | Trạng thái deal cần đồng bộ: `all` (mặc định), `open`, `closed_won`, `closed_lost` |
| `overwriteExisting`  | Boolean      | Không    | Có ghi đè lên dữ liệu đã tồn tại không (mặc định: `false`) |

### 3.4 Validate Rule

| Trường               | Điều kiện hợp lệ |
|----------------------|------------------|
| `syncMode`           | Một trong: `incremental`, `full` |
| `fromDate`           | - Định dạng: YYYY-MM-DD<br>- Không được là ngày trong tương lai<br>- Tối đa 365 ngày trước ngày hiện tại |
| `toDate`             | - Định dạng: YYYY-MM-DD<br>- Không được là ngày trong tương lai<br>- Phải sau hoặc bằng `fromDate` (nếu cả hai được cung cấp) |
| `dealStage`          | Một trong: `all`, `open`, `closed_won`, `closed_lost` |
| `overwriteExisting`  | Boolean: `true` hoặc `false` |

### 3.5 Phân quyền đặc biệt
- Chỉ người dùng có quyền `opportunities:sync` mới được kích hoạt đồng bộ
- Theo ma trận CRUD, chỉ Admin và Division Manager có quyền này
- Việc đồng bộ có thể tạo tải cho hệ thống, nên cần giới hạn tần suất sử dụng

---

## 4. Response

### 4.1 Success - 202 Accepted

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 202 |
| `data` | Object | Đối tượng chứa thông tin về tiến trình đồng bộ |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `syncId` | String | Mã định danh duy nhất của tiến trình đồng bộ |
| `message` | String | Thông báo mô tả tình trạng của tiến trình |
| `status` | String | Trạng thái hiện tại của tiến trình đồng bộ (queued, processing, completed, failed) |
| `estimatedTime` | Integer | Thời gian ước tính để hoàn thành tiến trình đồng bộ (giây) |
| `syncParams` | Object | Tham số đồng bộ đã sử dụng |
| `logsUrl` | String | URL để xem log của tiến trình đồng bộ |

#### SyncParams Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `syncMode` | String | Chế độ đồng bộ đã chọn |
| `fromDate` | String | Ngày bắt đầu khoảng thời gian đồng bộ |
| `toDate` | String | Ngày kết thúc khoảng thời gian đồng bộ |
| `dealStage` | String | Trạng thái deal đã chọn để đồng bộ |
| `overwriteExisting` | Boolean | Cài đặt ghi đè dữ liệu đã chọn |

```json
{
  "status": "success",
  "code": 202,
  "data": {
    "syncId": "SYNC-20250531-123456",
    "message": "Quá trình đồng bộ đã được khởi tạo",
    "status": "queued",
    "estimatedTime": 120,
    "syncParams": {
      "syncMode": "incremental",
      "fromDate": "2025-05-01",
      "toDate": "2025-05-31",
      "dealStage": "all",
      "overwriteExisting": false
    },
    "logsUrl": "/api/v1/opportunities/sync/logs"
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
      "field": "syncMode",
      "message": "Chế độ đồng bộ 'partial' không hợp lệ. Các giá trị hợp lệ: incremental, full"
    },
    {
      "field": "fromDate",
      "message": "Định dạng ngày không hợp lệ. Yêu cầu định dạng YYYY-MM-DD"
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

#### 409 Conflict

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E4004 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |
| `data` | Object | Đối tượng chứa thông tin về tiến trình đồng bộ đang chạy |

#### Conflict Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `syncId` | String | Mã định danh của tiến trình đồng bộ đang chạy |
| `status` | String | Trạng thái hiện tại của tiến trình đồng bộ |
| `startedAt` | String | Thời điểm bắt đầu tiến trình (ISO 8601) |
| `estimatedCompletion` | String | Thời điểm dự kiến hoàn thành (ISO 8601) |

```json
{
  "status": "error",
  "code": "E4004",
  "message": "Xung đột dữ liệu",
  "errors": [
    {
      "field": "sync",
      "message": "Đã có tiến trình đồng bộ đang chạy. Vui lòng đợi tiến trình hiện tại hoàn thành."
    }
  ],
  "data": {
    "syncId": "SYNC-20250531-123455",
    "status": "processing",
    "startedAt": "2025-05-31T14:50:22Z",
    "estimatedCompletion": "2025-05-31T14:52:22Z"
  }
}
```

#### 502 Bad Gateway

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "error" |
| `code` | String | Mã lỗi: E5002 |
| `message` | String | Thông báo lỗi tổng quát |
| `errors` | Array | Mảng chứa chi tiết các lỗi |

```json
{
  "status": "error",
  "code": "E5002",
  "message": "Lỗi đồng bộ dữ liệu Hubspot",
  "errors": [
    {
      "field": "hubspot",
      "message": "Dịch vụ Hubspot hiện không khả dụng. Vui lòng thử lại sau."
    }
  ]
}
``` 