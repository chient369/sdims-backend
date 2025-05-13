# Mô tả Chi tiết Màn hình: MH-CTR-03 - Form Thêm/Sửa Hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp form nhập liệu để **thêm mới** một hợp đồng hoặc **chỉnh sửa** thông tin của một hợp đồng hiện có. Nó cho phép người dùng định nghĩa các thông tin cơ bản, điều khoản thanh toán, liên kết với cơ hội/nhân sự và đính kèm tài liệu.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin, 課長:**
    *   Truy cập ở chế độ `Thêm mới` (từ `MH-CTR-01`).
    *   Truy cập ở chế độ `Sửa` (từ `MH-CTR-02` cho mọi HĐ).
    *   Có quyền nhập/sửa tất cả các trường thông tin.
*   **Sales:**
    *   Truy cập ở chế độ `Thêm mới` (từ `MH-CTR-01`).
    *   Truy cập ở chế độ `Sửa` (từ `MH-CTR-02` chỉ cho HĐ mình phụ trách).
    *   Có quyền nhập/sửa các trường thông tin của HĐ mình quản lý.
*   **Các vai trò khác (Leader, Nhân viên, Kế toán...):** **KHÔNG** có quyền truy cập màn hình này.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Tiêu đề:** "Thêm mới Hợp đồng" hoặc "Chỉnh sửa Hợp đồng: [Mã HĐ] - [Tên HĐ]"
*   **Form Nhập liệu:** Chia thành các Section/Group:
    *   Section 1: Thông tin Chung (Mã HĐ, Tên, Khách hàng, Sales, Loại HĐ, Trạng thái HĐ...)
    *   Section 2: Giá trị & Ngày tháng (Giá trị HĐ, Ngày ký/hiệu lực/hết hạn)
    *   Section 3: Điều khoản Thanh toán (Bảng động để thêm/sửa/xóa các mốc thanh toán)
    *   Section 4: Liên kết (Chọn Cơ hội, Chọn Nhân sự tham gia)
    *   Section 5: Tài liệu Đính kèm (Khu vực upload/quản lý file)
*   **Khu vực Hành động:** Nút `Lưu`, nút `Hủy`.

## 4. Các Thành phần Chính (Components)

### 4.1. Section: Thông tin Chung

*   `Mã Hợp đồng:` (Input text, có thể tự sinh hoặc yêu cầu nhập unique)
*   `Tên Hợp đồng/Dự án:` (Input text, Bắt buộc)
*   `Khách hàng:` (Dropdown/Autocomplete từ danh sách Khách hàng)
*   `Người phụ trách Sales:` (Dropdown từ danh sách User có vai trò Sales, mặc định là người tạo nếu là Sales)
*   `Loại Hợp đồng:` (Dropdown: Fixed Price, T&M...)
*   `Trạng thái Hợp đồng:` (Dropdown: Mới ký, Đang thực hiện, Tạm dừng, Hoàn thành, Đã hủy...)
*   `Mô tả/Ghi chú:` (Text area)

### 4.2. Section: Giá trị & Ngày tháng

*   `Giá trị Hợp đồng:` (Input number, định dạng tiền tệ)
*   `Đơn vị tiền tệ:` (Dropdown: VND, USD, JPY...)
*   `Ngày ký:` (Date picker)
*   `Ngày hiệu lực:` (Date picker)
*   `Ngày hết hạn (dự kiến):` (Date picker)

### 4.3. Section: Điều khoản Thanh toán

*   **Bảng động (dynamic table)** cho phép quản lý các mốc thanh toán:
    *   **Nút `Thêm Mốc Thanh toán`:** Thêm dòng mới.
    *   **Mỗi dòng gồm:**
        *   `Mô tả Đợt TT:` (Input text, VD: "Thanh toán đợt 1 - 30%")
        *   `Ngày dự kiến Thu:` (Date picker)
        *   `Số tiền dự kiến:` (Input number)
        *   `Ghi chú TT:` (Input text - Optional)
        *   **Nút `Xóa Mốc`:** Xóa dòng tương ứng.
*   **(Lưu ý):** Trạng thái Thu tiền, Ngày thu thực tế... không nhập ở đây mà quản lý ở `MH-CTR-02` (nếu Kế toán sửa) hoặc `MH-CTR-04`.

### 4.4. Section: Liên kết

*   **Liên kết Cơ hội:**
    *   Dropdown/Autocomplete cho phép chọn Cơ hội (từ `MH-OPP-01`) mà hợp đồng này được tạo ra từ đó (Optional).
