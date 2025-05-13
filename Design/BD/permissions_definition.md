# Định nghĩa Quyền trong Hệ thống

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2023-07-10 | Chiến Trần Văn | Tạo tài liệu định nghĩa quyền hệ thống | -           | Draft     |
| 1.1     | 2023-07-11 | Chiến Trần Văn | Bổ sung phần triển khai phân quyền trong frontend | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa các quyền được sử dụng trong hệ thống quản lý, bao gồm ý nghĩa của mỗi quyền và mối quan hệ giữa quyền với các vai trò người dùng.

---

## 2. Cấu trúc Phân quyền

Hệ thống áp dụng mô hình phân quyền dựa trên vai trò (Role-based Access Control - RBAC) với các tính năng:

- **Vai trò (Roles)**: Các nhóm quyền được gắn với một loại người dùng cụ thể (Admin, Division Manager, Leader, Sales, Employee)
- **Quyền (Permissions)**: Các đơn vị quyền nhỏ nhất, định nghĩa khả năng thực hiện một hành động cụ thể trên một tài nguyên
- **Phạm vi (Scopes)**: Giới hạn phạm vi của quyền (Own, Team, All, Basic, Assigned, etc.)

### 2.1 Định dạng quyền

Quyền trong hệ thống được định dạng theo cú pháp: `resource:action[:scope]`

Ví dụ:
- `employee:read:all` - Quyền đọc thông tin tất cả nhân viên
- `contract:update:own` - Quyền cập nhật thông tin các hợp đồng do mình quản lý
- `opportunity:create` - Quyền tạo cơ hội kinh doanh (không giới hạn phạm vi)

---

## 3. Danh sách Quyền theo Module

### 3.1 Quản lý Nhân sự (HRM)

