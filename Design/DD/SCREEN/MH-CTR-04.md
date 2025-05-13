# Mô tả Chi tiết Màn hình: MH-CTR-04 - (Kế toán) Cập nhật Trạng thái Thu tiền

**Version Control:**

| Version | Date       | Author         | Changes                                                          | Approved By | Status    |
| :------ | :--------- | :------------- | :--------------------------------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft - Focused on manual update / import for Accounting |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này được thiết kế **riêng cho bộ phận Kế toán** (hoặc người có vai trò tương đương) để cập nhật trạng thái thu tiền thực tế cho các đợt thanh toán của hợp đồng. Việc tách biệt màn hình này giúp đảm bảo tính chính xác và kiểm soát đối với dữ liệu tài chính quan trọng này, thay vì cho phép cập nhật trực tiếp trên màn hình chi tiết hợp đồng (`MH-CTR-02`). Màn hình hỗ trợ cập nhật thủ công hoặc import hàng loạt.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Kế toán (Accountant) / Người được ủy quyền:**
    *   Là người dùng chính của màn hình này.
    *   Có quyền xem danh sách các đợt thanh toán cần cập nhật.
    *   Có quyền cập nhật `Trạng thái Thu tiền`, `Ngày thu thực tế`, `Số tiền thực thu`.
    *   Có quyền sử dụng chức năng Import file.
*   **Admin:** Có thể cần quyền truy cập để hỗ trợ hoặc xem log.
*   **Các vai trò khác (Sales, Leader, 課長...):** **KHÔNG** có quyền truy cập hoặc thao tác trên màn hình này.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Bộ lọc:** Lọc các đợt thanh toán cần cập nhật (theo Hợp đồng, Khách hàng, Trạng thái TT, Khoảng ngày dự kiến thu).
*   **Tab/Phân khu lựa chọn phương thức cập nhật:**
    *   **Tab 1: Cập nhật Thủ công:** Hiển thị bảng các đợt thanh toán cho phép sửa trực tiếp.
    *   **Tab 2: Import từ File:** Khu vực upload file và hướng dẫn.
*   **Khu vực Phản hồi/Kết quả:** Hiển thị thông báo.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Bộ lọc

*   **Ô tìm kiếm:** Tìm nhanh theo `Mã HĐ`, `Tên HĐ`, `Tên Khách hàng`.
*   **Bộ lọc (Dropdown/Multi-select):**
    *   `Hợp đồng:` (Chọn từ danh sách HĐ có điều khoản TT).
    *   `Khách hàng:`
    *   `Trạng thái Thu tiền hiện tại:` (Chưa thu, Quá hạn). Mục đích là lọc ra những khoản cần cập nhật.
    *   `Ngày dự kiến Thu:` (Lọc theo khoảng thời gian).
*   **Nút:** `Tìm kiếm / Lọc`, `Xóa bộ lọc`.

### 4.2. Tab: Cập nhật Thủ công

*   **Bảng Danh sách Đợt Thanh toán:**
    *   Hiển thị danh sách các đợt thanh toán phù hợp với bộ lọc.
    *   **Cột (Hiển thị thông tin & Nhập liệu):**
        *   `Mã HĐ:` (Read-only, link đến `MH-CTR-02`?)
        *   `Tên HĐ:` (Read-only)
        *   `Khách hàng:` (Read-only)
        *   `Mô tả Đợt TT:` (Read-only)
        *   `Ngày dự kiến Thu:` (Read-only)
        *   `Số tiền dự kiến:` (Read-only)
        *   `Trạng thái Thu tiền:` (**Editable Dropdown:** Chọn "Đã thu")
        *   `Ngày Thu thực tế:` (**Editable Date picker**, Bắt buộc nếu chọn "Đã thu")
        *   `Số tiền Thực thu:` (**Editable Input number**, Bắt buộc nếu chọn "Đã thu")
        *   `Ghi chú TT:` (Editable Input text - Optional)
    *   **Nút `Lưu thay đổi`:** Lưu cập nhật trạng thái cho các dòng đã sửa.
