# Mô tả Chi tiết Màn hình: MH-HRM-03 - Form Thêm/Sửa Nhân sự

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp một form nhập liệu tập trung để **thêm mới** một nhân viên hoặc **chỉnh sửa** thông tin của một nhân viên hiện có. Các trường hiển thị và cho phép chỉnh sửa trên form này phụ thuộc vào **chế độ (Thêm/Sửa)** và **quyền của người dùng** đang thao tác.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Truy cập ở chế độ `Thêm mới` (từ `MH-HRM-01`).
    *   Truy cập ở chế độ `Sửa` (từ `MH-HRM-02` cho bất kỳ nhân viên nào).
    *   Có quyền **nhập/sửa tất cả các trường thông tin** (cơ bản, tổ chức, skills, trạng thái, phân bổ...). Có thể cần phân tách rõ quyền quản lý Skills, Trạng thái/Phân bổ thuộc về Leader/課長.
*   **課長 (General Manager（課長）):**
    *   Truy cập ở chế độ `Thêm mới` (nếu được phép).
    *   Truy cập ở chế độ `Sửa` (từ `MH-HRM-02` cho nhân viên trong phạm vi).
    *   Có quyền nhập/sửa hầu hết các trường, **đặc biệt là Thông tin Tổ chức (Team, Leader)**, có thể cả Trạng thái/Phân bổ.
*   **部長 (Team Leader):**
    *   **Không** truy cập ở chế độ `Thêm mới`.
    *   Truy cập ở chế độ `Sửa` (từ `MH-HRM-02` cho thành viên team).
    *   Chỉ có quyền **sửa các trường được phép** cho thành viên team, chủ yếu là:
        *   Quản lý `Skills & Kinh nghiệm` (thêm/sửa/xóa skill, cập nhật năm KN, đánh giá skill - optional).
        *   Cập nhật `Trạng thái & Phân bổ` dự án.
        *   (Có thể xem các trường khác ở dạng read-only).
*   **Nhân viên (Employee):**
    *   **Không** truy cập ở chế độ `Thêm mới`.
    *   Truy cập ở chế độ `Sửa` (từ `MH-HRM-02` cho chính mình).
    *   Chỉ có quyền **sửa một số trường giới hạn**: Thông tin liên hệ cá nhân (Địa chỉ, SĐT, Liên hệ khẩn cấp), tự cập nhật `Skills & Kinh nghiệm` (thêm/sửa/xóa skill, năm KN, tự đánh giá).
    *   Các trường khác hiển thị read-only.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Tiêu đề:** Ghi rõ "Thêm mới Nhân sự" hoặc "Chỉnh sửa Nhân sự: [Tên Nhân viên]"
*   **Form Nhập liệu:** Chia thành các Section/Group rõ ràng tương ứng với các nhóm thông tin (như các Tab bên MH-HRM-02):
    *   Section 1: Thông tin Cơ bản & Cá nhân
    *   Section 2: Thông tin Tổ chức (Vị trí, Team, Leader)
    *   Section 3: Quản lý Skills & Kinh nghiệm (Có thể là bảng động cho phép thêm/sửa/xóa dòng skill)
    *   Section 4: Trạng thái & Phân bổ Dự án
*   **Khu vực Hành động:** Nút `Lưu`, nút `Hủy`.

## 4. Các Thành phần Chính (Components)

**(Lưu ý: Tính Read-only/Editable của các trường phụ thuộc vào Quyền và Chế độ)**

### 4.1. Section: Thông tin Cơ bản & Cá nhân

*   `Mã Nhân viên:` (Thường là Read-only khi Sửa, có thể tự sinh hoặc nhập khi Thêm mới)
*   `Họ và Tên:` (Input text, Bắt buộc)
*   `Ngày sinh:` (Date picker)
*   `Email công ty:` (Input email, Bắt buộc, có thể cần unique)
*   `Tài khoản nội bộ:` (Input text)
*   `Địa chỉ:` (Text area)
*   `Số điện thoại:` (Input text)
*   `Thông tin liên hệ khẩn cấp:` (Text area)
*   `Ảnh đại diện:` (Upload control - Optional)

### 4.2. Section: Thông tin Tổ chức (Thường chỉ Admin/課長 sửa)

*   `Ngày vào công ty:` (Date picker)
*   `Vị trí công việc:` (Dropdown/Select từ danh mục cấu hình)
*   `Team:` (Dropdown/Select từ danh sách Team)
*   `Leader trực tiếp:` (Dropdown/Select từ danh sách User có vai trò Leader)

### 4.3. Section: Quản lý Skills & Kinh nghiệm

*   Có thể là một **bảng động (dynamic table)** hoặc khu vực lặp lại (repeater):
    *   **Nút `Thêm Skill`:** Mở popup/dòng mới để chọn/nhập skill.
    *   **Mỗi dòng Skill gồm:**
        *   `Loại Skill:` (Dropdown: Ngôn ngữ, Framework...)
        *   `Tên Skill:` (Dropdown/Autocomplete dựa trên Loại Skill đã chọn, lấy từ `MH-HRM-04`)
        *   `Số năm kinh nghiệm:` (Input number)
        *   `Cấp độ (Tự đánh giá):` (Dropdown: Basic, Intermediate, Advanced)
        *   `Cấp độ (Leader đánh giá):` (Dropdown, Read-only cho Nhân viên, Editable cho Leader)
        *   **Nút `Xóa Skill`:** Xóa dòng skill tương ứng.