| Mã Quyền                     | Mô tả                                                     | Vai trò được cấp |
| :--------------------------- | :-------------------------------------------------------- | :--------------- |
| `employee:read:all`          | Xem thông tin tất cả nhân viên                            | Division Manager |
| `employee:read:team`         | Xem thông tin nhân viên trong team                        | Leader |
| `employee:read:basic`        | Xem thông tin cơ bản của nhân viên                        | Sales |
| `employee:read:own`          | Xem thông tin cá nhân                                     | Employee |
| `employee:create`            | Tạo nhân viên mới                                         | Division Manager |
| `employee:update:all`        | Cập nhật thông tin tất cả nhân viên                       | Division Manager |
| `employee:update:team`       | Cập nhật thông tin nhân viên trong team                   | Leader |
| `employee:update:own`        | Cập nhật thông tin cá nhân                                | Employee |
| `employee:delete`            | Xoá nhân viên (soft delete)                               | Division Manager |
| `employee:import`            | Import danh sách nhân viên từ file                        | Division Manager |
| `employee:export`            | Export danh sách nhân viên                                | Division Manager, Leader |
| `skill-category:read`        | Xem danh mục kỹ năng                                      | Division Manager, Leader, Employee |
| `skill-category:create`      | Tạo danh mục kỹ năng                                      | Division Manager |
| `skill-category:update`      | Cập nhật danh mục kỹ năng                                 | Division Manager |
| `skill-category:delete`      | Xoá danh mục kỹ năng                                      | Division Manager |
| `skill:read`                 | Xem danh sách kỹ năng                                     | Division Manager, Leader, Employee |
| `skill:create`               | Tạo kỹ năng mới                                           | Division Manager |
| `skill:update`               | Cập nhật kỹ năng                                          | Division Manager |
| `skill:delete`               | Xoá kỹ năng                                               | Division Manager |
| `employee-skill:read:all`    | Xem kỹ năng của tất cả nhân viên                          | Division Manager |
| `employee-skill:read:team`   | Xem kỹ năng của nhân viên trong team                      | Leader |
| `employee-skill:read:own`    | Xem kỹ năng cá nhân                                       | Employee |
| `employee-skill:create:all`  | Thêm kỹ năng cho bất kỳ nhân viên                         | Division Manager |
| `employee-skill:create:team` | Thêm kỹ năng cho nhân viên trong team                     | Leader |
| `employee-skill:create:own`  | Thêm kỹ năng cá nhân                                      | Employee |
| `employee-skill:update:all`  | Cập nhật kỹ năng của bất kỳ nhân viên                     | Division Manager |
| `employee-skill:update:team` | Cập nhật kỹ năng của nhân viên trong team                 | Leader |
| `employee-skill:update:own`  | Cập nhật kỹ năng cá nhân                                  | Employee |
| `employee-skill:delete:all`  | Xoá kỹ năng của bất kỳ nhân viên                          | Division Manager |
| `employee-skill:delete:team` | Xoá kỹ năng của nhân viên trong team                      | Leader |
| `employee-skill:delete:own`  | Xoá kỹ năng cá nhân                                       | Employee |
| `employee-skill:evaluate`    | Đánh giá kỹ năng nhân viên                                | Division Manager, Leader |
| `employee-suggest:read`      | Xem gợi ý nhân sự phù hợp                                 | Division Manager, Leader |
| `employee-status:read:all`   | Xem trạng thái & phân bổ dự án của tất cả nhân viên       | Division Manager |
| `employee-status:read:team`  | Xem trạng thái & phân bổ dự án của nhân viên trong team   | Leader |
| `employee-status:read:own`   | Xem trạng thái & phân bổ dự án cá nhân                    | Employee |
| `employee-status:update:all` | Cập nhật trạng thái & phân bổ dự án tất cả nhân viên      | Division Manager |
| `employee-status:update:team`| Cập nhật trạng thái & phân bổ dự án nhân viên trong team  | Leader |
| `project-history:read:all`   | Xem lịch sử dự án của tất cả nhân viên                    | Division Manager |
| `project-history:read:team`  | Xem lịch sử dự án của nhân viên trong team                | Leader |
| `project-history:read:own`   | Xem lịch sử dự án cá nhân                                 | Employee |
| `utilization:read:all`       | Xem báo cáo utilization toàn bộ nhân viên                 | Division Manager |
| `utilization:read:team`      | Xem báo cáo utilization team                              | Leader |
| `employee-alert:read:all`    | Xem cảnh báo nhân sự sắp hết dự án (tất cả)               | Division Manager |
| `employee-alert:read:team`   | Xem cảnh báo nhân sự sắp hết dự án (team)                 | Leader |

### 3.2 Quản lý Hiệu suất & Margin

| Mã Quyền                   | Mô tả                                                  | Vai trò được cấp |
| :------------------------- | :----------------------------------------------------- | :--------------- |
| `employee-cost:read:all`   | Xem chi phí của tất cả nhân viên                       | Division Manager |
| `employee-cost:read:team`  | Xem chi phí của nhân viên trong team                   | Leader |
| `employee-cost:create`     | Tạo chi phí nhân viên                                  | Division Manager |
| `employee-cost:update:all` | Cập nhật chi phí của tất cả nhân viên                  | Division Manager |
| `employee-cost:delete`     | Xoá chi phí nhân viên                                  | Division Manager |
| `employee-cost:import`     | Import chi phí nhân viên từ file                       | Division Manager |
| `revenue:read:all`         | Xem doanh thu của tất cả nhân viên                     | Division Manager |
| `revenue:read:team`        | Xem doanh thu của nhân viên trong team                 | Leader |
| `margin:read:all`          | Xem margin của tất cả nhân viên                        | Division Manager |
| `margin:read:team`         | Xem margin của nhân viên trong team                    | Leader |
| `margin-summary:read:all`  | Xem tổng hợp margin toàn bộ                           | Division Manager |
| `margin-summary:read:team` | Xem tổng hợp margin team                              | Leader |
| `margin-alert:read:all`    | Xem cảnh báo margin toàn bộ                           | Division Manager |
| `margin-alert:read:team`   | Xem cảnh báo margin team                              | Leader |
| `margin-alert:config`      | Cấu hình thông báo margin thấp                        | Division Manager |

