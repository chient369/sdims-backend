# API List

**Version Control:**

| Version | Date       | Author         | Changes                                    | Status    |
| :------ | :--------- | :------------- | :----------------------------------------- | :-------- |
| 1.0     | 2025-04-30 | Chiến Trần Văn | Initial draft of API endpoints             | Draft     |

---

Đây là danh sách các API endpoint dự kiến, được nhóm theo module chức năng. Chi tiết về request body, response body, và validation sẽ được định nghĩa trong tài liệu thiết kế API chi tiết hơn.

> **Lưu ý về quyền truy cập**: Mỗi API đều có quyền truy cập tương ứng theo định dạng `resource:action[:scope]`. Chi tiết về các quyền và phạm vi truy cập được định nghĩa trong file `BD/permissions_definition.md`.

## 1. Authentication & Authorization

| API ID        | Method | Endpoint                      | Mô tả Chức năng                                   | Màn hình Liên quan | Chức năng Liên quan | Priority   | Documentation |
| :------------ | :----- | :---------------------------- | :------------------------------------------------ | :----------------- | :----------------- | :--------- | :------------ |
| API-AUTH-001  | POST   | `/api/v1/auth/login`          | Xác thực người dùng và trả về token (JWT).       | MH-AUTH-01         | -                  | Cao        | [Chi tiết](../../DD/API/API-AUTH-001.md) |
| API-AUTH-002  | POST   | `/api/v1/auth/logout`         | Hủy token phía server.                           | Mọi màn hình       | -                  | Cao        | [Chi tiết](../../DD/API/API-AUTH-002.md) |
| API-AUTH-003  | GET    | `/api/v1/auth/me`             | Lấy thông tin user và quyền của người dùng hiện tại. | Mọi màn hình       | F-1.2, F-6.2       | Cao        | [Chi tiết](../../DD/API/API-AUTH-003.md) |
| API-AUTH-004  | POST   | `/api/v1/auth/refresh-token`  | Làm mới access token sử dụng refresh token.       | Mọi màn hình       | -                  | Cao        | [Chi tiết](../../DD/API/API-AUTH-004.md) |

## 2. Quản lý Nhân sự (HRM)

