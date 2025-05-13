# Mô tả Chi tiết Màn hình: MH-MGN-02 - Form Nhập/Import Chi phí

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Gemini (AI)    | Initial draft based on requirements & flow |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện cho Leader (部長) và 課長 để nhập hoặc import dữ liệu chi phí (Cost) hàng tháng cho các nhân viên thuộc phạm vi quản lý của họ. Dữ liệu chi phí này là đầu vào quan trọng để tính toán Margin trong màn hình `MH-MGN-01`.

## 2. Đối tượng Sử dụng và Phân quyền

*   **課長 (General Manager（課長）):**
    *   Có thể chọn `Team` và `Kỳ` (Tháng/Năm) để nhập/import chi phí cho nhân viên trong các team đó.
    *   Có thể nhập liệu thủ công hoặc import file.
*   **部長 (Team Leader):**
    *   Chỉ có thể chọn `Kỳ` (Tháng/Năm) để nhập/import chi phí cho nhân viên *trong team mình quản lý*. Không thấy bộ chọn `Team`.
    *   Có thể nhập liệu thủ công hoặc import file.
*   **Admin/Các vai trò khác:** **KHÔNG** có quyền truy cập/thao tác trên màn hình này (trừ khi có cấu hình đặc biệt để hỗ trợ).

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Khu vực Chọn Kỳ & Team:** Đặt ở trên cùng.
*   **Tab/Phân khu lựa chọn phương thức:**
    *   **Tab 1: Nhập liệu Thủ công:** Hiển thị bảng để nhập trực tiếp.
    *   **Tab 2: Import từ File:** Hiển thị khu vực upload file và hướng dẫn.
*   **Nút Lưu/Import:** Đặt ở vị trí phù hợp tùy theo tab đang chọn.
*   **Khu vực Phản hồi/Kết quả:** Hiển thị thông báo thành công, lỗi hoặc kết quả validation.

## 4. Các Thành phần Chính (Components)

### 4.1. Khu vực Chọn Kỳ & Team

*   **Chọn Kỳ (Bắt buộc):**
    *   Dropdown/Calendar để chọn `Tháng` và `Năm` cần nhập chi phí (VD: Tháng 04 / Năm 2025).
*   **Chọn Team (Chỉ hiển thị cho 課長):**
    *   Dropdown cho phép chọn một `Team` cụ thể để nhập liệu.
*   **Nút `Tải dữ liệu / Chuẩn bị nhập`:** Sau khi chọn Kỳ (và Team nếu có), nút này sẽ:
    *   Nếu chọn Tab "Nhập liệu Thủ công": Tải danh sách nhân viên thuộc Kỳ và Team đã chọn vào bảng bên dưới, hiển thị chi phí đã nhập trước đó (nếu có) để sửa đổi.
    *   Nếu chọn Tab "Import từ File": Không cần thiết, nhưng có thể dùng để kiểm tra nhanh danh sách nhân viên dự kiến có trong file template.

### 4.2. Tab: Nhập liệu Thủ công

*   **Bảng Nhập liệu:**
    *   Hiển thị danh sách nhân viên thuộc Kỳ/Team đã chọn.
    *   **Cột:** `Mã Nhân viên`, `Họ và Tên`, `Chi phí (Cost)` (Ô nhập liệu dạng số), `Ghi chú` (Optional).
    *   Cho phép người dùng nhập hoặc sửa giá trị `Chi phí` cho từng nhân viên.
*   **Nút `Lưu Chi phí`:**
    *   Chức năng: Lưu lại các giá trị chi phí đã nhập/sửa vào CSDL cho Kỳ và Team đã chọn. Cần validation dữ liệu nhập (phải là số, không âm...). Ghi đè lên dữ liệu cũ nếu đã tồn tại cho cùng nhân viên/kỳ.

### 4.3. Tab: Import từ File

*   **Hướng dẫn & Template:**
    *   Hiển thị hướng dẫn định dạng file import (VD: CSV, Excel).
    *   Cung cấp nút/link `Tải file mẫu (Template)`: File mẫu này nên chứa sẵn danh sách `Mã Nhân viên`, `Họ tên` của Team/Kỳ đã chọn (nếu có thể) và các cột cần điền (`Chi phí`, `Ghi chú` - optional).
*   **Khu vực Upload:**
    *   Nút `Chọn file` để người dùng duyệt và chọn file từ máy tính.
    *   Hiển thị tên file đã chọn.