### 3.3 Quản lý Cơ hội Kinh doanh

| Mã Quyền                    | Mô tả                                               | Vai trò được cấp |
| :-------------------------- | :-------------------------------------------------- | :--------------- |
| `opportunity:read:all`      | Xem tất cả cơ hội kinh doanh                        | Division Manager, Leader, Sales |
| `opportunity:create`        | Tạo cơ hội kinh doanh                               | Sales |
| `opportunity:update:all`    | Cập nhật tất cả cơ hội kinh doanh                   | Division Manager |
| `opportunity:update:own`    | Cập nhật cơ hội kinh doanh do mình tạo              | Sales |
| `opportunity:update:assigned` | Cập nhật cơ hội kinh doanh được gán                | Leader |
| `opportunity:delete`        | Xoá cơ hội kinh doanh                               | Division Manager |
| `opportunity-sync:read`     | Xem thông tin đồng bộ từ Hubspot                    | Division Manager, Leader, Sales |
| `opportunity-sync:config`   | Cấu hình đồng bộ Hubspot                            | Division Manager |
| `opportunity-log:read:all`  | Xem log đồng bộ Hubspot                             | Division Manager, Leader, Sales |
| `opportunity-assign:update:all` | Gán Leader vào cơ hội (bất kỳ)                  | Division Manager, Sales |
| `opportunity-note:create:all` | Thêm ghi chú cho bất kỳ cơ hội                    | Division Manager, Sales |
| `opportunity-note:create:assigned` | Thêm ghi chú cho cơ hội được gán             | Leader |
| `opportunity-note:read:all` | Xem ghi chú của tất cả cơ hội                       | Division Manager, Sales |
| `opportunity-note:read:assigned` | Xem ghi chú của cơ hội được gán                | Leader |
| `opportunity-followup:read:all` | Xem trạng thái follow-up tất cả cơ hội          | Division Manager, Leader, Sales |
| `opportunity-onsite:update:all` | Cập nhật trạng thái ưu tiên onsite (bất kỳ)     | Division Manager, Sales |
| `opportunity-onsite:update:assigned` | Cập nhật trạng thái ưu tiên onsite (assigned) | Leader |
| `opportunity-alert:config`  | Cấu hình thông báo cơ hội                           | Division Manager |
| `opportunity-alert:read:all` | Xem thông báo tất cả cơ hội                        | Division Manager, Sales |
| `opportunity-alert:read:assigned` | Xem thông báo cơ hội được gán                 | Leader |

### 3.4 Quản lý Hợp đồng & Doanh thu

