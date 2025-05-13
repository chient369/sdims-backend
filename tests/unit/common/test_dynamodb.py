"""
Unit tests for common/dynamodb.py
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import boto3
from botocore.exceptions import ClientError
from common.dynamodb import DynamoDBRepository

class TestDynamoDBRepository(unittest.TestCase):
    """Test cases for DynamoDBRepository class"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {'TABLE_NAME': 'test-table'})
        self.env_patcher.start()
        
        # Mock boto3 resource
        self.boto3_resource_patcher = patch('boto3.resource')
        self.mock_boto3_resource = self.boto3_resource_patcher.start()
        
        # Create mock table
        self.mock_table = MagicMock()
        self.mock_resource = MagicMock()
        self.mock_resource.Table.return_value = self.mock_table
        self.mock_boto3_resource.return_value = self.mock_resource
        
        # Create repository instance
        self.repo = DynamoDBRepository()
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
        self.boto3_resource_patcher.stop()
    
    def test_init_with_table_name_param(self):
        """Test initializing repository with explicit table name"""
        repo = DynamoDBRepository(table_name='explicit-table')
        self.assertEqual(repo.table_name, 'explicit-table')
        self.mock_resource.Table.assert_called_with('explicit-table')
    
    def test_init_with_env_table_name(self):
        """Test initializing repository with table name from environment"""
        self.assertEqual(self.repo.table_name, 'test-table')
        self.mock_resource.Table.assert_called_with('test-table')
    
    def test_init_without_table_name(self):
        """Test initializing repository without table name raises error"""
        self.env_patcher.stop()  # Remove env var
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError):
                DynamoDBRepository()
        self.env_patcher.start()  # Restore env var
    
    def test_get_item(self):
        """Test get_item method"""
        # Mock response
        mock_response = {'Item': {'PK': 'test', 'SK': 'data', 'value': 'test-value'}}
        self.mock_table.get_item.return_value = mock_response
        
        # Call method
        key = {'PK': 'test', 'SK': 'data'}
        result = self.repo.get_item(key)
        
        # Verify
        self.mock_table.get_item.assert_called_with(Key=key)
        self.assertEqual(result, mock_response['Item'])
    
    def test_get_item_not_found(self):
        """Test get_item method when item not found"""
        # Mock response with no Item
        self.mock_table.get_item.return_value = {}
        
        # Call method
        key = {'PK': 'nonexistent', 'SK': 'data'}
        result = self.repo.get_item(key)
        
        # Verify
        self.mock_table.get_item.assert_called_with(Key=key)
        self.assertIsNone(result)
    
    def test_get_item_error(self):
        """Test get_item method when error occurs"""
        # Mock error
        error = ClientError(
            {'Error': {'Code': 'InternalServerError', 'Message': 'Test error'}},
            'get_item'
        )
        self.mock_table.get_item.side_effect = error
        
        # Call method
        key = {'PK': 'test', 'SK': 'data'}
        with self.assertRaises(ClientError):
            self.repo.get_item(key)
    
    def test_put_item(self):
        """Test put_item method"""
        # Mock response
        self.mock_table.put_item.return_value = {}
        
        # Call method
        item = {'PK': 'test', 'SK': 'data', 'value': 'test-value'}
        result = self.repo.put_item(item)
        
        # Verify
        self.mock_table.put_item.assert_called_with(Item=item)
        self.assertEqual(result, item)
    
    def test_update_item(self):
        """Test update_item method"""
        # Mock response
        mock_response = {'Attributes': {'updated': 'value'}}
        self.mock_table.update_item.return_value = mock_response
        
        # Call method
        key = {'PK': 'test', 'SK': 'data'}
        update_expression = 'SET #val = :val'
        expression_attribute_values = {':val': 'new-value'}
        expression_attribute_names = {'#val': 'value'}
        
        result = self.repo.update_item(
            key, 
            update_expression, 
            expression_attribute_values,
            expression_attribute_names
        )
        
        # Verify
        self.mock_table.update_item.assert_called_with(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues='UPDATED_NEW'
        )
        self.assertEqual(result, mock_response['Attributes'])
    
    def test_query(self):
        """Test query method"""
        # Mock response
        mock_response = {
            'Items': [{'PK': 'test', 'SK': 'data1'}, {'PK': 'test', 'SK': 'data2'}],
            'Count': 2,
            'ScannedCount': 2
        }
        self.mock_table.query.return_value = mock_response
        
        # Call method
        key_condition = 'PK = :pk'
        exp_values = {':pk': 'test'}
        result = self.repo.query(key_condition, exp_values)
        
        # Verify
        self.mock_table.query.assert_called_with(
            KeyConditionExpression=key_condition,
            ExpressionAttributeValues=exp_values,
            ScanIndexForward=True,
            Select='ALL_ATTRIBUTES'
        )
        self.assertEqual(result, mock_response)
    
    def test_scan(self):
        """Test scan method"""
        # Mock response
        mock_response = {
            'Items': [{'PK': 'test1', 'SK': 'data'}, {'PK': 'test2', 'SK': 'data'}],
            'Count': 2,
            'ScannedCount': 2
        }
        self.mock_table.scan.return_value = mock_response
        
        # Call method
        filter_expression = 'begins_with(SK, :sk)'
        exp_values = {':sk': 'data'}
        result = self.repo.scan(filter_expression, exp_values)
        
        # Verify
        self.mock_table.scan.assert_called_with(
            FilterExpression=filter_expression,
            ExpressionAttributeValues=exp_values,
            Select='ALL_ATTRIBUTES'
        )
        self.assertEqual(result, mock_response)
    
    def test_delete_item(self):
        """Test delete_item method"""
        # Mock response
        mock_response = {'Attributes': {'PK': 'test', 'SK': 'data'}}
        self.mock_table.delete_item.return_value = mock_response
        
        # Call method
        key = {'PK': 'test', 'SK': 'data'}
        result = self.repo.delete_item(key, return_values='ALL_OLD')
        
        # Verify
        self.mock_table.delete_item.assert_called_with(
            Key=key,
            ReturnValues='ALL_OLD'
        )
        self.assertEqual(result, mock_response['Attributes'])

if __name__ == '__main__':
    unittest.main() 