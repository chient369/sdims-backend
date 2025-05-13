# API Details: Cập nhật kỹ năng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-03 | Chiến Trần Văn | Tạo mới | -           | Draft     |
| 1.1     | 2025-05-10 | Chiến Trần Văn | Bổ sung mô tả chi tiết về cấu trúc API response | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên cập nhật thông tin của một kỹ năng (skill) đã tồn tại trong hệ thống, bao gồm các thông tin cơ bản và danh sách các cấp độ kỹ năng, giúp duy trì và điều chỉnh thông tin kỹ năng phù hợp với nhu cầu của tổ chức.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-HRM-015                                  |
| **Tên API**        | Cập nhật kỹ năng                             |
| **Mô tả**          | API cho phép cập nhật thông tin của một kỹ năng |
| **Module**         | Quản lý Nhân sự (HRM)                        |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/admin/skills/{id}`                  |
| **Quyền truy cập** | skill:update                                 |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên  | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------|--------------|----------|-------|
| `id` | Integer      | Có       | ID của kỹ năng cần cập nhật |

### 3.3 Request Body

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `name`         | String       | Không    | Tên kỹ năng |
| `description`  | String       | Không    | Mô tả về kỹ năng |
| `categoryId`   | Integer      | Không    | ID của loại kỹ năng |
| `active`       | Boolean      | Không    | Trạng thái kích hoạt |
| `levels`       | Array        | Không    | Mảng các cấp độ kỹ năng |

#### Chi tiết Object `levels`

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `id`           | Integer      | Không    | ID của cấp độ (nếu là cấp độ đã tồn tại) |
| `name`         | String       | Có       | Tên cấp độ kỹ năng |
| `description`  | String       | Không    | Mô tả về cấp độ |
| `sortOrder`    | Integer      | Không    | Thứ tự sắp xếp |
| `delete`       | Boolean      | Không    | Nếu `true`, xóa cấp độ này (chỉ áp dụng cho cấp độ đã tồn tại) |

### 3.4 Validate Rule

| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `id`           | Phải là số nguyên dương và tồn tại trong hệ thống |
| `name`         | Độ dài: 1-100 ký tự, Không được trùng lặp với các kỹ năng khác |
| `description`  | Độ dài tối đa: 500 ký tự |
| `categoryId`   | Phải là số nguyên dương và tồn tại trong hệ thống |
| `levels.name`  | Độ dài: 1-50 ký tự |
| `levels.id`    | Phải là số nguyên dương và tồn tại trong hệ thống (nếu có) |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả: "Cập nhật kỹ năng thành công" |
| `data` | Object | Đối tượng chứa thông tin chi tiết về kỹ năng sau khi cập nhật |

#### Data Object (Skill)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của kỹ năng |
| `name` | String | Tên kỹ năng (đã cập nhật) |
| `description` | String | Mô tả về kỹ năng (đã cập nhật) |
| `category` | Object | Thông tin về loại kỹ năng (đã cập nhật) |
| `active` | Boolean | Trạng thái kích hoạt (đã cập nhật) |
| `levels` | Array | Mảng các cấp độ kỹ năng (đã cập nhật) |
| `updatedAt` | String | Thời gian cập nhật (định dạng ISO 8601) |
| `updatedBy` | String | Người thực hiện cập nhật |

#### Category Object (trong Skill)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của loại kỹ năng |
| `name` | String | Tên loại kỹ năng |

#### Level Object (trong mảng levels)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của cấp độ kỹ năng |
| `name` | String | Tên cấp độ kỹ năng |
| `description` | String | Mô tả về cấp độ |
| `sortOrder` | Integer | Thứ tự sắp xếp |

```json
{
  "status": "success",
  "code": 200,
  "message": "Cập nhật kỹ năng thành công",
  "data": {
    "id": 51,
    "name": "Docker & Kubernetes",
    "description": "Công nghệ container và orchestration",
    "category": {
      "id": 9,
      "name": "DevOps & CI/CD"
    },
    "active": true,
    "levels": [
      {
        "id": 1,
        "name": "Basic",
        "description": "Hiểu biết cơ bản về Docker và Kubernetes",
        "sortOrder": 1
      },
      {
        "id": 2,
        "name": "Intermediate",
        "description": "Có thể tạo Dockerfile, sử dụng docker-compose, triển khai ứng dụng cơ bản trên Kubernetes",
        "sortOrder": 2
      },
      {
        "id": 3,
        "name": "Advanced",
        "description": "Có kinh nghiệm triển khai hệ thống phức tạp, hiểu sâu về networking, security, autoscaling",
        "sortOrder": 3
      },
      {
        "id": 4,
        "name": "Expert",
        "description": "Có thể thiết kế, triển khai và vận hành các hệ thống container phức tạp ở quy mô lớn",
        "sortOrder": 4
      }
    ],
    "updatedAt": "2025-05-02T15:30:00Z",
    "updatedBy": "admin"
  }
}
```

### 4.2 Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Dữ liệu không hợp lệ",
  "errors": [
    {
      "field": "name",
      "message": "Tên kỹ năng không được để trống"
    }
  ]
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4000",
  "message": "Dữ liệu đã tồn tại",
  "errors": [
    {
      "field": "name",
      "message": "Kỹ năng 'Kubernetes' đã tồn tại trong hệ thống"
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
  "code": "E3000",
  "message": "Không tìm thấy kỹ năng với ID: 99"
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4001",
  "message": "Không thể xóa cấp độ kỹ năng",
  "errors": [
    {
      "field": "levels[2].delete",
      "message": "Cấp độ này đang được sử dụng bởi 8 nhân viên"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi cập nhật kỹ năng"
}
``` 