| Mã Quyền                    | Mô tả                                                   | Vai trò được cấp |
| :-------------------------- | :------------------------------------------------------ | :--------------- |
| `contract:read:all`         | Xem tất cả hợp đồng                                     | Division Manager |
| `contract:read:own`         | Xem hợp đồng do mình quản lý                            | Sales |
| `contract:read:assigned`    | Xem hợp đồng được gán                                   | Leader |
| `contract:create`           | Tạo hợp đồng mới                                        | Division Manager, Sales |
| `contract:update:all`       | Cập nhật tất cả hợp đồng                                | Division Manager |
| `contract:update:own`       | Cập nhật hợp đồng do mình quản lý                       | Sales |
| `contract:delete`           | Xoá hợp đồng                                            | Division Manager |
| `contract-link:update:all`  | Liên kết hợp đồng với cơ hội/nhân sự (bất kỳ)           | Division Manager |
| `contract-link:update:own`  | Liên kết hợp đồng với cơ hội/nhân sự (của mình)         | Sales |
| `contract-link:update:assigned` | Liên kết hợp đồng với cơ hội/nhân sự (được gán)     | Leader |
| `contract-file:read:all`    | Xem file đính kèm (tất cả hợp đồng)                     | Division Manager |
| `contract-file:read:own`    | Xem file đính kèm (hợp đồng của mình)                   | Sales |
| `contract-file:read:assigned` | Xem file đính kèm (hợp đồng được gán)                 | Leader |
| `contract-file:create:all`  | Upload file cho bất kỳ hợp đồng                         | Division Manager |
| `contract-file:create:own`  | Upload file cho hợp đồng của mình                       | Sales |
| `contract-file:delete:all`  | Xoá file đính kèm của bất kỳ hợp đồng                   | Division Manager |
| `contract-file:delete:own`  | Xoá file đính kèm của hợp đồng mình quản lý             | Sales |
| `payment-term:read:all`     | Xem điều khoản thanh toán (tất cả)                      | Division Manager |
| `payment-term:read:own`     | Xem điều khoản thanh toán (hợp đồng của mình)           | Sales |
| `payment-term:read:assigned` | Xem điều khoản thanh toán (hợp đồng được gán)          | Leader |
| `payment-term:create:all`   | Thêm điều khoản thanh toán (bất kỳ hợp đồng)            | Division Manager |
| `payment-term:create:own`   | Thêm điều khoản thanh toán (hợp đồng của mình)          | Sales |
| `payment-term:update:all`   | Cập nhật điều khoản thanh toán (bất kỳ)                 | Division Manager |
| `payment-term:update:own`   | Cập nhật điều khoản thanh toán (hợp đồng của mình)      | Sales |
| `payment-term:delete:all`   | Xoá điều khoản thanh toán (bất kỳ)                      | Division Manager |
| `payment-term:delete:own`   | Xoá điều khoản thanh toán (hợp đồng của mình)           | Sales |
| `payment-status:update:all` | Cập nhật trạng thái thu tiền (bất kỳ)                   | Division Manager, Sales |
| `payment-status:import`     | Import trạng thái thu tiền từ file                      | Division Manager, Sales |
| `payment-alert:read:all`    | Xem cảnh báo thanh toán (tất cả)                        | Division Manager |
| `payment-alert:read:own`    | Xem cảnh báo thanh toán (hợp đồng của mình)             | Sales |
| `payment-alert:read:assigned` | Xem cảnh báo thanh toán (hợp đồng được gán)           | Leader |
| `payment-alert:config`      | Cấu hình cảnh báo thanh toán                            | Division Manager |
| `debt-report:read:all`      | Xem báo cáo công nợ (tất cả)                            | Division Manager |
| `debt-report:read:own`      | Xem báo cáo công nợ (của mình)                          | Sales |
| `sales-kpi:read:all`        | Xem KPI doanh thu (tất cả)                              | Division Manager |
| `sales-kpi:read:own`        | Xem KPI doanh thu (của mình)                            | Sales |
| `sales-kpi:create`          | Thiết lập KPI doanh thu                                 | Division Manager |
| `sales-kpi:update`          | Cập nhật KPI doanh thu                                  | Division Manager |
| `sales-kpi:delete`          | Xoá KPI doanh thu                                       | Division Manager |
| `revenue-report:read:all`   | Xem báo cáo doanh thu thực tế (tất cả)                  | Division Manager |
| `revenue-report:read:team`  | Xem báo cáo doanh thu thực tế (team)                    | Leader |
| `revenue-report:read:own`   | Xem báo cáo doanh thu thực tế (của mình)                | Sales |
| `revenue-summary:read:all`  | Xem tổng hợp doanh thu (tất cả)                         | Division Manager |
| `revenue-summary:read:team` | Xem tổng hợp doanh thu (team)                           | Leader |
| `revenue-summary:read:own`  | Xem tổng hợp doanh thu (của mình)                       | Sales |

### 3.5 Dashboard & Báo cáo