| API ID        | Method | Endpoint                             | Mô tả Chức năng                                                  | Màn hình Liên quan      | Chức năng Liên quan             | Priority   | Documentation |
| :------------ | :----- | :----------------------------------- | :--------------------------------------------------------------- | :---------------------- | :------------------------------ | :--------- | :------------ |
| API-HRM-001   | GET    | `/api/v1/employees`                  | Lấy danh sách nhân viên (có phân trang, lọc, tìm kiếm).         | MH-HRM-01               | F-1.1, F-1.3, F-1.9, F-1.12     | Cao        | [Chi tiết](../../DD/API/API-HRM-001.md) |
| API-HRM-002   | POST   | `/api/v1/employees`                  | Thêm một nhân viên mới (Admin/TP).                              | MH-HRM-01 -> MH-HRM-03  | F-1.1                           | Trung bình  | [Chi tiết](../../DD/API/API-HRM-002.md) |
| API-HRM-003   | GET    | `/api/v1/employees/{employeeId}`     | Lấy thông tin chi tiết của một nhân viên.                        | MH-HRM-02               | F-1.1, F-1.6, F-1.9, F-1.11     | Cao        | [Chi tiết](../../DD/API/API-HRM-003.md) |
| API-HRM-004   | PUT    | `/api/v1/employees/{employeeId}`     | Cập nhật thông tin nhân viên (Admin/TP/Leader/NV tùy quyền).    | MH-HRM-02 -> MH-HRM-03  | F-1.1, F-1.6, F-1.9, F-1.10     | Cao        | [Chi tiết](../../DD/API/API-HRM-004.md) |
| API-HRM-005   | DELETE | `/api/v1/employees/{employeeId}`     | Xóa mềm (soft delete) nhân viên (Admin/TP).                      | MH-HRM-01               | F-1.1                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-005.md) |
| API-HRM-006   | GET    | `/api/v1/employees/search/suggest`   | (Optional) Gợi ý nhân viên dựa trên skills (cho dự án/cơ hội).    | MH-OPP-02?              | F-1.8                           | Thấp       | [Chi tiết](../../DD/API/API-HRM-006.md) |
| API-HRM-007   | POST   | `/api/v1/employees/import`           | (Optional) Import danh sách nhân viên từ file (Admin/TP).        | MH-HRM-01               | F-1.4                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-007.md) |
| API-HRM-008   | GET    | `/api/v1/employees/export`           | (Optional) Export danh sách nhân viên (Admin/TP/Leader).         | MH-HRM-01               | F-1.4                           | Thấp       | [Chi tiết](../../DD/API/API-HRM-008.md) |
| API-HRM-009   | GET    | `/api/v1/skill-categories`           | Lấy danh sách các loại kỹ năng (skill categories).             | MH-HRM-03, MH-HRM-04    | F-1.5                           | Cao        | [Chi tiết](../../DD/API/API-HRM-009.md) |
| API-HRM-010   | POST   | `/api/v1/admin/skill-categories`     | (Admin) Thêm loại kỹ năng mới.                                 | MH-HRM-04               | F-1.5                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-010.md) |
| API-HRM-011   | PUT    | `/api/v1/admin/skill-categories/{id}`| (Admin) Cập nhật loại kỹ năng.                                   | MH-HRM-04               | F-1.5                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-011.md) |
| API-HRM-012   | DELETE | `/api/v1/admin/skill-categories/{id}`| (Admin) Xóa loại kỹ năng (cần kiểm tra ràng buộc).                | MH-HRM-04               | F-1.5                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-012.md) |
| API-HRM-013   | GET    | `/api/v1/skills`                     | Lấy danh sách các kỹ năng (lọc theo category).                    | MH-HRM-03, MH-HRM-04    | F-1.5                           | Cao        | [Chi tiết](../../DD/API/API-HRM-013.md) |
| API-HRM-014   | POST   | `/api/v1/admin/skills`               | (Admin) Thêm kỹ năng mới vào category.                          | MH-HRM-04               | F-1.5                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-014.md) |
| API-HRM-015   | PUT    | `/api/v1/admin/skills/{id}`          | (Admin) Cập nhật kỹ năng.                                        | MH-HRM-04               | F-1.5                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-015.md) |
| API-HRM-016   | DELETE | `/api/v1/admin/skills/{id}`          | (Admin) Xóa kỹ năng (cần kiểm tra ràng buộc).                    | MH-HRM-04               | F-1.5                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-016.md) |
| API-HRM-017   | GET    | `/api/v1/employees/{employeeId}/skills` | Lấy danh sách kỹ năng của một nhân viên.                        | MH-HRM-02, MH-HRM-03    | F-1.6                           | Cao        | [Chi tiết](../../DD/API/API-HRM-017.md) |
| API-HRM-018   | POST   | `/api/v1/employees/{employeeId}/skills` | Thêm/Cập nhật kỹ năng cho nhân viên (NV tự thêm/Leader cập nhật). | MH-HRM-03               | F-1.6                           | Cao        | [Chi tiết](../../DD/API/API-HRM-018.md) |
| API-HRM-019   | DELETE | `/api/v1/employees/{employeeId}/skills/{skillId}` | Xóa kỹ năng khỏi hồ sơ nhân viên.                             | MH-HRM-03               | F-1.6                           | Trung bình | [Chi tiết](../../DD/API/API-HRM-019.md) |
| API-HRM-020   | PUT    | `/api/v1/employees/{employeeId}/status` | Cập nhật trạng thái & phân bổ dự án cho nhân viên (Leader/TP).   | MH-HRM-03               | F-1.9, F-1.10                 | Cao        | [Chi tiết](../../DD/API/API-HRM-020.md) |
| API-HRM-021   | GET    | `/api/v1/employees/{employeeId}/project-history` | Lấy lịch sử dự án của nhân viên.                             | MH-HRM-02               | F-1.11                          | Cao        | [Chi tiết](../../DD/API/API-HRM-021.md) |

