# API Details: Lấy chi tiết hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API lấy chi tiết hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để lấy thông tin chi tiết của một hợp đồng, bao gồm các điều khoản thanh toán và danh sách nhân viên được gán vào dự án, giúp người dùng theo dõi tiến độ thực hiện, trạng thái thanh toán và phân bổ nguồn lực cho hợp đồng.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-003                                  |
| **Tên API**        | Lấy chi tiết hợp đồng                        |
| **Mô tả**          | API lấy thông tin chi tiết của một hợp đồng bao gồm các điều khoản thanh toán và nhân viên được gán |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/contracts/{contractId}`             |
| **Quyền truy cập** | contract:read                                |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Integer      | Có       | ID của hợp đồng cần lấy thông tin |

### 3.3 Query Parameters

| Tên                    | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|------------------------|------------------|----------|-------|
| `includePaymentTerms`  | Boolean          | Không    | Có kèm theo thông tin các đợt thanh toán không (mặc định: `true`) |
| `includeEmployees`     | Boolean          | Không    | Có kèm theo thông tin nhân viên tham gia không (mặc định: `true`) |
| `includeFiles`         | Boolean          | Không    | Có kèm theo thông tin file đính kèm không (mặc định: `true`) |

### 3.3 Validate Rule

| Trường               | Điều kiện hợp lệ |
|----------------------|------------------|
| `contractId`         | Số nguyên dương, phải tồn tại trong hệ thống |
| `includePaymentTerms`| Boolean: `true` hoặc `false` |
| `includeEmployees`   | Boolean: `true` hoặc `false` |
| `includeFiles`       | Boolean: `true` hoặc `false` |

### 3.4 Phân quyền đặc biệt
- Leader: Chỉ xem được các hợp đồng có liên kết với nhân viên thuộc team mình quản lý
- Sales: Xem được các hợp đồng do mình phụ trách
- Division Manager: Xem được tất cả hợp đồng thuộc bộ phận mình quản lý
- Kế toán: Xem được tất cả hợp đồng nhưng chỉ tập trung vào thông tin thanh toán
- Admin: Xem được tất cả hợp đồng

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin chi tiết hợp đồng |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contract` | Object | Thông tin chi tiết hợp đồng được yêu cầu |

