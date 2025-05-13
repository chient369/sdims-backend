# Mô tả Chi tiết Màn hình: MH-ADM-04 - (Admin) Xem Log Hệ thống

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Chiến Trần Văn | Initial draft based on requirements        |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện cho quản trị viên (Admin) để xem các log hoạt động và lỗi của hệ thống. Màn hình giúp Admin theo dõi, tìm kiếm, và lọc các sự kiện đã xảy ra trong hệ thống, hỗ trợ việc khắc phục sự cố, kiểm tra hoạt động của người dùng và giám sát tính toàn vẹn của hệ thống.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem tất cả các log hệ thống.
    *   Tìm kiếm, lọc log theo nhiều tiêu chí.
    *   Xuất log ra file để phân tích ngoại tuyến.
*   **課長 (General Manager) (Optional - tùy chọn phân quyền):**
    *   Có thể được cấp quyền giới hạn để xem một số loại log nhất định.
    *   Chỉ xem được log liên quan đến phạm vi quản lý.

Lưu ý: Mặc định, chỉ Admin mới có quyền truy cập màn hình này. Các vai trò khác trong hệ thống không có quyền truy cập, trừ khi được cấp phép đặc biệt.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Tiêu đề trang:** "Xem Log Hệ thống" - Nằm ở phía trên cùng.
*   **Khu vực Tìm kiếm & Bộ lọc:** Đặt ở phía trên, có thể mở rộng/thu gọn để tiết kiệm không gian.
*   **Khu vực Hiển thị Log:** Chiếm phần lớn diện tích, hiển thị danh sách log dạng bảng hoặc text có cấu trúc.
*   **Phân trang (Pagination):** Nằm ở cuối bảng danh sách.
*   **Khu vực Tác vụ:** Các nút chức năng như Export, Refresh, nằm phía trên khu vực hiển thị log.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Tìm kiếm / Bộ lọc

*   **Bộ lọc thời gian:**
    *   `Khoảng thời gian`: Chọn từ ngày - đến ngày.
    *   `Tìm nhanh`: Dropdown với các lựa chọn nhanh (Hôm nay, 24 giờ qua, 7 ngày qua, 30 ngày qua).
*   **Bộ lọc nội dung:**
    *   `Loại log`: Dropdown chọn loại log (Tất cả, Lỗi, Cảnh báo, Thông tin, Debug).
    *   `Module`: Dropdown chọn module liên quan (Tất cả, Đăng nhập, Nhân sự, Margin, Cơ hội, Hợp đồng, API...).
    *   `Người dùng`: Ô tìm kiếm/dropdown chọn người dùng liên quan.
    *   `Từ khóa`: Ô nhập text để tìm trong nội dung log.
    *   `IP Address`: Ô nhập để lọc theo địa chỉ IP nguồn.
*   **Nút:**
    *   `Tìm kiếm / Lọc`: Áp dụng các tiêu chí tìm kiếm và lọc.
    *   `Xóa bộ lọc`: Đặt lại tất cả các trường lọc về giá trị mặc định.

### 4.2. Khu vực Tác vụ

*   **Nút `Refresh`:**
    *   Làm mới danh sách log với bộ lọc hiện tại.
*   **Nút `Export`:**
    *   Xuất danh sách log hiện tại (đã lọc) ra file (CSV, TXT).
*   **Chọn chế độ xem (Optional):**
    *   Toggle hoặc radio buttons để chuyển đổi giữa chế độ xem dạng Bảng và dạng Text.

### 4.3. Khu vực Hiển thị Log

#### 4.3.1. Hiển thị dạng Bảng (Table View)

*   **Bảng danh sách log:**
    *   Cột `Thời gian`: Thời điểm xảy ra sự kiện (định dạng ngày giờ đầy đủ).
    *   Cột `Mức độ`: Mức độ của log (Error, Warning, Info, Debug) - Hiển thị với màu sắc tương ứng.
    *   Cột `Module`: Module/chức năng liên quan đến sự kiện log.
    *   Cột `Người dùng`: Tên người dùng thực hiện hành động (nếu có).
    *   Cột `IP Address`: Địa chỉ IP của người dùng hoặc hệ thống.
    *   Cột `Mô tả ngắn`: Mô tả ngắn gọn về sự kiện (có thể cắt ngắn nếu quá dài).
    *   Cột `Thao tác`: Nút xem chi tiết (mở modal/collapse để xem thông tin đầy đủ).
*   **Sắp xếp (Sorting):** Cho phép click vào tiêu đề cột để sắp xếp (mặc định sắp xếp theo thời gian mới nhất).
*   **Phân trang:** Hiển thị các điều khiển để chuyển trang khi số lượng log vượt quá giới hạn hiển thị.

#### 4.3.2. Hiển thị dạng Text (Text View - Optional)

