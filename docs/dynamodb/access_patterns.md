# Access Patterns cho SDIMS DynamoDB

Tài liệu này mô tả chi tiết các access patterns (mẫu truy cập) cho DynamoDB trong hệ thống SDIMS.
Các patterns này được sử dụng để truy vấn và cập nhật dữ liệu trong single-table design.

## 1. Quản lý người dùng và phân quyền

### 1.1. Lấy thông tin chi tiết của một người dùng

```python
def get_user_by_id(user_id: str) -> Dict:
    return dynamodb_repo.get_item(f"USER#{user_id}", f"METADATA#{user_id}")
```

### 1.2. Tìm người dùng theo username

```python
def get_user_by_username(username: str) -> Dict:
    response = dynamodb_repo.query(
        key_condition_expression="GSI1PK = :pk AND GSI1SK = :sk",
        expression_attribute_values={
            ":pk": "USER",
            ":sk": username
        },
        index_name="GSI1"
    )
    return response.get("Items", [])[0] if response.get("Items") else None
```

### 1.3. Tìm người dùng theo email

```python
def get_user_by_email(email: str) -> Dict:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk AND GSI2SK = :sk",
        expression_attribute_values={
            ":pk": "USER",
            ":sk": email
        },
        index_name="GSI2"
    )
    return response.get("Items", [])[0] if response.get("Items") else None
```

### 1.4. Lấy danh sách vai trò của một người dùng

```python
def get_user_roles(user_id: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"USER#{user_id}",
            ":sk_prefix": "ROLE#"
        }
    )
    return response.get("Items", [])
```

### 1.5. Lấy danh sách quyền của một vai trò

```python
def get_role_permissions(role_id: str) -> Dict:
    return dynamodb_repo.get_item(f"ROLE#{role_id}", f"METADATA#{role_id}")
```

## 2. Quản lý nhân sự (HRM)

### 2.1. Tìm nhân viên theo mã nhân viên

```python
def get_employee_by_code(employee_code: str) -> Dict:
    response = dynamodb_repo.query(
        key_condition_expression="GSI1PK = :pk AND GSI1SK = :sk",
        expression_attribute_values={
            ":pk": "EMPLOYEE",
            ":sk": employee_code
        },
        index_name="GSI1"
    )
    return response.get("Items", [])[0] if response.get("Items") else None
```

### 2.2. Lọc nhân viên theo trạng thái

```python
def get_employees_by_status(status: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk",
        expression_attribute_values={
            ":pk": f"EMPLOYEE_STATUS#{status}"
        },
        index_name="GSI2"
    )
    return response.get("Items", [])
```

### 2.3. Lọc nhân viên theo team

```python
def get_employees_by_team(team_id: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI3PK = :pk",
        expression_attribute_values={
            ":pk": f"EMPLOYEE_TEAM#{team_id}"
        },
        index_name="GSI3"
    )
    return response.get("Items", [])
```

### 2.4. Lấy kỹ năng của một nhân viên

```python
def get_employee_skills(employee_id: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"EMPLOYEE#{employee_id}",
            ":sk_prefix": "SKILL#"
        }
    )
    return response.get("Items", [])
```

### 2.5. Tìm nhân viên có kỹ năng cụ thể với mức kinh nghiệm

```python
def get_employees_with_skill_experience(skill_id: str, min_years: int) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk AND GSI2SK >= :min_years",
        expression_attribute_values={
            ":pk": f"SKILL#{skill_id}",
            ":min_years": str(min_years)
        },
        index_name="GSI2"
    )
    return response.get("Items", [])
```

## 3. Quản lý dự án

### 3.1. Lấy dự án theo trạng thái

```python
def get_projects_by_status(status: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk",
        expression_attribute_values={
            ":pk": f"PROJECT_STATUS#{status}"
        },
        index_name="GSI2"
    )
    return response.get("Items", [])
```

### 3.2. Tìm dự án theo hợp đồng

```python
def get_projects_by_contract(contract_id: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI3PK = :pk",
        expression_attribute_values={
            ":pk": f"CONTRACT#{contract_id}"
        },
        index_name="GSI3"
    )
    return response.get("Items", [])
```

### 3.3. Lấy lịch sử dự án của nhân viên

```python
def get_employee_project_history(employee_id: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"EMPLOYEE#{employee_id}",
            ":sk_prefix": "PROJECT_HISTORY#"
        }
    )
    return response.get("Items", [])
```

## 4. Quản lý hợp đồng

### 4.1. Lấy chi tiết hợp đồng theo mã hợp đồng

