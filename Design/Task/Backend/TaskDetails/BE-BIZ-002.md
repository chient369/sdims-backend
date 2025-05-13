**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task service notification | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa chi tiết công việc cần thực hiện để phát triển hệ thống thông báo (notification) trong ứng dụng, bao gồm email notifications và in-app notifications với khả năng tạo template và lập lịch.

# Chi tiết Task: Phát triển service notification

## Thông tin chung

**Task ID:** BE-BIZ-002  
**Task Name:** Phát triển service notification  
**Độ ưu tiên:** Thấp  
**Phụ thuộc vào:** BE-CORE-001, BE-CORE-004, BE-INF-005, BE-INF-007  
**Các task phụ thuộc vào task này:** BE-OPP-004, BE-HRM-007, BE-CTR-002  
**Các API:** Không có API trực tiếp, sử dụng thông qua các API khác

## Mô tả

Task này tập trung vào việc phát triển dịch vụ thông báo (notification service) để gửi thông báo qua email và hiển thị thông báo trong ứng dụng (in-app notifications). Service này sẽ hỗ trợ:

1. **Email Notifications**: Gửi email thông báo sử dụng AWS SES (Simple Email Service) với khả năng tùy biến mẫu email (templates).

2. **In-app Notifications**: Tạo và quản lý các thông báo trong ứng dụng, lưu trữ trong DynamoDB và hiển thị cho người dùng.

3. **Notification Templates**: Quản lý templates cho các loại thông báo khác nhau.

4. **Scheduled Notifications**: Lập lịch gửi thông báo theo thời gian định kỳ hoặc dựa trên sự kiện.

Dịch vụ này sẽ là một phần quan trọng để thông báo cho người dùng về các sự kiện quan trọng trong hệ thống như: phân công cơ hội, cập nhật trạng thái nhân viên, cảnh báo thanh toán hợp đồng, cảnh báo margin, v.v.

## Chi tiết công việc

### Phát triển Email Notification System

- [ ] Xây dựng core functionality cho Email Service:
  - Location: src/common/services/notification/email_service.py
  - Tạo class EmailService với các methods chính
  - Implement phương thức gửi email: `send_email(recipients, subject, body, attachments=None)`
  - Tích hợp với AWS SES sử dụng boto3
  - Implement cơ chế xử lý lỗi và retry

- [ ] Phát triển Email Template Engine:
  - Location: src/common/services/notification/email_template.py
  - Tạo class EmailTemplateEngine với các methods chính
  - Implement phương thức render template: `render_template(template_name, context)`
  - Tạo các helper functions cho việc load templates
  - Hỗ trợ Jinja2 hoặc một template engine tương tự
  - Lưu trữ templates trong S3 hoặc tích hợp trong code

- [ ] Xây dựng Email Logging & Analytics:
  - Location: src/common/services/notification/email_logging.py
  - Tạo class EmailLogger để ghi log các email đã gửi
  - Implement phương thức log email: `log_email_sent(recipient, subject, status)`
  - Tích hợp với DynamoDB để lưu logs
  - Tạo các phương thức để truy vấn lịch sử email

### Phát triển In-app Notification System

- [ ] Xây dựng core functionality cho In-app Notification Service:
  - Location: src/common/services/notification/inapp_service.py
  - Tạo class InAppNotificationService với các methods chính
  - Implement phương thức tạo thông báo: `create_notification(user_id, message, priority, related_entity_type, related_entity_id)`
  - Implement phương thức lấy thông báo chưa đọc: `get_unread_notifications(user_id, limit=10)`
  - Implement phương thức đánh dấu đã đọc: `mark_as_read(notification_id)`
  - Tích hợp với DynamoDB để lưu trữ thông báo

- [ ] Phát triển In-app Notification Templates:
  - Location: src/common/services/notification/inapp_template.py
  - Tạo class NotificationTemplateManager
  - Implement phương thức tạo thông báo từ template: `create_from_template(template_key, user_id, context)`
  - Tạo các helper functions cho việc quản lý templates
  - Lưu trữ templates trong config hoặc database

- [ ] Phát triển Notification Expiry & Cleanup:
  - Location: src/common/services/notification/notification_cleanup.py
  - Tạo class NotificationCleanupService
  - Implement phương thức xóa thông báo hết hạn: `cleanup_expired_notifications(days_to_keep)`
  - Tạo Lambda function định kỳ để cleanup thông báo

### Phát triển Scheduled Notification System

- [ ] Xây dựng Scheduler Service:
  - Location: src/common/services/notification/scheduler.py
  - Tạo class NotificationScheduler với các methods chính
  - Implement phương thức lập lịch thông báo: `schedule_notification(notification_type, recipients, context, schedule_time)`
  - Implement phương thức hủy lịch: `cancel_scheduled_notification(schedule_id)`
  - Tích hợp với DynamoDB để lưu thông tin lịch

- [ ] Phát triển Worker Process:
  - Location: src/scheduled/notification_worker.py
  - Tạo Lambda function để xử lý các scheduled notifications
  - Implement logic để kiểm tra và gửi thông báo đến hạn
  - Cấu hình CloudWatch Events/EventBridge để trigger Lambda

