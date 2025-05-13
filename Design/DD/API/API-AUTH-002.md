# API Details: Đăng xuất

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo tài liệu API đăng xuất | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để đăng xuất người dùng bằng cách hủy token hiện tại phía server.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-AUTH-002                                 |
| **Tên API**        | Đăng xuất                                    |
| **Mô tả**          | API hủy token hiện tại của người dùng phía server |
| **Module**         | Authentication & Authorization                |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/auth/logout`                        |
| **Quyền truy cập** | auth:read:own                                |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Request Body

Không yêu cầu body.

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `message` | String | Thông báo kết quả thao tác: "Đăng xuất thành công" |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "message": "Đăng xuất thành công"
}
```

### 4.2 Error Responses

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1000",
  "message": "Token không hợp lệ hoặc đã hết hạn"
}
```

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1001",
  "message": "Chưa đăng nhập"
}
``` 