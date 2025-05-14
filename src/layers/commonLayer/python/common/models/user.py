from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """
    User model representing a user in the system.
    Maps to USER entity in DynamoDB.
    """
    id: str
    username: str
    email: str
    full_name: str
    role_id: str
    is_active: bool = True
    password_hash: Optional[str] = None
    last_login_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """
        Create a User instance from dictionary data.
        
        Args:
            data: Dictionary containing user data from DynamoDB
            
        Returns:
            User: A User instance
        """
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            password_hash=data.get("password_hash"),
            email=data.get("email"),
            full_name=data.get("full_name"),
            role_id=data.get("role_id"),
            is_active=data.get("is_active", True),
            last_login_at=data.get("last_login_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            created_by=data.get("created_by"),
            updated_by=data.get("updated_by")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert User instance to dictionary for DynamoDB.
        
        Returns:
            Dict: Dictionary representation of the User
        """
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role_id": self.role_id,
            "is_active": self.is_active
        }
        
        # Add optional fields if they exist
        if self.password_hash:
            user_dict["password_hash"] = self.password_hash
        if self.last_login_at:
            user_dict["last_login_at"] = self.last_login_at
        if self.created_at:
            user_dict["created_at"] = self.created_at
        if self.updated_at:
            user_dict["updated_at"] = self.updated_at
        if self.created_by:
            user_dict["created_by"] = self.created_by
        if self.updated_by:
            user_dict["updated_by"] = self.updated_by
            
        return user_dict
    
    def to_response_dict(self) -> Dict[str, Any]:
        """
        Convert User instance to dictionary for API response (excluding sensitive data).
        
        Returns:
            Dict: Dictionary representation of the User for API response
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "last_login_at": self.last_login_at
        } 