```python
def get_contract_by_code(contract_code: str) -> Dict:
    response = dynamodb_repo.query(
        key_condition_expression="GSI1PK = :pk",
        expression_attribute_values={
            ":pk": f"CONTRACT_CODE#{contract_code}"
        },
        index_name="GSI1"
    )
    return response.get("Items", [])[0] if response.get("Items") else None
```

### 4.2. Lọc hợp đồng theo trạng thái

```python
def get_contracts_by_status(status: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk",
        expression_attribute_values={
            ":pk": f"CONTRACT_STATUS#{status}"
        },
        index_name="GSI2"
    )
    return response.get("Items", [])
```

### 4.3. Tìm hợp đồng theo khách hàng

```python
def get_contracts_by_customer(customer_name: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI3PK = :pk",
        expression_attribute_values={
            ":pk": f"CUSTOMER#{customer_name}"
        },
        index_name="GSI3"
    )
    return response.get("Items", [])
```

### 4.4. Lấy các điều khoản thanh toán của hợp đồng

```python
def get_contract_payment_terms(contract_id: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"CONTRACT#{contract_id}",
            ":sk_prefix": "PAYMENT_TERM#"
        }
    )
    return response.get("Items", [])
```

### 4.5. Lọc thanh toán theo trạng thái

```python
def get_payments_by_status(status: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI1PK = :pk",
        expression_attribute_values={
            ":pk": f"PAYMENT_STATUS#{status}"
        },
        index_name="GSI1"
    )
    return response.get("Items", [])
```

## 5. Quản lý cơ hội kinh doanh

### 5.1. Lấy tất cả cơ hội kinh doanh theo trạng thái

```python
def get_opportunities_by_stage(deal_stage: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk",
        expression_attribute_values={
            ":pk": f"OPPORTUNITY_STAGE#{deal_stage}"
        },
        index_name="GSI2"
    )
    return response.get("Items", [])
```

### 5.2. Lấy cơ hội kinh doanh được gán cho nhân viên sales

```python
def get_opportunities_by_sales(sales_id: str, followup_status: Optional[str] = None) -> List[Dict]:
    expression = "GSI3PK = :pk"
    values = {":pk": f"SALES#{sales_id}"}
    
    if followup_status:
        expression += " AND begins_with(GSI3SK, :sk_prefix)"
        values[":sk_prefix"] = f"OPPORTUNITY#{followup_status}"
    else:
        expression += " AND begins_with(GSI3SK, :sk_prefix)"
        values[":sk_prefix"] = "OPPORTUNITY#"
    
    response = dynamodb_repo.query(
        key_condition_expression=expression,
        expression_attribute_values=values,
        index_name="GSI3"
    )
    return response.get("Items", [])
```

### 5.3. Tìm kiếm cơ hội theo ID Hubspot

```python
def get_opportunity_by_hubspot_id(hubspot_id: str) -> Dict:
    response = dynamodb_repo.query(
        key_condition_expression="GSI1PK = :pk",
        expression_attribute_values={
            ":pk": f"HUBSPOT_OPPORTUNITY#{hubspot_id}"
        },
        index_name="GSI1"
    )
    return response.get("Items", [])[0] if response.get("Items") else None
```

## 6. Quản lý biên lợi nhuận

### 6.1. Lấy cấu hình ngưỡng biên lợi nhuận hiện tại

```python
def get_active_margin_configuration() -> Dict:
    response = dynamodb_repo.query(
        key_condition_expression="PK = :pk",
        expression_attribute_values={
            ":pk": "MARGIN_CONFIG"
        },
        filter_expression="is_active = :active",
        expression_attribute_values={
            ":pk": "MARGIN_CONFIG",
            ":active": True
        }
    )
    return response.get("Items", [])[0] if response.get("Items") else None
```

### 6.2. Lấy chi phí nhân viên theo tháng/năm

```python
def get_employee_cost(employee_id: str, year: int, month: int) -> Dict:
    return dynamodb_repo.get_item(
        f"EMPLOYEE#{employee_id}",
        f"COST#{year}#{month}"
    )
```

### 6.3. Lấy doanh thu nhân viên theo tháng/năm và hợp đồng

```python
def get_employee_revenue(employee_id: str, contract_id: str, year: int, month: int) -> Dict:
    return dynamodb_repo.get_item(
        f"EMPLOYEE#{employee_id}",
        f"REVENUE#{contract_id}#{year}#{month}"
    )
```

### 6.4. Lấy chi phí theo team và tháng

