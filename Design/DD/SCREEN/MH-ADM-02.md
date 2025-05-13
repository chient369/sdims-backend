# Mô tả Chi tiết Màn hình: MH-ADM-02 - (Admin) Quản lý Vai trò & Phân quyền

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Chiến Trần Văn | Initial draft based on requirements        |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện quản trị viên (Admin) để quản lý các vai trò (Roles) trong hệ thống và phân quyền chi tiết cho từng vai trò. Admin có thể tạo mới, chỉnh sửa, xóa các vai trò và cấu hình quyền truy cập đến các chức năng và dữ liệu cụ thể trong hệ thống. Màn hình này đóng vai trò quan trọng trong việc kiểm soát quyền truy cập và đảm bảo an toàn thông tin của hệ thống.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem danh sách vai trò.
    *   Tạo mới, chỉnh sửa, xóa vai trò.
    *   Cấu hình chi tiết quyền cho từng vai trò.
    *   Xem danh sách các quyền trong hệ thống.

Lưu ý: Chỉ Admin mới có quyền truy cập màn hình này. Các vai trò khác trong hệ thống không có quyền truy cập.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Tiêu đề trang:** "Quản lý Vai trò & Phân quyền" - Nằm ở phía trên cùng.
*   **Tab Navigation:** Cho phép chuyển đổi giữa hai chế độ xem chính:
    *   Tab `Danh sách Vai trò`: Hiển thị danh sách các vai trò hiện có.
    *   Tab `Phân quyền Chi tiết`: Giao diện phân quyền chi tiết cho vai trò đã chọn.
*   **Khu vực Hành động Chính:** Nút `Thêm vai trò mới` đặt ở trên cùng của tab Danh sách Vai trò.
*   **Khu vực Nội dung Chính:** Thay đổi tùy theo tab đang được chọn:
    *   Danh sách vai trò dạng bảng (Tab 1).
    *   Ma trận phân quyền chi tiết (Tab 2).
*   **Modal/Dialog:** Các hộp thoại popup để thực hiện các thao tác Thêm/Sửa vai trò.

## 4. Các Thành phần Chính (Components)

### 4.1. Tab `Danh sách Vai trò`

#### 4.1.1. Khu vực Hành động

*   **Nút `Thêm vai trò mới`:**
    *   Mở modal/dialog form thêm vai trò mới.
*   **Ô tìm kiếm (Optional):**
    *   Cho phép tìm kiếm nhanh trong danh sách vai trò theo tên vai trò.

#### 4.1.2. Bảng Danh sách Vai trò

Hiển thị dữ liệu dạng bảng, cho phép sắp xếp (sort) theo các cột.

*   **Các cột (Columns):**
    *   `Tên vai trò:` (Hiển thị text, VD: Admin, 課長, 部長, Nhân viên...).
    *   `Mô tả:` (Hiển thị text mô tả ngắn về vai trò).
    *   `Số người dùng:` (Số lượng người dùng đang được gán vai trò này).
    *   `Ngày tạo:` (Thời gian vai trò được tạo).
    *   `Ngày cập nhật:` (Thời gian vai trò được cập nhật gần nhất).
    *   `Thao tác:` Cột chứa các nút hành động:
        *   `Phân quyền`: Chuyển sang tab 2 để cấu hình quyền chi tiết cho vai trò.
        *   `Sửa`: Mở modal/dialog chỉnh sửa thông tin vai trò.
        *   `Xóa`: Mở dialog xác nhận xóa vai trò (chỉ cho phép xóa khi không có người dùng được gán vai trò này).
*   **Sắp xếp (Sorting):** Cho phép click vào tiêu đề cột để sắp xếp.

### 4.2. Tab `Phân quyền Chi tiết`

#### 4.2.1. Khu vực Thông tin Vai trò

*   **Thông tin vai trò đang chỉnh sửa:**
    *   Hiển thị tên vai trò và mô tả ngắn.
    *   Nút `Quay lại`: Quay lại tab Danh sách Vai trò.

#### 4.2.2. Ma trận Phân quyền

Hiển thị dạng ma trận (grid) hoặc cây (tree) các quyền theo module chức năng.

*   **Cấu trúc phân nhóm:**
    *   Nhóm theo Module chức năng (HRM, Margin, Cơ hội, Hợp đồng...).
    *   Trong mỗi module, liệt kê các chức năng/tính năng cụ thể.
    *   Với mỗi chức năng, hiển thị các loại quyền có thể gán (Xem, Thêm, Sửa, Xóa).
