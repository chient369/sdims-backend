import boto3
import os
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BaseRepository:
    """
    Base repository class for DynamoDB operations.
    Provides common operations for all repositories.
    """
    
    def __init__(self, table_name: str = None, dynamodb_client = None):
        """
        Initialize the repository with a DynamoDB table.
        
        Args:
            table_name: Name of the DynamoDB table
            dynamodb_client: Optional pre-configured DynamoDB resource
        """
        self.table_name = table_name or os.environ.get("DYNAMODB_TABLE", "SDIMS_Main")
        self.dynamodb = dynamodb_client or boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)
        
    def get_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get an item from DynamoDB by its key.
        
        Args:
            key: The primary key of the item to get
            
        Returns:
            Optional[Dict]: The item if found, None otherwise
            
        Raises:
            ClientError: If a DynamoDB error occurs
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get("Item")
        except ClientError as e:
            logger.error(f"Failed to get item with key {key}: {str(e)}")
            raise
            
    def put_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Put an item into DynamoDB.
        
        Args:
            item: The item to put
            
        Returns:
            Dict: The item that was put
            
        Raises:
            ClientError: If a DynamoDB error occurs
        """
        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            logger.error(f"Failed to put item: {str(e)}")
            raise
            
    def update_item(self, key: Dict[str, Any], update_expression: str, 
                   expression_attribute_values: Dict[str, Any],
                   expression_attribute_names: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Update an item in DynamoDB.
        
        Args:
            key: The primary key of the item to update
            update_expression: The update expression
            expression_attribute_values: Values for the update expression
            expression_attribute_names: Names for the update expression
            
        Returns:
            Dict: The updated item
            
        Raises:
            ClientError: If a DynamoDB error occurs
        """
        try:
            params = {
                "Key": key,
                "UpdateExpression": update_expression,
                "ExpressionAttributeValues": expression_attribute_values,
                "ReturnValues": "ALL_NEW"
            }
            
            if expression_attribute_names:
                params["ExpressionAttributeNames"] = expression_attribute_names
                
            response = self.table.update_item(**params)
            return response.get("Attributes", {})
        except ClientError as e:
            logger.error(f"Failed to update item with key {key}: {str(e)}")
            raise
            
    def delete_item(self, key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete an item from DynamoDB.
        
        Args:
            key: The primary key of the item to delete
            
        Returns:
            Dict: The deleted item
            
        Raises:
            ClientError: If a DynamoDB error occurs
        """
        try:
            response = self.table.delete_item(Key=key, ReturnValues="ALL_OLD")
            return response.get("Attributes", {})
        except ClientError as e:
            logger.error(f"Failed to delete item with key {key}: {str(e)}")
            raise
            
    def query(self, key_condition_expression, index_name: Optional[str] = None,
             filter_expression = None, limit: int = 20,
             exclusive_start_key: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query items from DynamoDB.
        
        Args:
            key_condition_expression: The key condition expression
            index_name: Name of the index to query
            filter_expression: Filter expression to apply
            limit: Maximum number of items to return
            exclusive_start_key: Key to start the query from (for pagination)
            
        Returns:
            Dict: Query result containing items and pagination info
            
        Raises:
            ClientError: If a DynamoDB error occurs
        """
        try:
            params = {
                "KeyConditionExpression": key_condition_expression,
                "Limit": limit
            }
            
            if index_name:
                params["IndexName"] = index_name
                
            if filter_expression:
                params["FilterExpression"] = filter_expression
                
            if exclusive_start_key:
                params["ExclusiveStartKey"] = exclusive_start_key
                
            response = self.table.query(**params)
            
            return {
                "items": response.get("Items", []),
                "last_evaluated_key": response.get("LastEvaluatedKey")
            }
        except ClientError as e:
            logger.error(f"Failed to query items: {str(e)}")
            raise
            
    def scan(self, filter_expression = None, index_name: Optional[str] = None,
            limit: int = 20, exclusive_start_key: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Scan items from DynamoDB.
        
        Args:
            filter_expression: Filter expression to apply
            index_name: Name of the index to scan
            limit: Maximum number of items to return
            exclusive_start_key: Key to start the scan from (for pagination)
            
        Returns:
            Dict: Scan result containing items and pagination info
            
        Raises:
            ClientError: If a DynamoDB error occurs
        """
        try:
            params = {
                "Limit": limit
            }
            
            if filter_expression:
                params["FilterExpression"] = filter_expression
                
            if index_name:
                params["IndexName"] = index_name
                
            if exclusive_start_key:
                params["ExclusiveStartKey"] = exclusive_start_key
                
            response = self.table.scan(**params)
            
            return {
                "items": response.get("Items", []),
                "last_evaluated_key": response.get("LastEvaluatedKey"),
                "count": response.get("Count", 0),
                "scanned_count": response.get("ScannedCount", 0)
            }
        except ClientError as e:
            logger.error(f"Failed to scan items: {str(e)}")
            raise 