## 3. Quản lý Hiệu suất & Margin

**Lưu ý:** Các API này cần kiểm tra quyền truy cập rất chặt chẽ (chỉ Leader/TP).

| API ID        | Method | Endpoint                             | Mô tả Chức năng                                                   | Màn hình Liên quan | Chức năng Liên quan         | Priority   | Documentation |
| :------------ | :----- | :----------------------------------- | :---------------------------------------------------------------- | :----------------- | :-------------------------- | :--------- | :------------ |
| API-MGN-001   | GET    | `/api/v1/margins/employee`           | Lấy dữ liệu margin của nhân viên (lọc theo team, thời gian).       | MH-MGN-01          | F-2.4, F-2.5, F-2.6, F-2.7 | Cao        | [Chi tiết](../../DD/API/API-MGN-001.md) |
| API-MGN-002   | GET    | `/api/v1/margins/summary`            | Lấy dữ liệu margin tổng hợp (Dashboard).                          | MH-DSH-01          | F-2.5                       | Cao        | [Chi tiết](../../DD/API/API-MGN-002.md) |
| API-MGN-003   | POST   | `/api/v1/margins/costs/import`       | Import chi phí nhân viên hàng tháng từ file (Leader/TP).         | MH-MGN-02          | F-2.1                       | Cao        | [Chi tiết](../../DD/API/API-MGN-003.md) |
| API-MGN-004   | POST   | `/api/v1/margins/costs`              | (Optional) Nhập chi phí thủ công cho nhân viên (Leader/TP).     | MH-MGN-02          | F-2.1                       | Trung bình | [Chi tiết](../../DD/API/API-MGN-004.md) |

## 4. Quản lý Cơ hội Kinh doanh

| API ID        | Method | Endpoint                             | Mô tả Chức năng                                                     | Màn hình Liên quan | Chức năng Liên quan         | Priority   | Documentation |
| :------------ | :----- | :----------------------------------- | :------------------------------------------------------------------ | :----------------- | :-------------------------- | :--------- | :------------ |
| API-OPP-001   | GET    | `/api/v1/opportunities`              | Lấy danh sách cơ hội (phân trang, lọc, tìm kiếm, theo quyền).        | MH-OPP-01          | F-3.8, F-3.6                | Cao        | [Chi tiết](../../DD/API/API-OPP-001.md) |
| API-OPP-002   | GET    | `/api/v1/opportunities/{oppId}`      | Lấy chi tiết một cơ hội.                                            | MH-OPP-02          | F-3.8                       | Cao        | [Chi tiết](../../DD/API/API-OPP-002.md) |
| API-OPP-003   | POST   | `/api/v1/opportunities/sync`         | Kích hoạt đồng bộ thủ công từ Hubspot (Admin/TP).                   | MH-OPP-01          | F-3.1                       | Thấp        | [Chi tiết](../../DD/API/API-OPP-003.md) |
| API-OPP-004   | GET    | `/api/v1/opportunities/sync/logs`    | Xem log đồng bộ Hubspot (Admin).                                    | MH-ADM-04?         | F-3.2                       | Thấp        | [Chi tiết](../../DD/API/API-OPP-004.md) |
| API-OPP-005   | POST   | `/api/v1/opportunities/{oppId}/assign` | Gán Leader vào cơ hội (Sales/TP).                                 | MH-OPP-02          | F-3.3                       | Cao        | [Chi tiết](../../DD/API/API-OPP-005.md) |
| API-OPP-006   | POST   | `/api/v1/opportunities/{oppId}/notes`  | Thêm ghi chú/log hoạt động cho cơ hội (Sales/Leader được assign). | MH-OPP-02          | F-3.4                       | Cao        | [Chi tiết](../../DD/API/API-OPP-006.md) |
| API-OPP-007   | GET    | `/api/v1/opportunities/{oppId}/notes`  | Lấy danh sách ghi chú của cơ hội.                                   | MH-OPP-02          | F-3.4                       | Cao        | [Chi tiết](../../DD/API/API-OPP-007.md) |
| API-OPP-008   | PUT    | `/api/v1/opportunities/{oppId}/onsite` | Đánh dấu/bỏ đánh dấu ưu tiên Onsite.                               | MH-OPP-02          | F-3.7                       | Trung bình | [Chi tiết](../../DD/API/API-OPP-008.md) |

