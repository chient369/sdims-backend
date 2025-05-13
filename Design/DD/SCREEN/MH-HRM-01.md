# Mô tả Chi tiết Màn hình: MH-HRM-01 - Danh sách Nhân sự

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |
| 1.1     | 2025-04-28 | Gemini (AI)    | Incorporated Visual Status suggestion into description |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp một giao diện tập trung để xem, tìm kiếm, lọc danh sách nhân sự trong bộ phận/công ty. Nó là điểm khởi đầu để truy cập thông tin chi tiết của từng nhân viên hoặc thực hiện các thao tác quản lý như thêm mới hoặc xuất dữ liệu. Màn hình này hỗ trợ các nhà quản lý (Leader, 課長) và Admin trong việc nắm bắt tình hình nguồn lực hiện tại.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem danh sách *tất cả* nhân viên.
    *   Sử dụng chức năng Tìm kiếm, Lọc.
    *   Sử dụng chức năng `Thêm mới`.
    *   Sử dụng chức năng `Export`.
    *   Truy cập Chi tiết nhân sự.
*   **課長 (General Manager（課長）):**
    *   Xem danh sách *tất cả* nhân viên (hoặc giới hạn trong các bộ phận quản lý nếu cần).
    *   Sử dụng chức năng Tìm kiếm, Lọc.
    *   Sử dụng chức năng `Thêm mới` (cần xác nhận lại quyền).
    *   Sử dụng chức năng `Export`.
    *   Truy cập Chi tiết nhân sự.
*   **部長 (Team Leader):**
    *   Xem danh sách nhân viên thuộc *team mình quản lý*.
    *   Sử dụng chức năng Tìm kiếm, Lọc (trong phạm vi team).
    *   Có thể sử dụng chức năng `Export` (dữ liệu team mình).
    *   Truy cập Chi tiết nhân sự (trong team).
    *   **(Note)** Không có quyền `Thêm mới` trực tiếp từ màn hình này (việc thêm mới thường do Admin/HR hoặc 課長 thực hiện).
*   **Nhân viên (Employee):** Thông thường không truy cập màn hình quản lý này. Có thể có một màn hình "Danh bạ" khác đơn giản hơn.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Bộ lọc & Tìm kiếm:** Đặt ở phía trên cùng, có thể ẩn/hiện để tiết kiệm không gian.
*   **Khu vực Hành động:** Các nút chức năng chính (`Thêm mới`, `Export`) đặt gần khu vực lọc.
*   **Bảng Danh sách Nhân sự:** Chiếm phần lớn diện tích, hiển thị dữ liệu dạng bảng.
*   **Phân trang (Pagination):** Nằm ở cuối bảng danh sách.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Bộ lọc / Tìm kiếm

*   **Ô tìm kiếm:** Tìm kiếm nhanh theo `Mã Nhân viên`, `Họ tên`, `Email`.
*   **Bộ lọc (Dropdown/Multi-select):**
    *   `Team:` (Lấy danh sách các Team hiện có). Chỉ hiển thị cho Admin/課長.
    *   `Vị trí công việc:` (Developer, Tester, BA, Leader...). Lấy từ danh mục cấu hình.
    *   `Trạng thái:` (Allocated, Available/Bench, Ending Soon, On Leave...). Lấy từ danh mục cấu hình.
    *   `(Optional) Skill:` Tìm kiếm nhân sự có skill cụ thể (VD: Java, React). Có thể là ô nhập text autocomplete hoặc multi-select.
*   **Nút:**
    *   `Tìm kiếm / Lọc`: Áp dụng các tiêu chí tìm kiếm và lọc.
    *   `Xóa bộ lọc`: Đặt lại tất cả các trường lọc về giá trị mặc định.

### 4.2. Khu vực Hành động Chính

*   **Nút `Thêm mới`:**
    *   Hiển thị cho: Admin, 課長 (dự kiến).
    *   Chức năng: Điều hướng đến màn hình `MH-HRM-03` (Form Thêm/Sửa Nhân sự) ở chế độ "Thêm mới".
*   **Nút `Export`:**
    *   Hiển thị cho: Admin, 課長, 部長.
    *   Chức năng: Xuất danh sách nhân sự hiện tại (sau khi lọc) ra file CSV/Excel. Nội dung export tuân theo quyền hạn (部長 chỉ export được team mình).

### 4.3. Bảng Danh sách Nhân sự

Hiển thị dữ liệu dạng bảng, cho phép sắp xếp (sort) theo các cột quan trọng.

