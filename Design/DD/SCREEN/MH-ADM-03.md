# Mô tả Chi tiết Màn hình: MH-ADM-03 - (Admin) Cấu hình Hệ thống

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Chiến Trần Văn | Initial draft based on requirements        |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện cho quản trị viên (Admin) để cấu hình các tham số chung của hệ thống, bao gồm các danh mục, ngưỡng cảnh báo, thiết lập API và các cài đặt hệ thống khác. Việc tập trung các cấu hình vào một màn hình quản lý giúp dễ dàng điều chỉnh hành vi của hệ thống mà không cần sửa đổi mã nguồn.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem và chỉnh sửa tất cả các cấu hình hệ thống.
    *   Cấu hình các danh mục, ngưỡng cảnh báo và thiết lập API.
    *   Thực hiện thao tác bảo trì hệ thống (nếu có).

Lưu ý: Chỉ Admin mới có quyền truy cập màn hình này. Các vai trò khác trong hệ thống không có quyền truy cập.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Tiêu đề trang:** "Cấu hình Hệ thống" - Nằm ở phía trên cùng.
*   **Menu/Tab Navigation:** Phân chia các nhóm cấu hình thành các tab:
    *   Tab `Danh mục Hệ thống`: Quản lý các danh mục dùng chung.
    *   Tab `Ngưỡng Cảnh báo`: Cấu hình các ngưỡng cảnh báo.
    *   Tab `Kết nối API`: Thiết lập các kết nối API (Hubspot, ...).
    *   Tab `Cài đặt Chung`: Các cấu hình chung khác.
*   **Khu vực Nội dung Chính:** Thay đổi tùy theo tab đang được chọn.
*   **Khu vực Tác vụ:** Các nút hành động chung (Lưu, Đặt lại...) nằm ở cuối mỗi tab.
*   **Thông báo Xác nhận/Kết quả:** Hiển thị kết quả của các thao tác cấu hình.

## 4. Các Thành phần Chính (Components)

### 4.1. Tab `Danh mục Hệ thống`

Quản lý các danh mục dùng chung trong hệ thống. Mỗi danh mục được hiển thị dưới dạng một section riêng biệt.

#### 4.1.1. Danh mục Trạng thái Nhân sự

*   **Tiêu đề section:** "Trạng thái Nhân sự"
*   **Mô tả:** Giải thích ngắn về mục đích của danh mục.
*   **Bảng Danh sách Trạng thái:**
    *   Cột `Mã`: Mã trạng thái (VD: ALLOCATED, BENCH, ...).
    *   Cột `Tên hiển thị`: Tên hiển thị trên giao diện (VD: "Đang tham gia dự án", "Sẵn sàng").
    *   Cột `Mô tả`: Mô tả chi tiết về trạng thái.
    *   Cột `Màu sắc`: Mã màu hoặc chọn màu để hiển thị trạng thái (sử dụng color picker).
    *   Cột `Trạng thái`: Kích hoạt/Vô hiệu hóa.
    *   Cột `Thao tác`: Nút Sửa/Xóa.
*   **Nút `Thêm trạng thái`:** Mở form thêm trạng thái mới.

#### 4.1.2. Danh mục Vị trí Công việc

*   **Tiêu đề section:** "Vị trí Công việc"
*   Tương tự như Danh mục Trạng thái Nhân sự, với các cột phù hợp.

#### 4.1.3. Danh mục Trạng thái Hợp đồng

*   **Tiêu đề section:** "Trạng thái Hợp đồng"
*   Tương tự như các danh mục khác, với các cột phù hợp.

#### 4.1.4. Danh mục Loại Hợp đồng

*   **Tiêu đề section:** "Loại Hợp đồng"
*   Tương tự như các danh mục khác, với các cột phù hợp.

#### 4.1.5. Nút Tác vụ Chung

*   **Nút `Lưu thay đổi`:** Lưu tất cả thay đổi đã thực hiện trên các danh mục.
*   **Nút `Đặt lại`:** Hủy bỏ các thay đổi chưa lưu.

### 4.2. Tab `Ngưỡng Cảnh báo`

Cấu hình các ngưỡng cảnh báo sử dụng trong hệ thống, được phân nhóm theo module chức năng.

#### 4.2.1. Ngưỡng Margin

*   **Tiêu đề section:** "Ngưỡng Cảnh báo Margin"
*   **Form cấu hình:**
    *   `Ngưỡng Đỏ (Red)`: Slider hoặc ô nhập số (%) cho margin <= X%.
    *   `Ngưỡng Vàng (Yellow)`: Slider hoặc ô nhập số (%) cho X% < margin <= Y%.
    *   `Ngưỡng Xanh (Green)`: Tự động tính (margin > Y%).
    *   Hiển thị trực quan các ngưỡng bằng thanh màu hoặc biểu đồ.
