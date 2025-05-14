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


class UserRepository(BaseRepository):
    """
    Repository for handling User entity operations in DynamoDB.
    """
    
    def get_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Get a user by ID.
        
        Args:
            user_id: The user ID
            
        Returns:
            Dict: The user data
            
        Raises:
            NotFoundException: If user is not found
            DatabaseError: If a database error occurs
        """
        try:
            key = {
                "PK": f"USER#{user_id}",
                "SK": f"METADATA#{user_id}"
            }
            
            item = self.get_item(key)
            
            if not item:
                raise NotFoundException(f"User with ID {user_id} not found")
                
            return item
        except ClientError as e:
            logger.error(f"Database error when getting user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve user {user_id}") from e
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error when getting user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve user {user_id}") from e
    
    def get_by_username(self, username: str) -> Dict[str, Any]:
        """
        Get a user by username.
        
        Args:
            username: The username
            
        Returns:
            Dict: The user data
            
        Raises:
            NotFoundException: If user is not found
            DatabaseError: If a database error occurs
        """
        try:
            # Using GSI1 (GSI1PK=USER, GSI1SK=username)
            key_condition = Key("GSI1PK").eq("USER") & Key("GSI1SK").eq(username)
            
            result = self.query(
                key_condition_expression=key_condition,
                index_name="GSI1",
                limit=1
            )
            
            items = result.get("items", [])
            
            if not items:
                raise NotFoundException(f"User with username {username} not found")
                
            return items[0]
        except ClientError as e:
            logger.error(f"Database error when getting user by username {username}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve user with username {username}") from e
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error when getting user by username {username}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve user with username {username}") from e
    
    def get_by_email(self, email: str) -> Dict[str, Any]:
        """
        Get a user by email.
        
        Args:
            email: The email address
            
        Returns:
            Dict: The user data
            
        Raises:
            NotFoundException: If user is not found
            DatabaseError: If a database error occurs
        """
        try:
            # Using GSI2 (GSI2PK=USER, GSI2SK=email)
            key_condition = Key("GSI2PK").eq("USER") & Key("GSI2SK").eq(email)
            
            result = self.query(
                key_condition_expression=key_condition,
                index_name="GSI2",
                limit=1
            )
            
            items = result.get("items", [])
            
            if not items:
                raise NotFoundException(f"User with email {email} not found")
                
            return items[0]
        except ClientError as e:
            logger.error(f"Database error when getting user by email {email}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve user with email {email}") from e
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error when getting user by email {email}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve user with email {email}") from e
    
    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            user_data: The user data
            
        Returns:
            Dict: The created user data
            
        Raises:
            DatabaseError: If a database error occurs
        """
        try:
            # Generate a new ID if not provided
            if not user_data.get("id"):
                user_data["id"] = str(uuid.uuid4())
                
            current_time = datetime.utcnow().isoformat()
            user_data["created_at"] = current_time
            user_data["updated_at"] = current_time
            
            # Prepare DynamoDB item with appropriate keys
            item = {
                "PK": f"USER#{user_data['id']}",
                "SK": f"METADATA#{user_data['id']}",
                "GSI1PK": "USER",
                "GSI1SK": user_data["username"],
                "GSI2PK": "USER",
                "GSI2SK": user_data["email"],
                **user_data
            }
            
            self.put_item(item)
            return user_data
        except ClientError as e:
            logger.error(f"Database error when creating user: {str(e)}")
            raise DatabaseError("Failed to create user") from e
        except Exception as e:
            logger.error(f"Unexpected error when creating user: {str(e)}")
            raise DatabaseError("Failed to create user") from e
            
    def update(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a user.
        
        Args:
            user_id: The user ID
            update_data: The data to update
            
        Returns:
            Dict: The updated user data
            
        Raises:
            NotFoundException: If user is not found
            DatabaseError: If a database error occurs
        """
        try:
            # First, ensure the user exists
            current_user = self.get_by_id(user_id)
            
            # Update timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Prepare update expression and attribute values
            update_expression_parts = ["SET"]
            expression_attribute_values = {}
            expression_attribute_names = {}
            
            for key, value in update_data.items():
                # Skip primary key attributes
                if key in ["id", "PK", "SK", "GSI1PK", "GSI1SK", "GSI2PK", "GSI2SK"]:
                    continue
                    
                placeholder = f":val_{key}"
                name_placeholder = f"#{key}"
                
                update_expression_parts.append(f" {name_placeholder} = {placeholder},")
                expression_attribute_values[placeholder] = value
                expression_attribute_names[name_placeholder] = key
                
            # Remove trailing comma
            update_expression = "".join(update_expression_parts)[:-1]
            
            # Handle special case for username and email updates (GSI keys)
            if "username" in update_data:
                update_expression += ", GSI1SK = :new_username"
                expression_attribute_values[":new_username"] = update_data["username"]
                
            if "email" in update_data:
                update_expression += ", GSI2SK = :new_email"
                expression_attribute_values[":new_email"] = update_data["email"]
            
            # Perform update
            key = {
                "PK": f"USER#{user_id}",
                "SK": f"METADATA#{user_id}"
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
            logger.error(f"Database error when updating user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to update user {user_id}") from e
        except Exception as e:
            logger.error(f"Unexpected error when updating user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to update user {user_id}") from e
    
    def update_last_login(self, user_id: str) -> Dict[str, Any]:
        """
        Update the last login timestamp for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            Dict: The updated user data
            
        Raises:
            NotFoundException: If user is not found
            DatabaseError: If a database error occurs
        """
        try:
            # Simple update with just the last_login_at field
            update_data = {
                "last_login_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            return self.update(user_id, update_data)
        except NotFoundException:
            raise
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error when updating last login for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to update last login for user {user_id}") from e
    
    def get_user_role(self, user_id: str) -> Dict[str, Any]:
        """
        Get the role for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            Dict: The role data
            
        Raises:
            NotFoundException: If user or role is not found
            DatabaseError: If a database error occurs
        """
        try:
            # First, get the user to ensure it exists and to get the role_id
            user = self.get_by_id(user_id)
            role_id = user.get("role_id")
            
            if not role_id:
                raise NotFoundException(f"No role assigned to user {user_id}")
            
            # Get the role by its ID
            key = {
                "PK": f"ROLE#{role_id}",
                "SK": f"METADATA#{role_id}"
            }
            
            role = self.get_item(key)
            
            if not role:
                raise NotFoundException(f"Role with ID {role_id} not found")
                
            return role
        except NotFoundException:
            raise
        except ClientError as e:
            logger.error(f"Database error when getting role for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve role for user {user_id}") from e
        except Exception as e:
            logger.error(f"Unexpected error when getting role for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve role for user {user_id}") from e 