| Mã Quyền                   | Mô tả                                              | Vai trò được cấp |
| :------------------------- | :------------------------------------------------- | :--------------- |
| `dashboard:read:all`       | Xem dashboard tổng hợp (tất cả dữ liệu)            | Division Manager |
| `dashboard:read:team`      | Xem dashboard tổng hợp (dữ liệu team)              | Leader |
| `dashboard:read:own`       | Xem dashboard tổng hợp (dữ liệu cá nhân)           | Sales |
| `report:read:all`          | Xem báo cáo chi tiết (tất cả)                      | Division Manager |
| `report:read:team`         | Xem báo cáo chi tiết (team)                        | Leader |
| `report:read:own`          | Xem báo cáo chi tiết (của mình)                    | Sales |
| `report:export`            | Xuất báo cáo ra file                               | Division Manager, Leader, Sales |

### 3.6 Quản trị Hệ thống

| Mã Quyền                | Mô tả                                              | Vai trò được cấp |
| :---------------------- | :------------------------------------------------- | :--------------- |
| `user:read`             | Xem danh sách người dùng                           | Admin |
| `user:create`           | Tạo người dùng mới                                 | Admin |
| `user:update`           | Cập nhật thông tin người dùng                      | Admin |
| `user:delete`           | Xoá người dùng                                     | Admin |
| `role:read`             | Xem danh sách vai trò                              | Admin |
| `role:create`           | Tạo vai trò mới                                    | Admin |
| `role:update`           | Cập nhật vai trò                                   | Admin |
| `role:delete`           | Xoá vai trò                                        | Admin |
| `permission:read`       | Xem danh sách quyền                                | Admin |
| `permission:assign`     | Gán quyền cho vai trò                              | Admin |
| `config:read`           | Xem cấu hình hệ thống                              | Admin, Division Manager, Leader |
| `config:update`         | Cập nhật cấu hình hệ thống                         | Admin |
| `alert-threshold:read`  | Xem ngưỡng cảnh báo                                | Admin, Division Manager, Leader |
| `alert-threshold:update`| Cập nhật ngưỡng cảnh báo                           | Admin |
| `api-connect:read`      | Xem thông tin kết nối API                          | Admin, Division Manager |
| `api-connect:update`    | Cập nhật thông tin kết nối API                     | Admin |
| `system-log:read:all`   | Xem log hệ thống (toàn bộ)                         | Admin |
| `system-log:read:limited`| Xem log hệ thống (giới hạn)                        | Division Manager |

---

## 4. Cấu hình Vai trò Mặc định

Bảng dưới đây mô tả cấu hình vai trò mặc định với các quyền tương ứng:

| Vai trò (Role)     | Mô tả                                                | Quyền kế thừa          | Quyền riêng                             |
| :----------------- | :--------------------------------------------------- | :------------------ | :--------------------------------------- |
| Admin              | Quản trị viên hệ thống với toàn quyền               | -                   | Tất cả quyền quản trị hệ thống           |
| Division Manager   | Quản lý bộ phận/phòng ban                           | -                   | Hầu hết quyền với phạm vi :all           |
| Leader (部長)       | Trưởng nhóm/Team leader                             | -                   | Quyền đọc/cập nhật trong phạm vi :team hoặc :assigned |
| Sales              | Nhân viên kinh doanh                                | -                   | Quyền đọc/cập nhật trong phạm vi :own và một số quyền đặc thù |
| Employee (Member)  | Nhân viên thông thường                              | -                   | Quyền đọc/cập nhật thông tin cá nhân (:own) |

---

## 5. Áp dụng Phân quyền trong API

Mỗi API trong hệ thống đều có trường `Quyền truy cập` định nghĩa quyền cần thiết để gọi API đó.

Ví dụ:
- API `/api/v1/employees` (API-HRM-001) yêu cầu quyền `employee:read`
- API `/api/v1/contracts` (API-CTR-001) yêu cầu quyền `contract:create`

Lưu ý:
- Phạm vi quyền (scope) sẽ được kiểm tra tại backend, không chỉ dựa vào quyền trong token
- Một số API có thể thực hiện kiểm tra quyền bổ sung dựa trên dữ liệu cụ thể

---

## 6. Ghi chú triển khai

1. Khi triển khai, hệ thống sẽ thực hiện logic phân quyền 2 lớp:
   - Lớp 1: Kiểm tra quyền truy cập API
   - Lớp 2: Kiểm tra phạm vi quyền (scope) dựa trên dữ liệu cụ thể