*   **Các cột (Columns) đề xuất:**
    *   `Mã Nhân viên:` (Hiển thị text).
    *   `Họ và Tên:` (Hiển thị text, **là link dẫn đến màn hình `MH-HRM-02` - Chi tiết Nhân sự**).
    *   `Vị trí công việc:` (Hiển thị text).
    *   `Team:` (Hiển thị tên Team).
    *   `Email công ty:` (Hiển thị text).
    *   `Trạng thái:` (Hiển thị text. **(Suggestion - Optional) Nên sử dụng tag màu hoặc biểu tượng rõ ràng** để dễ nhận biết, VD: màu xanh lá cho 'Available', màu đỏ cho 'Ending Soon').
    *   `(Optional)` `Leader trực tiếp:` (Tên Leader).
    *   `(Optional)` `Ngày vào công ty:` (Hiển thị ngày).
    *   `(Optional)` Cột `Hành động:` (Chứa icon/nút để truy cập nhanh vào sửa? - Cân nhắc vì đã có link ở tên).
*   **Sắp xếp (Sorting):** Cho phép người dùng click vào tiêu đề cột để sắp xếp tăng/giảm dần (VD: Họ tên, Mã NV, Vị trí, Team, Trạng thái...). Cột sắp xếp mặc định có thể là Họ tên hoặc Mã NV.
*   **Phân trang (Pagination):** Hiển thị các điều khiển để chuyển trang khi số lượng nhân sự vượt quá giới hạn hiển thị trên một trang (VD: 20, 50 bản ghi/trang).

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Hệ thống kiểm tra quyền người dùng.
    *   Truy vấn CSDL lấy danh sách nhân sự phù hợp với quyền (Admin/課長: all, 部長: team).
    *   Áp dụng bộ lọc/sắp xếp mặc định (nếu có).
    *   Hiển thị dữ liệu lên bảng và cập nhật phân trang.
*   **Thay đổi Bộ lọc/Nhập Tìm kiếm & Click `Tìm kiếm / Lọc`:**
    *   Hệ thống thực hiện truy vấn mới dựa trên tiêu chí và quyền hạn.
    *   Cập nhật lại Bảng Danh sách và phân trang.
*   **Click `Xóa bộ lọc`:**
    *   Đặt lại các trường lọc về giá trị mặc định.
    *   Thực hiện truy vấn lại như khi load màn hình lần đầu.
    *   Cập nhật Bảng Danh sách và phân trang.
*   **Click `Thêm mới`:** Điều hướng người dùng sang màn hình `MH-HRM-03` (chế độ Add).
*   **Click `Export`:**
    *   Hệ thống thu thập dữ liệu từ danh sách hiện tại (đã lọc, theo quyền).
    *   Tạo file Excel/CSV.
    *   Trigger tải file về máy người dùng.
*   **Click vào `Họ và Tên` nhân viên:**
    *   Lấy ID của nhân viên tương ứng.
    *   Điều hướng người dùng sang màn hình `MH-HRM-02` (Chi tiết Nhân sự), truyền ID theo.
*   **Click Sắp xếp (Tiêu đề cột):**
    *   Hệ thống thực hiện truy vấn lại với tham số sắp xếp mới (và các bộ lọc hiện tại).
    *   Cập nhật lại Bảng Danh sách và phân trang.
*   **Click Phân trang:**
    *   Hệ thống thực hiện truy vấn để lấy dữ liệu cho trang được yêu cầu (với bộ lọc và sắp xếp hiện tại).
    *   Cập nhật lại Bảng Danh sách và trạng thái phân trang.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền dữ liệu:** Cực kỳ quan trọng. Đảm bảo 部長 chỉ thấy và thao tác được với dữ liệu team mình. Admin/課長 thấy đúng phạm vi quản lý.
*   **Hiệu năng:** Tối ưu hóa truy vấn CSDL, đặc biệt khi lọc/sắp xếp với số lượng nhân viên lớn. Sử dụng index phù hợp. Cân nhắc lazy loading hoặc pagination hiệu quả.
*   **Dữ liệu Trạng thái:** Đảm bảo cột `Trạng thái` luôn hiển thị thông tin cập nhật và chính xác từ module quản lý trạng thái/phân bổ.
*   **Tính nhất quán Danh mục:** Dữ liệu trong các bộ lọc (Vị trí, Trạng thái, Team) phải được lấy từ nguồn cấu hình chung (Admin) để đảm bảo tính nhất quán.
*   **Chức năng Export:** Xử lý trường hợp dữ liệu lớn, thông báo cho người dùng nếu quá trình export mất thời gian. Đảm bảo file export đúng định dạng và đầy đủ thông tin cần thiết.