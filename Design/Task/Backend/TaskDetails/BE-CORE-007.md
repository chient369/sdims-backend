**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-07 | Chiến Trần Văn | Định nghĩa chi tiết task Database Migration Framework | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển một framework quản lý migration và seeding cho DynamoDB. Framework này sẽ cho phép quản lý phiên bản schema, thực hiện migration, và seeding dữ liệu một cách có kiểm soát.

# Chi tiết Task: BE-CORE-007 - Database Migration Framework

## Thông tin chung

**Task ID:** BE-CORE-007  
**Task Name:** Phát triển Database Migration Framework  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-CORE-001, BE-CORE-002, BE-INF-003  
**Các task phụ thuộc vào task này:** Tất cả các DB-xxx tasks

## Mô tả

Task này bao gồm việc phát triển một framework để quản lý schema và dữ liệu trong DynamoDB theo mô hình single-table design. Framework sẽ cho phép theo dõi và quản lý phiên bản của schema, thực hiện migration từ phiên bản này sang phiên bản khác, và seeding dữ liệu mẫu cho môi trường phát triển và testing. Framework cũng sẽ cung cấp các công cụ để đảm bảo tính nhất quán của dữ liệu trong quá trình migration.

## Chi tiết công việc

### Thiết kế Migration Framework Architecture

- [ ] Thiết kế kiến trúc tổng thể cho migration framework:
  - Mô hình migration versioning (phiên bản dựa trên timestamp)
  - Cấu trúc thư mục cho migration và seed scripts
  - Cơ chế theo dõi trạng thái migration đã thực hiện
  - Luồng thực thi migration và rollback
  - Cơ chế quản lý phiên bản cho single-table design

### Xây dựng Migration Tracking System

- [ ] Phát triển hệ thống theo dõi migration:
  - Lưu trữ thông tin migration trong DynamoDB (meta table hoặc trong main table)
  - Tracking thông tin như version, description, applied time, status
  - API để kiểm tra migration status và history
  - Cơ chế để lock table trong quá trình migration (tránh xung đột)
  - Logging chi tiết quá trình migration

### Phát triển Migration Script Framework

- [ ] Xây dựng framework cho script migration:
  - Tạo base class cho migration scripts
  - Cung cấp API để thao tác với DynamoDB
  - Hỗ trợ các thao tác phổ biến (tạo/cập nhật GSI, cập nhật item attributes)
  - Cơ chế transaction để đảm bảo atomicity
  - Hỗ trợ data transformation trong migration
  - API để rollback migration khi gặp lỗi

### Phát triển CLI Tool

- [ ] Xây dựng command-line interface cho migration framework:
  - Command để tạo migration script mới
  - Command để chạy migration (tất cả, đến version cụ thể)
  - Command để kiểm tra status của migration
  - Command để rollback migration
  - Command để reset database (chỉ dùng cho development)
  - Command để seed dữ liệu

### Phát triển Seed Data Framework

- [ ] Xây dựng framework cho seeding data:
  - Tạo base class cho seed scripts
  - Hỗ trợ các level seeding khác nhau (minimal, standard, full)
  - Cơ chế để seed dữ liệu có quan hệ phụ thuộc
  - Hỗ trợ seed data từ file (JSON, CSV)
  - Hỗ trợ seed random/fake data

### Xây dựng Batch Processing Component

- [ ] Phát triển component xử lý batch cho large-scale migrations:
  - Cơ chế để xử lý large datasets với pagination
  - Parallel processing cho migration
  - Monitoring progress của batch operations
  - Error handling và retry mechanism
  - Optimization cho throughput

### Xây dựng Schema Validation Component

- [ ] Phát triển component validation schema:
  - Kiểm tra tính hợp lệ của GSI
  - Validation các patterns cho data access trước khi migration
  - Kiểm tra tính nhất quán của data sau migration
  - Cảnh báo về các vấn đề tiềm ẩn (hot keys, large items)

### Phát triển Testing Component

- [ ] Xây dựng testing framework cho migrations:
  - Cơ chế để test migration trên môi trường local
  - Cơ chế để tạo test data
  - Assertions để kiểm tra tính chính xác của migration
  - Performance testing cho large migrations

