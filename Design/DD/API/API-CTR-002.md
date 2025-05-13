# API Details: Thêm hợp đồng mới

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-06-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API thêm hợp đồng mới | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để thêm mới một hợp đồng vào hệ thống, bao gồm thông tin cơ bản của hợp đồng, các điều khoản thanh toán và danh sách nhân viên tham gia dự án, giúp các bên liên quan dễ dàng theo dõi tiến độ thực hiện và thanh toán.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-002                                  |
| **Tên API**        | Thêm hợp đồng mới                            |
| **Mô tả**          | API cho phép thêm mới một hợp đồng vào hệ thống |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/contracts`                          |
| **Quyền truy cập** | contract:create                              |

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
  "name": "Hệ thống CRM cho Công ty ABC",
  "contractCode": "CTR-2025-045",
  "customerName": "Công ty ABC",
  "contractType": "FixedPrice",
  "amount": 1250000000,
  "signDate": "2025-05-15",
  "startDate": "2025-05-20",
  "endDate": "2025-11-20",
  "status": "Draft",
  "salesId": 5,
  "opportunityId": 134,
  "description": "Hợp đồng phát triển hệ thống CRM bao gồm quản lý khách hàng, bán hàng và báo cáo",
  "paymentTerms": [
    {
      "termNumber": 1,
      "dueDate": "2025-05-25",
      "amount": 312500000,
      "percentage": 25,
      "description": "Tạm ứng 25% khi khởi động dự án"
    },
    {
      "termNumber": 2,
      "dueDate": "2025-07-20",
      "amount": 312500000,
      "percentage": 25,
      "description": "25% sau khi hoàn thành giai đoạn phân tích yêu cầu và thiết kế"
    },
    {
      "termNumber": 3,
      "dueDate": "2025-09-20",
      "amount": 312500000,
      "percentage": 25,
      "description": "25% sau khi hoàn thành phát triển và bàn giao cho UAT"
    },
    {
      "termNumber": 4,
      "dueDate": "2025-11-30",
      "amount": 312500000,
      "percentage": 25,
      "description": "25% sau khi hoàn thành dự án và nghiệm thu"
    }
  ],
  "employeeAssignments": [
    {
      "employeeId": 15,
      "startDate": "2025-05-20",
      "endDate": "2025-11-20",
      "allocationPercentage": 100,
      "billRate": 25000000,
      "role": "Project Manager"
    },
    {
      "employeeId": 22,
      "startDate": "2025-05-20",
      "endDate": "2025-09-30",
      "allocationPercentage": 100,
      "billRate": 20000000,
      "role": "Senior Developer"
    },
    {
      "employeeId": 28,
      "startDate": "2025-06-01",
      "endDate": "2025-11-20",
      "allocationPercentage": 50,
      "billRate": 18000000,
      "role": "Tester"
    }
  ],
  "attachments": [
    {
      "name": "hop_dong_goc.pdf",
      "type": "application/pdf",
      "base64Content": "base64_encoded_file_content_here...",
      "description": "Bản scan hợp đồng gốc đã ký"
    }
  ],
  "tags": ["CRM", "Enterprise", "Software"]
}
```

### 3.3 Body Parameters

