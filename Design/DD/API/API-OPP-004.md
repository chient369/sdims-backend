# API Details: Xem log đồng bộ Hubspot

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-20 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để người dùng có quyền thích hợp có thể xem lịch sử và chi tiết các quá trình đồng bộ dữ liệu từ Hubspot, bao gồm thông tin tổng hợp và chi tiết từng quá trình đồng bộ cụ thể.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-OPP-004                                  |
| **Tên API**        | Xem log đồng bộ Hubspot                      |
| **Mô tả**          | API lấy danh sách các log đồng bộ Hubspot và chi tiết |
| **Module**         | Quản lý Cơ hội Kinh doanh                    |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/opportunities/sync/logs`            |
| **Quyền truy cập** | opportunity-log:read:all                                   |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|----------------|------------------|----------|-------|
| `syncId`       | String           | Không    | ID của tiến trình đồng bộ cụ thể cần xem log |
| `status`       | String           | Không    | Lọc theo trạng thái: `queued`, `processing`, `completed`, `failed` |
| `fromDate`     | String           | Không    | Lọc từ ngày (định dạng: YYYY-MM-DD) |
| `toDate`       | String           | Không    | Lọc đến ngày (định dạng: YYYY-MM-DD) |
| `sortBy`       | String           | Không    | Trường sắp xếp (mặc định: `startedAt`) |
| `sortDir`      | String           | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |
| `page`         | Integer          | Không    | Trang cần lấy (mặc định: `1`) |
| `size`         | Integer          | Không    | Số bản ghi mỗi trang (mặc định: `20`) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `syncId`       | Phải tuân theo định dạng: `SYNC-YYYYMMDD-XXXXXX` |
| `status`       | Một trong: `queued`, `processing`, `completed`, `failed` |
| `fromDate`     | Định dạng: YYYY-MM-DD |
| `toDate`       | Định dạng: YYYY-MM-DD, phải sau hoặc bằng `fromDate` (nếu cả hai đều được cung cấp) |
| `sortBy`       | Một trong: `syncId`, `startedAt`, `completedAt`, `status` |
| `sortDir`      | Một trong: `asc`, `desc` |
| `page`         | ≥ 1 |
| `size`         | 1 → 100 |

### 3.4 Phân quyền đặc biệt
- Chỉ người dùng có quyền `sync:read` mới được xem log đồng bộ
- Theo ma trận CRUD, chỉ Admin và Division Manager có quyền này
- Dữ liệu log có thể chứa thông tin nhạy cảm về cơ hội kinh doanh

---

## 4. Response

### 4.1 Success - 200 OK (Danh sách log)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu về các log đồng bộ |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `content` | Array | Mảng các đối tượng log đồng bộ |
| `pageable` | Object | Thông tin phân trang |

#### Sync Log Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `syncId` | String | ID của tiến trình đồng bộ |
| `status` | String | Trạng thái đồng bộ (queued, processing, completed, failed) |
| `initiatedBy` | Object | Thông tin người khởi tạo đồng bộ |
| `startedAt` | String | Thời điểm bắt đầu đồng bộ (ISO 8601) |
| `completedAt` | String | Thời điểm hoàn thành đồng bộ (ISO 8601) |
| `duration` | Integer | Thời gian thực hiện (giây) |
| `syncParams` | Object | Tham số đồng bộ đã sử dụng |
| `summary` | Object | Thông tin tổng hợp về kết quả đồng bộ |
| `error` | Object | Thông tin lỗi (nếu có, chỉ xuất hiện khi status là "failed") |

#### User Object (trong initiatedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `name` | String | Tên đầy đủ của người dùng |

#### SyncParams Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `syncMode` | String | Chế độ đồng bộ (incremental, full) |
| `fromDate` | String | Ngày bắt đầu khoảng thời gian đồng bộ (có thể không có) |
| `toDate` | String | Ngày kết thúc khoảng thời gian đồng bộ (có thể không có) |
| `dealStage` | String | Trạng thái deal đã chọn để đồng bộ |
| `overwriteExisting` | Boolean | Cài đặt ghi đè dữ liệu đã chọn |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalOpportunities` | Integer | Tổng số cơ hội được xử lý |
| `newOpportunities` | Integer | Số cơ hội mới được tạo |
| `updatedOpportunities` | Integer | Số cơ hội được cập nhật |
| `skippedOpportunities` | Integer | Số cơ hội bị bỏ qua |
| `failedOpportunities` | Integer | Số cơ hội xử lý thất bại |