### Phát triển Integration với CI/CD

- [ ] Xây dựng tích hợp với CI/CD pipeline:
  - Scripts để chạy migration tự động trong pipeline
  - Safety checks trước khi áp dụng migration
  - Rollback automation khi migration thất bại
  - Notifications khi migration hoàn thành hoặc thất bại

### Tạo Base Migrations

- [ ] Phát triển các migration scripts cơ bản:
  - Initial schema setup script
  - Global Secondary Indexes creation
  - Tạo metadata và configuration items
  - Setup permissions và system data

### Tạo Documentation và Examples

- [ ] Phát triển documentation và examples:
  - Hướng dẫn sử dụng migration framework
  - Best practices cho việc viết migration scripts
  - Guidelines cho data modeling với DynamoDB
  - Troubleshooting guide
  - Examples cho các use cases phổ biến

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách mong muốn sử dụng Database Migration Framework khi hoàn thành:

### Tạo Migration Script

Tạo migration script sử dụng CLI:

```bash
# Tạo migration script mới
python manage.py create_migration --name "add_employee_status_index"
```

Nội dung của migration script tạo ra:

```python
# migrations/20240807123456_add_employee_status_index.py
from common.migrations import Migration, MigrationContext

class AddEmployeeStatusIndex(Migration):
    """
    Migration to add GSI for querying employees by status
    """
    
    version = "20240807123456"
    description = "Add GSI for employee status"
    
    def up(self, context: MigrationContext):
        """
        Apply the migration
        """
        # Cập nhật DynamoDB table để thêm GSI mới
        context.update_table(
            GlobalSecondaryIndexUpdates=[
                {
                    "Create": {
                        "IndexName": "GSI2",
                        "KeySchema": [
                            {"AttributeName": "GSI2PK", "KeyType": "HASH"},
                            {"AttributeName": "GSI2SK", "KeyType": "RANGE"}
                        ],
                        "Projection": {
                            "ProjectionType": "ALL"
                        },
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 5,
                            "WriteCapacityUnits": 5
                        }
                    }
                }
            ],
            AttributeDefinitions=[
                {"AttributeName": "GSI2PK", "AttributeType": "S"},
                {"AttributeName": "GSI2SK", "AttributeType": "S"}
            ]
        )
        
        # Cập nhật tất cả employee items để thêm GSI keys
        employees = context.scan(
            FilterExpression="begins_with(PK, :pk_prefix)",
            ExpressionAttributeValues={
                ":pk_prefix": "EMPLOYEE#"
            }
        )
        
        for batch in context.batch_items(employees.get("Items", [])):
            with context.batch_writer() as batch_writer:
                for employee in batch:
                    status = employee.get("status", "ACTIVE")
                    
                    # Thêm GSI keys
                    employee["GSI2PK"] = f"STATUS#{status}"
                    employee["GSI2SK"] = employee["PK"]
                    
                    batch_writer.put_item(Item=employee)
                    
        context.log.info(f"Updated {len(employees.get('Items', []))} employee records")
    
    def down(self, context: MigrationContext):
        """
        Rollback the migration
        """
        # Xóa GSI attributes từ tất cả employee items
        employees = context.scan(
            FilterExpression="begins_with(PK, :pk_prefix)",
            ExpressionAttributeValues={
                ":pk_prefix": "EMPLOYEE#"
            }
        )
        
        for batch in context.batch_items(employees.get("Items", [])):
            with context.batch_writer() as batch_writer:
                for employee in batch:
                    # Xóa GSI keys
                    if "GSI2PK" in employee:
                        del employee["GSI2PK"]
                    if "GSI2SK" in employee:
                        del employee["GSI2SK"]
                    
                    batch_writer.put_item(Item=employee)
        
        # Xóa GSI
        context.update_table(
            GlobalSecondaryIndexUpdates=[
                {
                    "Delete": {
                        "IndexName": "GSI2"
                    }
                }
            ]
        )
        
        context.log.info("Rolled back employee status index")
```

### Chạy Migrations

