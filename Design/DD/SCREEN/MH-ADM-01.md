# Mô tả Chi tiết Màn hình: MH-ADM-01 - (Admin) Quản lý Người dùng

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Chiến Trần Văn | Initial draft based on requirements        |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện quản trị viên (Admin) để quản lý người dùng trong hệ thống, bao gồm các chức năng Thêm, Xem, Sửa, Khóa/Mở khóa tài khoản và Reset mật khẩu. Quản trị viên có thể dễ dàng tìm kiếm, lọc và thực hiện các thao tác quản lý tài khoản người dùng.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem tất cả thông tin người dùng và thực hiện mọi thao tác quản lý (CRUD).
    *   Phân quyền người dùng, gán vai trò (Roles).
    *   Khóa/Mở khóa tài khoản, Reset mật khẩu.
*   **課長 (General Manager):**
    *   Có thể được cấp quyền hạn chế để xem thông tin người dùng thuộc phạm vi quản lý.
    *   Không có quyền thêm, sửa, xóa tài khoản mặc định (trừ khi được cấp quyền đặc biệt).

Lưu ý: Cần phân quyền rõ ràng, chỉ Admin mới truy cập được màn hình này theo mặc định. Các vai trò khác trong hệ thống không có quyền truy cập.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Tiêu đề trang:** "Quản lý Người dùng" - Nằm ở phía trên cùng.
*   **Khu vực Tìm kiếm & Bộ lọc:** Đặt ở phía trên, ngay dưới tiêu đề.
*   **Khu vực Hành động:** Các nút chức năng chính (`Thêm người dùng`) đặt gần khu vực lọc.
*   **Bảng Danh sách Người dùng:** Chiếm phần lớn diện tích, hiển thị danh sách người dùng dạng bảng.
*   **Phân trang (Pagination):** Nằm ở cuối bảng danh sách.
*   **Modal/Dialog:** Các hộp thoại popup để thực hiện các thao tác Thêm/Sửa/Reset mật khẩu.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Tìm kiếm / Bộ lọc

*   **Ô tìm kiếm:** Tìm kiếm theo `Tên đăng nhập`, `Họ tên`, `Email`.
*   **Bộ lọc (Dropdown/Multi-select):**
    *   `Vai trò (Role):` Admin, 課長, 部長, Nhân viên, Kế toán, Sales...
    *   `Trạng thái:` Tất cả, Hoạt động, Bị khóa.
    *   `Team/Bộ phận:` Lọc theo team/bộ phận nếu cần.
*   **Nút:**
    *   `Tìm kiếm / Lọc`: Áp dụng các tiêu chí tìm kiếm và lọc.
    *   `Xóa bộ lọc`: Đặt lại tất cả các trường lọc về giá trị mặc định.

### 4.2. Khu vực Hành động Chính

*   **Nút `Thêm người dùng`:**
    *   Mở modal/dialog form thêm người dùng mới.

### 4.3. Bảng Danh sách Người dùng

Hiển thị dữ liệu dạng bảng, cho phép sắp xếp (sort) theo các cột.

*   **Các cột (Columns):**
    *   `Tên đăng nhập:` (Hiển thị text).
    *   `Họ và Tên:` (Hiển thị text).
    *   `Email:` (Hiển thị text).
    *   `Vai trò:` (Hiển thị vai trò/roles của người dùng).
    *   `Team/Bộ phận:` (Nếu áp dụng).
    *   `Trạng thái:` (Hoạt động/Bị khóa - hiển thị bằng tag màu hoặc biểu tượng).
    *   `Ngày tạo:` (Thời gian tạo tài khoản).
    *   `Đăng nhập cuối:` (Thời gian đăng nhập gần nhất).
    *   `Thao tác:` Cột chứa các nút hành động:
        *   `Sửa`: Mở modal/dialog chỉnh sửa thông tin người dùng.
        *   `Khóa/Mở khóa`: Toggle trạng thái tài khoản (khóa/mở).
        *   `Reset mật khẩu`: Mở modal xác nhận reset mật khẩu.
*   **Sắp xếp (Sorting):** Cho phép click vào tiêu đề cột để sắp xếp.
*   **Phân trang (Pagination):** Hiển thị các điều khiển để chuyển trang khi số lượng người dùng vượt quá giới hạn hiển thị trên một trang (VD: 20, 50 bản ghi/trang).

### 4.4. Modal/Dialog Forms

#### 4.4.1. Modal Thêm/Sửa Người dùng

*   **Tiêu đề:** "Thêm người dùng mới" hoặc "Chỉnh sửa người dùng".
*   **Các trường nhập liệu:**
    *   `Tên đăng nhập:` (Bắt buộc, không được trùng).
    *   `Họ và tên:` (Bắt buộc).
    *   `Email:` (Bắt buộc, định dạng email).
    *   `Vai trò:` (Dropdown/Multi-select, bắt buộc).
    *   `Team/Bộ phận:` (Dropdown, tùy thuộc vào vai trò).
    *   `Mật khẩu:` (Chỉ hiển thị khi thêm mới, có thể tự động tạo).
    *   `Xác nhận mật khẩu:` (Chỉ hiển thị khi thêm mới).
    *   `Trạng thái:` (Checkbox "Hoạt động").