*   **Các phần tử UI:**
    *   Checkbox cho từng quyền cụ thể.
    *   Checkbox "Select all" cho mỗi module/chức năng.
    *   Phân nhóm rõ ràng bằng các section, card hoặc khung viền.
*   **Ví dụ phân nhóm:**
    *   **Module: Quản lý Nhân sự (HRM)**
        *   Chức năng: Danh sách Nhân sự
            *   [ ] Xem (tất cả nhân sự)
            *   [ ] Xem (chỉ team mình)
            *   [ ] Thêm mới
            *   [ ] Chỉnh sửa (tất cả)
            *   [ ] Chỉnh sửa (chỉ team mình)
            *   [ ] Export
        *   Chức năng: Quản lý Skills
            *   [ ] Xem danh mục skills
            *   [ ] Thêm/Sửa danh mục skills
            *   ...
    *   **Module: Quản lý Margin**
        *   ...

#### 4.2.3. Khu vực Tác vụ

*   **Nút `Lưu thay đổi`:**
    *   Lưu cấu hình phân quyền đã thiết lập.
*   **Nút `Đặt lại`:**
    *   Đặt lại về trạng thái phân quyền hiện tại (hủy bỏ các thay đổi chưa lưu).
*   **Nút `Mẫu phân quyền` (Optional):**
    *   Cung cấp các mẫu phân quyền định sẵn (VD: "Chỉ xem", "Quản lý Team", "Full quyền"...) để nhanh chóng áp dụng.

### 4.3. Modal/Dialog Forms

#### 4.3.1. Modal Thêm/Sửa Vai trò

*   **Tiêu đề:** "Thêm vai trò mới" hoặc "Chỉnh sửa vai trò".
*   **Các trường nhập liệu:**
    *   `Tên vai trò:` (Bắt buộc, không được trùng).
    *   `Mô tả:` (Mô tả ngắn về vai trò và mục đích sử dụng).
    *   `Vai trò mặc định:` (Checkbox - Có/Không. Vai trò mặc định sẽ được tự động gán cho người dùng mới).
*   **Nút:**
    *   `Lưu`: Lưu thông tin và đóng modal.
    *   `Hủy`: Đóng modal không lưu thay đổi.

#### 4.3.2. Dialog Xác nhận Xóa Vai trò

*   **Tiêu đề:** "Xác nhận xóa vai trò".
*   **Nội dung:** Thông báo xác nhận việc xóa, hiển thị tên vai trò.
*   **Cảnh báo:** Thông báo rằng chỉ có thể xóa vai trò khi không có người dùng nào đang được gán vai trò này.
*   **Nút:**
    *   `Xác nhận`: Thực hiện xóa vai trò.
    *   `Hủy`: Đóng dialog không thực hiện thay đổi.

## 5. Luồng Sự kiện Chính

### 5.1. Tab Danh sách Vai trò

*   **Load Màn hình:**
    *   Hệ thống kiểm tra quyền người dùng (chỉ Admin mới được truy cập).
    *   Truy vấn CSDL lấy danh sách các vai trò hiện có và số lượng người dùng cho mỗi vai trò.
    *   Hiển thị dữ liệu lên bảng.
*   **Click `Thêm vai trò mới`:**
    *   Mở modal Thêm vai trò mới.
    *   Admin nhập thông tin và click `Lưu`.
    *   Hệ thống kiểm tra dữ liệu (validation).
    *   Nếu hợp lệ, lưu thông tin vai trò mới vào CSDL.
    *   Cập nhật lại danh sách và hiển thị thông báo thành công.
*   **Click `Sửa` trong cột Thao tác:**
    *   Mở modal Chỉnh sửa vai trò với thông tin đã được điền sẵn.
    *   Admin cập nhật thông tin và click `Lưu`.
    *   Hệ thống kiểm tra dữ liệu (validation).
    *   Nếu hợp lệ, cập nhật thông tin vai trò trong CSDL.
    *   Cập nhật lại danh sách và hiển thị thông báo thành công.
