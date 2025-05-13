"""
DynamoDB utilities for SDIMS backend.
"""
from typing import Any, Dict, List, Optional
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from aws_lambda_powertools import Logger
import json
import uuid
import logging
from datetime import datetime
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

# Kết nối đến DynamoDB
dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("DYNAMODB_TABLE", f"SDIMS-Main-{os.environ.get('STAGE', 'dev')}")
table = dynamodb.Table(table_name)

class DynamoDBRepository:
    """
    Repository class for DynamoDB operations.
    Implements common operations for DynamoDB tables.
    """
    
    def __init__(self, table_instance=None):
        """
        Initialize DynamoDB repository.
        
        Args:
            table_instance: Instance of DynamoDB table, if None uses default table
        """
        self.table = table_instance or table
        self.table_name = self.table.table_name
    
    def get_item(self, pk: str, sk: str) -> Dict[str, Any]:
        """
        Get an item from DynamoDB by primary key.
        
        Args:
            pk: Partition key
            sk: Sort key
            
        Returns:
            Dictionary containing item data
            
        Raises:
            Exception: If there is an error querying DynamoDB
        """
        try:
            response = self.table.get_item(
                Key={
                    'PK': pk,
                    'SK': sk
                }
            )
            return response.get('Item', {})
        except ClientError as e:
            logger.error(f"Error getting item from DynamoDB: {e}")
            raise
    
    def put_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add or update an item in DynamoDB.
        
        Args:
            item: Dictionary containing item data, including PK and SK
            
        Returns:
            Response from DynamoDB
            
        Raises:
            Exception: If there is an error adding item to DynamoDB
        """
        if 'PK' not in item or 'SK' not in item:
            raise ValueError("Item must contain PK and SK")
        
        try:
            # Add timestamp if not present
            if 'created_at' not in item:
                item['created_at'] = datetime.utcnow().isoformat()
            item['updated_at'] = datetime.utcnow().isoformat()
            
            response = self.table.put_item(
                Item=item
            )
            return response
        except ClientError as e:
            logger.error(f"Error putting item to DynamoDB: {e}")
            raise
    
    def delete_item(self, pk: str, sk: str) -> Dict[str, Any]:
        """
        Delete an item from DynamoDB.
        
        Args:
            pk: Partition key
            sk: Sort key
            
        Returns:
            Response from DynamoDB
            
        Raises:
            Exception: If there is an error deleting item from DynamoDB
        """
        try:
            response = self.table.delete_item(
                Key={
                    'PK': pk,
                    'SK': sk
                }
            )
            return response
        except ClientError as e:
            logger.error(f"Error deleting item from DynamoDB: {e}")
            raise
    
    def query(self, key_condition_expression: str, 
             expression_attribute_values: Dict[str, Any],
             index_name: Optional[str] = None,
             filter_expression: Optional[str] = None,
             projection_expression: Optional[str] = None,
             scan_index_forward: bool = True,
             limit: Optional[int] = None,
             exclusive_start_key: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a DynamoDB query with custom parameters.
        
        Args:
            key_condition_expression: Key condition expression
            expression_attribute_values: Expression attribute values
            index_name: Index name (if provided)
            filter_expression: Filter expression (if provided)
            projection_expression: Projection expression (if provided)
            scan_index_forward: Sort results in ascending (True) or descending (False) order
            limit: Limit the number of results returned (if provided)
            exclusive_start_key: Start key for pagination (if provided)
            
        Returns:
            Response từ DynamoDB
            
        Raises:
            Exception: Nếu có lỗi khi truy vấn DynamoDB
        """
        try:
            query_params = {
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ScanIndexForward': scan_index_forward
            }
            
            if index_name:
                query_params['IndexName'] = index_name
            
            if filter_expression:
                query_params['FilterExpression'] = filter_expression
            
            if projection_expression:
                query_params['ProjectionExpression'] = projection_expression
            
            if limit:
                query_params['Limit'] = limit
            
            if exclusive_start_key:
                query_params['ExclusiveStartKey'] = exclusive_start_key
            
            return self.table.query(**query_params)
        except ClientError as e:
            logger.error(f"Error querying DynamoDB: {e}")
            raise
    
    def generate_id(self) -> str:
        """
        Generate a random ID.
        
        Returns:
            Unique string ID
        """
        return str(uuid.uuid4())
    
    def batch_write(self, items: List[Dict[str, Any]]) -> None:
        """
        Write multiple items to DynamoDB in a batch transaction.
        
        Args:
            items: List of items to write to DynamoDB
            
        Raises:
            Exception: If there is an error performing batch write
        """
        try:
            with self.table.batch_writer() as batch:
                for item in items:
                    if 'created_at' not in item:
                        item['created_at'] = datetime.utcnow().isoformat()
                    item['updated_at'] = datetime.utcnow().isoformat()
                    batch.put_item(Item=item)
        except ClientError as e:
            logger.error(f"Error in batch write to DynamoDB: {e}")
            raise
    
    def transaction_write(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Thực hiện nhiều thao tác viết trong một giao dịch.
        
        Args:
            operations: Danh sách các thao tác viết (put, update, delete)
            
        Returns:
            Response từ DynamoDB
            
        Raises:
            Exception: Nếu có lỗi khi thực hiện transaction write
        """
        try:
            client = boto3.client('dynamodb')
            response = client.transact_write_items(
                TransactItems=operations
            )
            return response
        except ClientError as e:
            logger.error(f"Error in transaction write to DynamoDB: {e}")
            raise
    
    def scan(self, filter_expression: Optional[str] = None,
            expression_attribute_values: Optional[Dict[str, Any]] = None,
            projection_expression: Optional[str] = None,
            index_name: Optional[str] = None,
            limit: Optional[int] = None,
            exclusive_start_key: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Thực hiện scan DynamoDB với các tham số tùy chỉnh.
        
        Args:
            filter_expression: Biểu thức lọc (nếu có)
            expression_attribute_values: Giá trị thuộc tính biểu thức (nếu có)
            projection_expression: Biểu thức chiếu (nếu có)
            index_name: Tên của index (nếu có)
            limit: Giới hạn kết quả trả về (nếu có)
            exclusive_start_key: Khóa bắt đầu để phân trang (nếu có)
            
        Returns:
            Response từ DynamoDB
            
        Raises:
            Exception: Nếu có lỗi khi scan DynamoDB
        """
        try:
            scan_params = {}
            
            if filter_expression:
                scan_params['FilterExpression'] = filter_expression
            
            if expression_attribute_values:
                scan_params['ExpressionAttributeValues'] = expression_attribute_values
            
            if projection_expression:
                scan_params['ProjectionExpression'] = projection_expression
            
            if index_name:
                scan_params['IndexName'] = index_name
            
            if limit:
                scan_params['Limit'] = limit
            
            if exclusive_start_key:
                scan_params['ExclusiveStartKey'] = exclusive_start_key
            
            return self.table.scan(**scan_params)
        except ClientError as e:
            logger.error(f"Error scanning DynamoDB: {e}")
            raise

# Tạo instance mặc định của repository
dynamodb_repo = DynamoDBRepository()

def create_initial_data():
    """
    Create initial data for DynamoDB table.
    This function will create basic data like roles, permissions, and admin user.
    
    Returns:
        bool: True if successful, False if there is an error
    """
    try:
        # Create IDs for entities
        admin_role_id = str(uuid.uuid4())
        admin_user_id = str(uuid.uuid4())
        
        # Tạo admin role
        admin_role = {
            'PK': f'ROLE#{admin_role_id}',
            'SK': f'METADATA#{admin_role_id}',
            'GSI1PK': 'ROLE',
            'GSI1SK': 'Administrator',
            'id': admin_role_id,
            'name': 'Administrator',
            'description': 'Administrator role with full permissions',
            'permissions': ['ALL'],
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Tạo admin user với mật khẩu mặc định (sẽ yêu cầu đổi khi đăng nhập lần đầu)
        admin_user = {
            'PK': f'USER#{admin_user_id}',
            'SK': f'METADATA#{admin_user_id}',
            'GSI1PK': 'USER',
            'GSI1SK': 'admin',
            'GSI2PK': 'USER',
            'GSI2SK': 'admin@sdims.example.com',
            'id': admin_user_id,
            'username': 'admin',
            'password_hash': '$2b$12$B8oCZu9i/6Q5XVXzIdxjJ.YiYBSLNL6NUAgUZLKGT0BhRcDDRpMK2',  # "Admin@123"
            'email': 'admin@sdims.example.com',
            'full_name': 'System Administrator',
            'role_id': admin_role_id,
            'is_active': True,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Tạo liên kết user-role
        user_role = {
            'PK': f'USER#{admin_user_id}',
            'SK': f'ROLE#{admin_role_id}',
            'GSI1PK': f'ROLE#{admin_role_id}',
            'GSI1SK': f'USER#{admin_user_id}',
            'user_id': admin_user_id,
            'role_id': admin_role_id,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Tạo cấu hình margin mặc định
        margin_config_id = str(uuid.uuid4())
        margin_config = {
            'PK': 'MARGIN_CONFIG',
            'SK': f'CONFIG#{margin_config_id}',
            'GSI1PK': 'MARGIN_CONFIG',
            'GSI1SK': datetime.utcnow().isoformat(),
            'id': margin_config_id,
            'threshold_red': 10,
            'threshold_yellow': 20,
            'threshold_green': 30,
            'is_active': True,
            'effective_from': datetime.utcnow().isoformat(),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'created_by': admin_user_id
        }
        
        # Ghi dữ liệu vào DynamoDB
        items = [admin_role, admin_user, user_role, margin_config]
        dynamodb_repo.batch_write(items)
        
        logger.info("Initial data created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating initial data: {e}")
        return False 