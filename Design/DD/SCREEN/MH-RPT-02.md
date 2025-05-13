# Mô tả Chi tiết Màn hình: MH-RPT-02 - Xem Báo cáo Chi tiết

**Version Control:**

| Version | Date       | Author         | Changes                                    | Approved By | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :---------- | :-------- |
| 1.0     | 2025-04-28 | Chiến Trần Văn | Initial draft based on requirements        |             | Draft     |

---

## 1. Mục đích Màn hình

Màn hình này cung cấp giao diện để hiển thị chi tiết của một báo cáo cụ thể, cho phép người dùng xem dữ liệu báo cáo dưới dạng bảng, lọc theo các tiêu chí khác nhau và xuất dữ liệu ra các định dạng file phổ biến (Excel/CSV). Màn hình này được thiết kế để linh hoạt, có thể hiển thị nhiều loại báo cáo khác nhau dựa trên ID báo cáo được truyền vào.

## 2. Đối tượng Sử dụng và Phân quyền

*   **Admin:**
    *   Xem *tất cả* các báo cáo chi tiết trong hệ thống.
    *   Sử dụng đầy đủ các bộ lọc và chức năng xuất file.
*   **課長 (General Manager):**
    *   Xem các báo cáo liên quan đến toàn bộ vận hành theo phân quyền.
    *   Sử dụng đầy đủ bộ lọc và chức năng xuất file cho các báo cáo được phép.
*   **部長 (Team Leader):**
    *   Xem các báo cáo liên quan đến team mình quản lý.
    *   Dữ liệu trong báo cáo được lọc theo phạm vi team.
*   **Kế toán:**
    *   Xem các báo cáo tài chính, hợp đồng, doanh thu theo phân quyền.
*   **Sales:**
    *   Xem các báo cáo về cơ hội kinh doanh, KPI, doanh thu theo phân quyền.
*   **Nhân viên (Employee):**
    *   Có thể có quyền xem một số báo cáo cơ bản với dữ liệu được lọc và giới hạn.

## 3. Bố cục Màn hình (Layout Suggestion)

*   **Header:** Hiển thị tên báo cáo, mô tả ngắn, và nút quay lại.
*   **Khu vực Bộ lọc:** Đặt ở phía trên, có thể ẩn/hiện (collapsible) để tiết kiệm không gian.
*   **Khu vực Tác vụ:** Nằm bên cạnh hoặc dưới bộ lọc, chứa các nút chức năng như Export, In, v.v.
*   **Khu vực Hiển thị Dữ liệu:** Chiếm phần lớn diện tích màn hình, hiển thị dữ liệu báo cáo dạng bảng.
*   **Footer:** Hiển thị thông tin tổng hợp/tóm tắt và phân trang (nếu cần).

## 4. Các Thành phần Chính (Components)

### 4.1. Header

*   **Tên báo cáo:** Hiển thị tên đầy đủ của báo cáo (VD: "Báo cáo Margin Nhân sự Tháng 05/2025").
*   **Mô tả ngắn:** 1-2 dòng mô tả mục đích và nội dung của báo cáo.
*   **Nút quay lại:** Cho phép quay lại màn hình `MH-RPT-01` (Danh sách Báo cáo).
*   **Thời gian cập nhật:** Hiển thị thời điểm dữ liệu được cập nhật gần nhất.

### 4.2. Khu vực Bộ lọc

*   **Bộ lọc thời gian:**
    *   Khoảng thời gian: Tháng, Quý, Năm hoặc Từ ngày - Đến ngày (tùy theo loại báo cáo).
    *   Lựa chọn nhanh: Tháng hiện tại, Quý hiện tại, Năm hiện tại, v.v.
*   **Bộ lọc nội dung:** (Thay đổi tùy theo loại báo cáo)
    *   `Team`: Khi xem báo cáo liên quan đến nhân sự/margin.
    *   `Nhân viên`: Lọc theo cá nhân nhân viên cụ thể.
    *   `Khách hàng`: Khi xem báo cáo liên quan đến hợp đồng/cơ hội.
    *   `Trạng thái`: Lọc theo trạng thái (VD: Margin Red/Yellow/Green, Cơ hội theo giai đoạn...).
    *   Các bộ lọc khác tùy thuộc vào loại báo cáo.
*   **Nút:**
    *   `Áp dụng`: Áp dụng các bộ lọc và cập nhật dữ liệu báo cáo.
    *   `Xóa bộ lọc`: Đặt lại tất cả các trường lọc về giá trị mặc định.

### 4.3. Khu vực Tác vụ

*   **Nút `Export`:**
    *   Cho phép xuất dữ liệu báo cáo (đã lọc) ra file Excel hoặc CSV.
    *   Có thể cung cấp các tùy chọn định dạng xuất (VD: Bao gồm tổng hợp hay chỉ dữ liệu chi tiết).
*   **Nút `In`:**
    *   Định dạng báo cáo để in.
*   **Nút `Refresh`:**
    *   Làm mới dữ liệu báo cáo với các bộ lọc hiện tại.

### 4.4. Khu vực Hiển thị Dữ liệu