*   **Mô tả:** Giải thích cách áp dụng ngưỡng trong hệ thống.

#### 4.2.2. Ngưỡng Follow-up Cơ hội

*   **Tiêu đề section:** "Ngưỡng Cảnh báo Follow-up Cơ hội"
*   **Form cấu hình:**
    *   `Ngưỡng Đỏ (Red)`: Slider hoặc ô nhập số (ngày) cho thời gian không tương tác > X ngày.
    *   `Ngưỡng Vàng (Yellow)`: Slider hoặc ô nhập số (ngày) cho Y ngày < thời gian không tương tác <= X ngày.
    *   `Ngưỡng Xanh (Green)`: Tự động tính (thời gian không tương tác <= Y ngày).
*   **Mô tả:** Giải thích cách áp dụng ngưỡng trong module Cơ hội.

#### 4.2.3. Ngưỡng Cảnh báo Thanh toán

*   **Tiêu đề section:** "Ngưỡng Cảnh báo Thanh toán"
*   **Form cấu hình:**
    *   `Cảnh báo trước hạn`: Ô nhập số (ngày) - Cảnh báo trước khi đến hạn thanh toán X ngày.
    *   `Cảnh báo quá hạn`: Ô nhập số (ngày) - Mức độ cảnh báo dựa trên số ngày quá hạn.
*   **Mô tả:** Giải thích cách áp dụng ngưỡng trong hệ thống.

#### 4.2.4. Nút Tác vụ

*   **Nút `Lưu cấu hình`:** Lưu tất cả thay đổi đã thực hiện.
*   **Nút `Đặt lại mặc định`:** Đặt lại các ngưỡng về giá trị mặc định được đề xuất.

### 4.3. Tab `Kết nối API`

Thiết lập và quản lý các kết nối API với hệ thống bên ngoài.

#### 4.3.1. Kết nối Hubspot

*   **Tiêu đề section:** "Cấu hình Kết nối Hubspot"
*   **Form cấu hình:**
    *   `API Key`: Ô nhập text (masked), với nút hiện/ẩn.
    *   `Domain/Portal ID`: Ô nhập text.
    *   `Lịch đồng bộ`: Cấu hình tần suất đồng bộ tự động (dropdown: Mỗi giờ, Mỗi 3 giờ, Mỗi ngày...).
    *   `Phạm vi đồng bộ`: Chọn các đối tượng cần đồng bộ (Cơ hội, Khách hàng...).
*   **Trạng thái kết nối:** Hiển thị trạng thái kết nối hiện tại (Đã kết nối/Chưa kết nối/Lỗi).
*   **Nút `Kiểm tra kết nối`:** Thực hiện kiểm tra kết nối với thông tin đã cấu hình.
*   **Nút `Đồng bộ ngay`:** Kích hoạt đồng bộ thủ công.
*   **Log đồng bộ gần nhất:** Hiển thị thời gian và kết quả đồng bộ gần nhất.

#### 4.3.2. Kết nối Email (Optional)

*   **Tiêu đề section:** "Cấu hình Email Thông báo"
*   **Form cấu hình:**
    *   `SMTP Server`: Ô nhập text.
    *   `Port`: Ô nhập số.
    *   `Tài khoản email`: Ô nhập text.
    *   `Mật khẩu`: Ô nhập password (masked).
    *   `Email gửi đi`: Địa chỉ email hiển thị khi gửi thông báo.
    *   `Bật/Tắt thông báo email`: Toggle kích hoạt tính năng gửi email.
*   **Nút `Kiểm tra kết nối`:** Gửi email test để kiểm tra kết nối.

#### 4.3.3. Kết nối Khác (Optional)

*   Các kết nối API khác nếu cần, với format tương tự.

#### 4.3.4. Nút Tác vụ

*   **Nút `Lưu cấu hình`:** Lưu tất cả thay đổi đã thực hiện.
*   **Nút `Đặt lại`:** Hủy bỏ các thay đổi chưa lưu.

### 4.4. Tab `Cài đặt Chung`

Các cấu hình chung khác của hệ thống.

#### 4.4.1. Cài đặt Hiển thị

*   **Tiêu đề section:** "Cài đặt Hiển thị"
*   **Form cấu hình:**
    *   `Số bản ghi trên trang`: Dropdown số lượng (10, 20, 50, 100).
    *   `Timezone`: Chọn múi giờ mặc định.
    *   `Định dạng ngày`: Chọn định dạng hiển thị ngày tháng (DD/MM/YYYY, MM/DD/YYYY...).
    *   `Định dạng số/tiền tệ`: Chọn định dạng hiển thị số và tiền tệ.

#### 4.4.2. Cài đặt Hệ thống

