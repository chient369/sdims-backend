# Mô tả Chi tiết Màn hình: MH-DSH-01 - Dashboard Tổng quan

**Version Control:**

| Version | Date       | Author         | Changes                                                     | Approved By | Status    |
| :------ | :--------- | :------------- | :---------------------------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Gemini (AI)    | Initial draft based on requirements & flow                  |             | Draft     |
| 1.1     | 2025-04-28 | Gemini (AI)    | Incorporated suggestions into main description sections |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình Dashboard là điểm truy cập chính sau khi người dùng đăng nhập thành công. Mục tiêu là cung cấp một cái nhìn tổng quan, nhanh chóng về các chỉ số và thông tin hoạt động quan trọng của bộ phận, đồng thời là điểm điều hướng chính đến các module chức năng khác.

## 2. Đối tượng Sử dụng và Phân quyền

*   Tất cả người dùng đã đăng nhập đều có thể truy cập màn hình này.
*   Tuy nhiên, **dữ liệu hiển thị trên các widget, bố cục mặc định, và khả năng truy cập các menu điều hướng sẽ được cá nhân hóa và phụ thuộc vào vai trò và quyền hạn của người dùng**:
    *   **Admin:** Thấy toàn bộ widget, truy cập mọi menu. Layout mặc định có thể bao gồm các chỉ số hệ thống tổng quan.
    *   **Trưởng bộ phận:** Thấy toàn bộ widget, truy cập mọi menu. Layout tương tự Admin.
    *   **Team Leader:** Thấy widget liên quan đến team mình (Nhân sự, Margin team), widget Cơ hội/Hợp đồng được assign. Truy cập menu Nhân sự, Cơ hội, Hợp đồng, Báo cáo (có thể lọc theo team). Layout mặc định tập trung vào quản lý team.
    *   **Sales:** Thấy widget Cơ hội, Hợp đồng, KPI của mình. Truy cập menu Cơ hội, Hợp đồng, Báo cáo (lọc theo sales). Layout mặc định tập trung vào hoạt động kinh doanh.
    *   **Nhân viên (Member):** Thấy các widget thông tin chung (nếu có), widget liên quan đến bản thân (VD: dự án đang tham gia). Truy cập menu Nhân sự (chỉ xem/sửa thông tin cá nhân). Layout đơn giản.
    *   **Kế toán:** Thấy widget liên quan đến Hợp đồng/Công nợ. Truy cập menu Hợp đồng. Layout tập trung vào tài chính.

## 3. Bố cục Màn hình (Layout Suggestion)

Màn hình nên được chia thành các khu vực chính:

*   **Header:** Chứa logo công ty, tên hệ thống, thông tin người dùng đăng nhập (tên, avatar), nút Đăng xuất.
*   **Sidebar (Menu điều hướng chính):** Chứa các link/menu dẫn đến các module chức năng chính. Menu sẽ hiển thị/ẩn dựa trên quyền người dùng.
*   **Khu vực Bộ lọc Toàn cục (Optional but Recommended):** Có thể đặt phía trên khu vực widget, cho phép người dùng chọn khoảng thời gian (Tuần/Tháng/Quý/Năm) áp dụng chung cho nhiều widget.
*   **Khu vực Nội dung Chính (Dashboard Widgets):** Khu vực lớn nhất, hiển thị các widget thông tin. Bố cục mặc định được cá nhân hóa theo vai trò người dùng. Người dùng (đặc biệt là Admin/TP/Leader) nên có **khả năng chọn ẩn/hiện các widget** để tùy chỉnh giao diện.

### 3.1. Chi tiết Sidebar Menu (Dựa trên ScreenBD.md)

Các mục menu chính dự kiến trong Sidebar và màn hình đích tương ứng:

*   **Nhân sự:**
    *   **Mục đích:** Truy cập module quản lý thông tin nhân viên.
    *   **Điều hướng tới:** `MH-HRM-01: Danh sách Nhân sự`.
    *   **Hiển thị cho:** Hầu hết các vai trò (Admin, TP, Leader, Member), quyền truy cập chi tiết bên trong module sẽ khác nhau.