*   Có thể sử dụng cơ chế "inline editing" hoặc có nút "Sửa" trên từng dòng để mở popup sửa nhỏ.

### 4.3. Tab: Import từ File

*   **Tương tự MH-MGN-02:**
    *   Hướng dẫn định dạng file (CSV/Excel).
    *   Nút/Link `Tải file mẫu (Template)`: Template chứa các cột cần thiết để xác định đợt thanh toán (VD: Mã HĐ, Mô tả Đợt TT hoặc ID Đợt TT) và các cột cần cập nhật (`Trạng thái Thu tiền`, `Ngày Thu thực tế`, `Số tiền Thực thu`, `Ghi chú TT`).
    *   Khu vực `Chọn file` và hiển thị tên file.
    *   Nút `Import Dữ liệu Thanh toán`.
*   **Validation:** Kiểm tra file, định dạng, sự tồn tại của HĐ/Đợt TT, tính hợp lệ của ngày tháng, số tiền.
*   **Xử lý:** Cập nhật hàng loạt trạng thái thu tiền vào CSDL.

### 4.4. Khu vực Phản hồi/Kết quả

*   Hiển thị thông báo thành công hoặc lỗi chi tiết sau khi Lưu thủ công hoặc Import.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Kiểm tra quyền Kế toán.
    *   Áp dụng bộ lọc mặc định (VD: hiển thị các đợt TT "Chưa thu" và "Quá hạn" trong tháng).
    *   Tải dữ liệu các đợt thanh toán phù hợp.
    *   Hiển thị lên bảng (Tab Thủ công) hoặc giao diện Import.
*   **Thay đổi Bộ lọc & Click `Tìm kiếm / Lọc`:** Tải lại danh sách đợt thanh toán theo tiêu chí mới.
*   **(Tab Thủ công) Sửa dữ liệu trên bảng -> Click `Lưu thay đổi`:**
    *   Validation dữ liệu sửa (Ngày thực tế, Số tiền thực thu).
    *   Lưu cập nhật vào CSDL cho các dòng đã thay đổi.
    *   Refresh lại bảng, hiển thị thông báo.
*   **(Tab Import) Click `Tải file mẫu`:** Cung cấp file template.
*   **(Tab Import) Chọn file -> Click `Import Dữ liệu Thanh toán`:**
    *   Upload -> Validation -> Xử lý cập nhật CSDL.
    *   Hiển thị kết quả (thành công/số dòng lỗi).

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền:** Đảm bảo chỉ Kế toán/người được ủy quyền mới thao tác được.
*   **Xác định đúng Đợt Thanh toán:** Khi import, cần cơ chế để xác định chính xác đợt thanh toán cần cập nhật (qua ID nội bộ, hoặc tổ hợp Mã HĐ + Mô tả/Ngày dự kiến...).
*   **Validation Dữ liệu:**
    *   Ngày thu thực tế phải hợp lệ.
    *   Số tiền thực thu phải là số.
    *   Có thể cần validation thêm (VD: Số tiền thực thu không quá khác biệt so với dự kiến?).
*   **Ghi Log:** Nên ghi lại log ai đã cập nhật trạng thái thu tiền, khi nào, cho đợt thanh toán nào.
*   **Tính nhất quán:** Dữ liệu cập nhật ở đây phải phản ánh đúng lên màn hình Chi tiết Hợp đồng (`MH-CTR-02`) và các báo cáo liên quan.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Cập nhật hàng loạt Thủ công:** Cho phép chọn nhiều dòng và cập nhật nhanh trạng thái "Đã thu" (với cùng ngày thu chẳng hạn).
*   **Đối soát:** Có thể thêm chức năng đối soát giữa dữ liệu import và dữ liệu hiện có trước khi cập nhật chính thức.
*   **Liên kết Ngân hàng:** (Phức tạp) Trong tương lai, có thể tích hợp với sao kê ngân hàng để tự động gợi ý/cập nhật trạng thái thu tiền. 