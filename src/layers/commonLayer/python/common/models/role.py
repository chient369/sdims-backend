from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class Role:
    """
    Role model representing a user role in the system.
    Maps to ROLE entity in DynamoDB.
    """
    id: str
    name: str
    permissions: List[str]
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Role":
        """
        Create a Role instance from dictionary data.
        
        Args:
            data: Dictionary containing role data from DynamoDB
            
        Returns:
            Role: A Role instance
        """
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            permissions=data.get("permissions", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Role instance to dictionary for DynamoDB.
        
        Returns:
            Dict: Dictionary representation of the Role
        """
        role_dict = {
            "id": self.id,
            "name": self.name,
            "permissions": self.permissions
        }
        
        # Add optional fields if they exist
        if self.description:
            role_dict["description"] = self.description
        if self.created_at:
            role_dict["created_at"] = self.created_at
        if self.updated_at:
            role_dict["updated_at"] = self.updated_at
            
        return role_dict 