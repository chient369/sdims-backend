# Mô tả Chi tiết Màn hình: MH-OPP-01 - Danh sách Cơ hội Kinh doanh

**Version Control:**

| Version | Date       | Author         | Changes                                                               | Approved By | Status    |
| :------ | :--------- | :------------- | :-------------------------------------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Gemini (AI)    | Initial draft based on requirements & flow                            |             | Draft     |
| 1.1     | 2025-04-28 | Gemini (AI)    | Incorporated suggestions into main description sections, removed #7 |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này hiển thị danh sách các cơ hội kinh doanh được đồng bộ từ Hubspot. Nó cho phép người dùng (Sales, 部長 - Team Leader, 課長 - General Manager（課長）, Admin) xem tổng quan, theo dõi trạng thái, lọc, tìm kiếm và truy cập vào chi tiết của từng cơ hội để thực hiện các hành động cụ thể như ghi chú hoặc phân công.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:** Xem tất cả cơ hội. Có thể thực hiện Đồng bộ thủ công, xem logs.
*   **General Manager:** Xem tất cả cơ hội (có thể giới hạn trong bộ phận/team của mình nếu cần). Có thể assign 部長. Có thể thực hiện Đồng bộ thủ công.
*   **Team Leader:** Xem các cơ hội được assign cho mình, hoặc tất cả cơ hội (cần làm rõ). Có thể truy cập chi tiết để xem/thêm ghi chú.
*   **Sales:** Xem các cơ hội mình phụ trách (đồng bộ từ Hubspot). Có thể truy cập chi tiết để xem/thêm ghi chú.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Bộ lọc & Tìm kiếm:** Nằm ở phía trên cùng.
*   **Khu vực Hành động:** Các nút chức năng chính (VD: Đồng bộ, Export) đặt gần khu vực lọc.
*   **Khu vực Hiển thị:**
    *   Mặc định là **Bảng Danh sách Cơ hội**.
*   **Phân trang (Pagination):** Nằm ở cuối bảng danh sách (áp dụng cho dạng Bảng).

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Bộ lọc / Tìm kiếm

*   **Ô tìm kiếm:** Cho phép nhập từ khóa để tìm theo Tên cơ hội, Tên khách hàng.
*   **Bộ lọc (Dropdown/Multi-select):**
    *   `Người phụ trách Sales:` (Lấy danh sách Sales từ Hubspot/User hệ thống).
    *   `Leader được assign:` (Lấy danh sách User có vai trò Leader).
    *   `Giai đoạn Bán hàng (Deal Stage):` (Lấy các giá trị từ Hubspot).
    *   `Trạng thái Follow-up:` (Red, Yellow, Green).
    *   `Ưu tiên Onsite:` (Có, Không).
    *   `(Optional)` Bộ lọc theo khoảng thời gian (Ngày tạo, Ngày cập nhật cuối).
*   **Nút:**
    *   `Tìm kiếm / Lọc`: Áp dụng các tiêu chí tìm kiếm và lọc.
    *   `Xóa bộ lọc`: Đặt lại tất cả các trường lọc về giá trị mặc định.
*   **(Suggestion)** Nên có cơ chế **lưu lại trạng thái bộ lọc** người dùng đã chọn cho lần truy cập sau để tăng tính tiện dụng.

### 4.2. Khu vực Hành động Chính

*   **Nút `Đồng bộ thủ công`:**
    *   Hiển thị cho: Admin, General Manager.
    *   Chức năng: Kích hoạt việc lấy dữ liệu mới nhất từ Hubspot ngay lập tức. Cần có thông báo xác nhận và phản hồi kết quả (thành công/thất bại, số lượng bản ghi được cập nhật/thêm mới).
*   **(Optional) Nút `Export`:**
    *   Hiển thị cho: Có thể giới hạn theo vai trò (Admin, General Manager).
    *   Chức năng: Xuất danh sách cơ hội hiện tại (sau khi lọc) ra file CSV/Excel.

### 4.3. Bảng Danh sách Cơ hội (Default View)

Hiển thị dữ liệu dạng bảng với các cột thông tin chính. Cho phép sắp xếp (sort) theo các cột có thể sắp xếp.

*   **Hiển thị Dòng:**
    *   **(Suggestion)** Các dòng tương ứng với cơ hội **mới được đồng bộ hoặc có tương tác mới** có thể được **highlight** tạm thời (VD: màu nền khác biệt nhẹ) để dễ nhận biết.