## 5. Quản lý Hợp đồng & Doanh thu

| API ID        | Method | Endpoint                             | Mô tả Chức năng                                                      | Màn hình Liên quan      | Chức năng Liên quan         | Priority   | Documentation |
| :------------ | :----- | :----------------------------------- | :------------------------------------------------------------------- | :---------------------- | :-------------------------- | :--------- | :------------ |
| API-CTR-001   | GET    | `/api/v1/contracts`                  | Lấy danh sách hợp đồng (phân trang, lọc, tìm kiếm, theo quyền).     | MH-CTR-01               | F-4.1                       | Cao        | [Chi tiết](../../DD/API/API-CTR-001.md) |
| API-CTR-002   | POST   | `/api/v1/contracts`                  | Thêm hợp đồng mới (Admin/TP/Sales).                               | MH-CTR-01 -> MH-CTR-03  | F-4.1                       | Cao        | [Chi tiết](../../DD/API/API-CTR-002.md) |
| API-CTR-003   | GET    | `/api/v1/contracts/{contractId}`     | Lấy chi tiết hợp đồng.                                               | MH-CTR-02               | F-4.1, F-4.2, F-4.4         | Cao        | [Chi tiết](../../DD/API/API-CTR-003.md) |
| API-CTR-004   | PUT    | `/api/v1/contracts/{contractId}`     | Cập nhật thông tin hợp đồng (Admin/TP/Sales).                       | MH-CTR-02 -> MH-CTR-03  | F-4.1, F-4.2, F-4.4         | Cao        | [Chi tiết](../../DD/API/API-CTR-004.md) |
| API-CTR-005   | DELETE | `/api/v1/contracts/{contractId}`     | Xóa mềm hợp đồng (Admin/TP).                                        | MH-CTR-01               | F-4.1                       | Trung bình | [Chi tiết](../../DD/API/API-CTR-005.md) |
| API-CTR-006   | GET    | `/api/v1/contracts/{contractId}/payment-terms` | Lấy các điều khoản thanh toán của hợp đồng.                        | MH-CTR-02               | F-4.4                       | Cao        | [Chi tiết](../../DD/API/API-CTR-006.md) |
| API-CTR-007   | PUT    | `/api/v1/contracts/payment-terms/{termId}/status` | (Kế toán) Cập nhật trạng thái thu tiền cho một điều khoản.         | MH-CTR-04 (hoặc 02)   | F-4.5                       | Cao        | [Chi tiết](../../DD/API/API-CTR-007.md) |
| API-CTR-008   | POST   | `/api/v1/contracts/payment-terms/import-status` | (Kế toán) Import trạng thái thu tiền từ file.                     | MH-CTR-04               | F-4.5                       | Thấp        | [Chi tiết](../../DD/API/API-CTR-008.md) |
| API-CTR-009   | GET    | `/api/v1/contracts/{contractId}/files` | Lấy danh sách file đính kèm của hợp đồng.                          | MH-CTR-02               | F-4.3                       | Cao        | [Chi tiết](../../DD/API/API-CTR-009.md) |
| API-CTR-010   | POST   | `/api/v1/contracts/{contractId}/files` | Upload file đính kèm cho hợp đồng.                                | MH-CTR-03               | F-4.3                       | Cao        | [Chi tiết](../../DD/API/API-CTR-010.md) |
| API-CTR-011   | DELETE | `/api/v1/contracts/files/{fileId}`   | Xóa file đính kèm.                                                 | MH-CTR-02, MH-CTR-03    | F-4.3                       | Trung bình | [Chi tiết](../../DD/API/API-CTR-011.md) |
| API-CTR-012   | GET    | `/api/v1/contracts/{contractId}/employees` | Lấy danh sách nhân viên liên kết với hợp đồng.                     | MH-CTR-02               | F-4.2                       | Cao        | [Chi tiết](../../DD/API/API-CTR-012.md) |
| API-CTR-013   | POST   | `/api/v1/contracts/{contractId}/employees` | Liên kết nhân viên vào hợp đồng (khi tạo/sửa HĐ).                 | MH-CTR-03               | F-4.2                       | Cao        | [Chi tiết](../../DD/API/API-CTR-013.md) |
| API-CTR-014   | DELETE | `/api/v1/contracts/{contractId}/employees/{employeeId}` | Gỡ liên kết nhân viên khỏi hợp đồng.                            | MH-CTR-03               | F-4.2                       | Trung bình | [Chi tiết](../../DD/API/API-CTR-014.md) |
| API-CTR-015   | GET    | `/api/v1/sales-kpis`                 | (Admin) Lấy danh sách KPI doanh thu đã thiết lập (lọc theo Sales/Kỳ). | MH-CTR-05               | F-4.8, F-4.10, F-4.11       | Cao        | [Chi tiết](../../DD/API/API-CTR-015.md) |
| API-CTR-016   | POST   | `/api/v1/admin/sales-kpis`           | (Admin) Thêm/Sửa KPI doanh thu cho Sales.                           | MH-CTR-05               | F-4.8                       | Cao        | [Chi tiết](../../DD/API/API-CTR-016.md) |
| API-CTR-017   | DELETE | `/api/v1/admin/sales-kpis/{kpiId}`   | (Admin) Xóa KPI doanh thu.                                          | MH-CTR-05               | F-4.8                       | Trung bình | [Chi tiết](../../DD/API/API-CTR-017.md) |

