"""
DynamoDB Utilities for SDIMS

This module provides utilities for working with DynamoDB.
"""

import os
import boto3
import json
from typing import Dict, Any, List, Optional, TypeVar, Generic, Union, Type
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
            keys: List of keys to retrieve
                
        Returns:
            List of retrieved items
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        if not keys:
            return []
            
        try:
            # DynamoDB limits batch operations to 100 items
            batch_size = 100
            result = []
            
            # Process in batches
            for i in range(0, len(keys), batch_size):
                batch_keys = keys[i:i + batch_size]
                
                # Format request for batch_get_item
                request_items = {
                    self.table_name: {
                        'Keys': batch_keys
                    }
                }
                
                response = self.dynamodb.batch_get_item(RequestItems=request_items)
                
                # Add retrieved items to result
                if self.table_name in response.get('Responses', {}):
                    result.extend(response['Responses'][self.table_name])
                
                # Handle unprocessed keys
                unprocessed = response.get('UnprocessedKeys', {})
                while unprocessed and self.table_name in unprocessed:
                    # Retry unprocessed keys
                    response = self.dynamodb.batch_get_item(RequestItems=unprocessed)
                    
                    # Add retrieved items to result
                    if self.table_name in response.get('Responses', {}):
                        result.extend(response['Responses'][self.table_name])
                    
                    # Update unprocessed keys
                    unprocessed = response.get('UnprocessedKeys', {})
            
            return result
        except ClientError as e:
            logger.exception(f"Error batch getting items")
            raise
    
    def batch_write_items(self, items: List[Dict[str, Any]], delete_keys: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Batch write (put/delete) items to DynamoDB table
        
        Args:
            items: List of items to put
            delete_keys: List of keys to delete
                
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        if not items and not delete_keys:
            return
            
        try:
            # DynamoDB limits batch operations to 25 items
            batch_size = 25
            
            # Prepare write requests
            put_requests = [{'PutRequest': {'Item': item}} for item in items] if items else []
            delete_requests = [{'DeleteRequest': {'Key': key}} for key in delete_keys] if delete_keys else []
            write_requests = put_requests + delete_requests
            
            # Process in batches
            for i in range(0, len(write_requests), batch_size):
                batch_requests = write_requests[i:i + batch_size]
                
                # Format request for batch_write_item
                request_items = {
                    self.table_name: batch_requests
                }
                
                response = self.dynamodb.batch_write_item(RequestItems=request_items)
                
                # Handle unprocessed items
                unprocessed = response.get('UnprocessedItems', {})
                while unprocessed and self.table_name in unprocessed:
                    # Retry unprocessed items
                    response = self.dynamodb.batch_write_item(RequestItems=unprocessed)
                    
                    # Update unprocessed items
                    unprocessed = response.get('UnprocessedItems', {})
        except ClientError as e:
            logger.exception(f"Error batch writing items")
            raise
    
    def _handle_unprocessed_items(self, response: Dict[str, Any]) -> None:
        """
        Handle unprocessed items from batch operations
        
        Args:
            response: Response from batch operation
        """
        unprocessed = response.get('UnprocessedItems', {})
        if unprocessed and self.table_name in unprocessed:
            logger.warning(f"Unprocessed items: {len(unprocessed[self.table_name])}")
            
            # TODO: Implement retry mechanism for unprocessed items
            # This is a placeholder for future implementation
            pass
    
    # Model-based methods
    
    def get_model(self, model_class: Type[T], **keys) -> Optional[T]:
        """
        Get model by key(s)
        
        Args:
            model_class: The model class
            **keys: Key values by name (e.g., id='123')
                
        Returns:
            Model instance or None if not found
            
        Raises:
            ValueError: If model keys are not properly defined
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.decorators import get_model_keys, _get_property_metadata
        from common.models.mapper import dynamodb_item_to_model
        
        # Get key field names
        key_map = get_model_keys(model_class)
        pk_field = key_map.get('primary_key')
        sk_field = key_map.get('sort_key')
        
        if not pk_field:
            raise ValueError(f"Model {model_class.__name__} does not define a primary key")
        
        # Get DB key names
        pk_meta = _get_property_metadata(model_class, pk_field)
        pk_db_name = pk_meta.get('name', pk_field)
        
        sk_db_name = None
        if sk_field:
            sk_meta = _get_property_metadata(model_class, sk_field)
            sk_db_name = sk_meta.get('name', sk_field)
        
        # Build key
        db_key = {}
        
        # Handle different key formats:
        # 1. Keys by field name: id='123', metadata='DATA'
        # 2. Direct key values: 'USER#123', 'METADATA'
        if keys:
            # Keys provided by name
            if pk_field in keys:
                # Create temporary instance to get formatted key
                from common.models.base_model import BaseModel
                temp_instance = model_class(**keys)
                pk_value = getattr(temp_instance, pk_field)
                db_key[pk_db_name] = pk_value
                
                if sk_field and sk_field in keys:
                    sk_value = getattr(temp_instance, sk_field)
                    db_key[sk_db_name] = sk_value
            else:
                # Direct key values
                if len(keys) == 1 and pk_db_name:
                    db_key[pk_db_name] = list(keys.values())[0]
                elif len(keys) == 2 and pk_db_name and sk_db_name:
                    values = list(keys.values())
                    db_key[pk_db_name] = values[0]
                    db_key[sk_db_name] = values[1]
                else:
                    raise ValueError(f"Invalid keys format for {model_class.__name__}")
        else:
            raise ValueError(f"No keys provided for {model_class.__name__}")
        
        # Get item from DynamoDB
        item = self.get_item(db_key)
        if not item:
            return None
        
        # Convert to model
        return dynamodb_item_to_model(model_class, item)
    
    def save_model(self, model: T) -> T:
        """
        Save model to DynamoDB
        
        Args:
            model: The model instance
                
        Returns:
            The saved model instance
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.mapper import model_to_dynamodb_item
        
        # Convert model to DynamoDB item
        item = model_to_dynamodb_item(model)
        
        # Save to DynamoDB
        self.put_item(item)
        
        # Mark model as clean
        model.mark_clean()
        
        return model
    
    def delete_model(self, model: T) -> None:
        """
        Delete model from DynamoDB
        
        Args:
            model: The model instance
                
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.mapper import generate_key
        
        # Generate key for the model
        key = generate_key(model)
        
        # Delete from DynamoDB
        self.delete_item(key)
    
    def query_models(self, 
                    model_class: Type[T],
                    key_condition_expression: str, 
                    expression_attribute_values: Dict[str, Any],
                    expression_attribute_names: Optional[Dict[str, str]] = None,
                    filter_expression: Optional[str] = None,
                    index_name: Optional[str] = None,
                    limit: Optional[int] = None,
                    scan_index_forward: bool = True,
                    exclusive_start_key: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        Query models from DynamoDB
        
        Args:
            model_class: The model class
            key_condition_expression: The condition that specifies the key values for items to be retrieved
            expression_attribute_values: Values that are substituted in the expression
            expression_attribute_names: Names that are substituted in the expression
            filter_expression: The filter expression to apply after query
            index_name: Name of the index to query
            limit: Maximum number of items to return
            scan_index_forward: Specifies the order for index traversal (True for forward, False for backwards)
            exclusive_start_key: The key to start the query from (for pagination)
                
        Returns:
            List of model instances
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.mapper import dynamodb_item_to_model
        
        # Execute query
        response = self.query(
            key_condition_expression=key_condition_expression,
            expression_attribute_values=expression_attribute_values,
            expression_attribute_names=expression_attribute_names,
            filter_expression=filter_expression,
            index_name=index_name,
            limit=limit,
            scan_index_forward=scan_index_forward,
            exclusive_start_key=exclusive_start_key
        )
        
        # Convert items to models
        items = response.get('Items', [])
        models = [dynamodb_item_to_model(model_class, item) for item in items]
        
        return models
    
    def scan_models(self,
                   model_class: Type[T],
                   filter_expression: Optional[str] = None,
                   expression_attribute_values: Optional[Dict[str, Any]] = None,
                   expression_attribute_names: Optional[Dict[str, str]] = None,
                   index_name: Optional[str] = None,
                   limit: Optional[int] = None,
                   exclusive_start_key: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        Scan models from DynamoDB
        
        Args:
            model_class: The model class
            filter_expression: The filter expression to apply during scan
            expression_attribute_values: Values that are substituted in the expression
            expression_attribute_names: Names that are substituted in the expression
            index_name: Name of the index to scan
            limit: Maximum number of items to return
            exclusive_start_key: The key to start the scan from (for pagination)
                
        Returns:
            List of model instances
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.mapper import dynamodb_item_to_model
        
        # Execute scan
        response = self.scan(
            filter_expression=filter_expression,
            expression_attribute_values=expression_attribute_values,
            expression_attribute_names=expression_attribute_names,
            index_name=index_name,
            limit=limit,
            exclusive_start_key=exclusive_start_key
        )
        
        # Convert items to models
        items = response.get('Items', [])
        models = [dynamodb_item_to_model(model_class, item) for item in items]
        
        return models
    
    def batch_get_models(self, model_class: Type[T], keys: List[Dict[str, Any]]) -> List[T]:
        """
        Batch get models from DynamoDB
        
        Args:
            model_class: The model class
            keys: List of keys to retrieve
                
        Returns:
            List of model instances
            
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.mapper import dynamodb_item_to_model
        
        # Execute batch get
        items = self.batch_get_items(keys)
        
        # Convert items to models
        models = [dynamodb_item_to_model(model_class, item) for item in items]
        
        return models
    
    def batch_save_models(self, models: List[T]) -> None:
        """
        Batch save models to DynamoDB
        
        Args:
            models: List of model instances
                
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.mapper import model_to_dynamodb_item
        
        # Convert models to DynamoDB items
        items = [model_to_dynamodb_item(model) for model in models]
        
        # Save to DynamoDB
        self.batch_write_items(items)
        
        # Mark models as clean
        for model in models:
            model.mark_clean()
    
    def batch_delete_models(self, models: List[T]) -> None:
        """
        Batch delete models from DynamoDB
        
        Args:
            models: List of model instances
                
        Raises:
            ClientError: If there is an error with the DynamoDB client
        """
        from common.models.mapper import generate_key
        
        # Generate keys for the models
        keys = [generate_key(model) for model in models]
        
        # Delete from DynamoDB
        self.batch_write_items([], keys) 