| Tên                  | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|----------------------|------------------|----------|-------|
| `name`               | String           | Có       | Tên hợp đồng |
| `contractCode`       | String           | Không    | Mã hợp đồng (nếu không cung cấp, hệ thống sẽ tự động tạo) |
| `customerName`       | String           | Có       | Tên khách hàng |
| `contractType`       | String           | Có       | Loại hợp đồng |
| `amount`             | Number           | Có       | Tổng giá trị hợp đồng (VND) |
| `signDate`           | String           | Có       | Ngày ký hợp đồng (định dạng: YYYY-MM-DD) |
| `startDate`          | String           | Có       | Ngày bắt đầu hiệu lực (định dạng: YYYY-MM-DD) |
| `endDate`            | String           | Có       | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `status`             | String           | Có       | Trạng thái hợp đồng |
| `salesId`            | Integer          | Có       | ID của người phụ trách Sales |
| `opportunityId`      | Integer          | Không    | ID của cơ hội liên kết |
| `description`        | String           | Không    | Mô tả chi tiết về hợp đồng |
| `paymentTerms`       | Array of Object  | Có       | Các điều khoản thanh toán |
| `paymentTerms[].termNumber`        | Integer  | Có    | Số thứ tự của đợt thanh toán |
| `paymentTerms[].dueDate`           | String   | Có    | Ngày đến hạn thanh toán (định dạng: YYYY-MM-DD) |
| `paymentTerms[].amount`            | Number   | Có    | Số tiền phải thanh toán trong đợt này (VND) |
| `paymentTerms[].percentage`        | Number   | Có    | Phần trăm so với tổng giá trị hợp đồng (%) |
| `paymentTerms[].description`       | String   | Không | Mô tả về đợt thanh toán |
| `employeeAssignments`              | Array of Object | Không | Danh sách nhân viên tham gia |
| `employeeAssignments[].employeeId` | Integer  | Có    | ID của nhân viên |
| `employeeAssignments[].startDate`  | String   | Có    | Ngày bắt đầu tham gia (định dạng: YYYY-MM-DD) |
| `employeeAssignments[].endDate`    | String   | Có    | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `employeeAssignments[].allocationPercentage` | Number | Có | Phần trăm phân bổ thời gian (0-100) |
| `employeeAssignments[].billRate`   | Number   | Không | Đơn giá billing của nhân viên (VND/tháng) |
| `employeeAssignments[].role`       | String   | Không | Vai trò của nhân viên trong dự án |
| `attachments`                      | Array of Object | Không | Danh sách tài liệu đính kèm |
| `attachments[].name`               | String   | Có    | Tên file đính kèm |
| `attachments[].type`               | String   | Có    | Loại file (MIME type) |
| `attachments[].base64Content`      | String   | Có    | Nội dung file đã mã hóa Base64 |
| `attachments[].description`        | String   | Không | Mô tả về file đính kèm |
| `tags`                             | Array of String | Không | Các thẻ gắn với hợp đồng |

### 3.4 Validate Rule

| Trường               | Điều kiện hợp lệ |
|----------------------|------------------|
| `name`               | Không được để trống, tối đa 255 ký tự |
| `contractCode`       | (Nếu cung cấp) Định dạng hợp lệ, không trùng với mã đã tồn tại |
| `customerName`       | Không được để trống, tối đa 255 ký tự, phải tồn tại trong hệ thống |
| `contractType`       | (Nếu cung cấp) Một trong: `FixedPrice`, `TimeAndMaterial`, `Retainer`, `Maintenance`, `Other` |
| `amount`             | (Nếu cung cấp) Số dương > 0 |
| `signDate`           | (Nếu cung cấp) Định dạng: YYYY-MM-DD, không được là ngày trong tương lai |
| `startDate`          | (Nếu cung cấp) Định dạng: YYYY-MM-DD, phải sau hoặc bằng `signDate` |
| `endDate`            | (Nếu cung cấp) Định dạng: YYYY-MM-DD, phải sau `startDate` |
| `status`             | (Nếu cung cấp) Một trong: `Draft`, `InReview`, `Approved`, `Active`, `InProgress`, `OnHold`, `Completed`, `Terminated`, `Expired`, `Cancelled` |
| `salesId`            | Số nguyên dương, phải là ID người dùng có vai trò Sales tồn tại trong hệ thống |
| `opportunityId`      | (Nếu cung cấp) Số nguyên dương, phải là ID cơ hội tồn tại trong hệ thống |
| `description`        | (Nếu cung cấp) Tối đa 2000 ký tự |
| `paymentTerms`       | Ít nhất 1 đợt thanh toán |
| `paymentTerms[].termNumber` | Số nguyên dương, các đợt phải có số thứ tự liên tiếp từ 1 |
| `paymentTerms[].dueDate` | Định dạng: YYYY-MM-DD |
| `paymentTerms[].amount` | Số dương, tổng các đợt phải bằng giá trị `amount` |
| `employeeAssignments[].employeeId` | Số nguyên dương, phải là ID nhân viên tồn tại trong hệ thống |
| `employeeAssignments[].startDate` | Định dạng: YYYY-MM-DD, phải nằm trong khoảng `startDate` và `endDate` của hợp đồng |
| `employeeAssignments[].endDate` | Định dạng: YYYY-MM-DD, phải sau `startDate` của assignment và không được sau `endDate` của hợp đồng |
| `employeeAssignments[].allocationPercentage` | Số từ 1 đến 100 |
| `employeeAssignments[].billRate` | (Nếu cung cấp) Số không âm |

### 3.5 Phân quyền đặc biệt
- Sales: Chỉ tạo được hợp đồng do mình phụ trách
- Division Manager: Tạo được hợp đồng cho tất cả Sales thuộc bộ phận mình quản lý
- Admin: Tạo được hợp đồng cho bất kỳ Sales nào

---

## 4. Response

