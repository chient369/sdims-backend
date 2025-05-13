"""
DynamoDB Utilities for SDIMS

This module provides utilities for working with DynamoDB.
"""

import os
import boto3
import json
from typing import Dict, Any, List, Optional, TypeVar, Generic, Union
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger(service="dynamodb-utils")
T = TypeVar('T')

class DynamoDBRepository(Generic[T]):
    """
    Repository class for interacting with DynamoDB
    """
    
    def __init__(self, table_name: Optional[str] = None):
        """
        Initialize DynamoDB repository
        
        Args:
            table_name: Optional name of the DynamoDB table. If not provided, will use TABLE_NAME from environment.
        """
        self.table_name = table_name or os.environ.get('TABLE_NAME')
        if not self.table_name:
            raise ValueError("Table name must be provided or set as TABLE_NAME environment variable")
            
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)
        logger.debug(f"Initialized DynamoDBRepository for table {self.table_name}")
        
    def get_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get item from DynamoDB table
        
        Args:
            key: Key for retrieving the item, e.g. {"PK": "USER#123", "SK": "PROFILE"}
                
        Returns:
            Item from DynamoDB, or None if not found
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            logger.exception(f"Error getting item with key {key}")
            raise
    
    def put_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Put item into DynamoDB table
        
        Args:
            item: Item to store in DynamoDB
                
        Returns:
            The item that was stored
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            logger.exception(f"Error putting item {item}")
            raise
    
    def update_item(self, 
                  key: Dict[str, Any], 
                  update_expression: str,
                  expression_attribute_values: Dict[str, Any],
                  expression_attribute_names: Optional[Dict[str, str]] = None,
                  condition_expression: Optional[str] = None,
                  return_values: str = "UPDATED_NEW") -> Dict[str, Any]:
        """
        Update item in DynamoDB table
        
        Args:
            key: Key for identifying the item to update
            update_expression: The update expression for DynamoDB
            expression_attribute_values: Values that are substituted in the expression
            expression_attribute_names: Names that are substituted in the expression
            condition_expression: Condition to check before update
            return_values: What values to return after update
                
        Returns:
            The updated attributes
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            params = {
                'Key': key,
                'UpdateExpression': update_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ReturnValues': return_values
            }
            
            if expression_attribute_names:
                params['ExpressionAttributeNames'] = expression_attribute_names
                
            if condition_expression:
                params['ConditionExpression'] = condition_expression
                
            response = self.table.update_item(**params)
            return response.get('Attributes', {})
        except ClientError as e:
            logger.exception(f"Error updating item with key {key}")
            raise
    
    def delete_item(self, 
                   key: Dict[str, Any], 
                   condition_expression: Optional[str] = None,
                   expression_attribute_values: Optional[Dict[str, Any]] = None,
                   expression_attribute_names: Optional[Dict[str, str]] = None,
                   return_values: str = "NONE") -> Dict[str, Any]:
        """
        Delete item from DynamoDB table
        
        Args:
            key: Key for identifying the item to delete
            condition_expression: Condition to check before delete
            expression_attribute_values: Values that are substituted in the expression
            expression_attribute_names: Names that are substituted in the expression
            return_values: What values to return after delete
                
        Returns:
            The deleted item if return_values is ALL_OLD, otherwise empty dict
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            params = {
                'Key': key,
                'ReturnValues': return_values
            }
            
            if condition_expression:
                params['ConditionExpression'] = condition_expression
                
            if expression_attribute_values:
                params['ExpressionAttributeValues'] = expression_attribute_values
                
            if expression_attribute_names:
                params['ExpressionAttributeNames'] = expression_attribute_names
                
            response = self.table.delete_item(**params)
            return response.get('Attributes', {})
        except ClientError as e:
            logger.exception(f"Error deleting item with key {key}")
            raise
    
    def query(self, 
             key_condition_expression: str, 
             expression_attribute_values: Dict[str, Any],
             expression_attribute_names: Optional[Dict[str, str]] = None,
             filter_expression: Optional[str] = None,
             index_name: Optional[str] = None,
             limit: Optional[int] = None,
             scan_index_forward: bool = True,
             exclusive_start_key: Optional[Dict[str, Any]] = None,
             select: str = "ALL_ATTRIBUTES") -> Dict[str, Any]:
        """
        Query DynamoDB table or index
        
        Args:
            key_condition_expression: The condition that specifies the key values for items to be retrieved
            expression_attribute_values: Values that are substituted in the expression
            expression_attribute_names: Names that are substituted in the expression
            filter_expression: The filter expression to apply after query
            index_name: Name of the index to query
            limit: Maximum number of items to return
            scan_index_forward: Specifies the order for index traversal (True for forward, False for backwards)
            exclusive_start_key: The key to start the query from (for pagination)
            select: The attributes to return from the query
                
        Returns:
            Response from DynamoDB containing Items, Count, ScannedCount, and LastEvaluatedKey
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            params = {
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ScanIndexForward': scan_index_forward,
                'Select': select
            }
            
            if expression_attribute_names:
                params['ExpressionAttributeNames'] = expression_attribute_names
                
            if filter_expression:
                params['FilterExpression'] = filter_expression
                
            if index_name:
                params['IndexName'] = index_name
                
            if limit:
                params['Limit'] = limit
                
            if exclusive_start_key:
                params['ExclusiveStartKey'] = exclusive_start_key
            
            response = self.table.query(**params)
            return response
        except ClientError as e:
            logger.exception(f"Error querying with condition {key_condition_expression}")
            raise
    
    def scan(self,
            filter_expression: Optional[str] = None,
            expression_attribute_values: Optional[Dict[str, Any]] = None,
            expression_attribute_names: Optional[Dict[str, str]] = None,
            index_name: Optional[str] = None,
            limit: Optional[int] = None,
            exclusive_start_key: Optional[Dict[str, Any]] = None,
            select: str = "ALL_ATTRIBUTES") -> Dict[str, Any]:
        """
        Scan DynamoDB table or index
        
        Args:
            filter_expression: The filter expression to apply during scan
            expression_attribute_values: Values that are substituted in the expression
            expression_attribute_names: Names that are substituted in the expression
            index_name: Name of the index to scan
            limit: Maximum number of items to return
            exclusive_start_key: The key to start the scan from (for pagination)
            select: The attributes to return from the scan
                
        Returns:
            Response from DynamoDB containing Items, Count, ScannedCount, and LastEvaluatedKey
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            params = {
                'Select': select
            }
            
            if filter_expression:
                params['FilterExpression'] = filter_expression
                
            if expression_attribute_values:
                params['ExpressionAttributeValues'] = expression_attribute_values
                
            if expression_attribute_names:
                params['ExpressionAttributeNames'] = expression_attribute_names
                
            if index_name:
                params['IndexName'] = index_name
                
            if limit:
                params['Limit'] = limit
                
            if exclusive_start_key:
                params['ExclusiveStartKey'] = exclusive_start_key
            
            response = self.table.scan(**params)
            return response
        except ClientError as e:
            logger.exception("Error scanning table")
            raise
            
    def batch_get_items(self, keys: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Batch get items from DynamoDB table
        
        Args:
            keys: List of keys for items to retrieve
                
        Returns:
            List of items retrieved from DynamoDB
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            if not keys:
                return []
                
            # DynamoDB limits batch get to 100 items
            chunk_size = 100
            all_items = []
            
            # Process in chunks to avoid exceeding DynamoDB limits
            for i in range(0, len(keys), chunk_size):
                chunk = keys[i:i + chunk_size]
                response = self.dynamodb.batch_get_item(
                    RequestItems={
                        self.table_name: {
                            'Keys': chunk
                        }
                    }
                )
                
                if 'Responses' in response and self.table_name in response['Responses']:
                    all_items.extend(response['Responses'][self.table_name])
                    
                # Handle unprocessed items
                unprocessed = response.get('UnprocessedKeys', {}).get(self.table_name, {}).get('Keys', [])
                if unprocessed:
                    retry_response = self.dynamodb.batch_get_item(
                        RequestItems={
                            self.table_name: {
                                'Keys': unprocessed
                            }
                        }
                    )
                    if 'Responses' in retry_response and self.table_name in retry_response['Responses']:
                        all_items.extend(retry_response['Responses'][self.table_name])
                    
            return all_items
        except ClientError as e:
            logger.exception(f"Error batch getting {len(keys)} items")
            raise
            
    def batch_write_items(self, items: List[Dict[str, Any]], delete_keys: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Batch write (put or delete) items in DynamoDB table
        
        Args:
            items: List of items to put
            delete_keys: List of keys for items to delete
                
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        try:
            # DynamoDB limits batch write to 25 items
            chunk_size = 25
            
            # Process puts in chunks
            if items:
                for i in range(0, len(items), chunk_size):
                    chunk = items[i:i + chunk_size]
                    request_items = []
                    
                    for item in chunk:
                        request_items.append({
                            'PutRequest': {
                                'Item': item
                            }
                        })
                        
                    response = self.dynamodb.batch_write_item(
                        RequestItems={
                            self.table_name: request_items
                        }
                    )
                    
                    # Handle unprocessed items
                    self._handle_unprocessed_items(response)
            
            # Process deletes in chunks
            if delete_keys:
                for i in range(0, len(delete_keys), chunk_size):
                    chunk = delete_keys[i:i + chunk_size]
                    request_items = []
                    
                    for key in chunk:
                        request_items.append({
                            'DeleteRequest': {
                                'Key': key
                            }
                        })
                        
                    response = self.dynamodb.batch_write_item(
                        RequestItems={
                            self.table_name: request_items
                        }
                    )
                    
                    # Handle unprocessed items
                    self._handle_unprocessed_items(response)
                    
        except ClientError as e:
            item_count = len(items) if items else 0
            delete_count = len(delete_keys) if delete_keys else 0
            logger.exception(f"Error batch writing {item_count} items and deleting {delete_count} items")
            raise
            
    def _handle_unprocessed_items(self, response: Dict[str, Any]) -> None:
        """
        Handle unprocessed items from batch operations
        
        Args:
            response: The response from a batch operation that may contain unprocessed items
        """
        unprocessed = response.get('UnprocessedItems', {}).get(self.table_name, [])
        if unprocessed:
            retry_response = self.dynamodb.batch_write_item(
                RequestItems={
                    self.table_name: unprocessed
                }
            )
            # Could implement exponential backoff for multiple retries if needed 