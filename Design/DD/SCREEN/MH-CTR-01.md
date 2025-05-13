# Mô tả Chi tiết Màn hình: MH-CTR-01 - Danh sách Hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp một giao diện tổng quan để xem, tìm kiếm và lọc danh sách các hợp đồng/dự án đã ký với khách hàng. Nó là điểm xuất phát để truy cập thông tin chi tiết của từng hợp đồng (`MH-CTR-02`) và thực hiện thêm mới hợp đồng (`MH-CTR-03`).

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem *tất cả* các hợp đồng.
    *   Sử dụng chức năng Tìm kiếm, Lọc.
    *   Có nút `Thêm mới`.
    *   Truy cập Chi tiết Hợp đồng.
*   **課長 (General Manager（課長）):**
    *   Xem *tất cả* các hợp đồng (hoặc trong phạm vi bộ phận).
    *   Sử dụng chức năng Tìm kiếm, Lọc.
    *   Có nút `Thêm mới`.
    *   Truy cập Chi tiết Hợp đồng.
*   **部長 (Team Leader):**
    *   Xem các hợp đồng liên quan đến team mình (VD: các hợp đồng có thành viên team tham gia).
    *   Sử dụng chức năng Tìm kiếm, Lọc (trong phạm vi hợp đồng liên quan).
    *   **Không** có nút `Thêm mới`.
    *   Truy cập Chi tiết Hợp đồng (liên quan).
*   **Sales:**
    *   Xem các hợp đồng *mình phụ trách*.
    *   Sử dụng chức năng Tìm kiếm, Lọc (trong phạm vi hợp đồng của mình).
    *   Có nút `Thêm mới` (cho hợp đồng mình quản lý).
    *   Truy cập Chi tiết Hợp đồng (của mình).
*   **(Optional) Kế toán (Accountant):**
    *   Có thể cần quyền xem danh sách hợp đồng để đối chiếu hoặc truy cập vào chi tiết để cập nhật trạng thái thu tiền (nếu không dùng màn hình riêng `MH-CTR-04`).

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Bộ lọc & Tìm kiếm:** Đặt ở phía trên.
*   **Khu vực Hành động:** Nút `Thêm mới`.
*   **Bảng Danh sách Hợp đồng:** Chiếm phần lớn diện tích.
*   **Phân trang (Pagination):** Cuối bảng danh sách.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Bộ lọc / Tìm kiếm

*   **Ô tìm kiếm:** Tìm nhanh theo `Mã HĐ`, `Tên HĐ/Dự án`, `Tên Khách hàng`.
*   **Bộ lọc (Dropdown/Multi-select):**
    *   `Khách hàng:` (Lấy từ danh sách khách hàng có hợp đồng).
    *   `Người phụ trách Sales:` (Lấy từ danh sách Sales có hợp đồng).
    *   `Trạng thái Hợp đồng:` (Mới ký, Đang thực hiện, Tạm dừng, Hoàn thành, Đã hủy...). Lấy từ danh mục cấu hình.
    *   `Loại hợp đồng:` (Fixed Price, T&M...). Lấy từ danh mục cấu hình.
    *   `Khoảng thời gian:` Lọc theo `Ngày ký`, `Ngày hiệu lực`, `Ngày hết hạn`.
*   **Nút:**
    *   `Tìm kiếm / Lọc`: Áp dụng bộ lọc.
    *   `Xóa bộ lọc`: Đặt lại bộ lọc.

### 4.2. Khu vực Hành động Chính

*   **Nút `Thêm mới`:**
    *   Hiển thị cho: Admin, 課長, Sales (dự kiến).
    *   Chức năng: Điều hướng đến màn hình `MH-CTR-03` (Form Thêm/Sửa Hợp đồng) ở chế độ "Thêm mới".

### 4.3. Bảng Danh sách Hợp đồng

Hiển thị dữ liệu dạng bảng, cho phép sắp xếp.

*   **Các cột (Columns) đề xuất:**
    *   `Mã HĐ:` (Hiển thị text).
    *   `Tên HĐ/Dự án:` (Hiển thị text, **là link dẫn đến màn hình `MH-CTR-02` - Chi tiết Hợp đồng**).
    *   `Khách hàng:` (Tên khách hàng).
    *   `Người phụ trách Sales:` (Tên Sales).
    *   `Giá trị Hợp đồng:` (Hiển thị số tiền, định dạng tiền tệ).
    *   `Ngày ký:` (Hiển thị ngày).
    *   `Ngày hiệu lực:` (Hiển thị ngày).
    *   `Ngày hết hạn (dự kiến):` (Hiển thị ngày).
    *   `Trạng thái Hợp đồng:` (Hiển thị text hoặc tag màu).
    *   `Loại Hợp đồng:` (Hiển thị text).
*   **Sắp xếp (Sorting):** Cho phép sắp xếp theo Mã HĐ, Tên HĐ, Khách hàng, Sales, Ngày ký, Trạng thái...
*   **Phân trang (Pagination):** Hiển thị điều khiển chuyển trang.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Kiểm tra quyền người dùng.
    *   Truy vấn CSDL lấy danh sách hợp đồng phù hợp với quyền (Admin/課長: all/bộ phận, Leader: liên quan team, Sales: của mình).
    *   Áp dụng bộ lọc/sắp xếp mặc định.
    *   Hiển thị dữ liệu lên bảng và cập nhật phân trang.
*   **Thay đổi Bộ lọc/Nhập Tìm kiếm & Click `Tìm kiếm / Lọc`:**
    *   Thực hiện truy vấn mới dựa trên tiêu chí và quyền hạn.
    *   Cập nhật lại Bảng Danh sách và phân trang.
*   **Click `Xóa bộ lọc`:**
    *   Đặt lại bộ lọc.
    *   Thực hiện truy vấn lại như khi load màn hình lần đầu.
    *   Cập nhật Bảng Danh sách và phân trang.
*   **Click `Thêm mới`:** Điều hướng sang `MH-CTR-03` (chế độ Add).
*   **Click vào `Tên HĐ/Dự án`:**
    *   Lấy ID của hợp đồng.
    *   Điều hướng sang `MH-CTR-02` (Chi tiết Hợp đồng), truyền ID.
*   **Click Sắp xếp (Tiêu đề cột):**
    *   Thực hiện truy vấn lại với tham số sắp xếp mới.
    *   Cập nhật lại Bảng Danh sách và phân trang.
*   **Click Phân trang:**
    *   Thực hiện truy vấn lấy dữ liệu trang mới.
    *   Cập nhật lại Bảng Danh sách và trạng thái phân trang.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền Dữ liệu:** Rất quan trọng. Đảm bảo người dùng chỉ thấy các hợp đồng họ được phép xem.
*   **Dữ liệu Hiển thị:** Thông tin hiển thị trên bảng cần chính xác và được lấy từ nguồn dữ liệu hợp đồng tin cậy.
*   **Tính nhất quán Danh mục:** Dữ liệu trong bộ lọc (Trạng thái HĐ, Loại HĐ) phải lấy từ cấu hình chung.
*   **Hiệu năng:** Tối ưu truy vấn, đặc biệt khi lọc/sắp xếp với số lượng hợp đồng lớn.