*   Quyền sửa các thành phần này phụ thuộc vào vai trò (Nhân viên tự cập nhật, Leader đánh giá/quản lý team).

### 4.4. Section: Trạng thái & Phân bổ Dự án (Thường chỉ Leader/課長/Admin sửa)

*   `Trạng thái hiện tại:` (Dropdown: Allocated, Available/Bench, Ending Soon, On Leave, Resigned...)
*   **Các trường phụ thuộc vào `Trạng thái hiện tại`:**
    *   Nếu là `Allocated` hoặc `Ending Soon`:
        *   `Dự án đang tham gia:` (Dropdown/Autocomplete từ danh sách Dự án/Hợp đồng đang hoạt động - liên kết Module 4)
        *   `% Phân bổ:` (Input number, 1-100)
        *   `Ngày dự kiến kết thúc:` (Date picker, bắt buộc nếu là `Ending Soon`)
    *   Nếu là `Resigned`:
        *   `Ngày nghỉ việc:` (Date picker)

### 4.5. Khu vực Hành động

*   **Nút `Lưu`:**
    *   Chức năng: Thực hiện validation các trường bắt buộc và dữ liệu nhập. Nếu hợp lệ, lưu thông tin vào CSDL (tạo mới hoặc cập nhật bản ghi nhân viên). Cập nhật các bảng liên quan (skills, trạng thái, phân bổ...).
    *   Sau khi lưu thành công, điều hướng về màn hình `MH-HRM-02` (nếu Sửa) hoặc `MH-HRM-01` (nếu Thêm mới).
*   **Nút `Hủy`:**
    *   Chức năng: Hủy bỏ các thay đổi chưa lưu, điều hướng về màn hình trước đó (`MH-HRM-01` hoặc `MH-HRM-02`). Cần có thông báo xác nhận nếu có thay đổi chưa lưu.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình (Chế độ Thêm mới - từ `MH-HRM-01`):**
    *   Kiểm tra quyền (Admin/課長).
    *   Hiển thị form trống với các trường cho phép nhập khi thêm mới.
*   **Load Màn hình (Chế độ Sửa - từ `MH-HRM-02`):**
    *   Nhận ID nhân viên.
    *   Kiểm tra quyền của người dùng đối với nhân viên này.
    *   Truy vấn CSDL lấy thông tin hiện tại của nhân viên.
    *   Điền dữ liệu vào form.
    *   Thiết lập trạng thái Read-only/Editable cho các trường dựa trên quyền.
*   **Người dùng Nhập/Sửa dữ liệu:** Tương tác với các input, dropdown, date picker, bảng skill...
*   **Click `Thêm Skill`:** Thêm một dòng mới vào bảng skill, cho phép người dùng nhập thông tin.
*   **Click `Xóa Skill`:** Xóa dòng skill tương ứng khỏi bảng (chưa xóa khỏi CSDL cho đến khi Lưu).
*   **Thay đổi `Trạng thái hiện tại`:** Có thể ẩn/hiện các trường liên quan (Dự án, % Phân bổ, Ngày kết thúc...).
*   **Click Nút `Lưu`:**
    *   Thực hiện validation phía client (trường bắt buộc, định dạng...).
    *   Gửi dữ liệu lên server.
    *   Server thực hiện validation phía server (logic nghiệp vụ, unique constraints...).
    *   Nếu thành công -> Lưu dữ liệu vào CSDL (INSERT hoặc UPDATE).
    *   Điều hướng về màn hình chi tiết/danh sách.
    *   Hiển thị thông báo thành công.
    *   Nếu thất bại -> Hiển thị thông báo lỗi cụ thể trên form.
*   **Click Nút `Hủy`:**
    *   Nếu có thay đổi -> Hiển thị confirm.
    *   Nếu xác nhận hủy -> Điều hướng về màn hình trước đó.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền Sửa chi tiết:** Logic phân quyền cho từng trường/section phải chính xác và chặt chẽ.
*   **Validation Dữ liệu:**
    *   Các trường bắt buộc không được để trống.
    *   Đúng định dạng (Email, Số, Ngày tháng).
    *   Logic nghiệp vụ (VD: % Phân bổ từ 1-100, Ngày kết thúc phải sau Ngày bắt đầu nếu có...).
    *   Kiểm tra Unique (Mã NV, Email công ty).
*   **Quản lý Skills:** Giao diện bảng động cần thân thiện, dễ sử dụng. Dữ liệu skill lấy từ danh mục chuẩn (`MH-HRM-04`).
*   **Liên kết Dữ liệu:** Khi chọn Dự án, cần đảm bảo liên kết đúng với Module Hợp đồng/Dự án.
*   **Xác nhận Hủy:** Cần cảnh báo người dùng nếu họ hủy mà chưa lưu thay đổi.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Autocomplete/Suggestion:** Sử dụng gợi ý cho các trường như Tên Skill, Tên Dự án.
*   **Lưu nháp:** Cho phép lưu lại form đang nhập dở dang.
*   **Validation Real-time:** Cung cấp phản hồi validation ngay khi người dùng nhập liệu (cho các lỗi định dạng cơ bản). 