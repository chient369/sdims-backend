# Mô tả Chi tiết Màn hình: MH-RPT-01 - Danh sách Báo cáo

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Chiến Trần Văn | Initial draft based on requirements        |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện tập trung để hiển thị danh sách các loại báo cáo có sẵn trong hệ thống. Người dùng có thể dễ dàng tìm kiếm, xem thông tin tóm tắt và truy cập vào các báo cáo chi tiết cần thiết cho công việc của họ. Đây là điểm khởi đầu để truy cập tất cả các báo cáo trong hệ thống.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem danh sách *tất cả* các báo cáo trong hệ thống.
    *   Truy cập vào tất cả các báo cáo chi tiết.
*   **課長 (General Manager):**
    *   Xem danh sách các báo cáo liên quan đến toàn bộ khía cạnh vận hành.
    *   Truy cập vào các báo cáo chi tiết được phân quyền.
*   **部長 (Team Leader):**
    *   Xem danh sách các báo cáo liên quan đến team mình quản lý.
    *   Truy cập vào các báo cáo chi tiết của team được phân quyền.
*   **Kế toán:**
    *   Xem danh sách các báo cáo tài chính, hợp đồng, doanh thu.
    *   Truy cập vào các báo cáo chi tiết tài chính được phân quyền.
*   **Sales:**
    *   Xem danh sách các báo cáo về cơ hội kinh doanh, KPI, doanh thu.
    *   Truy cập vào các báo cáo chi tiết sales được phân quyền.
*   **Nhân viên (Employee):**
    *   Có thể có quyền truy cập hạn chế vào một số báo cáo cơ bản.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Tiêu đề trang:** "Danh sách Báo cáo" - Nằm ở phía trên cùng.
*   **Khu vực Tìm kiếm & Bộ lọc:** Đặt ở phía trên, ngay dưới tiêu đề.
*   **Khu vực Hiển thị Báo cáo:** Chiếm phần lớn diện tích màn hình, có thể hiển thị theo dạng:
    *   Bảng (Table) - Hiển thị thông tin dạng danh sách.
    *   Thẻ (Card) - Hiển thị dạng lưới với icon, tiêu đề, mô tả ngắn.
*   **Phân trang (Pagination):** Nằm ở cuối danh sách báo cáo.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Tìm kiếm / Bộ lọc

*   **Ô tìm kiếm:** Tìm kiếm báo cáo theo tên, mô tả.
*   **Bộ lọc (Dropdown/Multi-select):**
    *   `Loại báo cáo`: Nhân sự, Tài chính, Cơ hội, Hợp đồng, Margin, KPI...
    *   `Module liên quan`: HRM, Margin, Cơ hội, Hợp đồng & Doanh thu.
    *   `Phạm vi báo cáo`: Cá nhân, Team, Toàn bộ.
*   **Nút:**
    *   `Tìm kiếm / Lọc`: Áp dụng các tiêu chí tìm kiếm và lọc.
    *   `Xóa bộ lọc`: Đặt lại tất cả các trường lọc về giá trị mặc định.

### 4.2. Khu vực Hiển thị Báo cáo

**Hiển thị dạng Thẻ (Card View - Khuyến nghị):**
*   Mỗi báo cáo được hiển thị trong một thẻ (card) riêng biệt, bao gồm:
    *   `Icon`: Biểu tượng trực quan thể hiện loại báo cáo.
    *   `Tên báo cáo`: Tiêu đề rõ ràng, **là link dẫn đến màn hình `MH-RPT-02` (Xem Báo cáo Chi tiết)**.
    *   `Mô tả ngắn`: 1-2 dòng mô tả mục đích và nội dung báo cáo.
    *   `Loại báo cáo`: Tag hoặc badge thể hiện phân loại.
    *   `Thời gian cập nhật cuối`: Thời gian báo cáo được refresh dữ liệu gần nhất.
    *   `Nút Xem`: Nút để truy cập nhanh đến báo cáo chi tiết.

**Hoặc Hiển thị dạng Bảng (Table View - Thay thế):**
*   Bảng với các cột:
    *   `Tên báo cáo`: (Hiển thị text, **là link dẫn đến màn hình `MH-RPT-02`**).
    *   `Mô tả`: Mô tả ngắn về báo cáo.
    *   `Loại báo cáo`: Phân loại báo cáo.
    *   `Module liên quan`: Module chức năng liên quan.
    *   `Cập nhật cuối`: Thời gian dữ liệu được cập nhật gần nhất.
    *   `Thao tác`: Nút `Xem` để truy cập báo cáo.

### 4.3. Chuyển đổi Chế độ Xem

*   **Toggle View:** Cho phép chuyển đổi giữa chế độ Thẻ và Bảng.
*   **Phân trang:** Hiển thị các điều khiển để chuyển trang khi số lượng báo cáo vượt quá giới hạn hiển thị.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Hệ thống kiểm tra quyền người dùng.
    *   Truy vấn CSDL lấy danh sách báo cáo mà người dùng có quyền truy cập.
    *   Hiển thị danh sách báo cáo theo chế độ xem mặc định.
*   **Thực hiện Tìm kiếm / Lọc:**
    *   Người dùng nhập từ khóa tìm kiếm và/hoặc chọn các bộ lọc.
    *   Click nút `Tìm kiếm / Lọc`.
    *   Hệ thống thực hiện truy vấn và hiển thị kết quả phù hợp.
*   **Click `Xóa bộ lọc`:**
    *   Đặt lại tất cả các trường lọc về giá trị mặc định.
    *   Thực hiện truy vấn lại như khi load màn hình lần đầu.
*   **Click vào Tên báo cáo / Nút Xem:**
    *   Lấy ID của báo cáo tương ứng.
    *   Điều hướng người dùng sang màn hình `MH-RPT-02` (Xem Báo cáo Chi tiết), truyền ID báo cáo và các tham số cần thiết.
*   **Chuyển đổi Chế độ Xem:**
    *   Người dùng click vào toggle chế độ xem.
    *   Hệ thống chuyển đổi giữa hiển thị dạng Thẻ và Bảng, giữ nguyên dữ liệu và bộ lọc hiện tại.
*   **Click Phân trang:**
    *   Hệ thống thực hiện truy vấn để lấy dữ liệu cho trang được yêu cầu.
    *   Cập nhật lại danh sách báo cáo và trạng thái phân trang.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền báo cáo:** Cực kỳ quan trọng. Người dùng chỉ thấy được các báo cáo mà họ có quyền truy cập.
*   **Khả năng hiển thị:** Đảm bảo mô tả báo cáo rõ ràng để người dùng dễ dàng lựa chọn báo cáo phù hợp với nhu cầu.
*   **Thời gian cập nhật:** Hiển thị thời gian cập nhật dữ liệu để người dùng biết được độ mới/cũ của báo cáo.
*   **Hiệu năng:** Tối ưu hóa truy vấn CSDL, đặc biệt khi có nhiều báo cáo và người dùng thực hiện tìm kiếm, lọc.
*   **Giao diện thích ứng:** Đảm bảo hiển thị tốt trên các kích thước màn hình khác nhau, đặc biệt là chế độ xem dạng Thẻ.
*   **Dữ liệu danh mục:** Các loại báo cáo và module liên quan phải được lấy từ cấu hình hệ thống để đảm bảo tính nhất quán và dễ bảo trì. 