# Mô tả Chi tiết Màn hình: MH-OPP-02 - Chi tiết Cơ hội Kinh doanh

**Version Control:**

| Version | Date       | Author         | Changes                                                   | Approved By | Status    |
| :------ | :--------- | :------------- | :-------------------------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Gemini (AI)    | Initial draft based on requirements & flow                |             | Draft     |
| 1.1     | 2025-04-28 | Gemini (AI)    | Incorporated suggestions into main sections, removed #7 |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này hiển thị thông tin chi tiết về một cơ hội kinh doanh cụ thể đã được chọn từ màn hình danh sách (`MH-OPP-01`). Nó cho phép người dùng xem các thuộc tính chi tiết, lịch sử tương tác, thêm ghi chú, quản lý việc phân công Leader (部長) hỗ trợ, và đánh dấu các thông tin quan trọng như ưu tiên onsite.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem được chi tiết *tất cả* các cơ hội.
    *   Có thể xem lịch sử tương tác.
    *   (Cần xác nhận) Có thể assign/unassign Leader?
    *   (Cần xác nhận) Có thể thêm ghi chú?
*   **課長 (General Manager（課長）):**
    *   Xem được chi tiết *tất cả* các cơ hội (hoặc trong phạm vi quản lý).
    *   Xem lịch sử tương tác.
    *   Có quyền `Assign/Unassign 部長`.
    *   Có quyền `Thêm ghi chú`.
    *   Có quyền `Đánh dấu Ưu tiên Onsite`.
*   **部長 (Team Leader):**
    *   Chỉ xem được chi tiết các cơ hội *mình được assign* hoặc các cơ hội *thuộc team Sales mình quản lý* (cần làm rõ quy tắc).
    *   Xem lịch sử tương tác.
    *   Có quyền `Thêm ghi chú` vào các cơ hội mình được xem.
    *   **(Note)** Thông thường không có quyền Assign Leader hay đánh dấu Onsite.
*   **Sales:**
    *   Chỉ xem được chi tiết các cơ hội *mình phụ trách*.
    *   Xem lịch sử tương tác.
    *   Có quyền `Thêm ghi chú` vào cơ hội của mình.
    *   Có quyền `Assign/Unassign 部長` (hoặc yêu cầu assign qua 課長? - Cần làm rõ quy trình).
    *   Có quyền `Đánh dấu Ưu tiên Onsite`.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Thông tin Tổng quan:** Phía trên cùng, hiển thị các thông tin cốt lõi của cơ hội.
*   **Khu vực Hành động Chính:** Các nút như `Assign Leader`, `Thêm ghi chú`, `Đánh dấu Onsite` đặt ở vị trí dễ thấy.
*   **Khu vực Chi tiết & Lịch sử:** Có thể chia thành các Tab hoặc Section:
    *   **Tab/Section 1: Thông tin Chi tiết:** Hiển thị đầy đủ các trường dữ liệu đồng bộ từ Hubspot và các trường bổ sung của hệ thống.
    *   **Tab/Section 2: Lịch sử Tương tác / Ghi chú:** Hiển thị danh sách các ghi chú, hoạt động theo thời gian.
*   **Nút Điều hướng:** Nút quay lại danh sách (`MH-OPP-01`).

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Thông tin Tổng quan

*   Hiển thị các thông tin nổi bật, dễ nhận biết:
    *   `Tên Cơ hội:`
    *   `Khách hàng:`
    *   `Giá trị ước tính:`
    *   `Giai đoạn Bán hàng (Deal Stage):`
    *   `Người phụ trách Sales:`
    *   `Trạng thái Follow-up:` (Hiển thị màu Red/Yellow/Green và ngày tương tác cuối `Last Interaction Date`).

### 4.2. Khu vực Hành động Chính

*   **Nút `Assign/Manage Leader`:**
    *   Hiển thị cho: Sales, 課長 (dự kiến).
    *   Chức năng: Mở popup/dialog cho phép:
        *   Xem danh sách các 部長 đã được assign.
        *   Thêm (chọn từ danh sách 部長) hoặc Xóa (unassign) 部長 khỏi cơ hội này.
        *   Lưu thay đổi.
*   **Nút `Thêm Ghi chú`:**
    *   Hiển thị cho: Sales, 部長 (được assign/liên quan), 課長.
    *   Chức năng: Mở một popup/khung nhập liệu để:
        *   Nhập nội dung ghi chú (text area).
        *   (Optional) Chọn loại hoạt động (Call, Email, Meeting...).
        *   **(Suggestion - Optional)** Chọn loại/tag ghi chú (VD: Internal Note, Customer Interaction, Technical Note).
        *   Lưu ghi chú. (Khi lưu, hệ thống tự động cập nhật `Last Interaction Date` của cơ hội).
*   **Checkbox/Toggle `Ưu tiên Onsite`:**
    *   Hiển thị cho: Sales, 課長 (dự kiến).
    *   Chức năng: Cho phép đánh dấu hoặc bỏ đánh dấu cơ hội này cần ưu tiên xem xét yếu tố onsite.

### 4.3. Tab/Section: Thông tin Chi tiết

*   Hiển thị đầy đủ các trường dữ liệu của cơ hội:
    *   Các trường đồng bộ từ Hubspot (có thể nhóm lại cho gọn): Tên, Khách hàng, Giá trị, Deal Stage, Ngày tạo, Ngày đóng dự kiến, Mô tả, URL Hubspot (nếu có), ...
    *   Các trường của hệ thống:
        *   `Người phụ trách Sales:`
        *   `部長 được assign:` (Danh sách tên các Leader).
        *   `Last Interaction Date:`
        *   `Trạng thái Follow-up:` (Red/Yellow/Green).
        *   `Ưu tiên Onsite:` (Yes/No).