## 6. Dashboard & Báo cáo

| API ID        | Method | Endpoint                          | Mô tả Chức năng                                                      | Màn hình Liên quan | Chức năng Liên quan             | Priority   | Documentation |
| :------------ | :----- | :-------------------------------- | :------------------------------------------------------------------- | :----------------- | :------------------------------ | :--------- | :------------ |
| API-RPT-001   | GET    | `/api/v1/dashboard/summary`       | Lấy dữ liệu tổng hợp cho các widget trên dashboard chính.          | MH-DSH-01          | F-5.1                           | Cao        | [Chi tiết](../../DD/API/API-RPT-001.md) |
| API-RPT-002   | GET    | `/api/v1/reports/employee-list`   | Lấy báo cáo chi tiết danh sách nhân viên (kèm skill...).          | MH-RPT-01/02       | F-5.3, F-5.4, F-5.5             | Trung bình | [Chi tiết](../../DD/API/API-RPT-002.md) |
| API-RPT-003   | GET    | `/api/v1/reports/margin-detail`   | Lấy báo cáo chi tiết margin theo nhân viên/team.                   | MH-RPT-01/02       | F-5.3, F-5.4, F-5.5             | Trung bình | [Chi tiết](../../DD/API/API-RPT-003.md) |
| API-RPT-004   | GET    | `/api/v1/reports/opportunity-list`| Lấy báo cáo chi tiết danh sách cơ hội.                            | MH-RPT-01/02       | F-5.3, F-5.4, F-5.5             | Trung bình | [Chi tiết](../../DD/API/API-RPT-004.md) |
| API-RPT-005   | GET    | `/api/v1/reports/contract-list`   | Lấy báo cáo chi tiết danh sách hợp đồng.                          | MH-RPT-01/02       | F-5.3, F-5.4, F-5.5             | Trung bình | [Chi tiết](../../DD/API/API-RPT-005.md) |
| API-RPT-006   | GET    | `/api/v1/reports/payment-status`  | Lấy báo cáo chi tiết tình trạng thanh toán/công nợ.                | MH-RPT-01/02       | F-4.7, F-5.3, F-5.4, F-5.5      | Trung bình | [Chi tiết](../../DD/API/API-RPT-006.md) |
| API-RPT-007   | GET    | `/api/v1/reports/kpi-progress`    | Lấy báo cáo tiến độ KPI doanh thu Sales.                           | MH-RPT-01/02       | F-4.10, F-4.11, F-5.3, F-5.4, F-5.5 | Trung bình | [Chi tiết](../../DD/API/API-RPT-007.md) |
| API-RPT-008   | GET    | `/api/v1/reports/utilization`     | Lấy báo cáo tỷ lệ sử dụng nguồn lực.                              | MH-RPT-01/02       | F-1.12, F-5.3, F-5.4, F-5.5     | Trung bình | [Chi tiết](../../DD/API/API-RPT-008.md) |

