# Mô tả Chi tiết Màn hình: MH-CTR-02 - Chi tiết Hợp đồng

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-29 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này hiển thị thông tin chi tiết của một hợp đồng/dự án cụ thể được chọn từ danh sách (`MH-CTR-01`). Nó cho phép người dùng xem đầy đủ các điều khoản, thông tin liên quan (cơ hội, nhân sự), các mốc thanh toán, trạng thái thu tiền và quản lý file đính kèm. Đây cũng là điểm truy cập để chỉnh sửa thông tin hợp đồng (`MH-CTR-03`).

## 2. Đối tượng Sử dụng và Phân quyền

Việc xem chi tiết tuân theo quyền xem trên danh sách (`MH-CTR-01`):

*   **Admin, 課長:** Xem chi tiết tất cả hợp đồng (hoặc phạm vi quản lý).
*   **部長:** Xem chi tiết hợp đồng liên quan đến team.
*   **Sales:** Xem chi tiết hợp đồng mình phụ trách.
*   **Kế toán (Optional):** Xem chi tiết hợp đồng để cập nhật trạng thái thu tiền (nếu có quyền).

**Quyền Sửa:**
*   **Admin, 課長, Sales (phụ trách HĐ):** Có nút `Sửa` để điều hướng đến `MH-CTR-03`.
*   **Kế toán (Optional):** Có thể có quyền sửa trực tiếp `Trạng thái Thu tiền` trên màn hình này hoặc thông qua màn hình riêng (`MH-CTR-04`).
*   **部長:** Thường không có quyền sửa thông tin hợp đồng.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Thông tin Chính:** Phía trên, hiển thị Mã HĐ, Tên HĐ, Khách hàng, Trạng thái.
*   **Khu vực Hành động:** Nút `Sửa`, nút `Quay lại Danh sách`.
*   **Khu vực Chi tiết (Tabs/Sections):**
    *   **Tab/Section 1: Thông tin Chung:** Các thông tin cơ bản, giá trị, loại HĐ, ngày tháng...
    *   **Tab/Section 2: Điều khoản Thanh toán & Thu tiền:** Bảng liệt kê các mốc thanh toán, trạng thái.
    *   **Tab/Section 3: Liên kết:** Thông tin về Cơ hội liên quan (từ Module 3), Nhân sự đang tham gia (từ Module 1).
    *   **Tab/Section 4: Tài liệu Đính kèm:** Danh sách các file hợp đồng, phụ lục...

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Thông tin Chính

*   `Mã Hợp đồng:`
*   `Tên Hợp đồng/Dự án:`
*   `Khách hàng:`
*   `Trạng thái Hợp đồng:` (Hiển thị rõ ràng)
*   `Người phụ trách Sales:`

### 4.2. Khu vực Hành động

*   **Nút `Sửa`:**
    *   Hiển thị cho: Admin, 課長, Sales (phụ trách HĐ).
    *   Chức năng: Điều hướng đến `MH-CTR-03` ở chế độ "Sửa", truyền ID hợp đồng.
*   **Nút `Quay lại Danh sách`:**
    *   Chức năng: Điều hướng về `MH-CTR-01`.

### 4.3. Tab/Section: Thông tin Chung

*   Hiển thị các trường đọc (read-only):
    *   `Giá trị Hợp đồng:`
    *   `Loại Hợp đồng:` (Fixed Price, T&M...)
    *   `Ngày ký:`
    *   `Ngày hiệu lực:`
    *   `Ngày hết hạn (dự kiến):`
    *   `Mô tả/Ghi chú:` (Nếu có)
    *   (Các trường thông tin khác của HĐ)

### 4.4. Tab/Section: Điều khoản Thanh toán & Thu tiền

*   Hiển thị bảng liệt kê các mốc/đợt thanh toán theo hợp đồng:
    *   **Cột:** `Mô tả Đợt TT`, `Ngày dự kiến Thu`, `Số tiền dự kiến`, `Trạng thái Thu tiền` (Chưa thu, Đã thu, Quá hạn), `Ngày Thu thực tế`, `Số tiền Thực thu`, `Ghi chú TT` (Optional).
