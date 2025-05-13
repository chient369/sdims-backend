"""
Tests for repository integration with model mapping
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

from common.dynamodb import DynamoDBRepository
from common.models.base_model import BaseModel
from common.models.decorators import (
    dynamodb_model,
    attribute,
    primary_key,
    sort_key
)
from common.models.converters import StringConverter, DateTimeConverter, BooleanConverter


@dynamodb_model(table_name="TEST_TABLE")
class TestUser(BaseModel):
    @primary_key
    @attribute(converter=StringConverter)
    def id(self) -> str:
        return f"USER#{self._id}"
    
    @sort_key
    @attribute(converter=StringConverter)
    def metadata(self) -> str:
        return "METADATA"
    
    @attribute(converter=StringConverter)
    def username(self) -> str:
        return self._username
    
    @attribute(name="email_address", converter=StringConverter)
    def email(self) -> str:
        return self._email
    
    @attribute(converter=BooleanConverter, default_value=True)
    def is_active(self) -> bool:
        return self._is_active
    
    @attribute(converter=DateTimeConverter, auto_generate=datetime.now)
    def created_at(self) -> datetime:
        return self._created_at


class TestRepositoryWithModels(unittest.TestCase):
    def setUp(self):
        # Set up environment variable for table name
        os.environ['TABLE_NAME'] = 'TEST_TABLE'
        
        # Create a model instance for testing
        self.now = datetime.now()
        self.user = TestUser(
            id="123",
            username="testuser",
            email="test@example.com",
            created_at=self.now
        )
        
        # Expected DynamoDB item
        now_str = self.now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.expected_item = {
            "id": "USER#123",
            "metadata": "METADATA",
            "username": "testuser",
            "email_address": "test@example.com",
            "is_active": True,
            "created_at": now_str,
            "entity_type": "TEST_USER"
        }
        
        # Create patcher for DynamoDB table
        self.table_mock = MagicMock()
        self.dynamodb_mock = MagicMock()
        self.dynamodb_mock.Table.return_value = self.table_mock
        
        # Start the patcher
        self.patcher = patch('boto3.resource', return_value=self.dynamodb_mock)
        self.patcher.start()
        
        # Create repository
        self.repo = DynamoDBRepository()
    
    def tearDown(self):
        # Stop the patcher
        self.patcher.stop()
        
        # Clean up environment
        if 'TABLE_NAME' in os.environ:
            del os.environ['TABLE_NAME']
    
    def test_get_model(self):
        """Test get_model method"""
        # Set up mock response
        self.table_mock.get_item.return_value = {'Item': self.expected_item}
        
        # Test with field names
        user = self.repo.get_model(TestUser, id="123")
        
        # Verify correct key was used
        self.table_mock.get_item.assert_called_with(Key={"id": "USER#123", "metadata": "METADATA"})
        
        # Verify model was created correctly
        self.assertEqual(user.id, "USER#123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        
        # Test with direct key values
        self.repo.get_model(TestUser, "USER#123", "METADATA")
        # Verify correct key was used
        self.table_mock.get_item.assert_called_with(Key={"id": "USER#123", "metadata": "METADATA"})
        
        # Test item not found
        self.table_mock.get_item.return_value = {}
        user = self.repo.get_model(TestUser, id="456")
        self.assertIsNone(user)
    
    def test_save_model(self):
        """Test save_model method"""
        # Save the model
        result = self.repo.save_model(self.user)
        
        # Verify put_item was called with correct item
        self.table_mock.put_item.assert_called_once()
        args, kwargs = self.table_mock.put_item.call_args
        item = kwargs['Item']
        
        # Check key attributes
        self.assertEqual(item['id'], "USER#123")
        self.assertEqual(item['metadata'], "METADATA")
        self.assertEqual(item['username'], "testuser")
        self.assertEqual(item['email_address'], "test@example.com")
        
        # Verify model is marked clean
        self.assertFalse(result.is_dirty())
    
    def test_delete_model(self):
        """Test delete_model method"""
        # Delete the model
        self.repo.delete_model(self.user)
        
        # Verify delete_item was called with correct key
        self.table_mock.delete_item.assert_called_with(
            Key={"id": "USER#123", "metadata": "METADATA"},
            ReturnValues="NONE"
        )
    
    def test_query_models(self):
        """Test query_models method"""
        # Set up mock response
        self.table_mock.query.return_value = {
            'Items': [self.expected_item, self.expected_item],
            'Count': 2
        }
        
        # Query models
        users = self.repo.query_models(
            TestUser,
            key_condition_expression="id = :id",
            expression_attribute_values={":id": "USER#123"}
        )
        
        # Verify query was called correctly
        self.table_mock.query.assert_called_with(
            KeyConditionExpression="id = :id",
            ExpressionAttributeValues={":id": "USER#123"},
            ScanIndexForward=True,
            Select="ALL_ATTRIBUTES"
        )
        
        # Verify models were returned
        self.assertEqual(len(users), 2)
        self.assertIsInstance(users[0], TestUser)
        self.assertEqual(users[0].id, "USER#123")
    
    def test_scan_models(self):
        """Test scan_models method"""
        # Set up mock response
        self.table_mock.scan.return_value = {
            'Items': [self.expected_item, self.expected_item],
            'Count': 2
        }
        
        # Scan models
        users = self.repo.scan_models(
            TestUser,
            filter_expression="username = :username",
            expression_attribute_values={":username": "testuser"}
        )
        
        # Verify scan was called correctly
        self.table_mock.scan.assert_called_with(
            FilterExpression="username = :username",
            ExpressionAttributeValues={":username": "testuser"},
            Select="ALL_ATTRIBUTES"
        )
        
        # Verify models were returned
        self.assertEqual(len(users), 2)
        self.assertIsInstance(users[0], TestUser)
        self.assertEqual(users[0].id, "USER#123")
    
    def test_batch_operations(self):
        """Test batch operations with models"""
        # Set up mock responses
        self.dynamodb_mock.batch_get_item.return_value = {
            'Responses': {
                'TEST_TABLE': [self.expected_item]
            }
        }
        
        # Test batch_get_models
        keys = [{"id": "USER#123", "metadata": "METADATA"}]
        users = self.repo.batch_get_models(TestUser, keys)
        
        # Verify batch_get_item was called correctly
        self.dynamodb_mock.batch_get_item.assert_called_with(
            RequestItems={
                'TEST_TABLE': {
                    'Keys': keys
                }
            }
        )
        
        # Verify models were returned
        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], TestUser)
        self.assertEqual(users[0].id, "USER#123")
        
        # Test batch_save_models
        users = [self.user, self.user]
        self.repo.batch_save_models(users)
        
        # Verify batch_write_item was called with put requests
        self.dynamodb_mock.batch_write_item.assert_called()
        args, kwargs = self.dynamodb_mock.batch_write_item.call_args
        request_items = kwargs['RequestItems']['TEST_TABLE']
        
        # Verify there are two put requests
        self.assertEqual(len(request_items), 2)
        self.assertIn('PutRequest', request_items[0])
        
        # Test batch_delete_models
        self.repo.batch_delete_models(users)
        
        # Verify batch_write_item was called with delete requests
        args, kwargs = self.dynamodb_mock.batch_write_item.call_args
        request_items = kwargs['RequestItems']['TEST_TABLE']
        
        # Verify there are two delete requests
        self.assertEqual(len(request_items), 2)
        self.assertIn('DeleteRequest', request_items[0])
        self.assertEqual(request_items[0]['DeleteRequest']['Key']['id'], "USER#123")


if __name__ == '__main__':
    unittest.main() 