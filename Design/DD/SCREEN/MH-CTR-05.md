# Mô tả Chi tiết Màn hình: MH-CTR-05 - (Admin) Quản lý KPI Doanh thu Sales

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này dành cho Admin hoặc Quản lý cấp cao (VD: 課長) để thiết lập, xem và quản lý chỉ tiêu doanh thu (KPI Target Revenue) cho từng nhân viên Sales theo các kỳ (Tháng/Quý/Năm). Dữ liệu KPI này sẽ được sử dụng trong Module Dashboard & Báo cáo để so sánh với doanh thu thực tế.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin / Quản lý cấp cao (課長):**
    *   Là người dùng chính.
    *   Có quyền Xem, Thêm mới, Sửa, Xóa các bản ghi KPI doanh thu.
*   **Sales / Leader:** Thường chỉ xem được KPI của mình/team mình thông qua các báo cáo hoặc dashboard, **KHÔNG** có quyền truy cập trực tiếp màn hình quản lý này.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Bộ lọc:** Lọc theo Nhân viên Sales, Kỳ (Năm, Quý, Tháng).
*   **Khu vực Hành động:** Nút `Thêm mới KPI`.
*   **Bảng Danh sách KPI:** Hiển thị các KPI đã thiết lập.
*   **Form Nhập liệu (Popup hoặc Inline):** Để thêm/sửa KPI.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Bộ lọc

*   **Bộ lọc Nhân viên Sales:** (Dropdown/Multi-select) Chọn một hoặc nhiều Sales để xem KPI.
*   **Bộ lọc Kỳ:**
    *   Chọn `Năm` (Bắt buộc).
    *   (Optional) Chọn `Quý` (1, 2, 3, 4).
    *   (Optional) Chọn `Tháng` (1-12).
    *   -> Cho phép xem/quản lý KPI theo độ chi tiết mong muốn.
*   **Nút:** `Xem / Lọc`, `Xóa bộ lọc`.

### 4.2. Khu vực Hành động

*   **Nút `Thêm mới KPI`:**
    *   Chức năng: Mở popup/form nhập liệu để thiết lập KPI mới cho một Sales trong một Kỳ cụ thể.

### 4.3. Bảng Danh sách KPI

*   Hiển thị các bản ghi KPI đã thiết lập, phù hợp với bộ lọc.
*   **Cột:**
    *   `Nhân viên Sales:` (Tên Sales).
    *   `Kỳ:` (Hiển thị Năm/Quý/Tháng).
    *   `KPI Doanh thu (Target Revenue):` (Hiển thị số tiền, định dạng tiền tệ).
    *   `Đơn vị tiền tệ:`
    *   `Ngày tạo/cập nhật:` (Optional).
    *   `Người tạo/cập nhật:` (Optional).
    *   `Hành động:` (Nút `Sửa`, Nút `Xóa`).

### 4.4. Form Nhập liệu KPI (Popup/Inline)

*   `Nhân viên Sales:` (Dropdown/Select từ danh sách User có vai trò Sales - Bắt buộc).
*   `Kỳ:`
    *   `Năm:` (Dropdown/Input number - Bắt buộc).
    *   `Quý:` (Dropdown 1-4 - Optional, nếu quản lý theo quý).
    *   `Tháng:` (Dropdown 1-12 - Optional, nếu quản lý theo tháng).
*   `KPI Doanh thu (Target Revenue):` (Input number - Bắt buộc).
*   `Đơn vị tiền tệ:` (Dropdown: VND, USD, JPY... - Bắt buộc).
*   **Nút `Lưu`**, **Nút `Hủy`**.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Kiểm tra quyền Admin/Quản lý.
    *   Áp dụng bộ lọc mặc định (VD: Năm hiện tại, tất cả Sales).
    *   Tải danh sách KPI phù hợp.
    *   Hiển thị lên bảng.
*   **Thay đổi Bộ lọc & Click `Xem / Lọc`:** Tải lại danh sách KPI theo tiêu chí mới.
*   **Click `Thêm mới KPI`:** Mở form nhập liệu.
*   **(Form Nhập liệu) Chọn Sales, Kỳ, Nhập Target -> Click `Lưu`:**
    *   Validation dữ liệu (bắt buộc, số...).
    *   Kiểm tra xem đã tồn tại KPI cho Sales/Kỳ đó chưa (Nếu có, báo lỗi hay cho phép ghi đè? - Cần quyết định. Thường là không cho trùng, phải Sửa hoặc Xóa cũ đi).
    *   Nếu OK -> Lưu bản ghi KPI mới vào CSDL.
    *   Đóng form, refresh lại bảng danh sách, hiển thị thông báo thành công.
    *   Nếu lỗi -> Hiển thị lỗi trên form.
*   **Click `Sửa` (trên dòng KPI):**
    *   Mở form nhập liệu, điền dữ liệu KPI hiện tại.
    *   Người dùng sửa Target -> Click `Lưu`.
    *   Validation -> Cập nhật bản ghi KPI trong CSDL.
    *   Đóng form, refresh bảng, hiển thị thông báo.
*   **Click `Xóa` (trên dòng KPI):**
    *   Hiển thị confirm.
    *   Nếu OK -> Xóa bản ghi KPI khỏi CSDL.
    *   Refresh bảng, hiển thị thông báo.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền:** Chỉ Admin/Quản lý cấp cao mới được thao tác.
*   **Tính Unique:** Đảm bảo không có 2 bản ghi KPI trùng lặp cho cùng một Sales và cùng một Kỳ (Năm/Quý/Tháng tùy theo độ chi tiết quản lý).
*   **Validation Dữ liệu:** Target Revenue phải là số dương.
*   **Độ chi tiết Kỳ:** Xác định rõ sẽ quản lý KPI theo Tháng, Quý hay Năm và thiết kế form/bảng tương ứng.
*   **Đơn vị tiền tệ:** Cần lưu và hiển thị đúng đơn vị tiền tệ của KPI.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Import/Export KPI:** Cho phép thiết lập KPI hàng loạt cho nhiều Sales/Kỳ thông qua file Excel/CSV.
*   **Sao chép KPI:** Cho phép sao chép KPI từ kỳ này sang kỳ khác hoặc từ Sales này sang Sales khác để nhập liệu nhanh hơn.
*   **Lịch sử thay đổi KPI:** Ghi log lại việc ai đã thay đổi KPI nào, khi nào.
*   **Giao diện Trực quan hơn:** Có thể hiển thị biểu đồ nhỏ ngay trên bảng để so sánh nhanh KPI giữa các Sales (nếu số lượng Sales không quá lớn). 