2. Mỗi request API sẽ kèm theo JWT token chứa thông tin người dùng và các quyền được cấp.

3. API Gateway/Server sẽ giải mã token và xác thực quyền trước khi chuyển tiếp request tới các service.

4. Các service nghiệp vụ sẽ thực hiện kiểm tra phạm vi quyền dựa trên dữ liệu cụ thể.

5. Các quyền có thể được điều chỉnh trong quá trình triển khai và vận hành hệ thống. 

---

## 7. Triển khai Phân quyền trong Frontend

### 7.1 Nguyên tắc chung

1. **Phân quyền đồng nhất**: Frontend và Backend cần thực hiện kiểm tra quyền theo cùng một chuẩn, đảm bảo tính nhất quán trong toàn bộ hệ thống.

2. **Nhiều lớp bảo vệ**: Mặc dù Backend luôn là lớp kiểm soát quyền cuối cùng, Frontend vẫn cần thực hiện kiểm tra để:
   - Cải thiện trải nghiệm người dùng (không hiển thị chức năng không có quyền)
   - Giảm tải cho Backend (không gửi request không cần thiết)
   - Tạo thêm một lớp bảo vệ (defense in depth)

### 7.2 Lưu trữ và Quản lý Quyền

Sau khi đăng nhập, Frontend cần:

1. **Lưu trữ token**: Lưu JWT token trong localStorage hoặc sessionStorage
2. **Giải mã thông tin người dùng**: 
   - Giải mã JWT token để lấy thông tin cơ bản và danh sách quyền
   - Lưu trong Redux/Context API để dễ dàng truy cập trên toàn ứng dụng

```typescript
// Ví dụ cấu trúc dữ liệu user và permissions trong Redux store
interface UserState {
  id: number;
  username: string;
  fullName: string;
  role: string;
  permissions: string[]; // ['employee:read:team', 'contract:read:own', ...]
  teamId?: number;      // ID team nếu là Leader
}
```

### 7.3 Triển khai việc Kiểm tra Quyền

#### 7.3.1 Tạo Helper Functions

```typescript
// permissions.ts
export const hasPermission = (requiredPermission: string, userPermissions: string[]): boolean => {
  // Phân tách quyền thành các phần: resource, action, scope (nếu có)
  const [resource, action, scope] = requiredPermission.split(':');
  
  // Kiểm tra quyền chính xác (bao gồm cả scope)
  if (userPermissions.includes(requiredPermission)) {
    return true;
  }
  
  // Kiểm tra quyền không có scope
  if (!scope && userPermissions.includes(`${resource}:${action}`)) {
    return true;
  }
  
  // Nếu cần kiểm tra scope phức tạp hơn (all > team > own)
  if (scope) {
    // Nếu người dùng có quyền với scope rộng hơn
    if (scope === 'team' && userPermissions.includes(`${resource}:${action}:all`)) {
      return true;
    }
    if (scope === 'own' && (
      userPermissions.includes(`${resource}:${action}:all`) || 
      userPermissions.includes(`${resource}:${action}:team`)
    )) {
      return true;
    }
  }
  
  return false;
};

// Kiểm tra nhiều quyền (user cần có ít nhất một trong số các quyền)
export const hasAnyPermission = (requiredPermissions: string[], userPermissions: string[]): boolean => {
  return requiredPermissions.some(perm => hasPermission(perm, userPermissions));
};

// Kiểm tra phạm vi dữ liệu
export const hasDataAccess = (
  resourceOwnerId: number, 
  resourceTeamId: number | null,
  currentUser: UserState
): 'all' | 'team' | 'own' | 'none' => {
  // Admin hoặc Division Manager có quyền truy cập tất cả
  if (currentUser.role === 'Admin' || currentUser.role === 'Division Manager') {
    return 'all';
  }
  
  // Leader chỉ truy cập dữ liệu trong team
  if (currentUser.role === 'Leader' && resourceTeamId === currentUser.teamId) {
    return 'team';
  }
  
  // Người dùng truy cập dữ liệu của chính mình
  if (resourceOwnerId === currentUser.id) {
    return 'own';
  }
  
  return 'none';
};
```