*   **Khung văn bản có cấu trúc:**
    *   Hiển thị log dưới dạng text có định dạng, dễ đọc hơn khi cần xem nhiều chi tiết.
    *   Có thể áp dụng màu sắc hoặc font khác nhau cho các loại log khác nhau.
    *   Hỗ trợ tìm kiếm trong trang (Ctrl+F) để định vị nhanh thông tin.

### 4.4. Modal Chi tiết Log

*   **Tiêu đề:** "Chi tiết Log"
*   **Thông tin cơ bản:**
    *   Thời gian, Mức độ, Module, Người dùng, IP Address.
*   **Chi tiết log:**
    *   Mô tả đầy đủ sự kiện.
    *   Stack trace (nếu là lỗi).
    *   Dữ liệu bổ sung (nếu có).
*   **Thông tin liên quan (Optional):**
    *   Liên kết đến các log khác liên quan.
    *   Hành động gợi ý để xử lý (nếu là lỗi).
*   **Nút:**
    *   `Đóng`: Đóng modal chi tiết.
    *   `Log trước/sau`: Di chuyển đến log trước/sau trong danh sách.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Hệ thống kiểm tra quyền người dùng (chỉ Admin hoặc người được cấp quyền mới được truy cập).
    *   Truy vấn CSDL lấy danh sách log với bộ lọc mặc định (thường là log của 24 giờ qua, ưu tiên các mức Error và Warning).
    *   Hiển thị dữ liệu lên bảng và cập nhật phân trang.
*   **Thay đổi Bộ lọc & Click `Tìm kiếm / Lọc`:**
    *   Hệ thống thực hiện truy vấn mới dựa trên các tiêu chí đã chọn.
    *   Cập nhật lại khu vực hiển thị log và phân trang.
*   **Click `Xóa bộ lọc`:**
    *   Đặt lại tất cả các trường lọc về giá trị mặc định.
    *   Thực hiện truy vấn lại và cập nhật dữ liệu.
*   **Click `Refresh`:**
    *   Thực hiện truy vấn lại với các bộ lọc hiện tại để cập nhật dữ liệu mới nhất.
    *   Cập nhật lại khu vực hiển thị log và phân trang.
*   **Click `Export`:**
    *   Hệ thống thu thập dữ liệu từ danh sách log hiện tại (đã lọc).
    *   Tạo file CSV/TXT với định dạng phù hợp.
    *   Trigger tải file về máy người dùng.
*   **Chuyển chế độ xem (nếu có):**
    *   Người dùng chuyển đổi giữa chế độ xem Bảng và Text.
    *   Hệ thống cập nhật giao diện hiển thị nhưng giữ nguyên dữ liệu và bộ lọc.
*   **Click vào biểu tượng/nút Chi tiết:**
    *   Mở modal hiển thị chi tiết đầy đủ của log được chọn.
*   **Click Phân trang:**
    *   Hệ thống thực hiện truy vấn để lấy dữ liệu cho trang được yêu cầu.
    *   Cập nhật lại khu vực hiển thị log và trạng thái phân trang.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Bảo mật:**
    *   Đảm bảo chỉ người dùng được cấp quyền mới có thể truy cập màn hình này.
    *   Cân nhắc việc mã hóa hoặc ẩn thông tin nhạy cảm trong log (thông tin cá nhân, mật khẩu...).
    *   Ghi log việc truy cập và xuất log để kiểm soát (log của việc xem log).
*   **Hiệu năng:**
    *   Tối ưu hóa truy vấn CSDL khi làm việc với lượng log lớn.
    *   Cân nhắc phân trang hiệu quả và giới hạn số lượng bản ghi hiển thị.
    *   Cân nhắc việc nén hoặc lưu trữ log cũ để giảm tải cho CSDL.
*   **Quản lý log:**
    *   Cân nhắc chính sách lưu trữ log (VD: giữ log Error/Warning trong 1 năm, log Info trong 3 tháng...).
    *   Tự động xóa log cũ theo chính sách (có thể thông báo trước khi xóa).
*   **Trải nghiệm người dùng:**
    *   Đảm bảo hiển thị log rõ ràng, dễ đọc với màu sắc phù hợp.
    *   Cung cấp bộ lọc linh hoạt nhưng không gây rối.
    *   Đảm bảo modal chi tiết hiển thị đầy đủ thông tin và có định dạng tốt.
*   **Tính năng mở rộng (Optional):**
    *   Cân nhắc thêm khả năng đánh dấu log quan trọng để theo dõi sau.
    *   Cân nhắc chức năng thiết lập cảnh báo tự động khi phát hiện log lỗi nghiêm trọng.
    *   Cân nhắc tích hợp với công cụ phân tích log bên ngoài nếu cần. 