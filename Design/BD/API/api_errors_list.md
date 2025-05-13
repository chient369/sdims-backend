# Danh sách Mã lỗi API

**Version Control:**

| Version | Date       | Author      | Changes                                  | Status    |
| :------ | :--------- | :---------- | :--------------------------------------- | :-------- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Initial creation of error codes list     | Draft     |

---

Tài liệu này liệt kê tất cả các mã lỗi có thể gặp phải khi gọi API của hệ thống. Mỗi mã lỗi bao gồm mã HTTP status, mã lỗi nội bộ, và mô tả chi tiết về lỗi.

## 1. Lỗi Xác thực & Phân quyền (Authentication & Authorization) - E1xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E1000      | 401         | Token không hợp lệ hoặc đã hết hạn               | Làm mới token hoặc đăng nhập lại                  |
| E1001      | 401         | Chưa đăng nhập                                    | Đăng nhập để lấy token                            |
| E1002      | 403         | Không có quyền truy cập chức năng này            | Liên hệ Admin để cấp quyền                        |
| E1003      | 403         | Không có quyền xem dữ liệu này                   | Liên hệ Admin để cấp quyền                        |
| E1004      | 401         | Tài khoản bị khóa                                | Liên hệ Admin để mở khóa tài khoản                |
| E1005      | 401         | Sai tên đăng nhập hoặc mật khẩu                  | Kiểm tra thông tin đăng nhập                      |
| E1006      | 429         | Đăng nhập thất bại quá nhiều lần                 | Thử lại sau ít phút                               |

## 2. Lỗi Tham số Request (Request Parameter) - E2xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E2000      | 400         | Tham số không hợp lệ                             | Kiểm tra lại tham số gửi lên                      |
| E2001      | 400         | Thiếu tham số bắt buộc                           | Bổ sung tham số bắt buộc                          |
| E2002      | 400         | Giá trị tham số nằm ngoài phạm vi cho phép       | Điều chỉnh giá trị tham số                        |
| E2003      | 400         | Định dạng tham số không hợp lệ                   | Kiểm tra lại định dạng (ngày tháng, email...)     |
| E2004      | 400         | Upload file không hợp lệ                         | Kiểm tra kích thước, định dạng file               |
| E2005      | 400         | Quá nhiều tham số                                | Giảm số lượng tham số                             |
| E2006      | 414         | URL quá dài                                      | Rút gọn URL hoặc chuyển sang dùng POST với body   |

## 3. Lỗi Truy vấn Dữ liệu (Data Access) - E3xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E3000      | 404         | Không tìm thấy dữ liệu                           | Kiểm tra lại ID hoặc tham số tìm kiếm             |
| E3001      | 404         | Không tìm thấy nhân viên                         | Kiểm tra lại mã nhân viên                         |
| E3002      | 404         | Không tìm thấy cơ hội kinh doanh                 | Kiểm tra lại mã cơ hội                           |
| E3003      | 404         | Không tìm thấy hợp đồng                          | Kiểm tra lại mã hợp đồng                          |
| E3004      | 404         | Không tìm thấy vai trò (role)                    | Kiểm tra lại mã vai trò                           |
| E3005      | 404         | Không tìm thấy người dùng                        | Kiểm tra lại mã người dùng                        |
| E3006      | 404         | Không tìm thấy kỹ năng                           | Kiểm tra lại mã kỹ năng                           |
| E3007      | 404         | Không tìm thấy file đính kèm                     | Kiểm tra lại mã file                              |

## 4. Lỗi Thêm/Sửa/Xóa Dữ liệu - E4xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E4000      | 400         | Dữ liệu đã tồn tại                               | Kiểm tra lại thông tin (mã trùng lặp)             |
| E4001      | 400         | Dữ liệu không hợp lệ                             | Kiểm tra lại thông tin nhập                       |
| E4002      | 400         | Dữ liệu vi phạm ràng buộc                        | Kiểm tra lại mối quan hệ với dữ liệu khác         |
| E4003      | 400         | Không thể xóa do có dữ liệu liên quan            | Xóa dữ liệu liên quan trước                       |
| E4004      | 409         | Xung đột dữ liệu                                 | Dữ liệu đã bị thay đổi bởi người khác             |
| E4005      | 422         | Dữ liệu không thỏa mãn điều kiện nghiệp vụ       | Kiểm tra lại điều kiện nghiệp vụ                  |
| E4006      | 400         | Trạng thái không hợp lệ                          | Kiểm tra lại trạng thái hiện tại và mong muốn     |

