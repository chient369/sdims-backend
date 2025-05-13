# API Details: Cập nhật thông tin hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Chuẩn hóa tài liệu API cập nhật thông tin hợp đồng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để cập nhật thông tin của một hợp đồng đã tồn tại trong hệ thống, bao gồm thông tin cơ bản, điều khoản thanh toán và danh sách nhân viên tham gia, giúp duy trì tính chính xác của thông tin hợp đồng khi có thay đổi trong quá trình thực hiện.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-CTR-004                                  |
| **Tên API**        | Cập nhật thông tin hợp đồng                  |
| **Mô tả**          | API cho phép cập nhật thông tin của một hợp đồng đã tồn tại |
| **Module**         | Quản lý Hợp đồng & Doanh thu                 |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/contracts/{contractId}`             |
| **Quyền truy cập** | contract:update                             |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `contractId`   | Integer      | Có       | ID của hợp đồng cần cập nhật |

### 3.3 Request Body

```json
{
  "name": "Hệ thống CRM cho Công ty ABC (Phiên bản mở rộng)",
  "customerName": "Công ty ABC",
  "contractType": "FixedPrice",
  "amount": 1500000000,
  "signDate": "2025-05-15",
  "startDate": "2025-05-20",
  "endDate": "2025-12-31",
  "status": "InProgress",
  "salesId": 5,
  "oppId": 134,
  "description": "Hợp đồng phát triển hệ thống CRM bao gồm quản lý khách hàng, bán hàng, báo cáo và thêm module marketing automation",
  "paymentTerms": [
    {
      "id": 120,
      "termNumber": 1,
      "dueDate": "2025-05-25",
      "amount": 375000000,
      "description": "Tạm ứng 25% khi khởi động dự án",
      "status": "paid",
      "paidDate": "2025-05-23T00:00:00Z",
      "paidAmount": 312500000
    },
    {
      "id": 121,
      "termNumber": 2,
      "dueDate": "2025-07-20",
      "amount": 375000000,
      "description": "25% sau khi hoàn thành giai đoạn phân tích yêu cầu và thiết kế",
      "status": "unpaid"
    },
    {
      "id": 122,
      "termNumber": 3,
      "dueDate": "2025-10-20",
      "amount": 375000000,
      "description": "25% sau khi hoàn thành phát triển và bàn giao cho UAT",
      "status": "unpaid"
    },
    {
      "id": 123,
      "termNumber": 4,
      "dueDate": "2025-12-31",
      "amount": 375000000,
      "description": "25% sau khi hoàn thành dự án và nghiệm thu",
      "status": "unpaid"
    }
  ],
  "employeeAssignments": [
    {
      "id": 230,
      "employeeId": 15,
      "startDate": "2025-05-20",
      "endDate": "2025-12-31",
      "allocationPercentage": 100,
      "billRate": 25000000
    },
    {
      "id": 231,
      "employeeId": 22,
      "startDate": "2025-05-20",
      "endDate": "2025-11-30",
      "allocationPercentage": 100,
      "billRate": 20000000
    },
    {
      "id": 232,
      "employeeId": 28,
      "startDate": "2025-06-01",
      "endDate": "2025-12-31",
      "allocationPercentage": 50,
      "billRate": 18000000
    },
    {
      "employeeId": 35,
      "startDate": "2025-08-01",
      "endDate": "2025-12-31",
      "allocationPercentage": 100,
      "billRate": 22000000
    }
  ]
}
```

### 3.3 Body Parameters

| Tên                  | Kiểu dữ liệu     | Bắt buộc | Mô tả |
|----------------------|------------------|----------|-------|
| `name`               | String           | Không    | Tên hợp đồng |
| `customerName`       | String           | Không    | Tên khách hàng |
| `contractType`       | String           | Không    | Loại hợp đồng |
| `amount`             | Number           | Không    | Tổng giá trị hợp đồng (VND) |
| `signDate`           | String           | Không    | Ngày ký hợp đồng (định dạng: YYYY-MM-DD) |
| `startDate`          | String           | Không    | Ngày bắt đầu hiệu lực (định dạng: YYYY-MM-DD) |
| `endDate`            | String           | Không    | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `status`             | String           | Không    | Trạng thái hợp đồng |
| `salesId`            | Integer          | Không    | ID của người phụ trách Sales |
| `oppId`              | Integer          | Không    | ID của cơ hội liên kết |
| `description`        | String           | Không    | Mô tả chi tiết về hợp đồng |
| `paymentTerms`       | Array of Object  | Không    | Các điều khoản thanh toán |
| `paymentTerms[].id`              | Integer  | Không*   | ID của đợt thanh toán (nếu cập nhật đợt đã tồn tại) |
| `paymentTerms[].termNumber`      | Integer  | Có       | Số thứ tự của đợt thanh toán |
| `paymentTerms[].dueDate`         | String   | Có       | Ngày đến hạn thanh toán (định dạng: YYYY-MM-DD) |
| `paymentTerms[].amount`          | Number   | Có       | Số tiền phải thanh toán trong đợt này |
| `paymentTerms[].description`     | String   | Không    | Mô tả về đợt thanh toán |
| `paymentTerms[].status`          | String   | Không    | Trạng thái thanh toán (chỉ Admin/Kế toán mới có quyền cập nhật) |
| `paymentTerms[].paidDate`        | String   | Không    | Ngày thanh toán thực tế (định dạng ISO: YYYY-MM-DDTHH:MM:SSZ) |
| `paymentTerms[].paidAmount`      | Number   | Không    | Số tiền đã thanh toán thực tế |
| `employeeAssignments`            | Array of Object | Không    | Danh sách nhân viên tham gia |
| `employeeAssignments[].id`       | Integer  | Không*   | ID của assignment (nếu cập nhật assignment đã tồn tại) |
| `employeeAssignments[].employeeId` | Integer  | Có       | ID của nhân viên |
| `employeeAssignments[].startDate`  | String   | Có       | Ngày bắt đầu tham gia (định dạng: YYYY-MM-DD) |
| `employeeAssignments[].endDate`    | String   | Có       | Ngày kết thúc dự kiến (định dạng: YYYY-MM-DD) |
| `employeeAssignments[].allocationPercentage` | Number | Có | Phần trăm phân bổ thời gian (0-100) |
| `employeeAssignments[].billRate`   | Number   | Không    | Đơn giá billing của nhân viên (VND/tháng) |

*Bắt buộc khi cập nhật các đợt thanh toán hoặc assignment đã tồn tại

### 3.3 Validate Rule

| Trường               | Điều kiện hợp lệ |
|----------------------|------------------|
| `contractId`         | Số nguyên dương, phải tồn tại trong hệ thống |
| `name`               | (Nếu cung cấp) Không được để trống, tối đa 255 ký tự |
| `customerName`       | (Nếu cung cấp) Không được để trống, tối đa 255 ký tự |
| `contractType`       | (Nếu cung cấp) Một trong: `FixedPrice`, `TimeAndMaterial`, `Retainer`, `Maintenance`, `Other` |
| `amount`             | (Nếu cung cấp) Số dương |
| `signDate`           | (Nếu cung cấp) Định dạng: YYYY-MM-DD, không được là ngày trong tương lai |
| `startDate`          | (Nếu cung cấp) Định dạng: YYYY-MM-DD, phải sau hoặc bằng `signDate` |
| `endDate`            | (Nếu cung cấp) Định dạng: YYYY-MM-DD, phải sau `startDate` |
| `status`             | (Nếu cung cấp) Một trong: `Draft`, `InReview`, `Approved`, `Active`, `InProgress`, `OnHold`, `Completed`, `Terminated`, `Expired`, `Cancelled` |
| `salesId`            | (Nếu cung cấp) Số nguyên dương, phải là ID người dùng có vai trò Sales tồn tại trong hệ thống |
| `oppId`              | (Nếu cung cấp) Số nguyên dương, phải là ID cơ hội tồn tại trong hệ thống |
| `description`        | (Nếu cung cấp) Tối đa 2000 ký tự |
| `paymentTerms[].termNumber` | Số nguyên dương, các đợt phải có số thứ tự liên tiếp từ 1 |
| `paymentTerms[].dueDate` | Định dạng: YYYY-MM-DD |
| `paymentTerms[].amount` | Số dương, tổng các đợt phải bằng giá trị `amount` |
| `paymentTerms[].status` | (Nếu cung cấp) Một trong: `unpaid`, `partial`, `paid`, `overdue`, `cancelled` |
| `employeeAssignments[].employeeId` | Số nguyên dương, phải là ID nhân viên tồn tại trong hệ thống |
| `employeeAssignments[].startDate` | Định dạng: YYYY-MM-DD, phải nằm trong khoảng `startDate` và `endDate` của hợp đồng |
| `employeeAssignments[].endDate` | Định dạng: YYYY-MM-DD, phải sau `startDate` của assignment và không được sau `endDate` của hợp đồng |
| `employeeAssignments[].allocationPercentage` | Số từ 1 đến 100 |
| `employeeAssignments[].billRate` | (Nếu cung cấp) Số không âm |

### 3.4 Phân quyền đặc biệt
- Sales: Chỉ sửa được hợp đồng do mình phụ trách
- Division Manager: Sửa được hợp đồng cho tất cả Sales thuộc bộ phận mình quản lý
- Admin: Sửa được hợp đồng cho bất kỳ Sales nào
- **Lưu ý đặc biệt:** Chỉ Admin và Kế toán mới có quyền cập nhật trạng thái thanh toán (`status`, `paidDate`, `paidAmount`) của các đợt thanh toán. Các đợt thanh toán đã "paid" không nên sửa trừ khi có trường hợp đặc biệt (chỉ Admin).

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin chi tiết hợp đồng đã cập nhật và tóm tắt các thay đổi |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `contract` | Object | Thông tin chi tiết hợp đồng sau khi cập nhật |
| `changes` | Object | Thông tin tóm tắt về các thay đổi đã thực hiện |

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
| `paymentStatus` | Object | Tóm tắt trạng thái thanh toán hiện tại |
| `updatedBy` | Object | Thông tin người cập nhật |
| `updatedAt` | String | Thời gian cập nhật (định dạng ISO 8601) |

#### Changes Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `fieldName` | Object | Thông tin về thay đổi của từng trường (dynamically generated) |
| `paymentTerms` | Object | Thông tin về thay đổi của các điều khoản thanh toán |
| `employeeAssignments` | Object | Thông tin về thay đổi của các phân công nhân viên |

#### Customer Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của khách hàng |
| `name` | String | Tên khách hàng |

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

#### Payment Status Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái thanh toán tổng thể (unpaid, partial, paid, overdue) |
| `totalTerms` | Integer | Tổng số đợt thanh toán |
| `paidTerms` | Integer | Số đợt đã thanh toán |
| `remainingAmount` | Number | Số tiền còn lại cần thanh toán |
| `nextDueDate` | String/null | Ngày đến hạn thanh toán tiếp theo (định dạng: YYYY-MM-DD) |
| `nextDueAmount` | Number | Số tiền phải thanh toán ở đợt tiếp theo |

#### Updater Object (updatedBy)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người cập nhật |
| `name` | String | Họ tên người cập nhật |

#### Field Change Object (trong changes)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `from` | Any | Giá trị trước khi thay đổi |
| `to` | Any | Giá trị sau khi thay đổi |

#### Collection Change Object (trong changes.paymentTerms, changes.employeeAssignments)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `updated` | Integer | Số lượng item đã cập nhật |
| `added` | Integer | Số lượng item đã thêm mới |
| `removed` | Integer | Số lượng item đã xóa |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "contract": {
      "id": 45,
      "contractCode": "CTR-2025-045",
      "name": "Hệ thống CRM cho Công ty ABC (Phiên bản mở rộng)",
      "customerName": "Công ty ABC",
      "contractType": "FixedPrice",
      "amount": 1500000000,
      "signDate": "2025-05-15",
      "startDate": "2025-05-20",
      "endDate": "2025-12-31",
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
      "description": "Hợp đồng phát triển hệ thống CRM bao gồm quản lý khách hàng, bán hàng, báo cáo và thêm module marketing automation",
      "paymentTerms": [
        {
          "id": 120,
          "termNumber": 1,
          "dueDate": "2025-05-25",
          "amount": 375000000,
          "description": "Tạm ứng 25% khi khởi động dự án",
          "status": "paid",
          "paidDate": "2025-05-23T00:00:00Z",
          "paidAmount": 312500000
        },
        {
          "id": 121,
          "termNumber": 2,
          "dueDate": "2025-07-20",
          "amount": 375000000,
          "description": "25% sau khi hoàn thành giai đoạn phân tích yêu cầu và thiết kế",
          "status": "unpaid",
          "paidDate": null,
          "paidAmount": 0
        },
        {
          "id": 122,
          "termNumber": 3,
          "dueDate": "2025-10-20",
          "amount": 375000000,
          "description": "25% sau khi hoàn thành phát triển và bàn giao cho UAT",
          "status": "unpaid",
          "paidDate": null,
          "paidAmount": 0
        },
        {
          "id": 123,
          "termNumber": 4,
          "dueDate": "2025-12-31",
          "amount": 375000000,
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
            "position": "Senior Developer"
          },
          "startDate": "2025-05-20",
          "endDate": "2025-12-31",
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
          "endDate": "2025-11-30",
          "allocationPercentage": 100,
          "billRate": 20000000
        },
        {
          "id": 232,
          "employee": {
            "id": 28,
            "name": "Phạm Văn C",
            "position": "Tester"
          },
          "startDate": "2025-06-01",
          "endDate": "2025-12-31",
          "allocationPercentage": 50,
          "billRate": 18000000
        },
        {
          "id": 245,
          "employee": {
            "id": 35,
            "name": "Hoàng Thị D",
            "position": "Developer"
          },
          "startDate": "2025-08-01",
          "endDate": "2025-12-31",
          "allocationPercentage": 100,
          "billRate": 22000000
        }
      ],
      "paymentStatus": {
        "status": "partial",
        "paidAmount": 312500000,
        "totalAmount": 1500000000,
        "paidPercentage": 20.83,
        "nextDueDate": "2025-07-20",
        "nextDueAmount": 375000000,
        "totalTerms": 4,
        "paidTerms": 1,
        "remainingAmount": 1187500000
      },
      "updatedBy": {
        "id": 5,
        "name": "Trần Văn Sales"
      },
      "updatedAt": "2025-06-10T09:45:30Z"
    },
    "changes": {
      "amount": {
        "from": 1250000000,
        "to": 1500000000
      },
      "endDate": {
        "from": "2025-11-20",
        "to": "2025-12-31"
      },
      "description": {
        "updated": true
      },
      "paymentTerms": {
        "updated": 4,
        "added": 0,
        "removed": 0
      },
      "employeeAssignments": {
        "updated": 3,
        "added": 1,
        "removed": 0
      }
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
      "field": "amount",
      "message": "Giá trị hợp đồng phải là số dương"
    },
    {
      "field": "paymentTerms",
      "message": "Tổng giá trị các đợt thanh toán (1,400,000,000) phải bằng tổng giá trị hợp đồng (1,500,000,000)"
    },
    {
      "field": "paymentTerms[0].status",
      "message": "Không có quyền cập nhật trạng thái thanh toán"
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
  "message": "Bạn không có quyền cập nhật hợp đồng này"
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

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Xung đột dữ liệu",
  "errors": [
    {
      "field": "status",
      "message": "Không thể cập nhật: Hợp đồng này đã ở trạng thái 'Completed'"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E5000",
  "message": "Lỗi hệ thống khi cập nhật dữ liệu hợp đồng"
}
``` 