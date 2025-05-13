**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task service business rules và calculations | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa chi tiết công việc cần thực hiện để phát triển các dịch vụ xử lý tính toán và áp dụng business rules trong hệ thống, bao gồm tính toán margin, xác định trạng thái follow-up, và tính toán utilization rate.

# Chi tiết Task: Xây dựng service cho business rules và calculations

## Thông tin chung

**Task ID:** BE-BIZ-001  
**Task Name:** Xây dựng service cho business rules và calculations  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** BE-CORE-001, BE-CORE-002, BE-CORE-004, BE-INF-004  
**Các task phụ thuộc vào task này:** BE-MGN-002, BE-MGN-003, BE-OPP-003, BE-RPT-001, BE-RPT-002  
**Các API:** /api/v1/margins/employee, /api/v1/margins/summary, /api/v1/opportunities

## Mô tả

Task này tập trung vào việc phát triển các dịch vụ (services) chịu trách nhiệm tính toán các chỉ số kinh doanh quan trọng và áp dụng các business rules trong hệ thống. Các dịch vụ này sẽ bao gồm:

1. **Margin Calculation Service**: Tính toán margin dựa trên chi phí và doanh thu của nhân viên, xác định ngưỡng margin (Red/Yellow/Green).

2. **Follow-up Status Service**: Đánh giá và phân loại trạng thái follow-up của cơ hội kinh doanh dựa trên các tiêu chí như thời gian tương tác cuối, giai đoạn, và giá trị dự kiến.

3. **Utilization Rate Service**: Tính toán tỷ lệ sử dụng nguồn lực của nhân viên và team dựa trên thời gian phân bổ và dự án.

4. **Business Rule Engine**: Cơ chế quản lý và áp dụng các business rules cho toàn hệ thống.

Các dịch vụ này sẽ được triển khai dưới dạng module độc lập có thể tái sử dụng và tích hợp vào các Lambda functions khác nhau.

## Chi tiết công việc

### Phát triển Margin Calculation Service

- [ ] Xây dựng core functionality cho Margin Calculation:
  - Location: src/common/services/margin_service.py
  - Tạo class MarginCalculationService với các methods chính
  - Implement phương thức tính margin cá nhân: `calculate_employee_margin(employee_id, period)`
  - Implement phương thức tính margin theo team: `calculate_team_margin(team_id, period)`
  - Implement phương thức xác định trạng thái margin: `determine_margin_status(margin_value, thresholds)`
  - Tạo utilities để tổng hợp dữ liệu margin theo thời gian (tuần/tháng/quý)

- [ ] Phát triển Margin Threshold Configuration:
  - Location: src/common/services/margin_service.py
  - Tạo class MarginThresholdConfig để quản lý ngưỡng margin
  - Implement phương thức lấy ngưỡng hiện tại: `get_current_thresholds()`
  - Implement phương thức cập nhật ngưỡng: `update_thresholds(red, yellow, green)`
  - Tích hợp với DynamoDB để lưu và truy xuất cấu hình

- [ ] Xây dựng Margin History Tracking:
  - Location: src/common/services/margin_history_service.py
  - Tạo class MarginHistoryService để lưu và truy xuất lịch sử margin
  - Implement phương thức lưu history: `save_margin_history(employee_id, period, margin_data)`
  - Implement phương thức lấy history: `get_margin_history(employee_id, start_period, end_period)`
  - Tích hợp với DynamoDB để lưu và truy xuất dữ liệu

### Phát triển Follow-up Status Service

- [ ] Xây dựng core functionality cho Follow-up Status:
  - Location: src/common/services/followup_service.py
  - Tạo class FollowupStatusService với các methods chính
  - Implement phương thức đánh giá status: `evaluate_followup_status(opportunity_id)`
  - Implement phương thức xác định deadline dựa trên stage: `determine_followup_deadline(stage, last_interaction_date)`
  - Implement phương thức tính thời gian còn lại: `calculate_days_remaining(last_interaction_date, deadline_date)`

- [ ] Phát triển Follow-up Rules Configuration:
  - Location: src/common/services/followup_service.py
  - Tạo class FollowupRulesConfig để quản lý rules cho trạng thái follow-up
  - Implement phương thức lấy rules theo stage: `get_rules_by_stage(stage)`
  - Implement phương thức cập nhật rules: `update_rules(stage, days_yellow, days_red)`
  - Tích hợp với DynamoDB để lưu và truy xuất cấu hình

### Phát triển Utilization Rate Service

- [ ] Xây dựng core functionality cho Utilization Rate:
  - Location: src/common/services/utilization_service.py
  - Tạo class UtilizationService với các methods chính
  - Implement phương thức tính utilization cá nhân: `calculate_employee_utilization(employee_id, period)`
  - Implement phương thức tính utilization theo team: `calculate_team_utilization(team_id, period)`
  - Tạo utilities để tổng hợp dữ liệu utilization theo thời gian (tuần/tháng/quý)

- [ ] Phát triển Utilization Configuration:
  - Location: src/common/services/utilization_service.py
  - Tạo class UtilizationConfig để quản lý cấu hình tính utilization
  - Implement phương thức lấy cấu hình hiện tại: `get_current_config()`
  - Implement phương thức cập nhật cấu hình: `update_config(working_days_per_month, billable_threshold)`
  - Tích hợp với DynamoDB để lưu và truy xuất cấu hình