- [ ] Xây dựng Event-based Triggers:
  - Location: src/common/services/notification/event_triggers.py
  - Tạo class NotificationEventHandler
  - Implement phương thức xử lý sự kiện: `handle_event(event_type, event_data)`
  - Tích hợp với SNS/SQS để nhận và xử lý events

### Phát triển Notification Use Cases

- [ ] Implement Opportunity Assignment Notifications:
  - Location: src/functions/opportunity/notifications.py
  - Tạo logic để gửi thông báo khi Leader được assign vào cơ hội
  - Tích hợp với Lambda function xử lý assignment

- [ ] Implement Employee Status Change Notifications:
  - Location: src/functions/employee/notifications.py
  - Tạo logic để gửi thông báo khi trạng thái nhân viên thay đổi
  - Tích hợp với Lambda function xử lý status change

- [ ] Implement Contract Payment Reminders:
  - Location: src/functions/contract/notifications.py
  - Tạo logic để gửi nhắc nhở về thanh toán hợp đồng
  - Tạo scheduled job để kiểm tra và gửi nhắc nhở

### Phát triển Unit Tests

- [ ] Viết unit tests cho Email Service:
  - Location: tests/common/services/notification/test_email_service.py
  - Test gửi email với các trường hợp khác nhau
  - Test xử lý templates
  - Test error handling

- [ ] Viết unit tests cho In-app Notification Service:
  - Location: tests/common/services/notification/test_inapp_service.py
  - Test tạo, đọc, cập nhật thông báo
  - Test pagination và filtering
  - Test integration với DynamoDB

- [ ] Viết unit tests cho Scheduler Service:
  - Location: tests/common/services/notification/test_scheduler.py
  - Test lập lịch, hủy lịch thông báo
  - Test xử lý sự kiện
  - Test cơ chế trigger

### Tích hợp và Documentation

- [ ] Tích hợp với các services khác:
  - Tích hợp notification service với các business processes
  - Tạo các helper functions để dễ dàng sử dụng service từ các Lambda functions khác

- [ ] Viết tài liệu API và hướng dẫn sử dụng:
  - Tạo API documentation cho notification service
  - Viết hướng dẫn tích hợp chi tiết
  - Cung cấp ví dụ code

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách sử dụng Email Service:

```python
# Sử dụng Email Service
from common.services.notification.email_service import EmailService
from common.services.notification.email_template import EmailTemplateEngine

# Khởi tạo services
email_service = EmailService()
template_engine = EmailTemplateEngine()

# Gửi email từ template
context = {
    "recipient_name": "John Doe",
    "opportunity_name": "Client XYZ Website Development",
    "opportunity_link": "https://app.example.com/opportunities/123456"
}

# Render template với context
email_body = template_engine.render_template("opportunity_assignment", context)

# Gửi email
result = email_service.send_email(
    recipients=["john.doe@example.com"],
    subject="New Opportunity Assignment",
    body=email_body
)

# Kiểm tra kết quả
if result.success:
    print(f"Email sent successfully. Message ID: {result.message_id}")
else:
    print(f"Failed to send email: {result.error_message}")
```

Ví dụ về cách sử dụng In-app Notification Service:

```python
# Sử dụng In-app Notification Service
from common.services.notification.inapp_service import InAppNotificationService

# Khởi tạo service
notification_service = InAppNotificationService()

# Tạo thông báo mới
notification_id = notification_service.create_notification(
    user_id="USER-123",
    message="Bạn đã được phân công vào cơ hội mới: Client XYZ Website Development",
    priority="high",
    related_entity_type="opportunity",
    related_entity_id="OPP-456"
)

# Lấy danh sách thông báo chưa đọc của người dùng
unread_notifications = notification_service.get_unread_notifications("USER-123")

for notification in unread_notifications:
    print(f"ID: {notification.id}")
    print(f"Message: {notification.message}")
    print(f"Created at: {notification.created_at}")
    print(f"Priority: {notification.priority}")
    
# Đánh dấu thông báo đã đọc
notification_service.mark_as_read(notification_id)
```

## Tiêu chí hoàn thành

1. Email notification service hoạt động ổn định và tích hợp thành công với AWS SES
2. In-app notification service đã được triển khai và có thể lưu trữ, truy xuất thông báo
3. Template engine hoạt động chính xác với khả năng tùy biến cao
4. Scheduled notification service có thể lập lịch và gửi thông báo đúng thời điểm
5. Tích hợp thành công với các business processes liên quan
6. Unit tests đạt coverage ít nhất 80% cho tất cả các services
7. Tài liệu API và hướng dẫn sử dụng đầy đủ

## Ước tính thời gian

- 5-7 ngày làm việc

## Ghi chú

- Cần đảm bảo tuân thủ các quy định về việc gửi email (anti-spam)
- In-app notifications cần được thiết kế với hiệu suất cao để xử lý lượng lớn thông báo
- Nên sử dụng caching để tối ưu hiệu năng khi truy vấn thông báo thường xuyên
- Cần triển khai cơ chế retry cho email delivery để đảm bảo độ tin cậy
- Đảm bảo thông báo được ghi log đầy đủ để debug và audit
- Cân nhắc về khả năng mở rộng để hỗ trợ các kênh thông báo khác trong tương lai (như Slack, SMS, etc.) 