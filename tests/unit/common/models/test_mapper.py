"""
Tests for model mapper
"""

import unittest
from datetime import datetime

from common.models.base_model import BaseModel
from common.models.decorators import (
    dynamodb_model,
    attribute,
    primary_key,
    sort_key,
    gsi_partition_key,
    gsi_sort_key
)
from common.models.converters import StringConverter, DateTimeConverter, BooleanConverter
from common.models.mapper import (
    model_to_dynamodb_item,
    dynamodb_item_to_model,
    generate_key,
    generate_gsi_keys,
    ModelMapper
)


@dynamodb_model(table_name="TEST_TABLE", entity_type="USER")
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
    
    @attribute(converter=StringConverter)
    @gsi_partition_key("GSI1")
    def email_index(self) -> str:
        return f"EMAIL#{self._email}"
    
    @attribute(converter=StringConverter)
    @gsi_sort_key("GSI1")
    def status_index(self) -> str:
        return f"STATUS#{self._status}"
    
    @attribute(name="email_address", converter=StringConverter)
    def email(self) -> str:
        return self._email
    
    @attribute(converter=BooleanConverter, default_value=True)
    def is_active(self) -> bool:
        return self._is_active
    
    @attribute(converter=DateTimeConverter, auto_generate=datetime.now)
    def created_at(self) -> datetime:
        return self._created_at
    
    @attribute(converter=StringConverter)
    def status(self) -> str:
        return self._status


class TestMapper(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now()
        now_str = self.now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Create a model instance
        self.user = TestUser(
            id="123",
            username="testuser",
            email="test@example.com",
            status="active",
            created_at=self.now
        )
        
        # Expected DynamoDB item
        self.expected_item = {
            "id": "USER#123",
            "metadata": "METADATA",
            "username": "testuser",
            "email_index": "EMAIL#test@example.com",
            "status_index": "STATUS#active",
            "email_address": "test@example.com",
            "is_active": True,
            "created_at": now_str,
            "status": "active",
            "entity_type": "USER"
        }
    
    def test_model_to_dynamodb_item(self):
        """Test converting model to DynamoDB item"""
        item = model_to_dynamodb_item(self.user)
        
        # Compare all expected attributes
        for key, value in self.expected_item.items():
            self.assertIn(key, item)
            if key != "created_at":  # Skip datetime comparison
                self.assertEqual(item[key], value)
    
    def test_dynamodb_item_to_model(self):
        """Test converting DynamoDB item to model"""
        # Convert model to DynamoDB item and back
        item = model_to_dynamodb_item(self.user)
        user = dynamodb_item_to_model(TestUser, item)
        
        # Compare model attributes
        self.assertEqual(user.id, "USER#123")
        self.assertEqual(user.metadata, "METADATA")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.status, "active")
        self.assertTrue(user.is_active)
    
    def test_generate_key(self):
        """Test generating key from model"""
        key = generate_key(self.user)
        
        self.assertEqual(key, {
            "id": "USER#123",
            "metadata": "METADATA"
        })
    
    def test_generate_gsi_keys(self):
        """Test generating GSI keys from model"""
        gsi_keys = generate_gsi_keys(self.user, "GSI1")
        
        self.assertEqual(gsi_keys, {
            "email_index": "EMAIL#test@example.com",
            "status_index": "STATUS#active"
        })
        
        # Test non-existent GSI
        with self.assertRaises(ValueError):
            generate_gsi_keys(self.user, "GSI_NONEXISTENT")
    
    def test_model_mapper(self):
        """Test ModelMapper class"""
        # Test to_dynamodb_item
        item = ModelMapper.to_dynamodb_item(self.user)
        for key, value in self.expected_item.items():
            self.assertIn(key, item)
            if key != "created_at":  # Skip datetime comparison
                self.assertEqual(item[key], value)
        
        # Test from_dynamodb_item
        user = ModelMapper.from_dynamodb_item(TestUser, item)
        self.assertEqual(user.id, "USER#123")
        self.assertEqual(user.username, "testuser")
        
        # Test generate_key
        key = ModelMapper.generate_key(self.user)
        self.assertEqual(key, {
            "id": "USER#123",
            "metadata": "METADATA"
        })
        
        # Test generate_gsi_keys
        gsi_keys = ModelMapper.generate_gsi_keys(self.user, "GSI1")
        self.assertEqual(gsi_keys, {
            "email_index": "EMAIL#test@example.com",
            "status_index": "STATUS#active"
        })


if __name__ == '__main__':
    unittest.main() 