### Phát triển Business Rule Engine

- [ ] Xây dựng core Business Rule Engine:
  - Location: src/common/services/rule_engine.py
  - Tạo class BusinessRuleEngine với các methods chính
  - Implement cơ chế đăng ký rule: `register_rule(rule_id, rule_function, priority)`
  - Implement cơ chế thực thi rule: `execute_rules(context, rule_type)`
  - Implement cơ chế ghi log kết quả thực thi rule: `log_rule_execution(rule_id, context, result)`

- [ ] Phát triển Rule Definition System:
  - Location: src/common/services/rule_engine.py
  - Tạo class RuleDefinition để định nghĩa cấu trúc rule
  - Tạo utilities để quản lý rule dependencies
  - Implement cơ chế tải rule từ database hoặc config file

- [ ] Triển khai Scheduled Calculations:
  - Location: src/scheduled/calculation_handler.py
  - Tạo Lambda function cho việc tính toán định kỳ
  - Implement cơ chế lưu kết quả tính toán
  - Cấu hình CloudWatch Events/EventBridge triggers

### Phát triển Unit Tests

- [ ] Viết unit tests cho Margin Calculation Service:
  - Location: tests/common/services/test_margin_service.py
  - Test tính toán margin với các tình huống khác nhau
  - Test phân loại trạng thái margin
  - Test xử lý các trường hợp đặc biệt (division by zero, missing data)

- [ ] Viết unit tests cho Follow-up Status Service:
  - Location: tests/common/services/test_followup_service.py
  - Test đánh giá status với các tình huống khác nhau
  - Test logic xác định deadline
  - Test phân loại trạng thái follow-up

- [ ] Viết unit tests cho Utilization Rate Service:
  - Location: tests/common/services/test_utilization_service.py
  - Test tính toán utilization với các tình huống khác nhau
  - Test tổng hợp dữ liệu
  - Test xử lý dữ liệu không đầy đủ

- [ ] Viết unit tests cho Business Rule Engine:
  - Location: tests/common/services/test_rule_engine.py
  - Test đăng ký và thực thi rule
  - Test rule priorities và dependencies
  - Test error handling

### Tích hợp và Documentation

- [ ] Tích hợp với các services khác:
  - Tích hợp Margin Calculation Service với các Lambda functions liên quan
  - Tích hợp Follow-up Status Service với opportunity management
  - Tích hợp Utilization Rate Service với báo cáo

- [ ] Viết tài liệu API và hướng dẫn sử dụng:
  - Tạo API documentation cho các services
  - Viết hướng dẫn sử dụng chi tiết
  - Cung cấp ví dụ code

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng Margin Calculation Service:

```python
# Sử dụng Margin Calculation Service
from common.services.margin_service import MarginCalculationService, MarginPeriod

# Khởi tạo service
margin_service = MarginCalculationService()

# Tính margin cho một nhân viên trong tháng hiện tại
period = MarginPeriod.current_month()
employee_id = "EMP-12345"
margin_result = margin_service.calculate_employee_margin(employee_id, period)

# Kết quả trả về
print(f"Margin: {margin_result.margin_percentage}%")
print(f"Status: {margin_result.status}")  # 'RED', 'YELLOW', hoặc 'GREEN'
print(f"Revenue: ${margin_result.revenue}")
print(f"Cost: ${margin_result.cost}")

# Tính margin cho một team
team_id = "TEAM-67890"
team_margin = margin_service.calculate_team_margin(team_id, period)
print(f"Team Margin: {team_margin.margin_percentage}%")
```

Ví dụ về cách sử dụng Follow-up Status Service:

```python
# Sử dụng Follow-up Status Service
from common.services.followup_service import FollowupStatusService

# Khởi tạo service
followup_service = FollowupStatusService()

# Đánh giá status của một opportunity
opportunity_id = "OPP-123456"
status_result = followup_service.evaluate_followup_status(opportunity_id)

# Kết quả trả về
print(f"Status: {status_result.status}")  # 'RED', 'YELLOW', hoặc 'GREEN'
print(f"Days since last interaction: {status_result.days_since_interaction}")
print(f"Days remaining before deadline: {status_result.days_remaining}")
```

## Tiêu chí hoàn thành

1. Tất cả các services được phát triển đầy đủ và hoạt động chính xác
2. Unit tests đạt coverage ít nhất 80% cho tất cả các services
3. Các business rules được định nghĩa rõ ràng và có thể cấu hình
4. Performance đáp ứng yêu cầu (tính toán margin cho 100 nhân viên < 5 giây)
5. Tài liệu API và hướng dẫn sử dụng đầy đủ
6. Tích hợp thành công với các lambda functions liên quan

## Ước tính thời gian

- 6-8 ngày làm việc

## Ghi chú

- Các services cần được thiết kế để có thể mở rộng và thêm rules mới trong tương lai
- Cần xem xét hiệu suất khi xử lý dữ liệu lớn, đặc biệt là khi tính toán margin và utilization cho toàn bộ nhân viên
- Dữ liệu tính toán nên được cache ở một mức độ nhất định để tránh tính toán lại nhiều lần không cần thiết
- Cần đảm bảo các thao tác đọc/ghi database đều sử dụng connection pooling để tối ưu hiệu suất
- Nên sử dụng worker pattern hoặc queue để xử lý các tính toán định kỳ lớn 