#### Contract Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `customerName` | String | Tên khách hàng |
| `contractType` | String | Loại hợp đồng: `FixedPrice`, `TimeAndMaterial`, `Retainer`, `Maintenance`, `Other` |
| `amount` | Number | Tổng giá trị hợp đồng (VND) |
| `signDate` | String | Ngày ký hợp đồng (định dạng: YYYY-MM-DD) |
| `startDate` | String | Ngày bắt đầu hiệu lực (định dạng: YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `status` | String | Trạng thái hợp đồng: `Draft`, `InReview`, `Approved`, `Active`, `InProgress`, `OnHold`, `Completed`, `Terminated`, `Expired`, `Cancelled` |
| `salesPerson` | Object | Thông tin người phụ trách Sales |
| `relatedOpportunity` | Object | Thông tin cơ hội liên kết (nếu có) |
| `description` | String | Mô tả chi tiết về hợp đồng |
| `paymentTerms` | Array | Danh sách các điều khoản thanh toán |
| `employeeAssignments` | Array | Danh sách nhân viên được phân công cho hợp đồng |
| `files` | Array | Danh sách các file đính kèm hợp đồng |
| `paymentStatus` | Object | Tóm tắt trạng thái thanh toán hiện tại |
| `tags` | Array of String | Các thẻ gắn với hợp đồng |
| `createdBy` | Object | Thông tin người tạo hợp đồng |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |
| `updatedBy` | Object | Thông tin người cập nhật gần nhất |
| `updatedAt` | String | Thời gian cập nhật gần nhất (định dạng ISO 8601) |

#### Sales Person Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên Sales |
| `name` | String | Họ tên nhân viên Sales |

#### Opportunity Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cơ hội |
| `code` | String | Mã cơ hội |
| `name` | String | Tên cơ hội |

#### Payment Term Object (trong mảng paymentTerms)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của đợt thanh toán |
| `termNumber` | Integer | Số thứ tự đợt thanh toán |
| `dueDate` | String | Ngày đến hạn thanh toán (định dạng: YYYY-MM-DD) |
| `amount` | Number | Số tiền phải thanh toán |
| `description` | String | Mô tả về đợt thanh toán |
| `status` | String | Trạng thái thanh toán (paid, unpaid, invoiced, overdue) |
| `paidDate` | String/null | Ngày thanh toán thực tế (định dạng ISO 8601, hoặc null nếu chưa thanh toán) |
| `paidAmount` | Number | Số tiền đã thanh toán |

#### Employee Assignment Object (trong mảng employeeAssignments)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của bản ghi phân công |
| `employee` | Object | Thông tin nhân viên được phân công |
| `startDate` | String | Ngày bắt đầu tham gia (định dạng: YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `allocationPercentage` | Number | Phần trăm phân bổ thời gian (0-100) |
| `billRate` | Number | Đơn giá billing của nhân viên (VND/tháng) |

#### Employee Object (trong employee assignment)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên |
| `name` | String | Họ tên nhân viên |
| `position` | String | Vị trí công việc |
| `team` | Object | Thông tin team của nhân viên |

#### Team Object (trong employee)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### File Object (trong mảng files)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của file |
| `name` | String | Tên file |
| `type` | String | Loại file (MIME type) |
| `size` | Number | Kích thước file (byte) |
| `uploadedAt` | String | Thời gian upload (định dạng ISO 8601) |
| `uploadedBy` | Object | Thông tin người upload |
| `url` | String | Đường dẫn để tải file |

#### Payment Status Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái thanh toán tổng thể (unpaid, partial, paid, overdue) |
| `paidAmount` | Number | Số tiền đã thanh toán |
| `totalAmount` | Number | Tổng số tiền cần thanh toán |
| `paidPercentage` | Number | Phần trăm tiền đã thanh toán |
| `nextDueDate` | String/null | Ngày đến hạn thanh toán tiếp theo (định dạng: YYYY-MM-DD) |
| `nextDueAmount` | Number | Số tiền phải thanh toán ở đợt tiếp theo |
| `totalTerms` | Integer | Tổng số đợt thanh toán |
| `paidTerms` | Integer | Số đợt đã thanh toán |
| `remainingAmount` | Number | Số tiền còn lại cần thanh toán |

#### User Reference Object (createdBy, updatedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `name` | String | Họ tên người dùng |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "contract": {
      "id": 45,
      "contractCode": "CTR-2025-045",
      "name": "Hệ thống CRM cho Công ty ABC",
      "customerName": "Công ty ABC",
      "contractType": "FixedPrice",
      "amount": 1250000000,
      "signDate": "2025-05-15",
      "startDate": "2025-05-20",
      "endDate": "2025-11-20",
      "status": "InProgress",
      "salesPerson": {
        "id": 5,
        "name": "Trần Văn Sales"
      },
      "relatedOpportunity": {
        "id": 134,
        "code": "OPP-2025050134",
        "name": "Hệ thống CRM cho công ty ABC"
      },
      "description": "Hợp đồng phát triển hệ thống CRM bao gồm quản lý khách hàng, bán hàng và báo cáo",
      "paymentTerms": [
        {
          "id": 120,
          "termNumber": 1,
          "dueDate": "2025-05-25",
          "amount": 312500000,
          "description": "Tạm ứng 25% khi khởi động dự án",
          "status": "paid",
          "paidDate": "2025-05-23T00:00:00Z",
          "paidAmount": 312500000
        },
        {
          "id": 121,
          "termNumber": 2,
          "dueDate": "2025-07-20",
          "amount": 312500000,
          "description": "25% sau khi hoàn thành giai đoạn phân tích yêu cầu và thiết kế",
          "status": "unpaid",
          "paidDate": null,
          "paidAmount": 0
        },
        {
          "id": 122,
          "termNumber": 3,
          "dueDate": "2025-09-20",
          "amount": 312500000,
          "description": "25% sau khi hoàn thành phát triển và bàn giao cho UAT",
          "status": "unpaid",
          "paidDate": null,
          "paidAmount": 0
        },
        {
          "id": 123,
          "termNumber": 4,
          "dueDate": "2025-11-30",
          "amount": 312500000,
          "description": "25% sau khi hoàn thành dự án và nghiệm thu",
          "status": "unpaid",
          "paidDate": null,
          "paidAmount": 0
        }
      ],
      "employeeAssignments": [
        {
          "id": 230,
          "employee": {
            "id": 15,
            "name": "Nguyễn Văn A",
            "position": "Senior Developer",
            "team": {
              "id": 3,
              "name": "Team Alpha"
            }
          },
          "startDate": "2025-05-20",
          "endDate": "2025-11-20",
          "allocationPercentage": 100,
          "billRate": 25000000
        },
        {
          "id": 231,
          "employee": {
            "id": 22,
            "name": "Lê Thị B",
            "position": "Developer",
            "team": {
              "id": 3,
              "name": "Team Alpha"
            }
          },
          "startDate": "2025-05-20",
          "endDate": "2025-09-30",
          "allocationPercentage": 100,
          "billRate": 20000000
        },
        {
          "id": 232,
          "employee": {
            "id": 28,
            "name": "Phạm Văn C",
            "position": "Tester",
            "team": {
              "id": 4,
              "name": "Team Beta"
            }
          },
          "startDate": "2025-06-01",
          "endDate": "2025-11-20",
          "allocationPercentage": 50,
          "billRate": 18000000
        }
      ],
      "files": [
        {
          "id": 45,
          "name": "hop_dong_abc_signed.pdf",
          "type": "application/pdf",
          "size": 3256400,
          "uploadedAt": "2025-05-15T14:22:10Z",
          "uploadedBy": {
            "id": 5,
            "name": "Trần Văn Sales"
          },
          "url": "/api/v1/files/45"
        },
        {
          "id": 46,
          "name": "phu_luc_abc.pdf",
          "type": "application/pdf",
          "size": 1520300,
          "uploadedAt": "2025-05-15T14:22:35Z",
          "uploadedBy": {
            "id": 5,
            "name": "Trần Văn Sales"
          },
          "url": "/api/v1/files/46"
        }
      ],
      "paymentStatus": {
        "status": "partial",
        "paidAmount": 312500000,
        "totalAmount": 1250000000,
        "paidPercentage": 25,
        "nextDueDate": "2025-07-20",
        "nextDueAmount": 312500000,
        "totalTerms": 4,
        "paidTerms": 1,
        "remainingAmount": 937500000
      },
      "tags": ["CRM", "Development"],
      "createdBy": {
        "id": 5,
        "name": "Trần Văn Sales"
      },
      "createdAt": "2025-05-15T11:30:45Z",
      "updatedBy": {
        "id": 3,
        "name": "Trưởng Phòng Lê"
      },
      "updatedAt": "2025-05-23T14:10:25Z"
    }
  }
}
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
      "field": "contractId",
      "message": "ID hợp đồng phải là số nguyên dương"
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
  "message": "Bạn không có quyền truy cập hợp đồng này"
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
      "field": "contractId",
      "message": "Không tìm thấy hợp đồng với ID: 999"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi truy vấn dữ liệu hợp đồng"
}
``` 