#### 7.3.2 Bảo vệ Routes

```typescript
// ProtectedRoute.tsx
import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { hasPermission } from './permissions';

interface ProtectedRouteProps {
  component: React.ComponentType<any>;
  requiredPermission?: string;
  path: string;
  exact?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  component: Component,
  requiredPermission,
  ...rest
}) => {
  const { isAuthenticated, permissions } = useSelector((state) => state.auth);
  
  return (
    <Route
      {...rest}
      render={(props) => {
        if (!isAuthenticated) {
          return <Redirect to="/login" />;
        }
        
        if (requiredPermission && !hasPermission(requiredPermission, permissions)) {
          return <Redirect to="/forbidden" />;
        }
        
        return <Component {...props} />;
      }}
    />
  );
};

export default ProtectedRoute;
```

#### 7.3.3 Bảo vệ UI Elements

```typescript
// PermissionGuard.tsx
import React from 'react';
import { useSelector } from 'react-redux';
import { hasPermission } from './permissions';

interface PermissionGuardProps {
  requiredPermission: string;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const PermissionGuard: React.FC<PermissionGuardProps> = ({
  requiredPermission,
  children,
  fallback = null,
}) => {
  const { permissions } = useSelector((state) => state.auth);
  
  if (hasPermission(requiredPermission, permissions)) {
    return <>{children}</>;
  }
  
  return <>{fallback}</>;
};

export default PermissionGuard;
```

### 7.4 Ứng dụng trong Thực tế

#### 7.4.1 Bảo vệ Routes

```typescript
// App.tsx
import { ProtectedRoute } from './components';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/login" component={LoginPage} />
        <ProtectedRoute 
          path="/employees" 
          component={EmployeeListPage} 
          requiredPermission="employee:read"
        />
        <ProtectedRoute 
          path="/opportunities" 
          component={OpportunityListPage} 
          requiredPermission="opportunity:read:all"
        />
        <ProtectedRoute 
          path="/contracts/create" 
          component={CreateContractPage} 
          requiredPermission="contract:create"
        />
        {/* ... */}
      </Switch>
    </Router>
  );
}
```

#### 7.4.2 Điều kiện hiển thị UI elements

```tsx
// EmployeeDetailPage.tsx
import { PermissionGuard } from './components';

function EmployeeDetailPage({ employee }) {
  return (
    <div>
      <h1>{employee.name}</h1>
      
      <PermissionGuard requiredPermission="employee:update:all">
        <button onClick={handleEdit}>Chỉnh sửa</button>
      </PermissionGuard>
      
      <PermissionGuard requiredPermission="employee:delete">
        <button onClick={handleDelete}>Xóa</button>
      </PermissionGuard>
      
      {/* Chỉ hiển thị nút đánh giá kỹ năng cho Leader hoặc Division Manager */}
      <PermissionGuard requiredPermission="employee-skill:evaluate">
        <button onClick={handleEvaluate}>Đánh giá kỹ năng</button>
      </PermissionGuard>
    </div>
  );
}
```

#### 7.4.3 API Calls với Phân quyền

```typescript
// api.ts
import axios from 'axios';
import { store } from './store';
import { hasPermission } from './permissions';

// Tạo axios instance
const api = axios.create({
  baseURL: '/api/v1',
});

// Thêm token vào header
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Kiểm tra quyền trước khi gọi API
export const callApiWithPermissionCheck = async (
  endpoint: string,
  method: 'GET' | 'POST' | 'PUT' | 'DELETE',
  requiredPermission: string,
  data?: any
) => {
  const { permissions } = store.getState().auth;
  
  if (!hasPermission(requiredPermission, permissions)) {
    throw new Error('Permission denied');
  }
  
  try {
    let response;
    switch (method) {
      case 'GET':
        response = await api.get(endpoint);
        break;
      case 'POST':
        response = await api.post(endpoint, data);
        break;
      case 'PUT':
        response = await api.put(endpoint, data);
        break;
      case 'DELETE':
        response = await api.delete(endpoint);
        break;
    }
    return response.data;
  } catch (error) {
    // Xử lý lỗi 401, 403, etc.
    throw error;
  }
};
```