*   **Bảng dữ liệu chính:**
    *   Hiển thị dữ liệu báo cáo dưới dạng bảng với các cột thay đổi tùy theo loại báo cáo.
    *   Hỗ trợ sắp xếp (sort) khi click vào tiêu đề cột.
    *   Có thể có định dạng màu sắc hoặc biểu tượng để thể hiện trạng thái/cấp độ (VD: màu đỏ/vàng/xanh cho margin).
*   **Tổng hợp / Tóm tắt:**
    *   Hiển thị thông tin tổng hợp ở cuối bảng hoặc trong khu vực riêng (VD: Tổng doanh thu, Margin trung bình...).
*   **Biểu đồ (Optional):**
    *   Một số báo cáo có thể bao gồm biểu đồ trực quan hóa dữ liệu (VD: biểu đồ cột cho doanh thu theo tháng, biểu đồ tròn cho phân bố margin...).
*   **Phân trang:**
    *   Hiển thị các điều khiển để chuyển trang khi báo cáo có nhiều dữ liệu.

## 5. Luồng Sự kiện Chính

*   **Load Màn hình:**
    *   Nhận ID báo cáo từ màn hình `MH-RPT-01`.
    *   Hệ thống kiểm tra quyền người dùng với báo cáo cụ thể.
    *   Tải cấu hình báo cáo (tên, mô tả, cấu trúc, các bộ lọc có thể áp dụng).
    *   Tải dữ liệu báo cáo mặc định (có thể áp dụng bộ lọc mặc định như tháng hiện tại).
    *   Hiển thị dữ liệu trên giao diện.
*   **Thay đổi Bộ lọc & Click `Áp dụng`:**
    *   Hệ thống thực hiện truy vấn mới dựa trên các tiêu chí đã chọn.
    *   Cập nhật dữ liệu trong bảng và tổng hợp.
    *   Nếu có biểu đồ, cập nhật biểu đồ tương ứng.
*   **Click `Xóa bộ lọc`:**
    *   Đặt lại các trường lọc về giá trị mặc định.
    *   Thực hiện truy vấn lại và cập nhật dữ liệu.
*   **Click `Export`:**
    *   Hệ thống thu thập dữ liệu từ báo cáo hiện tại (đã lọc).
    *   Tạo file Excel/CSV với định dạng phù hợp.
    *   Trigger tải file về máy người dùng.
*   **Click `In`:**
    *   Hệ thống chuẩn bị phiên bản báo cáo thân thiện với việc in ấn.
    *   Mở hộp thoại in của trình duyệt hoặc tạo PDF để in.
*   **Click `Refresh`:**
    *   Tải lại dữ liệu báo cáo với các bộ lọc hiện tại.
    *   Cập nhật thời gian cập nhật cuối.
*   **Click vào tiêu đề cột để sắp xếp:**
    *   Hệ thống sắp xếp dữ liệu hiện tại theo cột được chọn (tăng/giảm dần).
    *   Cập nhật hiển thị bảng dữ liệu.
*   **Click vào các link trong báo cáo (nếu có):**
    *   Một số báo cáo có thể có các link để điều hướng đến thông tin chi tiết (VD: từ báo cáo margin có thể click vào tên nhân viên để xem chi tiết).
    *   Hệ thống điều hướng đến màn hình tương ứng với thông tin context.
*   **Click nút quay lại:**
    *   Điều hướng người dùng trở lại màn hình `MH-RPT-01` (Danh sách Báo cáo).

## 6. Các Điểm Cần Lưu ý / Validation

*   **Phân quyền dữ liệu:** Đảm bảo người dùng chỉ thấy dữ liệu mà họ được phép truy cập, ngay cả sau khi áp dụng các bộ lọc khác nhau.
*   **Hiệu năng báo cáo:** Tối ưu hóa truy vấn CSDL đặc biệt với các báo cáo có nhiều dữ liệu hoặc tính toán phức tạp:
    *   Cân nhắc sử dụng caching cho các báo cáo tổng hợp.
    *   Có thể sử dụng các báo cáo được tính toán trước (pre-calculated) cho các báo cáo phức tạp.
    *   Hiển thị indicator "đang tải" khi báo cáo đang được xử lý.
*   **Xuất file:** Đảm bảo định dạng file xuất rõ ràng, dễ đọc và đầy đủ thông tin:
    *   Bao gồm tiêu đề báo cáo, thời gian tạo, các bộ lọc đã áp dụng.
    *   Định dạng số, ngày tháng, tiền tệ phù hợp.
    *   Xử lý trường hợp dữ liệu lớn khi xuất file.
*   **Tương thích trình duyệt:** Đảm bảo các chức năng báo cáo, đặc biệt là xuất file và in ấn, hoạt động tốt trên các trình duyệt phổ biến.
*   **Ghi nhớ bộ lọc:** Cân nhắc lưu trạng thái bộ lọc trong session/localStorage để duy trì khi người dùng quay lại báo cáo.
*   **Độ chính xác dữ liệu:** Hiển thị rõ ràng thời gian cập nhật cuối của dữ liệu để người dùng biết độ "tươi" của báo cáo.
*   **Trải nghiệm người dùng:** Đảm bảo giao diện dễ sử dụng, trực quan, không gây rối với quá nhiều bộ lọc một lúc. 