*   **Margin:**
    *   **Mục đích:** Truy cập module quản lý hiệu suất và margin của nhân sự.
    *   **Điều hướng tới:** `MH-MGN-01: Bảng Margin Nhân sự`.
    *   **Hiển thị cho:** Chỉ Admin, TP, Leader (theo yêu cầu phân quyền chặt chẽ).
*   **Cơ hội:**
    *   **Mục đích:** Truy cập module quản lý cơ hội kinh doanh (từ Hubspot).
    *   **Điều hướng tới:** `MH-OPP-01: Danh sách Cơ hội Kinh doanh`.
    *   **Hiển thị cho:** Admin, TP, Leader, Sales.
*   **Hợp đồng:**
    *   **Mục đích:** Truy cập module quản lý thông tin hợp đồng và doanh thu.
    *   **Điều hướng tới:** `MH-CTR-01: Danh sách Hợp đồng`.
    *   **Hiển thị cho:** Admin, TP, Leader, Sales, Kế toán.
*   **Báo cáo:**
    *   **Mục đích:** Truy cập khu vực xem các báo cáo tổng hợp.
    *   **Điều hướng tới:** `MH-RPT-01: Danh sách Báo cáo`.
    *   **Hiển thị cho:** Admin, TP, Leader, Sales (dữ liệu báo cáo sẽ được lọc theo quyền).
*   **Quản trị:**
    *   **Mục đích:** Truy cập các chức năng quản trị hệ thống.
    *   **Điều hướng tới:** Có thể là một menu con hoặc màn hình tổng quan Admin, dẫn tới các màn hình như `MH-ADM-01` (User), `MH-ADM-02` (Role), `MH-ADM-03` (Config), `MH-ADM-04` (Log).
    *   **Hiển thị cho:** Chỉ Admin.

## 4. Các Thành phần Chính (Widgets)

Dưới đây là danh sách các widget dự kiến, dựa trên yêu cầu và mục tiêu. **Cần xác định rõ widget nào hiển thị cho vai trò nào.**