```python
def get_team_costs(team_id: str, year: int, month: int) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk AND begins_with(GSI2SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"TEAM#{team_id}",
            ":sk_prefix": f"COST#{year}#{month}"
        },
        index_name="GSI2"
    )
    return response.get("Items", [])
```

## 7. Thống kê và báo cáo

### 7.1. Lấy thông báo chưa đọc của người dùng

```python
def get_unread_notifications(user_id: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        filter_expression="is_read = :is_read",
        expression_attribute_values={
            ":pk": f"USER#{user_id}",
            ":sk_prefix": "NOTIFICATION#",
            ":is_read": False
        }
    )
    return response.get("Items", [])
```

### 7.2. Lọc thông báo theo mức độ ưu tiên

```python
def get_notifications_by_priority(priority: str) -> List[Dict]:
    response = dynamodb_repo.query(
        key_condition_expression="GSI2PK = :pk",
        expression_attribute_values={
            ":pk": f"NOTIFICATION_PRIORITY#{priority}"
        },
        index_name="GSI2"
    )
    return response.get("Items", [])
```

### 7.3. Lấy KPI của nhân viên sales theo thời gian

```python
def get_sales_kpi(sales_user_id: str, year: int, quarter: Optional[int] = None) -> List[Dict]:
    if quarter:
        response = dynamodb_repo.query(
            key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
            expression_attribute_values={
                ":pk": f"SALES#{sales_user_id}",
                ":sk_prefix": f"KPI#{year}#{quarter}"
            }
        )
    else:
        response = dynamodb_repo.query(
            key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
            expression_attribute_values={
                ":pk": f"SALES#{sales_user_id}",
                ":sk_prefix": f"KPI#{year}"
            }
        )
    return response.get("Items", [])
```

## 8. Lưu ý quan trọng về transactions và consistency

### 8.1. Sử dụng transactions khi cập nhật nhiều items liên quan

```python
def create_user_with_role(user_data: Dict, role_id: str) -> Dict:
    user_id = str(uuid.uuid4())
    
    user_item = {
        'PK': f'USER#{user_id}',
        'SK': f'METADATA#{user_id}',
        'GSI1PK': 'USER',
        'GSI1SK': user_data['username'],
        'GSI2PK': 'USER',
        'GSI2SK': user_data['email'],
        'id': user_id,
        # ...các trường khác
    }
    
    user_role_item = {
        'PK': f'USER#{user_id}',
        'SK': f'ROLE#{role_id}',
        'GSI1PK': f'ROLE#{role_id}',
        'GSI1SK': f'USER#{user_id}',
        'user_id': user_id,
        'role_id': role_id
    }
    
    # Sử dụng transaction để đảm bảo tất cả các items đều được tạo thành công
    operations = [
        {
            'Put': {
                'TableName': dynamodb_repo.table_name,
                'Item': user_item
            }
        },
        {
            'Put': {
                'TableName': dynamodb_repo.table_name,
                'Item': user_role_item
            }
        }
    ]
    
    dynamodb_repo.transaction_write(operations)
    return user_item
```

### 8.2. Consistency và denormalization

Khi dữ liệu được denormalize (sao chép) để tối ưu truy vấn, việc cập nhật tất cả các bản sao là cần thiết để duy trì tính nhất quán. Ví dụ:

```python
def update_employee_status(employee_id: str, new_status: str, project_id: Optional[str] = None) -> Dict:
    # 1. Lấy thông tin nhân viên hiện tại
    employee = dynamodb_repo.get_item(f"EMPLOYEE#{employee_id}", f"METADATA#{employee_id}")
    
    previous_status = employee.get('current_status')
    timestamp = datetime.utcnow().isoformat()
    
    # 2. Cập nhật thông tin nhân viên
    updated_employee = dynamodb_repo.update_item(
        f"EMPLOYEE#{employee_id}", 
        f"METADATA#{employee_id}",
        "SET current_status = :new_status, status_updated_at = :timestamp",
        {
            ":new_status": new_status,
            ":timestamp": timestamp
        }
    )
    
    # 3. Tạo log thay đổi trạng thái
    status_log = {
        'PK': f'EMPLOYEE#{employee_id}',
        'SK': f'STATUS_LOG#{timestamp}',
        'GSI1PK': f'STATUS#{new_status}',
        'GSI1SK': timestamp,
        'id': str(uuid.uuid4()),
        'employee_id': employee_id,
        'previous_status': previous_status,
        'new_status': new_status,
        'project_id': project_id,
        'log_timestamp': timestamp,
        'created_at': timestamp
    }
    
    dynamodb_repo.put_item(status_log)
    
    return updated_employee
``` 