### 7.5 Kiểm tra phạm vi dữ liệu trong components

Để kiểm tra quyền dựa trên dữ liệu cụ thể, Frontend cần thực hiện thêm logic:

```tsx
// OpportunityDetailPage.tsx
import { hasPermission, hasDataAccess } from './permissions';
import { useSelector } from 'react-redux';

function OpportunityDetailPage({ opportunity }) {
  const currentUser = useSelector(state => state.auth.user);
  const userPermissions = useSelector(state => state.auth.permissions);
  
  // Xác định mức độ truy cập dữ liệu
  const accessLevel = hasDataAccess(
    opportunity.createdBy.id,  // ID người tạo
    opportunity.assignedTo?.teamId,  // ID team của người được gán
    currentUser
  );
  
  // Kiểm tra xem người dùng có quyền chỉnh sửa cơ hội này không
  const canEdit = 
    hasPermission('opportunity:update:all', userPermissions) ||
    (hasPermission('opportunity:update:own', userPermissions) && accessLevel === 'own') ||
    (hasPermission('opportunity:update:assigned', userPermissions) && accessLevel === 'team');
  
  return (
    <div>
      <h1>{opportunity.name}</h1>
      
      {canEdit && (
        <button onClick={handleEdit}>Chỉnh sửa</button>
      )}
      
      {/* Hiển thị các tabs dựa trên quyền */}
      <Tabs>
        <Tab label="Chi tiết" />
        
        {hasPermission('opportunity-note:read:all', userPermissions) || 
         (hasPermission('opportunity-note:read:assigned', userPermissions) && accessLevel === 'team') && (
          <Tab label="Ghi chú" />
        )}
        
        {/* Chỉ hiển thị tab Lịch sử nếu có quyền xem log */}
        {hasPermission('opportunity-log:read:all', userPermissions) && (
          <Tab label="Lịch sử" />
        )}
      </Tabs>
    </div>
  );
}
```

### 7.6 Xử lý lỗi phân quyền

```typescript
// errorHandler.ts
export const handlePermissionError = (error, navigate) => {
  if (error.response) {
    switch (error.response.status) {
      case 401:
        // Token hết hạn hoặc không hợp lệ
        localStorage.removeItem('token');
        navigate('/login', { state: { message: 'Phiên làm việc đã hết hạn, vui lòng đăng nhập lại' } });
        break;
      case 403:
        // Không có quyền
        navigate('/forbidden', { 
          state: { 
            message: 'Bạn không có quyền thực hiện hành động này',
            code: error.response.data.code 
          } 
        });
        break;
      default:
        // Xử lý lỗi khác
        break;
    }
  }
};
```

---

## 8. Ví dụ Mẫu JSON Web Token

JWT được sử dụng trong hệ thống có cấu trúc payload như sau:

```json
{
  "sub": "123",                                       // User ID
  "name": "Nguyễn Văn A",                            // Tên người dùng
  "role": "Leader",                                   // Vai trò chính
  "teamId": 5,                                        // ID team/bộ phận (nếu có)
  "permissions": [                                    // Danh sách quyền
    "employee:read:team",
    "employee:update:team",
    "employee-skill:read:team",
    "employee-skill:evaluate",
    "opportunity:read:all",
    "opportunity:update:assigned",
    "dashboard:read:team",
    "report:read:team",
    "report:export"
  ],
  "iat": 1625097600,                                  // Thời gian phát hành
  "exp": 1625184000                                   // Thời gian hết hạn
}
```

JWT được ký bằng thuật toán HS256 hoặc RS256 để đảm bảo tính toàn vẹn. 