## 5. Lỗi Kết nối Bên ngoài (External Integration) - E5xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E5000      | 502         | Lỗi kết nối Hubspot                              | Kiểm tra cấu hình kết nối Hubspot                 |
| E5001      | 504         | Hubspot timeout                                  | Thử lại sau                                       |
| E5002      | 502         | Lỗi đồng bộ dữ liệu Hubspot                      | Kiểm tra log để biết chi tiết lỗi                 |
| E5003      | 502         | Lỗi kết nối API bên ngoài                        | Kiểm tra cấu hình kết nối                         |

## 6. Lỗi Hệ thống (System Errors) - E6xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E6000      | 500         | Lỗi hệ thống không xác định                      | Liên hệ quản trị viên                             |
| E6001      | 500         | Lỗi database                                     | Liên hệ quản trị viên                             |
| E6002      | 500         | Lỗi xử lý file                                   | Kiểm tra file và thử lại                          |
| E6003      | 503         | Hệ thống tạm thời không khả dụng                 | Thử lại sau                                       |
| E6004      | 500         | Lỗi xử lý nghiệp vụ                              | Liên hệ quản trị viên với mã lỗi                  |
| E6005      | 507         | Hết dung lượng lưu trữ                           | Liên hệ quản trị viên                             |

## 7. Lỗi Import/Export Dữ liệu - E7xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E7000      | 400         | File import không hợp lệ                         | Kiểm tra định dạng file và template               |
| E7001      | 400         | Dữ liệu trong file import không hợp lệ           | Kiểm tra và sửa dữ liệu trong file                |
| E7002      | 400         | Lỗi xử lý file import                            | Kiểm tra và thử lại với file khác                 |
| E7003      | 500         | Lỗi tạo file export                              | Thử lại hoặc liên hệ quản trị viên               |

## 8. Lỗi Margin & Hiệu suất - E8xxx

| Error Code | HTTP Status | Mô tả                                            | Giải pháp                                         |
|------------|-------------|--------------------------------------------------|---------------------------------------------------|
| E8000      | 400         | Dữ liệu chi phí không hợp lệ                     | Kiểm tra dữ liệu chi phí nhập vào                 |
| E8001      | 400         | Dữ liệu doanh thu không hợp lệ                   | Kiểm tra dữ liệu doanh thu nhập vào               |
| E8002      | 400         | Thời gian tính toán margin không hợp lệ          | Kiểm tra thời gian tính toán                      |
| E8003      | 404         | Không tìm thấy dữ liệu margin                    | Kiểm tra xem đã nhập chi phí chưa                 |

## Response Format Mẫu

### Mẫu Lỗi Tham số (400 Bad Request)
```json
{
  "status": "error",
  "code": "E2000",
  "message": "Tham số không hợp lệ",
  "errors": [
    {
      "field": "size",
      "message": "Kích thước trang phải nhỏ hơn hoặc bằng 100"
    }
  ]
}
```

### Mẫu Lỗi Không tìm thấy (404 Not Found)
```json
{
  "status": "error",
  "code": "E3001",
  "message": "Không tìm thấy nhân viên với ID: 123"
}
```

### Mẫu Lỗi Không có quyền (403 Forbidden)
```json
{
  "status": "error",
  "code": "E1002",
  "message": "Không có quyền truy cập chức năng này"
}
```

### Mẫu Lỗi Hệ thống (500 Internal Server Error)
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống không xác định",
  "traceId": "abc-xyz-123" // ID truy vết để tìm trong log
}
``` 