*   **Nút:**
    *   `Lưu`: Lưu thông tin và đóng modal.
    *   `Hủy`: Đóng modal không lưu thay đổi.

#### 4.4.2. Modal Reset Mật khẩu

*   **Tiêu đề:** "Reset mật khẩu người dùng".
*   **Nội dung:** Thông báo xác nhận việc reset mật khẩu, hiển thị tên người dùng.
*   **Tùy chọn:**
    *   `Tạo mật khẩu tự động`: Hệ thống tự tạo mật khẩu ngẫu nhiên.
    *   `Nhập mật khẩu mới`: Admin nhập mật khẩu mới cho người dùng.
*   **Nút:**
    *   `Xác nhận`: Thực hiện reset mật khẩu.
    *   `Hủy`: Đóng modal không thực hiện thay đổi.

#### 4.4.3. Dialog Xác nhận Khóa/Mở khóa

*   **Tiêu đề:** "Xác nhận khóa tài khoản" hoặc "Xác nhận mở khóa tài khoản".
*   **Nội dung:** Thông báo xác nhận hành động, hiển thị tên người dùng.
*   **Nút:**
    *   `Xác nhận`: Thực hiện khóa/mở khóa tài khoản.
    *   `Hủy`: Đóng dialog không thực hiện thay đổi.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Hệ thống kiểm tra quyền người dùng (chỉ Admin mới được truy cập).
    *   Truy vấn CSDL lấy danh sách người dùng.
    *   Áp dụng bộ lọc/sắp xếp mặc định (nếu có).
    *   Hiển thị dữ liệu lên bảng và cập nhật phân trang.
*   **Thay đổi Bộ lọc/Nhập Tìm kiếm & Click `Tìm kiếm / Lọc`:**
    *   Hệ thống thực hiện truy vấn mới dựa trên tiêu chí.
    *   Cập nhật lại Bảng Danh sách và phân trang.
*   **Click `Thêm người dùng`:**
    *   Mở modal Thêm người dùng mới.
    *   Admin nhập thông tin và click `Lưu`.
    *   Hệ thống kiểm tra dữ liệu (validation).
    *   Nếu hợp lệ, lưu thông tin người dùng mới vào CSDL.
    *   Cập nhật lại danh sách và hiển thị thông báo thành công.
*   **Click `Sửa` trong cột Thao tác:**
    *   Mở modal Chỉnh sửa người dùng với thông tin người dùng đã được điền sẵn.
    *   Admin cập nhật thông tin và click `Lưu`.
    *   Hệ thống kiểm tra dữ liệu (validation).
    *   Nếu hợp lệ, cập nhật thông tin người dùng trong CSDL.
    *   Cập nhật lại danh sách và hiển thị thông báo thành công.
*   **Click `Khóa/Mở khóa` trong cột Thao tác:**
    *   Mở dialog xác nhận Khóa/Mở khóa tài khoản.
    *   Admin click `Xác nhận`.
    *   Hệ thống cập nhật trạng thái tài khoản trong CSDL.
    *   Cập nhật lại trạng thái trong danh sách và hiển thị thông báo thành công.
*   **Click `Reset mật khẩu` trong cột Thao tác:**
    *   Mở modal Reset mật khẩu.
    *   Admin chọn phương thức reset và click `Xác nhận`.
    *   Hệ thống reset mật khẩu theo phương thức đã chọn.
    *   Hiển thị mật khẩu mới (nếu tạo tự động) hoặc thông báo đã reset thành công.
*   **Click Sắp xếp (Tiêu đề cột):**
    *   Hệ thống thực hiện truy vấn lại với tham số sắp xếp mới.
    *   Cập nhật lại Bảng Danh sách và phân trang.
*   **Click Phân trang:**
    *   Hệ thống thực hiện truy vấn để lấy dữ liệu cho trang được yêu cầu.
    *   Cập nhật lại Bảng Danh sách và trạng thái phân trang.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Bảo mật:** Đảm bảo chỉ Admin mới có quyền truy cập màn hình này.
*   **Kiểm tra dữ liệu nhập:**
    *   Tên đăng nhập: Không được trùng, độ dài và ký tự hợp lệ.
    *   Email: Định dạng email hợp lệ, không trùng.
    *   Mật khẩu: Đảm bảo mạnh theo chính sách (khi thêm mới hoặc reset).
*   **Xử lý mật khẩu:**
    *   Không hiển thị mật khẩu gốc trong CSDL (phải được mã hóa).
    *   Khi reset mật khẩu, cân nhắc gửi email thông báo cho người dùng (nếu có tích hợp email).
*   **Admin không thể tự khóa tài khoản của chính mình** để tránh tình trạng mất quyền truy cập hệ thống.
*   **Log thay đổi:** Ghi log đầy đủ các thao tác quản lý người dùng (thêm, sửa, khóa/mở, reset mật khẩu) để kiểm tra sau này nếu cần.
*   **Hiệu năng:** Tối ưu hóa truy vấn CSDL khi lọc/sắp xếp, đặc biệt khi số lượng người dùng lớn.
*   **Phân quyền chi tiết:** Nếu cần thiết, có thể mở rộng để hỗ trợ phân quyền chi tiết hơn (gán quyền cụ thể thay vì chỉ gán vai trò). 