*   **Nút `Import Chi phí`:**
    *   Chức năng: Trigger quá trình upload và xử lý file.
    *   **Validation:** Hệ thống đọc file, kiểm tra định dạng, kiểm tra sự tồn tại của `Mã Nhân viên` trong hệ thống và thuộc Team/Kỳ đang chọn, kiểm tra dữ liệu `Chi phí` (số, không âm...).
    *   **Xử lý:** Nếu validation thành công, cập nhật/ghi đè dữ liệu chi phí vào CSDL. Nếu có lỗi, hiển thị thông báo lỗi chi tiết (VD: Lỗi ở dòng nào, lỗi gì).

### 4.4. Khu vực Phản hồi/Kết quả

*   Hiển thị thông báo sau khi thực hiện Lưu hoặc Import:
    *   `Thành công:` VD: "Đã lưu chi phí thành công cho 15 nhân viên.", "Import thành công 50 bản ghi chi phí."
    *   `Lỗi:` VD: "Lỗi: Dữ liệu chi phí ở dòng 5 không hợp lệ.", "Lỗi: Mã nhân viên 'XYZ' không tìm thấy hoặc không thuộc Team A.", "Import thất bại, vui lòng kiểm tra lại file."

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Kiểm tra quyền (Leader/課長).
    *   Hiển thị bộ chọn Kỳ/Team.
    *   Mặc định có thể chọn Tab "Nhập liệu Thủ công".
*   **Chọn Kỳ (và Team nếu là 課長) -> Click `Tải dữ liệu / Chuẩn bị nhập` (khi ở Tab Nhập liệu):**
    *   Hệ thống truy vấn danh sách nhân viên và chi phí đã có (nếu có) của kỳ/team.
    *   Hiển thị dữ liệu lên Bảng Nhập liệu.
*   **Nhập/Sửa dữ liệu trong Bảng -> Click `Lưu Chi phí`:**
    *   Validation dữ liệu nhập.
    *   Nếu OK -> Lưu vào CSDL.
    *   Hiển thị thông báo thành công/lỗi.
*   **Chuyển sang Tab "Import từ File":** Hiển thị giao diện Import.
*   **Click `Tải file mẫu (Template)`:** Hệ thống tạo và cho phép tải về file template (CSV/Excel).
*   **Click `Chọn file` -> Chọn file -> Click `Import Chi phí`:**
    *   Upload file lên server.
    *   Thực hiện validation file.
    *   Nếu OK -> Xử lý, cập nhật dữ liệu vào CSDL.
    *   Hiển thị thông báo thành công hoặc chi tiết lỗi validation.
*   **Điều hướng:** Có thể có nút "Quay lại Bảng Margin" để về `MH-MGN-01`.

## 6. Các Điểm Cần Lưu ý / Validation

*   **Quyền truy cập:** Đảm bảo đúng Leader/課長 mới vào được và chỉ thao tác được với phạm vi dữ liệu của mình.
*   **Validation Dữ liệu Nhập:** Chi phí phải là số, không âm. Có thể có giới hạn min/max hợp lý nếu cần.
*   **Validation File Import:**
    *   Đúng định dạng (CSV/Excel).
    *   Đúng cấu trúc cột như template.
    *   Mã Nhân viên phải tồn tại và thuộc phạm vi quản lý/Kỳ đã chọn.
    *   Dữ liệu chi phí trong file phải hợp lệ.
*   **Xử lý Ghi đè:** Khi Lưu hoặc Import, dữ liệu mới sẽ ghi đè lên dữ liệu chi phí cũ của cùng nhân viên trong cùng kỳ. Cần làm rõ hành vi này cho người dùng.
*   **Bảo mật File Upload:** Kiểm tra loại file, kích thước file, quét virus nếu cần.
*   **Phản hồi lỗi:** Thông báo lỗi phải rõ ràng, chỉ rõ lỗi ở đâu (dòng nào, cột nào, giá trị nào) để người dùng dễ dàng sửa lại.

## 7. Đề xuất Cải thiện (Suggestions)

*   **Xem lại Lịch sử Nhập/Import:** Lưu lại log ai đã nhập/import chi phí cho kỳ nào, khi nào.
*   **Cho phép Nhập Nhanh:** Có thể cho phép copy-paste từ Excel vào bảng nhập liệu thủ công.
*   **Khóa Dữ liệu:** Sau một thời gian nhất định (VD: sau khi kỳ kế toán đã chốt), có thể khóa việc nhập/sửa chi phí cho các kỳ cũ. 