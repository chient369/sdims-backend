"""
Unit tests for DynamoDB utilities.
"""
import unittest
from unittest.mock import patch, MagicMock

from src.common.dynamodb import DynamoDBRepository


class TestDynamoDBRepository(unittest.TestCase):
    """Test cases for DynamoDB repository."""

    def setUp(self):
        """Set up test cases."""
        self.table_mock = MagicMock()
        self.table_name = "test-table"
        
        # Create a patcher for the boto3 resource
        self.boto3_patcher = patch('src.common.dynamodb.boto3.resource')
        self.boto3_mock = self.boto3_patcher.start()
        
        # Configure the mock
        self.dynamodb_mock = MagicMock()
        self.boto3_mock.return_value = self.dynamodb_mock
        self.dynamodb_mock.Table.return_value = self.table_mock
        
        # Create the repository
        self.repo = DynamoDBRepository(self.table_name)

    def tearDown(self):
        """Clean up after tests."""
        self.boto3_patcher.stop()

    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.repo.table_name, self.table_name)
        self.assertEqual(self.repo.table, self.table_mock)
        self.boto3_mock.assert_called_once_with('dynamodb')
        self.dynamodb_mock.Table.assert_called_once_with(self.table_name)

    def test_get_item(self):
        """Test get_item method."""
        # Setup
        key = {"id": "123"}
        expected_item = {"id": "123", "name": "Test Item"}
        
        self.table_mock.get_item.return_value = {"Item": expected_item}
        
        # Execute
        result = self.repo.get_item(key)
        
        # Assert
        self.assertEqual(result, expected_item)
        self.table_mock.get_item.assert_called_once_with(Key=key)

    def test_get_item_not_found(self):
        """Test get_item method when item not found."""
        # Setup
        key = {"id": "not-exist"}
        
        self.table_mock.get_item.return_value = {}
        
        # Execute
        result = self.repo.get_item(key)
        
        # Assert
        self.assertIsNone(result)
        self.table_mock.get_item.assert_called_once_with(Key=key)

    def test_put_item(self):
        """Test put_item method."""
        # Setup
        item = {"id": "123", "name": "Test Item"}
        expected_response = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        
        self.table_mock.put_item.return_value = expected_response
        
        # Execute
        result = self.repo.put_item(item)
        
        # Assert
        self.assertEqual(result, expected_response)
        self.table_mock.put_item.assert_called_once_with(Item=item)

    def test_update_item(self):
        """Test update_item method."""
        # Setup
        key = {"id": "123"}
        update_expression = "SET #name = :name"
        expression_attribute_values = {":name": "Updated Name"}
        expression_attribute_names = {"#name": "name"}
        
        expected_response = {
            "Attributes": {
                "id": "123",
                "name": "Updated Name"
            }
        }
        
        self.table_mock.update_item.return_value = expected_response
        
        # Execute
        result = self.repo.update_item(
            key, 
            update_expression, 
            expression_attribute_values,
            expression_attribute_names
        )
        
        # Assert
        self.assertEqual(result, expected_response)
        self.table_mock.update_item.assert_called_once_with(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues='ALL_NEW'
        )

    def test_delete_item(self):
        """Test delete_item method."""
        # Setup
        key = {"id": "123"}
        expected_response = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        
        self.table_mock.delete_item.return_value = expected_response
        
        # Execute
        result = self.repo.delete_item(key)
        
        # Assert
        self.assertEqual(result, expected_response)
        self.table_mock.delete_item.assert_called_once_with(Key=key)

    def test_query(self):
        """Test query method."""
        # Setup
        from boto3.dynamodb.conditions import Key, Attr
        
        key_condition = Key('id').eq('123')
        filter_expression = Attr('status').eq('active')
        index_name = "status-index"
        limit = 10
        
        expected_items = [
            {"id": "123", "name": "Test 1", "status": "active"},
            {"id": "123", "name": "Test 2", "status": "active"}
        ]
        
        expected_response = {
            "Items": expected_items,
            "Count": 2,
            "ScannedCount": 2
        }
        
        self.table_mock.query.return_value = expected_response
        
        # Execute
        result = self.repo.query(
            key_condition,
            filter_expression,
            index_name,
            limit
        )
        
        # Assert
        self.assertEqual(result, expected_response)
        self.table_mock.query.assert_called_once_with(
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expression,
            IndexName=index_name,
            Limit=limit,
            ScanIndexForward=True
        )


if __name__ == '__main__':
    unittest.main() 