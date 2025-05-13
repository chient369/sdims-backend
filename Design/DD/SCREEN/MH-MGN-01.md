# Mô tả Chi tiết Màn hình: MH-MGN-01 - Bảng Margin Nhân sự

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cho phép các nhà quản lý (部長 - Team Leader, 課長 - General Manager（課長）) theo dõi hiệu suất tài chính (cụ thể là margin) của từng nhân viên và tổng hợp theo team/bộ phận. Nó cung cấp cái nhìn chi tiết về chi phí, doanh thu và tỷ lệ lợi nhuận gộp, kèm theo cảnh báo trạng thái margin để hỗ trợ việc ra quyết định quản lý và tối ưu hóa nguồn lực.

## 2. Đối tượng Sử dụng và Phân quyền (Rất Quan trọng)

**Truy cập màn hình này phải được kiểm soát chặt chẽ:**

*   **課長 (General Manager（課長）):**
    *   Xem được dữ liệu margin của *tất cả* nhân viên thuộc bộ phận mình quản lý (hoặc toàn công ty nếu được cấu hình).
    *   Có thể lọc dữ liệu theo `Team`.
    *   Sử dụng chức năng `Export` (cho phạm vi dữ liệu được xem).
    *   Có thể điều hướng đến màn hình `Nhập Chi phí` (`MH-MGN-02`).
*   **部長 (Team Leader):**
    *   Chỉ xem được dữ liệu margin của nhân viên thuộc *team mình quản lý trực tiếp*.
    *   Không thấy bộ lọc `Team` (dữ liệu đã được lọc sẵn theo team của Leader).
    *   Sử dụng chức năng `Export` (chỉ cho dữ liệu team mình).
    *   Có thể điều hướng đến màn hình `Nhập Chi phí` (`MH-MGN-02`).
*   **Admin:** Có thể cần quyền truy cập để cấu hình hoặc hỗ trợ, nhưng không phải người dùng nghiệp vụ chính.
*   **Các vai trò khác (Sales, Nhân viên...):** **KHÔNG** có quyền truy cập màn hình này.

## 3. Bố cục Màn hình

*   **Khu vực Bộ lọc:** Đặt ở phía trên, bao gồm bộ lọc Thời gian và Team (nếu có quyền).
*   **Khu vực Hành động:** Nút `Export`, nút điều hướng `Nhập Chi phí`.
*   **Bảng Dữ liệu Margin:** Chiếm phần chính, hiển thị chi tiết từng nhân viên.
*   **(Optional) Khu vực Tổng hợp/Tóm tắt:** Hiển thị margin trung bình/tổng hợp cho phạm vi dữ liệu đang xem.
*   **Phân trang (Pagination):** Nếu danh sách nhân viên dài.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Bộ lọc

*   **Bộ lọc Thời gian (Bắt buộc):**
    *   Cho phép chọn Kỳ xem dữ liệu: Theo Tháng (VD: Tháng 4/2025), theo Quý (VD: Q2/2025), theo Năm (VD: 2025).
    *   Mặc định có thể là Tháng/Quý hiện tại hoặc gần nhất.
    *   Cần có cơ chế chọn lựa dễ dàng (VD: dropdowns, date picker range).
*   **Bộ lọc `Team` (Chỉ hiển thị cho 課長):**
    *   Dropdown cho phép chọn một hoặc nhiều Team cụ thể để xem, hoặc chọn "Tất cả" (trong phạm vi quản lý của 課長).
*   **Nút:**
    *   `Xem / Lọc`: Áp dụng bộ lọc Thời gian và Team (nếu có).

### 4.2. Khu vực Hành động

*   **Nút `Export`:**
    *   Chức năng: Xuất dữ liệu margin đang hiển thị (sau khi lọc) ra file CSV/Excel.
    *   Quyền: Chỉ xuất được dữ liệu người dùng có quyền xem.
*   **Nút `Đi đến Nhập Chi phí`:**
    *   Chức năng: Điều hướng người dùng đến màn hình `MH-MGN-02` để nhập hoặc import dữ liệu chi phí.

### 4.3. Bảng Dữ liệu Margin Nhân sự

Hiển thị chi tiết hiệu suất tài chính của từng nhân viên trong kỳ đã chọn.