| ID Widget    | Tên Widget Gợi ý                      | Mô tả Hiển thị                                                                                                                                        | Dữ liệu Liên quan                                                                    | Vai trò Thấy (Dự kiến)       |
| :----------- | :------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- | :-------------------------- |
| **W-HRM-01** | **Nhân sự Sẵn sàng (Bench)**          | Số lượng nhân viên đang ở trạng thái `Available` / `Bench`. Có thể click để xem danh sách.                                                              | Dữ liệu từ Module HRM (Trạng thái NV)                                               | Admin, TP, Leader           |
| **W-HRM-02** | **Nhân sự Sắp hết Dự án**           | Số lượng nhân viên đang ở trạng thái `Ending Soon`. Có thể click để xem danh sách.                                                                  | Dữ liệu từ Module HRM (Trạng thái NV, Ngày kết thúc dự kiến)                        | Admin, TP, Leader           |
| **W-HRM-03** | **Tỷ lệ Sử dụng Nguồn lực (%)**     | Biểu đồ (Gauge/Donut) hiển thị % Utilization Rate trung bình (theo bộ lọc thời gian toàn cục hoặc mặc định).                                           | Tính toán từ Module HRM (Phân bổ dự án)                                              | Admin, TP, Leader           |
| **W-MGN-01** | **Phân bổ Margin (Team/Bộ phận)**   | Biểu đồ tròn thể hiện tỷ lệ % nhân viên theo trạng thái Margin (Red/Yellow/Green). Có thể lọc theo Team. Cho phép **drill-down** (VD: click vào phần Red -> popup list). | Dữ liệu từ Module Margin (Trạng thái Margin NV)                                     | Admin, TP, Leader           |
| **W-OPP-01** | **Cơ hội Mới**                       | Số lượng cơ hội mới được tạo/đồng bộ (theo bộ lọc thời gian toàn cục). Click để xem danh sách.                                                         | Dữ liệu từ Module Opportunity (Ngày tạo)                                             | Admin, TP, Leader, Sales    |
| **W-OPP-02** | **Cơ hội Cần Theo dõi (Red/Yellow)** | Số lượng cơ hội đang ở trạng thái Follow-up `Red` hoặc `Yellow`. Click để xem danh sách (lọc tương ứng).                                                | Dữ liệu từ Module Opportunity (Trạng thái Follow-up)                               | Admin, TP, Leader, Sales    |
| **W-OPP-03** | **Phễu Bán hàng (Tổng quan)**        | Biểu đồ cột/phễu hiển thị số lượng hoặc giá trị cơ hội theo từng Deal Stage.                                                                           | Dữ liệu từ Module Opportunity (Deal Stage)                                         | Admin, TP, Leader, Sales    |
| **W-CTR-01** | **Hợp đồng Mới Ký**                 | Số lượng hoặc Tổng giá trị hợp đồng mới ký (theo bộ lọc thời gian toàn cục). Click để xem danh sách.                                                  | Dữ liệu từ Module Contract (Ngày ký)                                                 | Admin, TP, Leader, Sales    |
| **W-CTR-02** | **Doanh thu (vs KPI)**              | Biểu đồ cột/Gauge hiển thị Doanh thu thực tế so với KPI (theo bộ lọc thời gian, của cá nhân Sales hoặc tổng).                                        | Dữ liệu từ Module Contract (Actual Revenue, KPI)                                   | Admin, TP, Leader, Sales    |
| **W-CTR-03** | **Công nợ Quá hạn**                 | Số lượng hoặc Tổng giá trị các khoản thanh toán đang ở trạng thái `Quá hạn`. Click để xem chi tiết (drill-down).                                        | Dữ liệu từ Module Contract (Trạng thái thanh toán)                                | Admin, TP, Leader, Kế toán |
| **W-GEN-01** | **Thông báo/Cảnh báo Quan trọng**    | Khu vực **nổi bật** hiển thị các thông báo/cảnh báo (VD: NV margin đỏ, HĐ sắp hết hạn...). Cần có cơ chế **đánh dấu đã đọc/xử lý**.                   | Tổng hợp từ các module khác                                                          | Tất cả                    |

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:** Hệ thống lấy dữ liệu tổng hợp (theo bộ lọc thời gian mặc định/đã lưu nếu có) dựa trên quyền của người dùng và hiển thị lên các widget/layout tương ứng.
*   **Thay đổi Bộ lọc Toàn cục:** Người dùng chọn khoảng thời gian mới -> Hệ thống load lại dữ liệu cho các widget bị ảnh hưởng.
*   **Click Menu Điều hướng:** Chuyển hướng người dùng đến màn hình danh sách của module tương ứng. Kiểm tra quyền truy cập.
*   **Click vào Widget:**
    *   Hành vi mặc định: Điều hướng đến màn hình danh sách liên quan, với bộ lọc đã được áp dụng sẵn (VD: Click W-HRM-01 -> `MH-HRM-01` lọc theo trạng thái 'Bench').
    *   **(Drill-down)** Hành vi nâng cao cho một số widget: Hiển thị popup/modal với danh sách chi tiết hơn thay vì điều hướng (VD: Click phần "Red" của W-MGN-01 -> Popup danh sách NV Margin Red).
*   **Click Ẩn/Hiện Widget:** (Nếu có quyền tùy chỉnh) Hệ thống lưu trạng thái hiển thị widget cho người dùng.
*   **Click Đăng xuất:** Kết thúc phiên làm việc và chuyển hướng về màn hình Đăng nhập (`MH-AUTH-01`).

## 6. Các Điểm Cần Lưu ý / Validation

*   Dữ liệu trên Dashboard cần được cập nhật gần như real-time hoặc có cơ chế refresh định kỳ/thủ công. **Cần tối ưu hiệu năng truy vấn và xem xét sử dụng caching** do Dashboard tổng hợp nhiều nguồn dữ liệu.
*   Cần xử lý trường hợp không có dữ liệu cho một widget nào đó (hiển thị thông báo "Không có dữ liệu" thay vì lỗi).
*   Kiểm tra quyền truy cập chặt chẽ trước khi hiển thị widget, dữ liệu trong widget, hoặc cho phép điều hướng/thao tác.
