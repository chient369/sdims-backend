from typing import Dict, Any, Optional, List
from datetime import datetime
import time
import logging
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from repositories.base_repository import BaseRepository
from common.errors import DatabaseError

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TokenRepository(BaseRepository):
    """
    Repository for handling token blacklist operations in DynamoDB.
    """
    
    def add_to_blacklist(self, token_id: str, user_id: str, expires_at: int) -> Dict[str, Any]:
        """
        Add a token to the blacklist.
        
        Args:
            token_id: The JWT ID (jti) of the token
            user_id: The user ID associated with the token
            expires_at: The expiration timestamp (in seconds)
            
        Returns:
            Dict: The blacklisted token record
            
        Raises:
            DatabaseError: If a database error occurs
        """
        try:
            # Prepare current timestamp
            current_time = int(time.time())
            
            # Prepare blacklist item
            item = {
                "PK": f"BLACKLIST#TOKEN",
                "SK": f"TOKEN#{token_id}",
                "GSI1PK": f"USER#{user_id}",
                "GSI1SK": f"TOKEN#{token_id}",
                "token_id": token_id,
                "user_id": user_id,
                "expires_at": expires_at,
                "blacklisted_at": current_time,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Store in DynamoDB
            self.put_item(item)
            
            return item
        except ClientError as e:
            logger.error(f"Database error when blacklisting token {token_id}: {str(e)}")
            raise DatabaseError(f"Failed to blacklist token") from e
        except Exception as e:
            logger.error(f"Unexpected error when blacklisting token {token_id}: {str(e)}")
            raise DatabaseError(f"Failed to blacklist token") from e
            
    def is_token_blacklisted(self, token_id: str) -> bool:
        """
        Check if a token is blacklisted.
        
        Args:
            token_id: The JWT ID (jti) of the token
            
        Returns:
            bool: True if the token is blacklisted, False otherwise
            
        Raises:
            DatabaseError: If a database error occurs
        """
        try:
            key = {
                "PK": f"BLACKLIST#TOKEN",
                "SK": f"TOKEN#{token_id}"
            }
            
            item = self.get_item(key)
            
            return item is not None
        except ClientError as e:
            logger.error(f"Database error when checking blacklisted token {token_id}: {str(e)}")
            raise DatabaseError(f"Failed to check blacklisted token") from e
        except Exception as e:
            logger.error(f"Unexpected error when checking blacklisted token {token_id}: {str(e)}")
            raise DatabaseError(f"Failed to check blacklisted token") from e
            
    def get_user_blacklisted_tokens(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all blacklisted tokens for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            List[Dict]: List of blacklisted token records
            
        Raises:
            DatabaseError: If a database error occurs
        """
        try:
            # Using GSI1 (GSI1PK=USER#{user_id}, GSI1SK begins with TOKEN#)
            key_condition = Key("GSI1PK").eq(f"USER#{user_id}") & Key("GSI1SK").begins_with("TOKEN#")
            
            result = self.query(
                key_condition_expression=key_condition,
                index_name="GSI1"
            )
            
            return result.get("items", [])
        except ClientError as e:
            logger.error(f"Database error when getting blacklisted tokens for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve blacklisted tokens") from e
        except Exception as e:
            logger.error(f"Unexpected error when getting blacklisted tokens for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve blacklisted tokens") from e
    
    def cleanup_expired_tokens(self) -> int:
        """
        Clean up expired blacklisted tokens.
        This would typically be called by a scheduled Lambda function.
        
        Returns:
            int: Number of tokens removed
            
        Raises:
            DatabaseError: If a database error occurs
        """
        try:
            # Prepare current timestamp
            current_time = int(time.time())
            
            # Scan for expired tokens
            # Note: This would be inefficient for large tables, 
            # consider using a GSI with expires_at as the sort key
            filter_expression = Attr("expires_at").lt(current_time)
            
            result = self.scan(filter_expression=filter_expression)
            expired_tokens = result.get("items", [])
            
            # Delete expired tokens
            count = 0
            for token in expired_tokens:
                key = {
                    "PK": token["PK"],
                    "SK": token["SK"]
                }
                
                self.delete_item(key)
                count += 1
                
            return count
        except ClientError as e:
            logger.error(f"Database error when cleaning up expired tokens: {str(e)}")
            raise DatabaseError(f"Failed to clean up expired tokens") from e
        except Exception as e:
            logger.error(f"Unexpected error when cleaning up expired tokens: {str(e)}")
            raise DatabaseError(f"Failed to clean up expired tokens") from e 