### 4.1 Success - 201 Created

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 201 |
| `data` | Object | Đối tượng chứa thông tin chi tiết hợp đồng đã tạo |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contract` | Object | Thông tin chi tiết hợp đồng đã tạo |

#### Contract Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của hợp đồng |
| `contractCode` | String | Mã hợp đồng |
| `name` | String | Tên hợp đồng |
| `customerName` | String | Tên khách hàng |
| `contractType` | String | Loại hợp đồng |
| `amount` | Number | Tổng giá trị hợp đồng (VND) |
| `signDate` | String | Ngày ký hợp đồng (định dạng: YYYY-MM-DD) |
| `startDate` | String | Ngày bắt đầu hiệu lực (định dạng: YYYY-MM-DD) |
| `endDate` | String | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `status` | String | Trạng thái hợp đồng |
| `salesPerson` | Object | Thông tin người phụ trách Sales |
| `relatedOpportunity` | Object | Thông tin cơ hội liên kết (nếu có) |
| `description` | String | Mô tả chi tiết về hợp đồng |
| `paymentTerms` | Array | Danh sách các điều khoản thanh toán |
| `employeeAssignments` | Array | Danh sách nhân viên được phân công cho hợp đồng |
| `paymentStatus` | Object | Thông tin trạng thái thanh toán của hợp đồng |
| `createdBy` | Object | Thông tin người tạo hợp đồng |
| `createdAt` | String | Thời gian tạo (định dạng ISO 8601) |
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
| `status` | String | Trạng thái thanh toán (unpaid, invoiced, paid, overdue) |

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

#### Creator Object (createdBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người tạo |
| `name` | String | Họ tên người tạo |

#### Payment Status Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái thanh toán của hợp đồng |
| `paidAmount` | Number | Số tiền đã thanh toán |
| `totalAmount` | Number | Tổng giá trị hợp đồng |
| `paidPercentage` | Number | Phần trăm đã thanh toán |
| `nextDueDate` | String | Ngày đến hạn thanh toán tiếp theo |
| `nextDueAmount` | Number | Số tiền đến hạn thanh toán tiếp theo |
| `totalTerms` | Integer | Tổng số đợt thanh toán |
| `paidTerms` | Integer | Số đợt đã thanh toán |
| `remainingAmount` | Number | Số tiền còn lại phải thanh toán |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 201,
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
          "status": "unpaid"
        },
        {
          "id": 121,
          "termNumber": 2,
          "dueDate": "2025-07-20",
          "amount": 312500000,
          "description": "25% sau khi hoàn thành giai đoạn phân tích yêu cầu và thiết kế",
          "status": "unpaid"
        },
        {
          "id": 122,
          "termNumber": 3,
          "dueDate": "2025-09-20",
          "amount": 312500000,
          "description": "25% sau khi hoàn thành phát triển và bàn giao cho UAT",
          "status": "unpaid"
        },
        {
          "id": 123,
          "termNumber": 4,
          "dueDate": "2025-11-30",
          "amount": 312500000,
          "description": "25% sau khi hoàn thành dự án và nghiệm thu",
          "status": "unpaid"
        }
      ],
      "employeeAssignments": [
        {
          "id": 230,
          "employee": {
            "id": 15,
            "name": "Nguyễn Văn A",
            "position": "Senior Developer"
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
            "position": "Developer"
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
            "name": "Phan Văn C",
            "position": "UI/UX Designer"
          },
          "startDate": "2025-06-01",
          "endDate": "2025-11-20",
          "allocationPercentage": 50,
          "billRate": 18000000
        }
      ],
      "paymentStatus": {
        "status": "unpaid",
        "paidAmount": 0,
        "totalAmount": 1250000000,
        "paidPercentage": 0,
        "nextDueDate": "2025-05-25",
        "nextDueAmount": 312500000,
        "totalTerms": 4,
        "paidTerms": 0,
        "remainingAmount": 1250000000
      },
      "createdBy": {
        "id": 5,
        "name": "Trần Văn Sales"
      },
      "createdAt": "2025-05-15T10:30:45Z",
      "updatedAt": "2025-05-15T10:30:45Z"
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
      "field": "paymentTerms",
      "message": "Tổng số tiền các đợt thanh toán (1300000000) không khớp với tổng giá trị hợp đồng (1250000000)"
    },
    {
      "field": "endDate",
      "message": "Ngày kết thúc phải sau ngày bắt đầu"
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
  "message": "Bạn không có quyền tạo hợp đồng cho Sales này"
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
      "field": "customerName",
      "message": "Không tìm thấy khách hàng với tên: Công ty XYZ"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Xung đột dữ liệu",
  "errors": [
    {
      "field": "contractCode",
      "message": "Mã hợp đồng 'CTR-2025-045' đã tồn tại trong hệ thống"
    }
  ]
} 