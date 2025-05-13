**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-04 | Chiến Trần Văn | Định nghĩa chi tiết task Event Bus & Message Queue | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển hệ thống Event Bus và Message Queue cho backend system. Hệ thống này sẽ cho phép giao tiếp và điều phối giữa các Lambda function thông qua pattern pub/sub, hỗ trợ các tác vụ bất đồng bộ và tăng khả năng mở rộng.

# Chi tiết Task: BE-CORE-004 - Event Bus & Message Queue

## Thông tin chung

**Task ID:** BE-CORE-004  
**Task Name:** Phát triển Event Bus & Message Queue  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-CORE-001, BE-INF-001  
**Các task phụ thuộc vào task này:** BE-SYS-xxx (Scheduled Tasks), BE-API-xxx (Asynchronous Operations)

## Mô tả

Task này bao gồm việc phát triển hệ thống Event Bus và Message Queue để hỗ trợ kiến trúc dựa trên sự kiện trong ứng dụng. Hệ thống này sẽ cho phép các thành phần khác nhau của ứng dụng giao tiếp với nhau thông qua các event, giúp giảm sự phụ thuộc trực tiếp và tăng khả năng mở rộng. Đây là nền tảng cho các tác vụ bất đồng bộ, xử lý đồng bộ dữ liệu với hệ thống bên ngoài (Hubspot), thông báo, và các tác vụ theo lịch.

## Chi tiết công việc

### Thiết kế Event Bus Architecture

- [ ] Thiết kế tổng thể kiến trúc event-driven:
  - Mô hình Publish-Subscribe (Pub/Sub)
  - Định nghĩa các event type và topic/channel
  - Quy tắc định danh và đặt tên cho events
  - Cấu trúc message chuẩn (schema)
  - Định nghĩa các queue và các kênh truyền tải event

### Cấu hình AWS Infrastructure cho Event Bus

- [ ] Cấu hình AWS EventBridge:
  - Tạo custom event bus cho hệ thống
  - Thiết lập event patterns và rules
  - Cấu hình permission model
  - Xác định cơ chế retry và dead-letter queue (DLQ)

- [ ] Cấu hình AWS SQS:
  - Tạo các SQS queue cho các loại xử lý khác nhau
  - Thiết lập visibility timeout, message retention, DLQ
  - Cấu hình Long-polling 
  - Xác định cơ chế scaling cho Lambda consumers

- [ ] Tích hợp với SNS:
  - Thiết lập SNS topics cho fan-out pattern
  - Cấu hình subscription filters
  - Thiết lập các subscription endpoint

### Xây dựng Event Publisher Component

- [ ] Phát triển lớp EventPublisher:
  - Phương thức publish_event() để gửi event lên event bus
  - Hỗ trợ định nghĩa metadata và event attribute cho routing
  - Triển khai cơ chế retry và circuit breaker
  - Cấu hình tracing và logging cho event publication

- [ ] Phát triển Event Object models:
  - Lớp BaseEvent với cấu trúc event chuẩn
  - Event types khác nhau kế thừa từ BaseEvent
  - Serialization/deserialization support
  - Validation trước khi publish

### Xây dựng Event Consumer Component

- [ ] Phát triển decorators và helpers cho Lambda event consumers:
  - Decorator `@event_handler` để đăng ký handler cho event type
  - Cơ chế tự động deserialization và validation
  - Xử lý lỗi và retry strategy
  - Tracing và logging cho event consumption

- [ ] Phát triển EventProcessor cho xử lý batch và queue:
  - Xử lý SQS message batches
  - Kiểm soát concurrency và throughput
  - Xử lý partial failures trong batch
  - Tối ưu hóa Lambda scaling cho queue processing

### Phát triển Event Registry và Catalog

- [ ] Xây dựng Event Registry để quản lý các event type:
  - Hệ thống đăng ký và discovery event types
  - Định nghĩa schema cho từng event type
  - Cơ chế versioning cho events
  - Documentation tự động cho event catalog

- [ ] Phát triển Event Catalog admin UI (nếu có thời gian):
  - Giao diện để xem các event type đã đăng ký
  - Tracking sự phụ thuộc giữa các service
  - Lịch sử và số liệu thống kê về event

### Xây dựng Message Queue Abstraction

- [ ] Phát triển MessageQueue abstract class:
  - Phương thức `send_message()` để gửi message vào queue
  - Phương thức `process_messages()` để xử lý message từ queue
  - Hỗ trợ message priority và delay
  - Cơ chế message visibility và ack/nack

- [ ] Triển khai SQSQueue concrete class:
  - Triển khai MessageQueue interface sử dụng AWS SQS
  - Tối ưu hóa batch operations
  - Xử lý throughput và throttling
  - Giám sát queue metrics

### Xây dựng Event-Driven Workflows

- [ ] Phát triển WorkflowEngine cho các quy trình phức tạp:
  - Định nghĩa workflow dạng mã hoặc cấu hình
  - Step functions integration (nếu cần)
  - Tracking workflow state
  - Error handling và recovery

- [ ] Triển khai các pattern hữu ích:
  - Saga pattern cho giao dịch phân tán
  - CQRS cho separation of concerns
  - Event sourcing cho audit trail (nếu cần)

### Xây dựng Event Replay và Recovery