#### Error Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `code` | String | Mã lỗi hệ thống |
| `message` | String | Thông báo lỗi chi tiết |

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
    "content": [
      {
        "syncId": "SYNC-20250531-123456",
        "status": "completed",
        "initiatedBy": {
          "id": 1,
          "name": "Admin Nguyễn"
        },
        "startedAt": "2025-05-31T15:00:22Z",
        "completedAt": "2025-05-31T15:02:45Z",
        "duration": 143,
        "syncParams": {
          "syncMode": "incremental",
          "fromDate": "2025-05-01",
          "toDate": "2025-05-31",
          "dealStage": "all",
          "overwriteExisting": false
        },
        "summary": {
          "totalOpportunities": 25,
          "newOpportunities": 12,
          "updatedOpportunities": 10,
          "skippedOpportunities": 3,
          "failedOpportunities": 0
        }
      },
      {
        "syncId": "SYNC-20250530-123455",
        "status": "failed",
        "initiatedBy": {
          "id": 3,
          "name": "Trưởng Phòng Lê"
        },
        "startedAt": "2025-05-30T09:15:10Z",
        "completedAt": "2025-05-30T09:15:45Z",
        "duration": 35,
        "syncParams": {
          "syncMode": "full",
          "dealStage": "all",
          "overwriteExisting": true
        },
        "summary": {
          "totalOpportunities": 0,
          "newOpportunities": 0,
          "updatedOpportunities": 0,
          "skippedOpportunities": 0,
          "failedOpportunities": 0
        },
        "error": {
          "code": "HUBSPOT_API_ERROR",
          "message": "Không thể kết nối với Hubspot API sau 3 lần thử lại"
        }
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 2,
      "totalPages": 5,
      "totalElements": 10,
      "sort": "startedAt,desc"
    }
  }
}
```

### 4.2 Success - 200 OK (Chi tiết log một tiến trình)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa chi tiết log một tiến trình đồng bộ |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `syncId` | String | ID của tiến trình đồng bộ |
| `status` | String | Trạng thái đồng bộ (queued, processing, completed, failed) |
| `initiatedBy` | Object | Thông tin người khởi tạo đồng bộ |
| `startedAt` | String | Thời điểm bắt đầu đồng bộ (ISO 8601) |
| `completedAt` | String | Thời điểm hoàn thành đồng bộ (ISO 8601) |
| `duration` | Integer | Thời gian thực hiện (giây) |
| `syncParams` | Object | Tham số đồng bộ đã sử dụng |
| `summary` | Object | Thông tin tổng hợp về kết quả đồng bộ |
| `details` | Array | Chi tiết về từng cơ hội được xử lý |
| `logs` | Array | Các bản ghi log của tiến trình |

#### Detail Object (trong mảng details)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `hubspotDealId` | String | ID của deal trong Hubspot |
| `action` | String | Hành động thực hiện (created, updated, skipped) |
| `status` | String | Trạng thái xử lý (success, skipped, failed) |
| `opportunity` | Object | Thông tin cơ hội (nếu thành công) |
| `reason` | String | Lý do bỏ qua/lỗi (nếu có) |
| `changes` | Array | Mảng các thay đổi (chỉ có khi action là "updated") |
| `timestamp` | String | Thời điểm xử lý (ISO 8601) |

#### Opportunity Object (trong detail)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội kinh doanh |
| `code` | String | Mã cơ hội (tự động sinh) |
| `name` | String | Tên cơ hội kinh doanh |

#### Change Object (trong mảng changes)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `field` | String | Tên trường dữ liệu được thay đổi |
| `oldValue` | String | Giá trị cũ |
| `newValue` | String | Giá trị mới |

#### Log Object (trong mảng logs)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `level` | String | Mức độ log (INFO, WARNING, ERROR) |
| `message` | String | Nội dung thông báo log |
| `timestamp` | String | Thời điểm ghi log (ISO 8601) |

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "syncId": "SYNC-20250531-123456",
    "status": "completed",
    "initiatedBy": {
      "id": 1,
      "name": "Admin Nguyễn"
    },
    "startedAt": "2025-05-31T15:00:22Z",
    "completedAt": "2025-05-31T15:02:45Z",
    "duration": 143,
    "syncParams": {
      "syncMode": "incremental",
      "fromDate": "2025-05-01",
      "toDate": "2025-05-31",
      "dealStage": "all",
      "overwriteExisting": false
    },
    "summary": {
      "totalOpportunities": 25,
      "newOpportunities": 12,
      "updatedOpportunities": 10,
      "skippedOpportunities": 3,
      "failedOpportunities": 0
    },
    "details": [
      {
        "hubspotDealId": "12345678",
        "action": "created",
        "status": "success",
        "opportunity": {
          "id": 134,
          "code": "OPP-2025050134",
          "name": "Hệ thống CRM cho công ty ABC"
        },
        "timestamp": "2025-05-31T15:01:12Z"
      },
      {
        "hubspotDealId": "12345679",
        "action": "updated",
        "status": "success",
        "opportunity": {
          "id": 133,
          "code": "OPP-2025050133",
          "name": "Phát triển ứng dụng di động cho ngân hàng XYZ"
        },
        "changes": [
          {
            "field": "status",
            "oldValue": "proposal",
            "newValue": "negotiation"
          },
          {
            "field": "amount",
            "oldValue": "3000000000",
            "newValue": "3500000000"
          }
        ],
        "timestamp": "2025-05-31T15:01:35Z"
      },
      {
        "hubspotDealId": "12345680",
        "action": "skipped",
        "status": "skipped",
        "reason": "No changes detected",
        "timestamp": "2025-05-31T15:01:55Z"
      }
    ],
    "logs": [
      {
        "level": "INFO",
        "message": "Bắt đầu quá trình đồng bộ",
        "timestamp": "2025-05-31T15:00:22Z"
      },
      {
        "level": "INFO",
        "message": "Lấy thành công 25 deal từ Hubspot API",
        "timestamp": "2025-05-31T15:00:45Z"
      },
      {
        "level": "INFO",
        "message": "Hoàn thành quá trình đồng bộ",
        "timestamp": "2025-05-31T15:02:45Z"
      }
    ]
  }
}
```

### 4.3 Error Responses

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
      "field": "syncId",
      "message": "Định dạng syncId không hợp lệ. Yêu cầu định dạng SYNC-YYYYMMDD-XXXXXX"
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
| `code` | String | Mã lỗi: E3001 |
| `message` | String | Thông báo lỗi |

```json
{
  "status": "error",
  "code": "E3001",
  "message": "Không tìm thấy tiến trình đồng bộ với ID: SYNC-20250101-000000"
}
``` 