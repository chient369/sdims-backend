from typing import Dict, List, Any, Optional
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import uuid
import logging
from datetime import datetime

from repositories.base_repository import BaseRepository
from common.errors import DatabaseError, NotFoundException

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RoleRepository(BaseRepository):
    """
    Repository for handling Role entity operations in DynamoDB.
    """
    
    def get_by_id(self, role_id: str) -> Dict[str, Any]:
        """
        Get a role by ID.
        
        Args:
            role_id: The role ID
            
        Returns:
            Dict: The role data
            
        Raises:
            NotFoundException: If role is not found
            DatabaseError: If a database error occurs
        """
        try:
            key = {
                "PK": f"ROLE#{role_id}",
                "SK": f"METADATA#{role_id}"
            }
            
            item = self.get_item(key)
            
            if not item:
                raise NotFoundException(f"Role with ID {role_id} not found")
                
            return item
        except ClientError as e:
            logger.error(f"Database error when getting role {role_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve role {role_id}") from e
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error when getting role {role_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve role {role_id}") from e
    
    def get_by_name(self, role_name: str) -> Dict[str, Any]:
        """
        Get a role by name.
        
        Args:
            role_name: The role name
            
        Returns:
            Dict: The role data
            
        Raises:
            NotFoundException: If role is not found
            DatabaseError: If a database error occurs
        """
        try:
            # Using GSI1 (GSI1PK=ROLE, GSI1SK=role_name)
            key_condition = Key("GSI1PK").eq("ROLE") & Key("GSI1SK").eq(role_name)
            
            result = self.query(
                key_condition_expression=key_condition,
                index_name="GSI1",
                limit=1
            )
            
            items = result.get("items", [])
            
            if not items:
                raise NotFoundException(f"Role with name {role_name} not found")
                
            return items[0]
        except ClientError as e:
            logger.error(f"Database error when getting role by name {role_name}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve role with name {role_name}") from e
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error when getting role by name {role_name}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve role with name {role_name}") from e
    
    def list_roles(self, limit: int = 50, last_evaluated_key: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all roles.
        
        Args:
            limit: Maximum number of roles to return
            last_evaluated_key: Key to start from for pagination
            
        Returns:
            Dict: List of roles and pagination info
            
        Raises:
            DatabaseError: If a database error occurs
        """
        try:
            # Using GSI1 (GSI1PK=ROLE)
            key_condition = Key("GSI1PK").eq("ROLE")
            
            result = self.query(
                key_condition_expression=key_condition,
                index_name="GSI1",
                limit=limit,
                exclusive_start_key=last_evaluated_key
            )
            
            return result
        except ClientError as e:
            logger.error(f"Database error when listing roles: {str(e)}")
            raise DatabaseError("Failed to list roles") from e
        except Exception as e:
            logger.error(f"Unexpected error when listing roles: {str(e)}")
            raise DatabaseError("Failed to list roles") from e
    
    def create(self, role_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new role.
        
        Args:
            role_data: The role data
            
        Returns:
            Dict: The created role data
            
        Raises:
            DatabaseError: If a database error occurs
        """
        try:
            # Generate a new ID if not provided
            if not role_data.get("id"):
                role_data["id"] = str(uuid.uuid4())
                
            current_time = datetime.utcnow().isoformat()
            role_data["created_at"] = current_time
            role_data["updated_at"] = current_time
            
            # Prepare DynamoDB item with appropriate keys
            item = {
                "PK": f"ROLE#{role_data['id']}",
                "SK": f"METADATA#{role_data['id']}",
                "GSI1PK": "ROLE",
                "GSI1SK": role_data["name"],
                **role_data
            }
            
            self.put_item(item)
            return role_data
        except ClientError as e:
            logger.error(f"Database error when creating role: {str(e)}")
            raise DatabaseError("Failed to create role") from e
        except Exception as e:
            logger.error(f"Unexpected error when creating role: {str(e)}")
            raise DatabaseError("Failed to create role") from e
            
    def update(self, role_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a role.
        
        Args:
            role_id: The role ID
            update_data: The data to update
            
        Returns:
            Dict: The updated role data
            
        Raises:
            NotFoundException: If role is not found
            DatabaseError: If a database error occurs
        """
        try:
            # First, ensure the role exists
            current_role = self.get_by_id(role_id)
            
            # Update timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Prepare update expression and attribute values
            update_expression_parts = ["SET"]
            expression_attribute_values = {}
            expression_attribute_names = {}
            
            for key, value in update_data.items():
                # Skip primary key attributes
                if key in ["id", "PK", "SK", "GSI1PK", "GSI1SK"]:
                    continue
                    
                placeholder = f":val_{key}"
                name_placeholder = f"#{key}"
                
                update_expression_parts.append(f" {name_placeholder} = {placeholder},")
                expression_attribute_values[placeholder] = value
                expression_attribute_names[name_placeholder] = key
                
            # Remove trailing comma
            update_expression = "".join(update_expression_parts)[:-1]
            
            # Handle special case for name update (GSI key)
            if "name" in update_data:
                update_expression += ", GSI1SK = :new_name"
                expression_attribute_values[":new_name"] = update_data["name"]
            
            # Perform update
            key = {
                "PK": f"ROLE#{role_id}",
                "SK": f"METADATA#{role_id}"
            }
            
            updated_item = self.update_item(
                key=key,
                update_expression=update_expression,
                expression_attribute_values=expression_attribute_values,
                expression_attribute_names=expression_attribute_names
            )
            
            return updated_item
        except NotFoundException:
            raise
        except ClientError as e:
            logger.error(f"Database error when updating role {role_id}: {str(e)}")
            raise DatabaseError(f"Failed to update role {role_id}") from e
        except Exception as e:
            logger.error(f"Unexpected error when updating role {role_id}: {str(e)}")
            raise DatabaseError(f"Failed to update role {role_id}") from e
    
    def delete(self, role_id: str) -> Dict[str, Any]:
        """
        Delete a role.
        
        Args:
            role_id: The role ID
            
        Returns:
            Dict: The deleted role data
            
        Raises:
            NotFoundException: If role is not found
            DatabaseError: If a database error occurs
        """
        try:
            # First, ensure the role exists
            current_role = self.get_by_id(role_id)
            
            # Delete the role
            key = {
                "PK": f"ROLE#{role_id}",
                "SK": f"METADATA#{role_id}"
            }
            
            deleted_item = self.delete_item(key)
            
            return deleted_item
        except NotFoundException:
            raise
        except ClientError as e:
            logger.error(f"Database error when deleting role {role_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete role {role_id}") from e
        except Exception as e:
            logger.error(f"Unexpected error when deleting role {role_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete role {role_id}") from e 