*   **Tiêu đề section:** "Cài đặt Hệ thống"
*   **Form cấu hình:**
    *   `Thời gian timeout session`: Ô nhập số (phút).
    *   `Số lần đăng nhập sai tối đa`: Ô nhập số.
    *   `Thời gian khóa tài khoản`: Ô nhập số (phút) - sau khi đăng nhập sai quá số lần cho phép.
    *   `Độ phức tạp mật khẩu`: Checkbox các yêu cầu (ký tự hoa/thường, số, ký tự đặc biệt...).
    *   `Thời hạn mật khẩu`: Ô nhập số (ngày) - yêu cầu đổi mật khẩu sau X ngày.

#### 4.4.3. Cài đặt Thông báo

*   **Tiêu đề section:** "Cài đặt Thông báo"
*   **Form cấu hình:**
    *   `Bật/Tắt thông báo trong hệ thống`: Toggle.
    *   `Tự động đánh dấu đã đọc sau`: Dropdown (Ngay lập tức, 1 phút, 5 phút, Không bao giờ).
    *   `Lưu thông báo trong`: Ô nhập số (ngày) - Thời gian lưu trữ thông báo.
    *   Checkbox cho từng loại thông báo: Cơ hội mới, Nhân sự sắp hết dự án, Thanh toán sắp đến hạn...

#### 4.4.4. Nút Tác vụ

*   **Nút `Lưu cấu hình`:** Lưu tất cả thay đổi đã thực hiện.
*   **Nút `Đặt lại mặc định`:** Đặt lại các cài đặt về giá trị mặc định.

## 5. Luồng Sự kiện Chính

### 5.1. Chung cho Tất cả Tab

*   **Load Màn hình:**
    *   Hệ thống kiểm tra quyền người dùng (chỉ Admin mới được truy cập).
    *   Hiển thị tab mặc định (VD: Danh mục Hệ thống).
    *   Truy vấn CSDL lấy dữ liệu cấu hình hiện tại.
    *   Hiển thị dữ liệu lên các form tương ứng.
*   **Chuyển Tab:**
    *   Khi Admin click vào một tab khác, hệ thống kiểm tra xem có thay đổi chưa lưu không.
    *   Nếu có, hiển thị dialog xác nhận có muốn lưu thay đổi trước khi chuyển tab.
    *   Nếu Admin xác nhận lưu, thực hiện lưu thay đổi rồi chuyển tab.
    *   Nếu Admin chọn không lưu, hủy bỏ thay đổi và chuyển tab.
    *   Nếu không có thay đổi, chuyển trực tiếp sang tab mới.
    *   Truy vấn CSDL lấy dữ liệu cấu hình cho tab mới và hiển thị.

### 5.2. Tab Danh mục Hệ thống

*   **Thêm mục danh mục mới:**
    *   Admin click nút `Thêm` trong một danh mục cụ thể.
    *   Hệ thống hiển thị form thêm mới (có thể là hàng mới trong bảng hoặc modal).
    *   Admin nhập thông tin và xác nhận.
    *   Hệ thống kiểm tra dữ liệu (validation).
    *   Nếu hợp lệ, thêm mục mới vào danh sách tạm thời (chưa lưu vào CSDL).
*   **Sửa mục danh mục:**
    *   Admin click nút `Sửa` trong một mục danh mục.
    *   Hệ thống hiển thị form chỉnh sửa (có thể là chế độ edit inline hoặc modal).
    *   Admin cập nhật thông tin và xác nhận.
    *   Hệ thống cập nhật dữ liệu trong danh sách tạm thời.
*   **Xóa mục danh mục:**
    *   Admin click nút `Xóa` trong một mục danh mục.
    *   Hệ thống hiển thị dialog xác nhận xóa.
    *   Nếu Admin xác nhận, hệ thống kiểm tra xem mục này có đang được sử dụng không.
    *   Nếu đang được sử dụng, hiển thị thông báo lỗi và không cho phép xóa.
    *   Nếu không được sử dụng, đánh dấu mục này để xóa (chưa thực sự xóa khỏi CSDL).
*   **Lưu thay đổi danh mục:**
    *   Admin click nút `Lưu thay đổi` sau khi thực hiện các thao tác thêm/sửa/xóa.
    *   Hệ thống thực hiện lưu tất cả thay đổi vào CSDL.
    *   Hiển thị thông báo kết quả (thành công/thất bại).

### 5.3. Tab Ngưỡng Cảnh báo

*   **Chỉnh sửa ngưỡng:**
    *   Admin điều chỉnh các giá trị ngưỡng bằng slider hoặc nhập số.
    *   Giao diện cập nhật trực quan (VD: thanh màu thay đổi) theo giá trị mới.