*   **Quyền sửa Trạng thái Thu tiền:**
    *   Nếu Kế toán có quyền sửa trực tiếp: Cột `Trạng thái Thu tiền`, `Ngày Thu thực tế`, `Số tiền Thực thu` có thể là ô cho phép sửa (inline edit hoặc nút mở popup sửa nhỏ).
    *   Nếu Kế toán sửa qua `MH-CTR-04`: Các cột này chỉ hiển thị read-only.
*   Trạng thái `Quá hạn` được tự động xác định dựa trên `Ngày dự kiến Thu` và ngày hiện tại (nếu `Trạng thái` là `Chưa thu`).

### 4.5. Tab/Section: Liên kết

*   **Cơ hội liên quan:**
    *   Hiển thị thông tin cơ hội (nếu HĐ được tạo từ cơ hội): `Tên Cơ hội`, `Link đến MH-OPP-02`.
*   **Nhân sự tham gia:**
    *   Hiển thị danh sách nhân viên đang được phân bổ cho hợp đồng/dự án này.
    *   **Cột:** `Mã NV`, `Họ và Tên` (có thể là link đến `MH-HRM-02`), `Vai trò`, `% Phân bổ`.
    *   Dữ liệu lấy từ Module HRM (`MH-HRM-03`).

### 4.6. Tab/Section: Tài liệu Đính kèm

*   Hiển thị danh sách các file đã được đính kèm (quản lý qua `MH-CTR-03`):
    *   **Cột:** `Tên File`, `Ngày Upload`, `Người Upload`, `Hành động` (Nút Tải xuống, Nút Xóa - nếu có quyền).

## 5. Luồng Sự kiện Chính

*   **Load Màn hình (Truy cập từ `MH-CTR-01`):**
    *   Nhận ID hợp đồng.
    *   Kiểm tra quyền xem của người dùng.
    *   Truy vấn CSDL lấy thông tin chi tiết HĐ, điều khoản TT, liên kết cơ hội/nhân sự, file đính kèm.
    *   Hiển thị dữ liệu lên các khu vực/tab.
    *   Hiển thị nút `Sửa` nếu có quyền.
*   **Click Nút `Sửa`:** Điều hướng sang `MH-CTR-03` (chế độ Sửa), truyền ID hợp đồng.
*   **Click Nút `Quay lại Danh sách`:** Điều hướng về `MH-CTR-01`.
*   **Chuyển Tab/Section:** Hiển thị nội dung tương ứng.
*   **(Nếu có quyền sửa TT) Sửa Trạng thái Thu tiền:** Người dùng sửa trực tiếp trên bảng -> Hệ thống lưu thay đổi vào CSDL.
*   **Click Tải xuống File:** Trigger tải file đính kèm.
*   **Click Xóa File:** (Nếu có quyền) Hiển thị confirm -> Xóa file và bản ghi liên kết.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền Xem/Sửa:** Đảm bảo đúng người dùng xem/sửa đúng thông tin.
*   **Tính toàn vẹn Dữ liệu:** Thông tin hiển thị phải khớp với dữ liệu gốc.
*   **Cập nhật Trạng thái Thu tiền:** Logic cập nhật phải chính xác, có thể cần ghi log thay đổi.
*   **Hiển thị Trạng thái Quá hạn:** Logic xác định quá hạn phải đúng.
*   **Liên kết Dữ liệu:** Đảm bảo các liên kết đến Cơ hội, Nhân sự hoạt động chính xác.
*   **Quản lý File:** Cơ chế xem/tải/xóa file đính kèm cần an toàn và phân quyền đúng.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Lịch sử Thay đổi:** Ghi log các thay đổi quan trọng trên hợp đồng (VD: thay đổi giá trị, trạng thái, người sửa, thời gian sửa).
*   **Cảnh báo Tự động:** Hệ thống tự động gửi cảnh báo (email/notification) khi có đợt thanh toán sắp đến hạn hoặc quá hạn.
*   **Tổng hợp Nhanh:** Hiển thị tóm tắt nhanh tình hình thanh toán (VD: % đã thu / tổng giá trị) ở Khu vực Thông tin Chính. 