*   **Các cột (Columns) đề xuất:**
    *   `Tên Cơ hội:` (Hiển thị text, **là link dẫn đến màn hình `MH-OPP-02`**).
    *   `Khách hàng:` (Tên khách hàng).
    *   `Giá trị ước tính:` (Hiển thị số tiền, định dạng tiền tệ rõ ràng).
    *   `Giai đoạn Bán hàng (Deal Stage):` (Tên stage).
    *   `Người phụ trách Sales:` (Tên Sales).
    *   `Leader được assign:` (Hiển thị tên các 部長 được gán, có thể là danh sách nếu nhiều người).
    *   `Ngày tương tác cuối:` (Hiển thị ngày `Last Interaction Date`).
    *   `Trạng thái Follow-up:` (Hiển thị chỉ báo màu **Red/Yellow/Green** dựa trên tính toán từ `Last Interaction Date` và ngưỡng cấu hình).
    *   `Ưu tiên Onsite:` (Hiển thị biểu tượng/checkbox thể hiện trạng thái `Onsite Priority Flag`).
    *    `Ngày tạo:`
    *    `Ngày cập nhật cuối:`
    *   **Quick Actions** Cột `Hành động:` (Optional): Chứa các nút cho phép thực hiện nhanh một số thao tác phổ biến mà không cần vào chi tiết, ví dụ:
        *   Nút `Assign Leader` (nếu Sales/GM có quyền).
        *   Nút `Thêm Ghi chú` (mở popup nhanh).
*   **Sắp xếp (Sorting):** Cho phép người dùng click vào tiêu đề cột để sắp xếp tăng/giảm dần. Cột mặc định có thể là Ngày cập nhật cuối hoặc Ngày tạo (giảm dần).
*   **Phân trang (Pagination):** Hiển thị các điều khiển để chuyển trang.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:** Hệ thống truy vấn CSDL, lấy danh sách cơ hội dựa trên quyền hạn và bộ lọc đã lưu (nếu có). Hiển thị dữ liệu lên view mặc định (Bảng/Kanban) và cập nhật phân trang.
*   **Thay đổi Bộ lọc/Nhập Tìm kiếm & Click `Tìm kiếm / Lọc`:** Hệ thống thực hiện truy vấn mới, lưu lại bộ lọc (nếu có), cập nhật Bảng/Kanban và phân trang.
*   **Click `Xóa bộ lọc`:** Đặt lại các trường lọc, xóa bộ lọc đã lưu (nếu có), thực hiện truy vấn lại, cập nhật Bảng/Kanban và phân trang.
*   **Click `Tên Cơ hội` (trong Bảng) hoặc Thẻ Cơ hội (trong Kanban):** Điều hướng đến `MH-OPP-02`.
*   **Click `Đồng bộ thủ công`:** Thực hiện đồng bộ, thông báo kết quả, refresh lại view hiện tại.
*   **Click Sắp xếp (Tiêu đề cột - trong Bảng):** Thực hiện truy vấn lại với sắp xếp mới, cập nhật Bảng và phân trang.
*   **Click Phân trang (trong Bảng):** Thực hiện truy vấn lấy dữ liệu trang mới, cập nhật Bảng và phân trang.
*   **Click Quick Action (trên dòng Bảng):** Thực hiện hành động tương ứng (mở popup Assign Leader, popup Thêm Ghi chú...).*
*   **Kéo thả Thẻ (trong Kanban):** (Nếu impl.) Hiển thị confirm thay đổi Stage -> Gọi API cập nhật Stage -> Refresh Kanban.
*   **Click Chuyển đổi View:** Thay đổi cách hiển thị giữa Bảng và Kanban.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Hiệu năng:** Tối ưu truy vấn, đặc biệt khi lọc/sắp xếp. Cân nhắc hiệu năng khi hiển thị Kanban view với nhiều cơ hội.
*   **Đồng bộ Hubspot:** Xử lý lỗi, xác định cơ chế cập nhật/xóa.
*   **Trạng thái Follow-up:** Logic tính toán chính xác.
*   **Phân quyền dữ liệu:** Đảm bảo chỉ hiển thị dữ liệu được phép.
*   **Consistency giữa Views:** Nếu có cả Bảng và Kanban, dữ liệu và bộ lọc phải đồng nhất giữa hai view.
 