*   **Đặt lại mặc định:**
    *   Admin click nút `Đặt lại mặc định`.
    *   Hệ thống hiển thị dialog xác nhận.
    *   Nếu Admin xác nhận, hệ thống đặt lại tất cả giá trị ngưỡng về giá trị mặc định được đề xuất.
*   **Lưu cấu hình ngưỡng:**
    *   Admin click nút `Lưu cấu hình` sau khi điều chỉnh các ngưỡng.
    *   Hệ thống kiểm tra tính hợp lệ của các giá trị (VD: ngưỡng Yellow phải nhỏ hơn ngưỡng Red).
    *   Nếu hợp lệ, lưu cấu hình vào CSDL và hiển thị thông báo thành công.
    *   Nếu không hợp lệ, hiển thị thông báo lỗi và yêu cầu điều chỉnh.

### 5.4. Tab Kết nối API

*   **Cấu hình kết nối Hubspot:**
    *   Admin nhập/cập nhật thông tin kết nối (API Key, Domain...).
    *   Admin click nút `Kiểm tra kết nối`.
    *   Hệ thống thực hiện kiểm tra kết nối với Hubspot.
    *   Hiển thị kết quả kiểm tra (thành công/thất bại) và thông tin chi tiết nếu có lỗi.
*   **Đồng bộ thủ công:**
    *   Admin click nút `Đồng bộ ngay`.
    *   Hệ thống hiển thị xác nhận và thông báo quá trình có thể mất thời gian.
    *   Nếu Admin xác nhận, hệ thống thực hiện đồng bộ dữ liệu từ Hubspot ngay lập tức.
    *   Hiển thị kết quả đồng bộ sau khi hoàn tất.
*   **Lưu cấu hình API:**
    *   Admin click nút `Lưu cấu hình` sau khi cập nhật các thông tin kết nối.
    *   Hệ thống lưu cấu hình vào CSDL và cập nhật lịch đồng bộ nếu có thay đổi.
    *   Hiển thị thông báo kết quả.

### 5.5. Tab Cài đặt Chung

*   **Cập nhật cài đặt:**
    *   Admin thay đổi các cài đặt thông qua form.
    *   Admin click nút `Lưu cấu hình`.
    *   Hệ thống kiểm tra tính hợp lệ của dữ liệu.
    *   Nếu hợp lệ, lưu cấu hình vào CSDL và hiển thị thông báo thành công.
    *   Nếu không hợp lệ, hiển thị thông báo lỗi và yêu cầu điều chỉnh.
*   **Đặt lại mặc định:**
    *   Admin click nút `Đặt lại mặc định`.
    *   Hệ thống hiển thị dialog xác nhận.
    *   Nếu Admin xác nhận, hệ thống đặt lại tất cả cài đặt trong tab về giá trị mặc định.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Bảo mật:**
    *   Đảm bảo chỉ Admin mới có quyền truy cập màn hình này.
    *   Mã hóa thông tin nhạy cảm như API Key, mật khẩu SMTP khi lưu trong CSDL.
    *   Ghi log đầy đủ các thao tác thay đổi cấu hình để kiểm tra sau này.
*   **Kiểm tra dữ liệu nhập:**
    *   Kiểm tra tính hợp lệ của các giá trị ngưỡng (VD: ngưỡng Yellow phải nằm giữa Green và Red).
    *   Đảm bảo các giá trị số nằm trong khoảng cho phép.
    *   Kiểm tra định dạng của các trường đặc biệt (Email, URL, API Key...).
*   **Tác động hệ thống:**
    *   Cảnh báo Admin về tác động của việc thay đổi một số cấu hình quan trọng (VD: thay đổi API Key sẽ yêu cầu đồng bộ lại dữ liệu).
    *   Có cơ chế để Admin có thể dễ dàng quay lại cấu hình trước đó nếu thay đổi gây ra vấn đề.
*   **Xử lý xung đột:**
    *   Xử lý trường hợp nhiều Admin cùng truy cập và sửa đổi cấu hình (VD: khóa chỉnh sửa, hiển thị cảnh báo).
*   **Hiệu năng:**
    *   Tối ưu hóa việc tải và lưu cấu hình, đặc biệt với danh mục lớn.
    *   Cân nhắc caching dữ liệu cấu hình để giảm tải cho CSDL.
*   **Giao diện người dùng:**
    *   Thiết kế trực quan, dễ sử dụng dù có nhiều tham số cấu hình.
    *   Nhóm các cấu hình liên quan với nhau.
    *   Cung cấp mô tả rõ ràng cho từng cài đặt.
*   **Xử lý lỗi:**
    *   Hiển thị thông báo lỗi rõ ràng, chi tiết khi có vấn đề (đặc biệt với kết nối API).
    *   Không cho phép xóa các mục danh mục đang được sử dụng trong hệ thống. 