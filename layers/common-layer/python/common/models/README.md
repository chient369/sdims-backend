# Model Mapping Utilities

This package provides utilities for mapping between DynamoDB items and Python model objects.

## Overview

The model mapping utilities allow you to define Python model classes that correspond to items in a DynamoDB table.
The utilities handle the conversion between the NoSQL/flat structure of DynamoDB and the object-oriented structure of Python.

Key features:
- Decorators for defining model structure and attributes
- Type converters for different data types
- Change tracking for model objects
- Integration with DynamoDBRepository for CRUD operations
- Support for GSI and complex data structures

## Key Components

- **BaseModel**: Base class for all model classes
- **Decorators**: For defining model structure, keys, and attributes
- **Converters**: For converting between Python types and DynamoDB representation
- **ModelMapper**: For converting between models and DynamoDB items
- **DynamoDBRepository Extensions**: Methods for working with models directly

## Usage

### Defining a Model

```python
from common.models import BaseModel, dynamodb_model, attribute, primary_key, sort_key
from common.models.converters import StringConverter, DateTimeConverter, BooleanConverter
from datetime import datetime
import uuid

@dynamodb_model(table_name="SDIMS_Main", entity_type="USER")
class User(BaseModel):
    @primary_key
    @attribute(converter=StringConverter)
    def id(self) -> str:
        return f"USER#{self._id}"
    
    @sort_key
    @attribute(converter=StringConverter)
    def metadata(self) -> str:
        return "METADATA"
    
    @attribute(name="_id", converter=StringConverter, auto_generate=lambda: str(uuid.uuid4()))
    def user_id(self) -> str:
        return self._id
    
    @attribute(converter=StringConverter)
    def username(self) -> str:
        return self._username
    
    @attribute(converter=StringConverter)
    def email(self) -> str:
        return self._email
    
    @attribute(converter=BooleanConverter, default_value=True)
    def is_active(self) -> bool:
        return self._is_active
    
    @attribute(converter=DateTimeConverter, auto_generate=datetime.now)
    def created_at(self) -> datetime:
        return self._created_at
    
    def __init__(self, username: str, email: str, is_active: bool = True, **kwargs):
        self._username = username
        self._email = email
        self._is_active = is_active
        super().__init__(**kwargs)
```

### Using with Repository

```python
from common.dynamodb import DynamoDBRepository

# Create repository
repo = DynamoDBRepository()

# Create a new user
user = User(username="johndoe", email="john.doe@example.com")
repo.save_model(user)

# Get user by ID
user = repo.get_model(User, id="123")

# Query users
users = repo.query_models(
    User, 
    key_condition_expression="id = :pk",
    expression_attribute_values={":pk": "USER#123"}
)

# Update user
user.username = "newusername"
repo.save_model(user)

# Delete user
repo.delete_model(user)
```

### Using Global Secondary Indexes (GSI)

```python
@dynamodb_model(table_name="SDIMS_Main")
class Employee(BaseModel):
    @primary_key
    @attribute(converter=StringConverter)
    def id(self) -> str:
        return f"EMPLOYEE#{self._id}"
    
    @sort_key
    @attribute(converter=StringConverter)
    def metadata(self) -> str:
        return "METADATA"
    
    @attribute(converter=StringConverter)
    @gsi_partition_key("GSI1")
    def email_index(self) -> str:
        return f"EMAIL#{self._email}"
    
    @attribute(converter=StringConverter)
    @gsi_sort_key("GSI1")
    def department_index(self) -> str:
        return f"DEPARTMENT#{self._department}"
    
    # ... other attributes

# Query using GSI
employees = repo.query_models(
    Employee,
    key_condition_expression="email_index = :email",
    expression_attribute_values={":email": "EMAIL#john.doe@example.com"},
    index_name="GSI1"
)
```

## Available Decorators

- `@dynamodb_model(table_name, entity_type)`: Define a DynamoDB model
- `@attribute(name, converter, auto_generate, default_value)`: Define a model attribute
- `@primary_key`: Mark attribute as primary key
- `@sort_key`: Mark attribute as sort key
- `@gsi_partition_key(index_name)`: Mark attribute as GSI partition key
- `@gsi_sort_key(index_name)`: Mark attribute as GSI sort key
- `@auto_generate(generator)`: Auto-generate values for attributes
- `@default_value(value)`: Define default values
- `@validate(validator, error_message)`: Validate attribute values

## Type Converters

- `StringConverter`: For string values
- `NumberConverter`: For numbers (int, float, decimal)
- `BooleanConverter`: For boolean values
- `UUIDConverter`: For UUID values
- `DateTimeConverter`: For datetime values
- `DateConverter`: For date values
- `EnumConverter`: For enum values
- `ListConverter`: For list values
- `SetConverter`: For set values
- `MapConverter`: For dictionary/map values
- `JsonConverter`: For JSON serialization
- `ModelConverter`: For embedded models 