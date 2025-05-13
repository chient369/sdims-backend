# Bảng Ma trận Phân quyền CRUD theo Vai trò

**Tài liệu:** Định nghĩa quyền Tạo (Create), Đọc (Read), Cập nhật (Update), Xóa (Delete) cho các vai trò người dùng khác nhau đối với các chức năng/tài nguyên chính của hệ thống.

**Tham chiếu:** Dựa trên các yêu cầu chức năng được định nghĩa trong `BD/FunctionDesign/FunctionList.md`.

**Chú thích:**
*   **C:** Create (Tạo mới)
*   **R:** Read (Xem)
*   **U:** Update (Cập nhật)
*   **D:** Delete (Xóa - thường là xóa logic)
*   **-:** Không có quyền
*   **(Own):** Chỉ trên dữ liệu của bản thân
*   **(Team):** Chỉ trên dữ liệu của thành viên trong nhóm mình quản lý
*   **(Assigned):** Chỉ trên dữ liệu được phân công cho mình
*   **(All):** Trên tất cả dữ liệu liên quan
*   **(Evaluate):** Quyền đánh giá (ví dụ: skill)
*   **(Note):** Quyền thêm ghi chú
*   **(Basic):** Chỉ thông tin cơ bản

| Chức năng / Tài nguyên                     | ID Tham chiếu       | Admin      | Division Manager | 部長 (Leader) | Sales        | Nhân viên (Member) |
| :----------------------------------------- | :----------------- | :--------- | :-------------- | :----------- | :----------- | :----------------- |
| **1. Quản lý Nhân sự (HRM)**              |                    |            |                 |              |              |                    |
| Hồ sơ Nhân sự (Thông tin cơ bản/tổ chức)   | F-1.1, F-1.3       | -          | CRUD (All)      | RU (Team)    | R (Basic)    | RU (Own)           |
| Import/Export Nhân sự                     | F-1.4              | -          | CRUD            | -            | -            | -                  |
| Danh mục Skills                           | F-1.5              | -          | CRUD            | R            | -            | -                  |
| Profile Skills Nhân viên                  | F-1.6, F-1.7       | -          | CRUD (All)      | R (Team)     | -            | RU (Own)           |
| Đánh giá Skills Nhân viên                 | F-1.6              | -          | U (Evaluate)    | U (Evaluate) | -            | -                  |
| Gợi ý Nhân sự phù hợp (Qua AI)            | F-1.8              | -          | R               | R            | -            | -                  |
| Trạng thái & Phân bổ Dự án                | F-1.9, F-1.10      | -          | CRUD (All)      | RU (Team)    | -            | R (Own)            |
| Lịch sử Dự án Nhân viên                   | F-1.11             | -          | R (All)         | R (Team)     | -            | R (Own)            |
| Báo cáo Utilization                       | F-1.12             | -          | R (All)         | R (Team)     | -            | -                  |
| Cảnh báo Nhân sự sắp hết dự án            | F-1.13             | -          | R (All)         | R (Team)     | -            | -                  |
| **2. Quản lý Margin (Phân quyền chặt)**    |                    |            |                 |              |              |                    |
| Chi phí Nhân sự                           | F-2.1              | -          | CRUD (All)      | R (Team)     | -            | -                  |
| Doanh thu Nhân sự (Tính toán tự động)      | F-2.2              | -          | R (All)         | R (Team)     | -            | -                  |
| Margin Nhân sự (Tính toán/Xem chi tiết)   | F-2.3, F-2.4, F-2.7| -          | R (All)         | R (Team)     | -            | -                  |
| Tổng hợp Margin Team/Bộ phận              | F-2.5              | -          | R (All)         | R (Team)     | -            | -                  |
| Cảnh báo Margin (Tự động/Xem)            | F-2.6              | -          | R (All)         | R (Team)     | -            | -                  |
| Thông báo Margin thấp (Optional)          | F-2.8              | -          | R (Config)      | R (Team)     | -            | -                  |
| **3. Quản lý Cơ hội Kinh doanh**         |                    |            |                 |              |              |                    |
| Đồng bộ/Log Hubspot                      | F-3.1, F-3.2       | -          | R (Config)      | R (All)      | R (All)      | -                  |
| Xem/Tìm kiếm Cơ hội                     | F-3.8              | -          | R (All)         | R (All)      | R (All)      | -                  |
| Assign Leader vào Cơ hội                 | F-3.3              | -          | U (All)         | -            | U (All)      | -                  |
| Ghi chú/Log Hoạt động Cơ hội             | F-3.4              | -          | U (All)         | U (Assigned) | U (All)      | -                  |
| Cập nhật Ngày tương tác cuối (Tự động)    | F-3.5              | -          | -               | -            | -            | -                  |
| Trạng thái Follow-up (Tự động/Xem)      | F-3.6              | -          | R (All)         | R (All)      | R (All)      | -                  |
| Đánh dấu Ưu tiên Onsite                  | F-3.7              | -          | U (All)         | U (Assigned) | U (All)      | -                  |
| Thông báo liên quan Cơ hội (Tự động)    | F-3.9              | -          | R (Config)      | R (Assigned) | R (All)      | -                  |
| **4. Quản lý Hợp đồng & Doanh thu**    |                    |            |                 |              |              |                    |
| Thông tin Hợp đồng                      | F-4.1              | -          | CRUD (All)      | R (Assigned) | RU (Own)     | -      |
| Liên kết HĐ với Cơ hội/Nhân sự         | F-4.2              | -          | U (All)         | U (Assigned) | U (Own)      | -                  |
| Upload/Đính kèm File Hợp đồng           | F-4.3              | -          | U (All)         | -            | U (Own)      | -                  |
| Điều khoản Thanh toán                     | F-4.4              | -          | CRUD (All)      | R (Assigned) | RU (Own)     | -                  |
| Cập nhật Trạng thái Thu tiền              | F-4.5              | -          | U (All)         | -            | U (All)      | -                  |
| Cảnh báo Thanh toán (Tự động)           | F-4.6              | -          | R (Config)      | R (Assigned) | R (Own)      | -                  |
| Báo cáo Công nợ                         | F-4.7              | -          | R (All)         | -            | R (Own)      | -                  |
| Thiết lập KPI Doanh thu                 | F-4.8              | -          | CRUD            | -            | R (Own)      | -                  |
| Doanh thu Thực tế (Tự động/Xem)        | F-4.9, F-4.10      | -          | R (All)         | R (Team)     | R (Own)      | -                  |
| Báo cáo Tổng hợp Doanh thu             | F-4.11             | -          | R (All)         | R (Team)     | R (Own)      | -                  |
| **5. Dashboard & Báo cáo**             |                    |            |                 |              |              |                    |
| Dashboard Tổng hợp                       | F-5.1, F-5.2       | -          | R (All)         | R (Team)     | R (Own Opps) | -    |
| Báo cáo Chi tiết                         | F-5.3, F-5.4       | -          | R (All)         | R (Team)     | R (Own)      | -            |
| Xuất Báo cáo ra File                   | F-5.5              | -          | C               | C            | C            | -                |
| **6. Quản trị Hệ thống (Admin)**        |                    |            |                 |              |              |                    |
| Quản lý Người dùng                      | F-6.1              | CRUD       | -               | -            | -            | -                  |
| Quản lý Vai trò & Phân quyền            | F-6.2              | CRUD       | -               | -            | -            | -                  |
| Cấu hình Danh mục Hệ thống             | F-6.3              | CRUD       | R               | R            | -            | -                  |
| Cấu hình Ngưỡng Cảnh báo               | F-6.4              | CRUD       | R               | R            | -            | -                  |
| Quản lý Kết nối API (Hubspot)         | F-6.5              | CRUD       | R               | -            | -            | -                  |
| Xem Log Hệ thống                         | F-6.6              | R (All)    | R (Limited?)    | -            | -            | -                  |

**Refrence:** [Function List](./FunctionDesign/FunctionList.md)
**Lưu ý:**
*   Quyền thực tế có thể cần điều chỉnh chi tiết hơn trong quá trình triển khai.
*   AI Agent sẽ hoạt động dựa trên quyền của người dùng đang tương tác với nó. Ví dụ, nếu một `部長` hỏi Agent thông tin về nhân sự, Agent chỉ có thể truy cập và trả về thông tin của các nhân viên trong team của `部長` đó.
*   Một số quyền `R` (Read) có thể được giới hạn ở mức độ chi tiết (ví dụ: Sales chỉ xem thông tin cơ bản của Nhân viên, Nhân viên chỉ xem thông tin cơ bản trên Dashboard). 