- [ ] Phát triển cơ chế Event Replay:
  - Lưu trữ events vào event store
  - Replaying events cho recovery hoặc testing
  - Xây dựng checkpoint mechanism
  - Tracking và monitoring replay process

### Viết Unit Tests và Integration Tests

- [ ] Viết unit tests cho tất cả components:
  - Tests cho EventPublisher
  - Tests cho EventConsumer và decorators
  - Tests cho MessageQueue
  - Tests cho WorkflowEngine

- [ ] Viết integration tests cho end-to-end flows:
  - Publishing và consuming events
  - Queue processing và failure handling
  - Full workflow execution
  - Replay scenarios

### Xây dựng Monitoring và Alerting

- [ ] Thiết lập monitoring cho event system:
  - CloudWatch metrics và dashboard
  - Alerting cho event processing failures
  - Tracking end-to-end latency
  - Visibility vào queue depth và processing rate

### Tài liệu hóa và Examples

- [ ] Tạo tài liệu hướng dẫn sử dụng:
  - Cách publish events
  - Cách tạo event consumers
  - Best practices cho event-driven architecture
  - Troubleshooting guide
- [ ] Tạo các ví dụ mẫu cho các use case phổ biến

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách mong muốn sử dụng Event Bus khi hoàn thành:

### Publishing Events

```python
from common.events import EventPublisher, BaseEvent

class EmployeeCreatedEvent(BaseEvent):
    event_type = "employee.created"
    version = "1.0"
    
    def __init__(self, employee_id, employee_data):
        self.employee_id = employee_id
        self.employee_data = employee_data
        super().__init__()

# Trong Lambda function sau khi tạo employee thành công
def create_employee_handler(event, context):
    # Xử lý request và tạo employee
    employee_id = "EMP-12345"
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        # ...
    }
    
    # Publish event sau khi tạo thành công
    publisher = EventPublisher()
    publisher.publish_event(
        EmployeeCreatedEvent(
            employee_id=employee_id,
            employee_data=employee_data
        )
    )
    
    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Employee created successfully", "id": employee_id})
    }
```

### Consuming Events

```python
from common.events import event_handler

# Định nghĩa Lambda function để handle employee.created events
@event_handler(event_type="employee.created")
def handle_employee_created(event, context):
    # event data đã được deserialized thành Python object
    employee_id = event["payload"]["employee_id"]
    employee_data = event["payload"]["employee_data"]
    
    # Thực hiện các tác vụ như:
    # - Tạo tài khoản email
    # - Cập nhật metrics
    # - Gửi notification
    
    print(f"Processed employee creation for: {employee_id}")
    return True  # Thành công

# Định nghĩa Lambda function để handle queue messages
@event_handler(source="sqs")
def process_queue_messages(event, context):
    for record in event.get("Records", []):
        message_body = json.loads(record["body"])
        message_id = record["messageId"]
        
        # Xử lý message
        try:
            # Thực hiện task dựa trên message content
            print(f"Processed message: {message_id}")
        except Exception as e:
            # Log lỗi nhưng không retry message này
            print(f"Error processing message {message_id}: {str(e)}")
    
    return True
```

### Workflow Definition

```python
from common.workflows import Workflow, Step

# Định nghĩa quy trình onboarding nhân viên
onboarding_workflow = Workflow(
    name="employee_onboarding",
    steps=[
        Step(
            name="create_account",
            lambda_function="create_employee_account",
            retry_count=3
        ),
        Step(
            name="assign_equipment",
            lambda_function="assign_employee_equipment",
            retry_count=2
        ),
        Step(
            name="schedule_training",
            lambda_function="schedule_employee_training",
            condition=lambda data: data.get("position") == "Developer"
        ),
        Step(
            name="send_welcome_email",
            lambda_function="send_employee_welcome_email"
        )
    ]
)

# Bắt đầu workflow khi nhận employee.created event
@event_handler(event_type="employee.created")
def start_onboarding_workflow(event, context):
    employee_id = event["payload"]["employee_id"]
    employee_data = event["payload"]["employee_data"]
    
    workflow_execution = onboarding_workflow.start(
        input_data={
            "employee_id": employee_id,
            **employee_data
        }
    )
    
    print(f"Started onboarding workflow: {workflow_execution.execution_id}")
    return True
```

## Tiêu chí hoàn thành

- Infrastructure cho Event Bus và Message Queue được cấu hình đầy đủ
- EventPublisher, EventConsumer components được phát triển hoàn chỉnh
- MessageQueue abstraction và SQS implementation được hoàn thành
- Tất cả các components được unit test và integration test kỹ lưỡng
- Monitoring và alerting được thiết lập
- Tài liệu hướng dẫn và ví dụ được tạo
- Ít nhất 3 business workflow được triển khai sử dụng event system

## Ước tính thời gian

- 5-6 ngày làm việc

## Ghi chú

- Cần đảm bảo khả năng mở rộng và hiệu suất cao cho event bus
- Xử lý lỗi và retry strategy là vô cùng quan trọng để tránh mất dữ liệu
- Events nên được thiết kế để tương thích ngược (backward compatible)
- Đặc biệt chú ý đến security và permission model cho event bus
- Cần có mechanism cho việc debugging và troubleshooting
- Nên áp dụng idempotent processing để tránh xử lý trùng lặp 