### 4.4. Tab/Section: Lịch sử Tương tác / Ghi chú

*   Hiển thị danh sách các ghi chú/hoạt động đã được thêm vào cơ hội, sắp xếp theo thời gian (mới nhất lên trên).
*   Mỗi mục trong danh sách hiển thị:
    *   `Ngày giờ tạo ghi chú:`
    *   `Người tạo ghi chú:` (Tên người dùng).
    *   `Nội dung ghi chú:`
    *   `(Optional)` Loại hoạt động.
    *   **(Suggestion - Optional)** Loại/Tag ghi chú (nếu có).
*   **(Suggestion - Optional)** Có thể có chức năng lọc/tìm kiếm trong lịch sử ghi chú theo người tạo, loại/tag, nội dung.
*   **(Suggestion - Optional)** Cân nhắc có cho phép **chỉnh sửa/xóa ghi chú** hay không và phân quyền chặt chẽ cho hành động này.

### 4.5. (Optional) Tab/Section: Tài liệu Đính kèm

*   **Chức năng:** Cho phép người dùng (Sales, Leader, 課長) upload và quản lý các file tài liệu liên quan đến cơ hội (VD: tài liệu kỹ thuật, yêu cầu chi tiết, báo giá sơ bộ...).
*   **Hiển thị:** Danh sách các file đã upload, kèm thông tin tên file, ngày upload, người upload.
*   **Hành động:** Nút `Upload File`, nút `Tải xuống`, nút `Xóa File` (cần phân quyền).

### 4.6. Nút Điều hướng

*   **Nút `Quay lại Danh sách`:** Điều hướng người dùng về màn hình `MH-OPP-01` (giữ nguyên trạng thái lọc/phân trang trước đó nếu có thể).

## 5. Luồng Sự kiện Chính

*   **Load Màn hình (Truy cập từ `MH-OPP-01`):**
    *   Nhận ID cơ hội.
    *   Kiểm tra quyền truy cập của người dùng đối với cơ hội này.
    *   Truy vấn CSDL lấy thông tin chi tiết và lịch sử ghi chú.
    *   Hiển thị dữ liệu lên các khu vực tương ứng.
    *   Hiển thị/ẩn các nút hành động dựa trên quyền.
*   **Click `Assign/Manage Leader`:**
    *   Mở popup, hiển thị danh sách Leader đã assign và danh sách Leader có thể assign.
    *   Người dùng chọn/bỏ chọn Leader -> Click `Lưu`.
    *   Hệ thống cập nhật danh sách assign trong CSDL.
    *   Đóng popup, refresh lại khu vực hiển thị Leader được assign.
    *   **(Suggestion)** **Gửi thông báo** (in-app/email) cho Leader được assign/unassign.
*   **Click `Thêm Ghi chú`:**
    *   Mở popup nhập liệu.
    *   Người dùng nhập nội dung -> Click `Lưu`.
    *   Hệ thống lưu ghi chú vào CSDL, cập nhật `Last Interaction Date` của cơ hội.
    *   Đóng popup, refresh lại danh sách Lịch sử Tương tác và cập nhật Trạng thái Follow-up.
    *   **(Suggestion)** **Gửi thông báo** (in-app/email) cho những người liên quan (VD: Sales, Leader được assign) khi có ghi chú mới (có thể cấu hình loại ghi chú nào thì gửi).
*   **Click Checkbox/Toggle `Ưu tiên Onsite`:**
    *   Hệ thống cập nhật trạng thái cờ `Onsite Priority Flag` trong CSDL.
    *   Hiển thị trạng thái mới trên UI.
*   **(Optional) Upload File (trong Tab Tài liệu):**
    *   Mở dialog chọn file.
    *   Upload file, lưu trữ và liên kết với cơ hội.
    *   Refresh danh sách file đính kèm.
*   **Click `Quay lại Danh sách`:** Điều hướng về `MH-OPP-01`.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền:** Đảm bảo người dùng chỉ xem và thao tác được trên những cơ hội họ có quyền. Các nút hành động phải được ẩn/hiện đúng theo vai trò.
*   **Cập nhật `Last Interaction Date`:** Logic cập nhật phải chính xác khi thêm ghi chú mới.
*   **Tính toán `Trạng thái Follow-up`:** Phải được tính toán lại và hiển thị đúng mỗi khi `Last Interaction Date` thay đổi hoặc khi load màn hình.
*   **Đồng bộ Dữ liệu:** Các thông tin hiển thị từ Hubspot phải là thông tin mới nhất đã được đồng bộ.
*   **Giao diện Người dùng (UI):** Hiển thị thông tin rõ ràng, dễ đọc. Lịch sử ghi chú cần trình bày khoa học.
*   **(Optional) Quản lý File:** Cần có cơ chế lưu trữ file an toàn, giới hạn dung lượng/loại file nếu cần.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Phân loại Ghi chú:** Cho phép gắn thẻ (tag) hoặc phân loại ghi chú (VD: Internal Note, Customer Interaction, Technical Note) để dễ lọc và tìm kiếm.
*   **Thông báo (Notifications):** Cần có cơ chế thông báo rõ ràng (VD: trong hệ thống, qua email) khi có Leader mới được assign, hoặc khi có ghi chú mới quan trọng.
*   **Liên kết Tài liệu:** Cho phép đính kèm file (tài liệu kỹ thuật, báo giá...) liên quan đến cơ hội.
*   **Chỉnh sửa/Xóa Ghi chú:** Cân nhắc có nên cho phép chỉnh sửa/xóa ghi chú hay không và phân quyền cho hành động này. 