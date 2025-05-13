# Mô tả Chi tiết Màn hình: MH-HRM-02 - Chi tiết Nhân sự

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này hiển thị thông tin chi tiết và toàn diện về một nhân viên cụ thể được chọn từ màn hình danh sách (`MH-HRM-01`). Nó cho phép người dùng (tùy theo quyền) xem thông tin cá nhân, kỹ năng, kinh nghiệm, trạng thái hiện tại, lịch sử dự án và cung cấp điểm truy cập để chỉnh sửa thông tin (thông qua MH-HRM-03).

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem chi tiết *tất cả* nhân viên.
    *   Thấy tất cả các mục thông tin (bao gồm cả thông tin nhạy cảm nếu có).
    *   Có nút `Sửa` để điều hướng đến `MH-HRM-03`.
*   **課長 (General Manager（課長）):**
    *   Xem chi tiết *tất cả* nhân viên (hoặc trong phạm vi quản lý).
    *   Thấy các mục thông tin cần thiết cho quản lý.
    *   Có nút `Sửa`.
*   **部長 (Team Leader):**
    *   Chỉ xem được chi tiết nhân viên *thuộc team mình quản lý*.
    *   Thấy các mục thông tin liên quan đến quản lý team (VD: skills, trạng thái, dự án).
    *   Có nút `Sửa` (để cập nhật skill, trạng thái, phân bổ dự án cho thành viên team).
*   **Nhân viên (Employee):**
    *   Xem thông tin chi tiết *của chính mình*.
    *   Có thể có quyền sửa một số thông tin cơ bản hoặc cập nhật skills (thông qua nút `Sửa` điều hướng đến `MH-HRM-03` với form được giới hạn trường).

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Thông tin Cá nhân:** Phía trên hoặc cột bên trái, hiển thị ảnh đại diện (nếu có), họ tên, mã NV, vị trí, team.
*   **Khu vực Hành động:** Nút `Sửa`, nút `Quay lại Danh sách`.
*   **Khu vực Chi tiết (Tabs/Sections):** Chia thành các phần logic để dễ theo dõi:
    *   **Tab/Section 1: Thông tin Cơ bản:** Chi tiết thông tin cá nhân, liên hệ, tổ chức.
    *   **Tab/Section 2: Kỹ năng & Kinh nghiệm:** Danh sách các kỹ năng, năm kinh nghiệm, cấp độ.
    *   **Tab/Section 3: Trạng thái & Phân bổ:** Trạng thái hiện tại, dự án đang tham gia, % phân bổ.
    *   **Tab/Section 4: Lịch sử Dự án:** Danh sách các dự án đã tham gia.
    *   **(Optional) Tab/Section 5: Đánh giá/Feedback:** (Nếu có module này trong tương lai).

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Thông tin Cá nhân

*   Ảnh đại diện (Avatar) - Optional.
*   `Họ và Tên:`
*   `Mã Nhân viên:`
*   `Vị trí công việc:`
*   `Team:`
*   `Leader trực tiếp:` (Tên Leader)

### 4.2. Khu vực Hành động

*   **Nút `Sửa`:**
    *   Hiển thị cho: Admin, 課長, 部長, và Nhân viên (với quyền giới hạn).
    *   Chức năng: Điều hướng đến màn hình `MH-HRM-03` (Form Thêm/Sửa Nhân sự) ở chế độ "Sửa", truyền ID của nhân viên đang xem. Form `MH-HRM-03` sẽ hiển thị các trường tương ứng với quyền của người dùng.
*   **Nút `Quay lại Danh sách`:**
    *   Chức năng: Điều hướng người dùng về màn hình `MH-HRM-01`.

### 4.3. Tab/Section: Thông tin Cơ bản

