# Mô tả Chi tiết Màn hình: MH-AUTH-01 - Đăng nhập

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Chiến Trần Văn    | Initial draft based on requirements      |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện đăng nhập cho người dùng để xác thực và truy cập vào hệ thống. Đây là điểm khởi đầu và cổng vào chính của hệ thống, đảm bảo chỉ những người dùng đã được cấp phép mới có thể sử dụng các chức năng trong hệ thống.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Tất cả người dùng** đều sử dụng màn hình này để đăng nhập vào hệ thống:
    *   Admin
    *   課長 (General Manager)
    *   部長 (Team Leader)
    *   Nhân viên (Employee)
    *   Kế toán và các vai trò khác

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Logo công ty:** Đặt ở phần trên cùng của form đăng nhập.
*   **Form đăng nhập:** Đặt ở trung tâm màn hình, nổi bật trên nền trang (có thể sử dụng card/box với đổ bóng).
*   **Thông báo lỗi:** Hiển thị phía trên form hoặc dưới trường nhập liệu tương ứng.
*   **Hình nền:** Có thể sử dụng hình nền đơn giản, chuyên nghiệp phù hợp với thương hiệu công ty.

## 4. Các Thành phần Chính (Components)

### 4.1. Form Đăng nhập

*   **Tiêu đề Form:** "Đăng nhập" hoặc "Đăng nhập hệ thống quản lý nội bộ".
*   **Trường Đăng nhập:**
    *   `Tên đăng nhập / Email`: Ô nhập text, placeholder "Nhập tên đăng nhập hoặc email".
    *   `Mật khẩu`: Ô nhập password (masked), placeholder "Nhập mật khẩu", có icon để hiện/ẩn mật khẩu.
*   **Checkbox:**
    *   `Ghi nhớ đăng nhập`: Cho phép lưu thông tin đăng nhập (tên người dùng) cho lần sau.
*   **Nút:**
    *   `Đăng nhập`: Nút chính, kích thước lớn, nổi bật để gửi form.
*   **Liên kết:**
    *   `Quên mật khẩu?`: Liên kết nhỏ bên dưới form, dẫn đến quy trình đặt lại mật khẩu.

### 4.2. Thông báo lỗi

*   **Thông báo lỗi chung:** Hiển thị phía trên form khi có lỗi xác thực hoặc lỗi hệ thống.
*   **Thông báo lỗi trường cụ thể:** Hiển thị dưới trường nhập liệu tương ứng (VD: "Tên đăng nhập không được để trống").

### 4.3. Thông tin Phiên bản

*   **Footer:** Hiển thị thông tin phiên bản hệ thống ở góc dưới của trang (nhỏ, nhẹ, không gây mất tập trung).

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Hiển thị form đăng nhập.
    *   Nếu đã lưu "Ghi nhớ đăng nhập", điền sẵn tên đăng nhập.
    *   Focus vào trường đầu tiên cần nhập (tên đăng nhập hoặc mật khẩu).
*   **Nhập Thông tin & Nhấn `Đăng nhập`:**
    *   Kiểm tra dữ liệu nhập (validation).
    *   Gửi thông tin đăng nhập tới server để xác thực.
    *   Nếu thành công: Chuyển người dùng đến màn hình Dashboard (`MH-DSH-01`).
    *   Nếu thất bại: Hiển thị thông báo lỗi thích hợp.
*   **Click `Quên mật khẩu?`:**
    *   Chuyển người dùng đến màn hình/quy trình đặt lại mật khẩu.
*   **Thoát/Đóng Browser:**
    *   Không lưu mật khẩu.
    *   Lưu tên đăng nhập nếu đã chọn "Ghi nhớ đăng nhập".

## 6. Các Điểm Cần Lưu ý / Validation

*   **Bảo mật:**
    *   Sử dụng HTTPS cho toàn bộ quá trình đăng nhập.
    *   Không lưu mật khẩu ở client-side.
    *   Mã hóa mật khẩu khi gửi đến server.
    *   Có thể sử dụng captcha nếu phát hiện nhiều lần đăng nhập thất bại.
*   **Validation:**
    *   Tên đăng nhập: Không được để trống.
    *   Mật khẩu: Không được để trống, độ dài tối thiểu.
*   **Xử lý Lỗi:**
    *   Hiển thị thông báo lỗi rõ ràng nhưng không cung cấp thông tin quá chi tiết về nguyên nhân (bảo mật).
    *   Xử lý các trường hợp như: tài khoản không tồn tại, mật khẩu sai, tài khoản bị khóa, lỗi kết nối...
*   **Trải nghiệm Người dùng:**
    *   Form đơn giản, dễ sử dụng.
    *   Có thể sử dụng phím Enter để submit form.
    *   Hiển thị loader/spinner khi đang xác thực để thông báo cho người dùng.
*   **Tính Tương thích:**
    *   Đảm bảo hiển thị đúng trên các thiết bị và trình duyệt khác nhau.
    *   Hỗ trợ trải nghiệm mobile (responsive design). 