*   **Liên kết Nhân sự tham gia:**
    *   **Nút `Thêm Nhân sự`:** Mở popup/dialog để chọn nhân viên từ danh sách (`MH-HRM-01`).
    *   **Bảng danh sách Nhân sự đã chọn:**
        *   **Cột:** `Mã NV`, `Họ và Tên`, `Vai trò` (Input text), `% Phân bổ` (Input number).
        *   **Nút `Xóa Nhân sự`:** Xóa nhân viên khỏi danh sách tham gia HĐ này.
    *   **(Note):** Việc liên kết này chỉ ghi nhận ban đầu, việc cập nhật phân bổ chi tiết theo thời gian thực hiện ở Module HRM (`MH-HRM-03`).

### 4.5. Section: Tài liệu Đính kèm

*   **Nút `Upload File`:** Mở dialog chọn file từ máy tính.
*   **Danh sách File đã upload:**
    *   Hiển thị `Tên File`, `Kích thước`, `Ngày Upload`.
    *   **Nút `Xóa File`:** Xóa file đã upload (chưa xóa khỏi server cho đến khi Lưu HĐ).

### 4.6. Khu vực Hành động

*   **Nút `Lưu`:**
    *   Thực hiện validation form.
    *   Nếu OK -> Lưu dữ liệu HĐ, Điều khoản TT, Liên kết, File đính kèm vào CSDL (INSERT hoặc UPDATE).
    *   Điều hướng về `MH-CTR-02` (chi tiết HĐ vừa lưu).
*   **Nút `Hủy`:**
    *   Hủy bỏ thay đổi, điều hướng về màn hình trước đó (`MH-CTR-01` hoặc `MH-CTR-02`).
    *   Cần confirm nếu có thay đổi chưa lưu.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình (Chế độ Thêm mới):**
    *   Kiểm tra quyền.
    *   Hiển thị form trống.
*   **Load Màn hình (Chế độ Sửa):**
    *   Nhận ID hợp đồng.
    *   Kiểm tra quyền.
    *   Truy vấn CSDL lấy thông tin HĐ hiện tại.
    *   Điền dữ liệu vào form.
*   **Người dùng Nhập/Sửa dữ liệu:** Tương tác với các thành phần form.
*   **Click `Thêm Mốc Thanh toán` / `Xóa Mốc`:** Cập nhật bảng điều khoản thanh toán trên UI.
*   **Click `Thêm Nhân sự`:** Mở popup chọn NV -> Chọn -> Thêm vào bảng liên kết nhân sự trên UI.
*   **Click `Xóa Nhân sự`:** Xóa dòng NV khỏi bảng trên UI.
*   **Click `Upload File`:** Chọn file -> Hiển thị trong danh sách file chuẩn bị upload.
*   **Click `Xóa File`:** Xóa file khỏi danh sách chuẩn bị upload/đính kèm.
*   **Click Nút `Lưu`:**
    *   Validation -> Gửi dữ liệu lên server.
    *   Server Validation -> Lưu CSDL (HĐ chính, các bảng liên quan: điều khoản TT, liên kết NV, file đính kèm - xử lý upload file lên server).
    *   Điều hướng về `MH-CTR-02`, hiển thị thông báo thành công.
    *   Nếu lỗi -> Hiển thị lỗi trên form.
*   **Click Nút `Hủy`:** Confirm -> Điều hướng về màn hình trước.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền Sửa:** Đảm bảo chỉ người có quyền mới sửa được HĐ.
*   **Validation Dữ liệu:**
    *   Các trường bắt buộc.
    *   Định dạng số, tiền tệ, ngày tháng.
    *   Mã HĐ unique.
    *   Tổng tiền các mốc thanh toán (có cần khớp giá trị HĐ không?).
    *   % Phân bổ nhân sự hợp lệ (1-100).
*   **Quản lý Bảng động:** Giao diện thêm/sửa/xóa dòng trong bảng Điều khoản TT và Liên kết NV phải dễ dùng.
*   **Xử lý File Upload:** Giới hạn loại file, kích thước, lưu trữ an toàn, xử lý lỗi upload.
*   **Liên kết:** Đảm bảo chọn đúng Cơ hội, Nhân sự từ các module khác.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Tự động tính toán:** Có thể tự động gợi ý chia mốc thanh toán dựa trên giá trị HĐ và số đợt.
*   **Template Hợp đồng:** Có thể tạo HĐ từ các template có sẵn (nếu nghiệp vụ phức tạp và lặp lại).
*   **Workflow Phê duyệt:** Nếu cần, có thể thêm quy trình phê duyệt trước khi HĐ được lưu chính thức. 