*   **Các cột (Columns) đề xuất:**
    *   `Mã Nhân viên:`
    *   `Họ và Tên:`
    *   `Team:` (Quan trọng để nhóm/lọc)
    *   `Kỳ:` (Hiển thị Tháng/Quý/Năm đang xem)
    *   `Chi phí (Cost):` (Hiển thị số tiền, định dạng rõ ràng)
    *   `Doanh thu (Revenue):` (Hiển thị số tiền, định dạng rõ ràng. Tính toán từ phân bổ dự án & rate hợp đồng)
    *   `Margin (%):` (Hiển thị tỷ lệ %, tính theo công thức: `((Revenue - Cost) / Revenue) * 100%` nếu Revenue > 0)
    *   `Trạng thái Margin:` (Hiển thị **màu cảnh báo Red/Yellow/Green** dựa trên ngưỡng cấu hình. Có thể kèm text trạng thái).
*   **Sắp xếp (Sorting):** Cho phép sắp xếp theo `Họ tên`, `Team`, `Margin (%)`, `Trạng thái Margin`.
*   **Dữ liệu:**
    *   Cost: Lấy từ dữ liệu được nhập/import qua `MH-MGN-02`.
    *   Revenue: Tính toán tự động dựa trên dữ liệu phân bổ nhân sự (từ `MH-HRM-01`/`MH-HRM-03`) và thông tin đơn giá từ hợp đồng (`MH-CTR-01`/`MH-CTR-03`). Cần logic tính toán chuẩn xác.
    *   Margin & Status: Tính toán dựa trên Cost, Revenue và ngưỡng cấu hình (từ `MH-ADM-03`).
*   **Phân trang (Pagination):** Nếu cần thiết.

### 4.4. Khu vực Tổng hợp/Tóm tắt (Optional)

*   Hiển thị các chỉ số tổng hợp cho phạm vi dữ liệu đang xem (VD: Team A, Quý 2/2025):
    *   `Tổng Cost:`
    *   `Tổng Revenue:`
    *   `Margin Trung bình (%):`
    *   `Số lượng nhân sự theo trạng thái (Red/Yellow/Green):`

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Kiểm tra quyền truy cập (chỉ Leader/課長).
    *   Lấy bộ lọc mặc định (Kỳ hiện tại, Team của Leader hoặc tất cả cho 課長).
    *   Truy vấn CSDL để lấy dữ liệu Cost, tính toán Revenue, Margin, Status cho các nhân viên thuộc phạm vi quyền và bộ lọc.
    *   Hiển thị dữ liệu lên bảng và khu vực tổng hợp (nếu có).
    *   Cập nhật phân trang.
*   **Thay đổi Bộ lọc Thời gian/Team & Click `Xem / Lọc`:**
    *   Hệ thống thực hiện truy vấn mới dựa trên tiêu chí lọc và quyền hạn.
    *   Cập nhật lại Bảng dữ liệu, Khu vực tổng hợp và phân trang.
*   **Click `Export`:**
    *   Thu thập dữ liệu đang hiển thị.
    *   Tạo file Excel/CSV.
    *   Trigger tải file.
*   **Click `Đi đến Nhập Chi phí`:** Điều hướng sang màn hình `MH-MGN-02`.
*   **Click Sắp xếp (Tiêu đề cột):**
    *   Thực hiện truy vấn lại với tham số sắp xếp mới.
    *   Cập nhật Bảng dữ liệu và phân trang.
*   **Click Phân trang:**
    *   Thực hiện truy vấn lấy dữ liệu trang mới.
    *   Cập nhật Bảng dữ liệu và trạng thái phân trang.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Bảo mật và Phân quyền:** Nghiêm ngặt! Leader chỉ thấy team mình, 課長 thấy bộ phận. Dữ liệu tài chính nhạy cảm.
*   **Tính chính xác dữ liệu:**
    *   Cost: Phải được nhập/import đầy đủ và đúng kỳ.
    *   Revenue: Logic tính toán phải chuẩn, dựa trên % allocation và đơn giá chính xác.
    *   Margin: Công thức tính đúng.
*   **Ngưỡng Margin:** Phải được lấy từ cấu hình (`MH-ADM-03`) và áp dụng nhất quán.
*   **Hiệu năng:** Truy vấn có thể phức tạp do cần join/tính toán từ nhiều nguồn (Cost, Allocation, Contract Rate). Cần tối ưu và sử dụng index.
*   **Xử lý trường hợp đặc biệt:** Nhân viên mới vào, nhân viên nghỉ giữa kỳ, nhân viên không có doanh thu (Revenue = 0 hoặc Cost = 0)... cần có cách hiển thị hoặc tính toán phù hợp.