*   **Click `Xóa` trong cột Thao tác:**
    *   Hệ thống kiểm tra xem có người dùng nào đang được gán vai trò này không.
    *   Nếu có người dùng: Hiển thị thông báo lỗi và không cho phép xóa.
    *   Nếu không có người dùng: Mở dialog xác nhận xóa vai trò.
    *   Admin click `Xác nhận`.
    *   Hệ thống xóa vai trò khỏi CSDL.
    *   Cập nhật lại danh sách và hiển thị thông báo thành công.
*   **Click `Phân quyền` trong cột Thao tác:**
    *   Hệ thống chuyển sang tab Phân quyền Chi tiết.
    *   Truy vấn CSDL lấy thông tin phân quyền hiện tại của vai trò được chọn.
    *   Hiển thị ma trận phân quyền với các checkbox đã được tích/bỏ tích tương ứng.

### 5.2. Tab Phân quyền Chi tiết

*   **Load Tab Phân quyền:**
    *   Hiển thị thông tin vai trò đang được cấu hình.
    *   Truy vấn CSDL lấy danh sách tất cả các quyền trong hệ thống.
    *   Truy vấn CSDL lấy thông tin phân quyền hiện tại của vai trò.
    *   Hiển thị ma trận phân quyền với các checkbox đã được tích/bỏ tích tương ứng.
*   **Thay đổi Cấu hình Quyền:**
    *   Admin tích/bỏ tích các checkbox để cấu hình quyền.
    *   Khi tích/bỏ tích checkbox "Select all" của một module/chức năng, tất cả các quyền con được tích/bỏ tích tương ứng.
*   **Click `Lưu thay đổi`:**
    *   Hệ thống thu thập trạng thái tất cả các checkbox.
    *   Cập nhật thông tin phân quyền vào CSDL.
    *   Hiển thị thông báo lưu thành công.
*   **Click `Đặt lại`:**
    *   Hệ thống tái tạo trạng thái của các checkbox dựa trên dữ liệu hiện tại trong CSDL.
    *   Hủy bỏ tất cả các thay đổi chưa lưu.
*   **Click `Mẫu phân quyền` (nếu có):**
    *   Hiển thị dropdown với các mẫu phân quyền định sẵn.
    *   Admin chọn một mẫu.
    *   Hệ thống cập nhật tự động trạng thái các checkbox theo mẫu đã chọn.
    *   Thay đổi chưa được lưu vào CSDL cho đến khi Admin click `Lưu thay đổi`.
*   **Click `Quay lại`:**
    *   Nếu có thay đổi chưa lưu: Hiển thị dialog xác nhận có muốn lưu thay đổi không.
    *   Nếu không có thay đổi hoặc đã xử lý dialog xác nhận: Quay lại tab Danh sách Vai trò.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Bảo mật:**
    *   Đảm bảo chỉ Admin mới có quyền truy cập màn hình này.
    *   Ngăn chặn việc thay đổi quyền của vai trò Admin thông qua API/hệ thống (để tránh mất quyền quản trị).
*   **Kiểm tra dữ liệu nhập:**
    *   Tên vai trò: Không được trùng, độ dài và ký tự hợp lệ.
    *   Không cho phép xóa vai trò khi có người dùng đang được gán vai trò đó.
    *   Không cho phép xóa các vai trò mặc định của hệ thống (VD: Admin).
*   **Hiệu năng:**
    *   Tối ưu hóa cách hiển thị ma trận phân quyền, đặc biệt khi có nhiều module và quyền.
    *   Cân nhắc phân trang hoặc accordion cho ma trận phân quyền nếu quá lớn.
*   **Giao diện người dùng:**
    *   Thiết kế ma trận phân quyền rõ ràng, dễ hiểu.
    *   Sử dụng màu sắc, indent, và grouping để phân biệt các module, chức năng và quyền.
    *   Cung cấp tooltip hoặc thông tin trợ giúp giải thích ý nghĩa của từng quyền.
*   **Phụ thuộc giữa các quyền:**
    *   Xử lý logic phụ thuộc giữa các quyền (VD: Nếu có quyền Sửa thì mặc định phải có quyền Xem).
    *   Hiển thị cảnh báo hoặc tự động tích các quyền phụ thuộc khi cần.
*   **Log thay đổi:**
    *   Ghi log đầy đủ các thao tác tạo, sửa, xóa vai trò và thay đổi phân quyền.
*   **Tác động hệ thống:**
    *   Thông báo rõ ràng khi thay đổi quyền của một vai trò sẽ ảnh hưởng đến tất cả người dùng đang được gán vai trò đó. 