*   Hiển thị các trường đọc (read-only) từ hồ sơ:
    *   `Ngày sinh:`
    *   `Email công ty:`
    *   `Tài khoản nội bộ:` (Nếu có)
    *   `Ngày vào công ty:`
    *   `Địa chỉ:`
    *   `Số điện thoại:`
    *   `Thông tin liên hệ khẩn cấp:`
    *   (Các trường khác nếu cần)

### 4.4. Tab/Section: Kỹ năng & Kinh nghiệm

*   Hiển thị danh sách/bảng các kỹ năng nhân viên đã đăng ký/được cập nhật:
    *   **Cột:** `Loại Skill` (Ngôn ngữ, Framework, Nghiệp vụ...), `Tên Skill`, `Số năm kinh nghiệm`, `Cấp độ` (Tự đánh giá), `Cấp độ Leader đánh giá` (Optional).
*   Dữ liệu được lấy từ profile kỹ năng của nhân viên (quản lý qua `MH-HRM-03`).

### 4.5. Tab/Section: Trạng thái & Phân bổ

*   Hiển thị thông tin về tình trạng làm việc hiện tại:
    *   `Trạng thái hiện tại:` (Allocated, Available/Bench, Ending Soon, On Leave...)
    *   Nếu `Allocated` hoặc `Ending Soon`:
        *   `Dự án đang tham gia:` (Tên dự án)
        *   `% Phân bổ:` (VD: 50%, 100%)
        *   `Ngày dự kiến kết thúc:` (Nếu là `Ending Soon`)

### 4.6. Tab/Section: Lịch sử Dự án

*   Hiển thị danh sách/bảng các dự án nhân viên đã từng tham gia:
    *   **Cột:** `Tên Dự án`, `Khách hàng`, `Vai trò trong dự án`, `Thời gian Bắt đầu`, `Thời gian Kết thúc`.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình (Truy cập từ `MH-HRM-01`):**
    *   Nhận ID nhân viên.
    *   Kiểm tra quyền truy cập của người dùng đối với hồ sơ nhân viên này (Admin/課長/Leader của team/Chính nhân viên đó).
    *   Truy vấn CSDL lấy toàn bộ thông tin chi tiết (cơ bản, skills, trạng thái, lịch sử dự án).
    *   Hiển thị dữ liệu lên các khu vực/tab tương ứng.
    *   Hiển thị nút `Sửa` nếu người dùng có quyền chỉnh sửa.
*   **Click Nút `Sửa`:**
    *   Điều hướng sang màn hình `MH-HRM-03` ở chế độ "Sửa", truyền ID nhân viên.
*   **Click Nút `Quay lại Danh sách`:**
    *   Điều hướng về màn hình `MH-HRM-01`.
*   **Chuyển Tab/Section:** Hiển thị nội dung của Tab/Section được chọn.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền Xem:** Đảm bảo Leader chỉ xem được thành viên team, nhân viên chỉ xem được chính mình. Admin/課長 xem được phạm vi rộng hơn.
*   **Phân quyền Sửa:** Nút `Sửa` chỉ hiển thị khi có quyền. Form sửa (`MH-HRM-03`) phải được giới hạn trường dựa trên người sửa.
*   **Tính đầy đủ thông tin:** Màn hình cần hiển thị đầy đủ các thông tin liên quan được định nghĩa trong yêu cầu.
*   **Dữ liệu liên kết:** Thông tin `Trạng thái`, `Phân bổ`, `Lịch sử dự án` phải được cập nhật nhất quán từ các nguồn quản lý tương ứng.
*   **Dữ liệu Skills:** Hiển thị đúng danh sách kỹ năng và cấp độ đã được cập nhật.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Biểu đồ Skill:** Có thể trực quan hóa danh sách skill bằng biểu đồ (VD: radar chart) để dễ nhìn hơn.
*   **Highlight Skill chính:** Đánh dấu những skill quan trọng hoặc có kinh nghiệm lâu năm.
*   **Liên kết Dự án:** Tên dự án trong lịch sử có thể là link dẫn đến thông tin chi tiết dự án (nếu có module quản lý dự án riêng). 