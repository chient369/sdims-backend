"""
Model definitions for Authentication
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from common.models.base_model import BaseModel
from common.models.decorators import (
    dynamodb_model,
    attribute,
    primary_key,
    sort_key,
    gsi_partition_key,
    gsi_sort_key,
    auto_generate,
    default_value,
    validate
)
from common.models.converters import (
    StringConverter,
    BooleanConverter,
    DateTimeConverter,
    ListConverter,
    EnumConverter
)


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


@dynamodb_model(table_name="SDIMS_Main", entity_type="USER")
class User(BaseModel):
    """
    User model for authentication and access control
    """
    
    @primary_key
    @attribute(converter=StringConverter)
    def id(self) -> str:
        """
        Primary key for the user
        Format: USER#{uuid}
        """
        return f"USER#{self._id}"
    
    @sort_key
    @attribute(converter=StringConverter)
    def metadata(self) -> str:
        """
        Sort key for the user
        Fixed value: METADATA
        """
        return "METADATA"
    
    @attribute(name="_id", converter=StringConverter, auto_generate=lambda: str(uuid.uuid4()))
    def user_id(self) -> str:
        """The unique ID for the user"""
        return self._id
    
    @attribute(converter=StringConverter)
    @validate(lambda x: x and len(x) >= 3, "Username must be at least 3 characters")
    def username(self) -> str:
        """Username for login"""
        return self._username
    
    @attribute(converter=StringConverter)
    @gsi_partition_key("GSI1")
    def email_index(self) -> str:
        """
        GSI1 partition key for email lookups
        Format: EMAIL#{email}
        """
        return f"EMAIL#{self._email}"
    
    @attribute(converter=StringConverter)
    @validate(lambda x: x and '@' in x, "Email must be valid")
    def email(self) -> str:
        """Email address"""
        return self._email
    
    @attribute(converter=StringConverter)
    def password_hash(self) -> str:
        """Hashed password"""
        return self._password_hash
    
    @attribute(converter=StringConverter)
    def full_name(self) -> str:
        """Full name of the user"""
        return self._full_name
    
    @attribute(converter=EnumConverter(UserRole))
    @default_value(UserRole.USER)
    def role(self) -> UserRole:
        """User role"""
        return self._role
    
    @attribute(converter=EnumConverter(UserStatus))
    @default_value(UserStatus.PENDING)
    @gsi_sort_key("GSI1")
    def status(self) -> UserStatus:
        """Account status"""
        return self._status
    
    @attribute(converter=ListConverter(StringConverter))
    @default_value([])
    def permissions(self) -> List[str]:
        """Special permissions"""
        return self._permissions
    
    @attribute(converter=BooleanConverter)
    @default_value(False)
    def email_verified(self) -> bool:
        """Whether email has been verified"""
        return self._email_verified
    
    @attribute(converter=DateTimeConverter)
    @auto_generate(datetime.now)
    def created_at(self) -> datetime:
        """Timestamp of account creation"""
        return self._created_at
    
    @attribute(converter=DateTimeConverter)
    @auto_generate(datetime.now)
    def updated_at(self) -> datetime:
        """Timestamp of last update"""
        return self._updated_at
    
    @attribute(converter=DateTimeConverter)
    def last_login(self) -> Optional[datetime]:
        """Timestamp of last login"""
        return self._last_login if hasattr(self, '_last_login') else None
    
    def __init__(
        self,
        username: str,
        email: str,
        password_hash: str,
        full_name: str,
        role: UserRole = UserRole.USER,
        status: UserStatus = UserStatus.PENDING,
        permissions: List[str] = None,
        email_verified: bool = False,
        last_login: Optional[datetime] = None,
        **kwargs
    ):
        """
        Initialize a new User
        
        Args:
            username: Username for login
            email: Email address
            password_hash: Hashed password
            full_name: Full name
            role: User role
            status: Account status
            permissions: Special permissions
            email_verified: Whether email is verified
            last_login: Last login timestamp
            **kwargs: Additional attributes
        """
        self._username = username
        self._email = email
        self._password_hash = password_hash
        self._full_name = full_name
        self._role = role
        self._status = status
        self._permissions = permissions or []
        self._email_verified = email_verified
        
        if last_login:
            self._last_login = last_login
            
        super().__init__(**kwargs) 