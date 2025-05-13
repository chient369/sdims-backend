# API Details: Lấy danh sách cơ hội kinh doanh

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo tài liệu API lấy danh sách cơ hội kinh doanh | -           | Draft     |
| 1.1     | 2023-10-17 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response bằng bảng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để lấy danh sách cơ hội kinh doanh với các tùy chọn lọc, sắp xếp và phân trang, giúp người dùng có thể dễ dàng theo dõi và quản lý các cơ hội kinh doanh theo nhiều tiêu chí khác nhau.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-OPP-001                                  |
| **Tên API**        | Lấy danh sách cơ hội kinh doanh              |
| **Mô tả**          | API lấy danh sách cơ hội kinh doanh với các bộ lọc và phân trang |
| **Module**         | Quản lý Cơ hội Kinh doanh                    |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/opportunities`                      |
| **Quyền truy cập** | opportunity:read:all                             |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Query Parameters

| Tên            | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|----------------|------------------|----------|-------|
| `keyword`      | String           | Không    | Từ khóa tìm kiếm (tên cơ hội, mã cơ hội, tên khách hàng) |
| `status`       | String           | Không    | Lọc theo trạng thái cơ hội, có thể truyền nhiều giá trị, phân tách bằng dấu phẩy |
| `dealSize`     | String           | Không    | Lọc theo quy mô cơ hội: `small`, `medium`, `large`, `extra_large` |
| `fromAmount`   | Number           | Không    | Lọc các cơ hội có giá trị từ số tiền này (VNĐ) |
| `toAmount`     | Number           | Không    | Lọc các cơ hội có giá trị đến số tiền này (VNĐ) |
| `priority`     | Boolean          | Không    | Lọc theo ưu tiên onsite (`true` hoặc `false`) |
| `assignedTo`   | Integer          | Không    | ID của người được gán vào cơ hội (Leader) |
| `createdBy`    | Integer          | Không    | ID của người tạo cơ hội (Sales) |
| `fromDate`     | String           | Không    | Lọc các cơ hội từ ngày tạo (định dạng: YYYY-MM-DD) |
| `toDate`       | String           | Không    | Lọc các cơ hội đến ngày tạo (định dạng: YYYY-MM-DD) |
| `sortBy`       | String           | Không    | Trường sắp xếp (mặc định: `createdAt`) |
| `sortDir`      | String           | Không    | Hướng sắp xếp: `asc` hoặc `desc` (mặc định: `desc`) |
| `page`         | Integer          | Không    | Trang cần lấy (mặc định: `1`) |
| `size`         | Integer          | Không    | Số bản ghi mỗi trang (mặc định: `20`) |

### 3.3 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `status`       | Một hoặc nhiều giá trị từ: `new`, `contacted`, `qualified`, `proposal`, `negotiation`, `won`, `lost`, `closed` |
| `dealSize`     | Một trong: `small`, `medium`, `large`, `extra_large` |
| `fromAmount`   | Số không âm |
| `toAmount`     | Số không âm, lớn hơn hoặc bằng `fromAmount` (nếu cả hai đều được cung cấp) |
| `priority`     | Boolean: `true` hoặc `false` |
| `assignedTo`   | Số nguyên dương, ID của Leader tồn tại trong hệ thống |
| `createdBy`    | Số nguyên dương, ID của Sales tồn tại trong hệ thống |
| `fromDate`     | Định dạng: YYYY-MM-DD |
| `toDate`       | Định dạng: YYYY-MM-DD, phải sau hoặc bằng `fromDate` (nếu cả hai đều được cung cấp) |
| `sortBy`       | Một trong: `createdAt`, `updatedAt`, `name`, `customerName`, `amount`, `status`, `closingDate` |
| `sortDir`      | Một trong: `asc`, `desc` |
| `page`         | ≥ 1 |
| `size`         | 1 → 100 |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được các cơ hội được gán cho mình
- Sales: Xem được các cơ hội do mình tạo và các cơ hội chưa được gán
- Division Manager: Xem được tất cả cơ hội thuộc bộ phận mình quản lý
- Admin: Xem được tất cả cơ hội

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa dữ liệu cơ hội kinh doanh và thông tin phân trang |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `summary` | Object | Thông tin tổng hợp về danh sách cơ hội |
| `content` | Array | Mảng các đối tượng cơ hội kinh doanh |
| `pageable` | Object | Thông tin phân trang |

#### Summary Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `totalCount` | Integer | Tổng số cơ hội kinh doanh |
| `totalAmount` | Number | Tổng giá trị tất cả các cơ hội (VNĐ) |
| `byStatus` | Object | Phân bố các cơ hội theo trạng thái |
| `byDealSize` | Object | Phân bố các cơ hội theo quy mô |

#### ByStatus Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `new` | Integer | Số lượng cơ hội ở trạng thái mới |
| `contacted` | Integer | Số lượng cơ hội ở trạng thái đã liên hệ |
| `qualified` | Integer | Số lượng cơ hội ở trạng thái đủ điều kiện |
| `proposal` | Integer | Số lượng cơ hội ở trạng thái đã gửi đề xuất |
| `negotiation` | Integer | Số lượng cơ hội ở trạng thái đang đàm phán |
| `won` | Integer | Số lượng cơ hội ở trạng thái thắng thầu |
| `lost` | Integer | Số lượng cơ hội ở trạng thái thua thầu |
| `closed` | Integer | Số lượng cơ hội ở trạng thái đã đóng |

#### ByDealSize Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `small` | Integer | Số lượng cơ hội quy mô nhỏ |
| `medium` | Integer | Số lượng cơ hội quy mô vừa |
| `large` | Integer | Số lượng cơ hội quy mô lớn |
| `extra_large` | Integer | Số lượng cơ hội quy mô cực lớn |

#### Opportunity Object (trong mảng content)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội kinh doanh |
| `code` | String | Mã cơ hội (tự động sinh) |
| `name` | String | Tên cơ hội kinh doanh |
| `description` | String | Mô tả chi tiết về cơ hội |
| `customerName` | String | Tên khách hàng/công ty |
| `customerContact` | String | Người liên hệ bên phía khách hàng |
| `status` | String | Trạng thái hiện tại của cơ hội |
| `dealSize` | String | Quy mô của cơ hội |
| `amount` | Number | Giá trị của cơ hội (VNĐ) |
| `priority` | Boolean | Cơ hội có được ưu tiên không |
| `createdBy` | Object | Thông tin người tạo cơ hội |
| `assignedTo` | Object | Thông tin người được gán xử lý cơ hội |
| `source` | String | Nguồn gốc của cơ hội (manual, hubspot, website, ...) |
| `externalId` | String | ID tham chiếu đến hệ thống bên ngoài (nếu có) |
| `closingDate` | String | Ngày dự kiến đóng cơ hội (YYYY-MM-DD) |
| `closingProbability` | Integer | Xác suất thành công (0-100%) |
| `createdAt` | String | Thời điểm tạo cơ hội (ISO 8601) |
| `updatedAt` | String | Thời điểm cập nhật gần nhất (ISO 8601) |
| `tags` | Array | Danh sách các tag liên quan đến cơ hội |

#### User Object (trong createdBy và assignedTo)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `name` | String | Tên đầy đủ của người dùng |

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
    "summary": {
      "totalCount": 127,
      "totalAmount": 25750000000,
      "byStatus": {
        "new": 15,
        "contacted": 22,
        "qualified": 18,
        "proposal": 30,
        "negotiation": 25,
        "won": 10,
        "lost": 7
      },
      "byDealSize": {
        "small": 45,
        "medium": 35,
        "large": 30,
        "extra_large": 17
      }
    },
    "content": [
      {
        "id": 134,
        "code": "OPP-2025050134",
        "name": "Hệ thống CRM cho công ty ABC",
        "description": "Triển khai hệ thống CRM cho công ty ABC trong vòng 6 tháng",
        "customerName": "Công ty ABC",
        "customerContact": "Nguyễn Văn A",
        "status": "proposal",
        "dealSize": "large",
        "amount": 1250000000,
        "priority": true,
        "createdBy": {
          "id": 5,
          "name": "Trần Văn Sales"
        },
        "assignedTo": {
          "id": 8,
          "name": "Lê Thị Leader"
        },
        "source": "hubspot",
        "externalId": "HS-12345678",
        "closingDate": "2025-07-31",
        "closingProbability": 70,
        "createdAt": "2025-05-10T09:15:32Z",
        "updatedAt": "2025-05-15T14:22:45Z",
        "tags": ["Java", "Web", "CRM"]
      },
      {
        "id": 133,
        "code": "OPP-2025050133",
        "name": "Phát triển ứng dụng di động cho ngân hàng XYZ",
        "description": "Xây dựng ứng dụng mobile banking cho ngân hàng XYZ",
        "customerName": "Ngân hàng XYZ",
        "customerContact": "Phạm Thị B",
        "status": "negotiation",
        "dealSize": "extra_large",
        "amount": 3500000000,
        "priority": true,
        "createdBy": {
          "id": 5,
          "name": "Trần Văn Sales"
        },
        "assignedTo": {
          "id": 9,
          "name": "Phạm Huy Leader"
        },
        "source": "manual",
        "externalId": null,
        "closingDate": "2025-08-15",
        "closingProbability": 80,
        "createdAt": "2025-05-09T15:30:22Z",
        "updatedAt": "2025-05-16T10:45:18Z",
        "tags": ["Mobile", "Banking", "Flutter"]
      }
    ],
    "pageable": {
      "pageNumber": 1,
      "pageSize": 2,
      "totalPages": 64,
      "totalElements": 127,
      "sort": "createdAt,desc"
    }
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
      "field": "status",
      "message": "Trạng thái 'pending' không hợp lệ. Các giá trị hợp lệ: new, contacted, qualified, proposal, negotiation, won, lost, closed"
    },
    {
      "field": "toDate",
      "message": "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu"
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