(Lưu ý: Các API báo cáo có thể cần tham số lọc/xuất file phức tạp hơn).

## 7. Quản trị Hệ thống (Admin)

**Lưu ý:** Các API này yêu cầu quyền Admin.

| API ID        | Method | Endpoint                             | Mô tả Chức năng                                    | Màn hình Liên quan | Chức năng Liên quan         | Priority   | Documentation |
| :------------ | :----- | :----------------------------------- | :------------------------------------------------- | :----------------- | :-------------------------- | :--------- | :------------ |
| API-ADM-001   | GET    | `/api/v1/admin/users`                | Lấy danh sách người dùng hệ thống.                  | MH-ADM-01          | F-6.1                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-001.md) |
| API-ADM-002   | POST   | `/api/v1/admin/users`                | Tạo người dùng mới.                              | MH-ADM-01          | F-6.1                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-002.md) |
| API-ADM-003   | GET    | `/api/v1/admin/users/{userId}`       | Lấy chi tiết người dùng.                           | MH-ADM-01          | F-6.1                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-003.md) |
| API-ADM-004   | PUT    | `/api/v1/admin/users/{userId}`       | Cập nhật thông tin người dùng (khóa/mở, reset...). | MH-ADM-01          | F-6.1                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-004.md) |
| API-ADM-005   | DELETE | `/api/v1/admin/users/{userId}`       | Xóa người dùng.                                    | MH-ADM-01          | F-6.1                       | Trung bình | [Chi tiết](../../DD/API/API-ADM-005.md) |
| API-ADM-006   | GET    | `/api/v1/admin/roles`                | Lấy danh sách các vai trò.                          | MH-ADM-02          | F-6.2                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-006.md) |
| API-ADM-007   | POST   | `/api/v1/admin/roles`                | Tạo vai trò mới.                                  | MH-ADM-02          | F-6.2                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-007.md) |
| API-ADM-008   | PUT    | `/api/v1/admin/roles/{roleId}`       | Cập nhật vai trò (gán/gỡ quyền).                   | MH-ADM-02          | F-6.2                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-008.md) |
| API-ADM-009   | DELETE | `/api/v1/admin/roles/{roleId}`       | Xóa vai trò.                                      | MH-ADM-02          | F-6.2                       | Trung bình | [Chi tiết](../../DD/API/API-ADM-009.md) |
| API-ADM-010   | GET    | `/api/v1/admin/permissions`          | Lấy danh sách các quyền.                           | MH-ADM-02          | F-6.2                       | Trung bình        | [Chi tiết](../../DD/API/API-ADM-010.md) |
| API-ADM-011   | GET    | `/api/v1/admin/configs`              | Lấy danh sách cấu hình hệ thống.                   | MH-ADM-03          | F-6.3, F-6.4, F-6.5         | Trung bình        | [Chi tiết](../../DD/API/API-ADM-011.md) |
| API-ADM-012   | PUT    | `/api/v1/admin/configs/{configKey}`  | Cập nhật giá trị cấu hình.                        | MH-ADM-03          | F-6.3, F-6.4, F-6.5         | Trung bình        | [Chi tiết](../../DD/API/API-ADM-012.md) |
| API-ADM-013   | GET    | `/api/v1/admin/system-logs`          | Xem log hệ thống (cần cơ chế lọc/phân trang).     | MH-ADM-04          | F-6.6                       | Trung bình | [Chi tiết](../../DD/API/API-ADM-013.md) |