Chạy tất cả migrations chưa được applied:

```bash
# Chạy tất cả pending migrations
python manage.py migrate

# Hoặc chạy đến một version cụ thể
python manage.py migrate --to 20240807123456

# Hoặc rollback một migration
python manage.py rollback --steps 1

# Xem trạng thái migration
python manage.py migration_status
```

### Tạo Seed Script

```python
# seeds/employee_seed.py
from common.seeds import Seed, SeedContext
import uuid
from datetime import datetime, timedelta
import random

class EmployeeSeed(Seed):
    """
    Seed data for employees
    """
    
    depends_on = ["department_seed"]  # Phụ thuộc vào seed departments
    
    def run(self, context: SeedContext, level="standard"):
        """
        Run the seed
        
        Levels:
        - minimal: Creates just a few core employees
        - standard: Creates a realistic set of employees (~50)
        - full: Creates a large set of employees for performance testing (~500)
        """
        departments = ["Engineering", "HR", "Sales", "Marketing", "Finance"]
        statuses = ["ACTIVE", "ON_LEAVE", "INACTIVE"]
        positions = ["Junior", "Mid-level", "Senior", "Lead", "Manager", "Director"]
        
        if level == "minimal":
            num_employees = 5
        elif level == "standard":
            num_employees = 50
        else:  # full
            num_employees = 500
            
        employees = []
        
        for i in range(num_employees):
            employee_id = str(uuid.uuid4())
            department = random.choice(departments)
            status = random.choice(statuses)
            position = random.choice(positions)
            
            # Calculate a random hire date in the past 5 years
            days_ago = random.randint(0, 365 * 5)
            hire_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            employee = {
                "PK": f"EMPLOYEE#{employee_id}",
                "SK": "METADATA",
                "GSI1PK": "EMPLOYEE",
                "GSI1SK": f"{department}#{position}#{employee_id}",
                "GSI2PK": f"STATUS#{status}",
                "GSI2SK": f"EMPLOYEE#{employee_id}",
                "id": employee_id,
                "first_name": f"FirstName{i}",
                "last_name": f"LastName{i}",
                "email": f"employee{i}@example.com",
                "department": department,
                "position": position,
                "status": status,
                "hire_date": hire_date,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            employees.append(employee)
            
        # Batch write employees to DynamoDB
        for batch in context.batch_items(employees, batch_size=25):
            with context.batch_writer() as batch_writer:
                for employee in batch:
                    batch_writer.put_item(Item=employee)
                    
        context.log.info(f"Seeded {num_employees} employees at level '{level}'")
```

### Chạy Seed Data

```bash
# Seed tất cả dữ liệu với level mặc định (standard)
python manage.py seed

# Seed với level cụ thể
python manage.py seed --level minimal

# Seed một class cụ thể
python manage.py seed --class EmployeeSeed

# Reset database và seed lại từ đầu (chỉ dùng cho development)
python manage.py reset_db --confirm
python manage.py migrate
python manage.py seed
```

## Tiêu chí hoàn thành

- Migration Framework được thiết kế và phát triển đầy đủ
- Migration Tracking System hoạt động chính xác
- CLI Tool hỗ trợ tất cả các tính năng cần thiết
- Seed Data Framework được triển khai
- Batch Processing Component hoạt động hiệu quả với large datasets
- Schema Validation Component hoạt động chính xác
- Integration với CI/CD được triển khai
- Base Migrations và Seeds được tạo
- Documentation và Examples được tạo
- Unit Tests và Integration Tests cho framework

## Ước tính thời gian

- 5-6 ngày làm việc

## Ghi chú

- Cần đặc biệt chú ý đến performance khi làm việc với large datasets
- DynamoDB có nhiều ràng buộc khác với SQL databases, cần điều chỉnh migration approach phù hợp
- Framework cần hỗ trợ cả local development và cloud environments
- Cần thiết kế để dễ dàng test migrations trước khi áp dụng vào production
- Rollback capability rất quan trọng, đặc biệt là cho migrations ảnh hưởng đến data
- Cần có logging chi tiết để debug migration issues
- Security là ưu tiên khi làm việc với production data 