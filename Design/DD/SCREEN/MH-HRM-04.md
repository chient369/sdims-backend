# Mô tả Chi tiết Màn hình: MH-HRM-04 - (Admin) Quản lý Danh mục Skills

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này dành cho quản trị viên hệ thống (Admin) hoặc vai trò được ủy quyền (VD: Leader cấp cao) để quản lý danh mục các kỹ năng (Skills) được sử dụng trong toàn bộ hệ thống. Việc quản lý tập trung này đảm bảo tính nhất quán và chuẩn hóa khi nhân viên hoặc Leader cập nhật profile kỹ năng (`MH-HRM-03`).

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Toàn quyền truy cập: Xem, Thêm, Sửa, Xóa các Loại Skill và Tên Skill.
*   **(Optional) Leader cấp cao/HR Manager:** Có thể được cấp quyền tương tự Admin để quản lý danh mục này.
*   **Các vai trò khác (Leader thông thường, Nhân viên...):** **KHÔNG** có quyền truy cập màn hình này.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Quản lý Loại Skill:**
    *   Danh sách các Loại Skill hiện có (VD: Ngôn ngữ lập trình, Framework, Database, Nghiệp vụ, Ngoại ngữ...).
    *   Nút `Thêm Loại Skill`.
*   **Khu vực Quản lý Tên Skill (theo Loại Skill đã chọn):**
    *   Hiển thị danh sách các Tên Skill thuộc Loại Skill đang được chọn ở trên.
    *   Nút `Thêm Skill` (vào loại đang chọn).
*   **Form Nhập liệu (Popup hoặc Inline):** Form nhỏ để thêm/sửa tên Loại Skill hoặc Tên Skill.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Quản lý Loại Skill

*   **Danh sách Loại Skill:**
    *   Hiển thị dạng bảng hoặc danh sách các Loại Skill đang có.
    *   **Cột/Thông tin:** `Tên Loại Skill`, `Mô tả` (Optional), `Hành động` (Nút Sửa, Xóa).
    *   Click vào một Loại Skill sẽ tải danh sách Tên Skill tương ứng ở khu vực dưới.
*   **Nút `Thêm Loại Skill`:**
    *   Chức năng: Mở popup/form cho phép nhập `Tên Loại Skill` mới và `Mô tả` (optional).
    *   Lưu Loại Skill mới vào CSDL.
*   **Nút `Sửa` (trên từng dòng Loại Skill):**
    *   Chức năng: Mở popup/form hiển thị thông tin Loại Skill hiện tại, cho phép sửa Tên và Mô tả.
    *   Lưu thay đổi vào CSDL.
*   **Nút `Xóa` (trên từng dòng Loại Skill):**
    *   Chức năng: Xóa Loại Skill khỏi danh mục.
    *   **Validation:** Cần kiểm tra xem có Tên Skill nào đang thuộc Loại này không. Nếu có, không cho xóa hoặc yêu cầu chuyển các Skill đó sang Loại khác trước.
    *   Cần có **xác nhận** trước khi xóa.

### 4.2. Khu vực Quản lý Tên Skill

*   **Tiêu đề:** Hiển thị rõ "Danh sách Skill cho Loại: [Tên Loại Skill đang chọn]"
*   **Danh sách Tên Skill:**
    *   Hiển thị dạng bảng các Tên Skill thuộc Loại đã chọn.
    *   **Cột/Thông tin:** `Tên Skill`, `Mô tả` (Optional), `Hành động` (Nút Sửa, Xóa).
*   **Nút `Thêm Skill`:**
    *   Chức năng: Mở popup/form cho phép nhập `Tên Skill` mới và `Mô tả` (optional) cho Loại Skill đang chọn.
    *   Lưu Tên Skill mới vào CSDL, liên kết với Loại Skill tương ứng.
*   **Nút `Sửa` (trên từng dòng Tên Skill):**
    *   Chức năng: Mở popup/form hiển thị thông tin Tên Skill hiện tại, cho phép sửa Tên và Mô tả.
    *   Lưu thay đổi vào CSDL.
*   **Nút `Xóa` (trên từng dòng Tên Skill):**
    *   Chức năng: Xóa Tên Skill khỏi danh mục.
    *   **Validation:** Cần kiểm tra xem có nhân viên nào đang được gán Skill này không (`MH-HRM-03`). Nếu có, không cho xóa hoặc có cơ chế xử lý phù hợp (VD: gỡ skill khỏi hồ sơ nhân viên).
    *   Cần có **xác nhận** trước khi xóa.

### 4.3. Form Nhập liệu (Popup/Inline)

*   Các trường nhập liệu đơn giản cho `Tên Loại Skill`, `Tên Skill`, `Mô tả`.
*   Nút `Lưu` và `Hủy`.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Kiểm tra quyền Admin.
    *   Tải danh sách các Loại Skill hiện có.
    *   Mặc định có thể chọn Loại Skill đầu tiên và tải danh sách Tên Skill tương ứng.
*   **Click vào một Loại Skill:** Tải lại danh sách Tên Skill ở khu vực dưới tương ứng với Loại Skill được chọn.
*   **Click `Thêm Loại Skill`:** Mở form -> Nhập liệu -> Click `Lưu` -> Hệ thống lưu vào CSDL -> Refresh lại Danh sách Loại Skill.
*   **Click `Sửa` (Loại Skill):** Mở form với dữ liệu hiện tại -> Sửa -> Click `Lưu` -> Hệ thống cập nhật CSDL -> Refresh lại Danh sách Loại Skill.
*   **Click `Xóa` (Loại Skill):** Hiển thị confirm -> Nếu xác nhận và validation OK -> Xóa khỏi CSDL -> Refresh lại Danh sách Loại Skill.
*   **Click `Thêm Skill`:** Mở form -> Nhập liệu (Tên Skill mới cho Loại đang chọn) -> Click `Lưu` -> Lưu vào CSDL -> Refresh lại Danh sách Tên Skill.
*   **Click `Sửa` (Tên Skill):** Mở form với dữ liệu hiện tại -> Sửa -> Click `Lưu` -> Cập nhật CSDL -> Refresh lại Danh sách Tên Skill.
*   **Click `Xóa` (Tên Skill):** Hiển thị confirm -> Nếu xác nhận và validation OK -> Xóa khỏi CSDL -> Refresh lại Danh sách Tên Skill.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Quyền truy cập:** Chỉ Admin hoặc vai trò được cấp quyền mới truy cập được.
*   **Validation Xóa:** Rất quan trọng. Không cho phép xóa Loại Skill nếu còn Tên Skill phụ thuộc. Không cho phép xóa Tên Skill nếu còn nhân viên đang được gán skill đó. Cần có cơ chế xử lý/thông báo rõ ràng.
*   **Tính Unique:** Tên Loại Skill phải là duy nhất. Tên Skill phải là duy nhất trong cùng một Loại Skill.
*   **Giao diện:** Cần rõ ràng, dễ thao tác để quản lý hai cấp (Loại và Tên).

## 7. Đề xuất Cải thiện (Suggestions)

*   **Tìm kiếm/Lọc:** Thêm ô tìm kiếm để nhanh chóng tìm Loại Skill hoặc Tên Skill.
*   **Import/Export:** Cho phép import/export danh mục skill từ file Excel/CSV để quản lý hàng loạt dễ dàng hơn.
*   **Gắn thẻ (Tagging):** Có thể cho phép gắn thẻ cho các Skill để nhóm theo các tiêu chí khác (VD: Skill mới, Skill ưu tiên...). 