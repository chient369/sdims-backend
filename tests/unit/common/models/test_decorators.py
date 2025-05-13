"""
Tests for model decorators
"""

import unittest
import uuid
from datetime import datetime

from common.models.base_model import BaseModel
from common.models.decorators import (
    dynamodb_model,
    attribute,
    primary_key,
    sort_key,
    gsi_partition_key,
    gsi_sort_key,
    auto_generate,
    default_value,
    validate,
    get_model_table_name,
    get_model_entity_type,
    get_model_keys,
    get_model_gsi_keys
)
from common.models.converters import StringConverter, DateTimeConverter, BooleanConverter


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
    @validate(lambda x: x in ["active", "inactive", "pending"], "Status must be active, inactive, or pending")
    def status(self) -> str:
        return self._status


class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now()
        self.user = TestUser(
            id=str(uuid.uuid4()),
            username="testuser",
            email="test@example.com",
            status="active"
        )
    
    def test_model_decorators(self):
        """Test model decorators"""
        # Test table name
        self.assertEqual(get_model_table_name(TestUser), "TEST_TABLE")
        
        # Test entity type
        self.assertEqual(get_model_entity_type(TestUser), "USER")
    
    def test_key_decorators(self):
        """Test key decorators"""
        # Test primary and sort keys
        keys = get_model_keys(TestUser)
        self.assertEqual(keys['primary_key'], 'id')
        self.assertEqual(keys['sort_key'], 'metadata')
        
        # Test GSI keys
        gsi_keys = get_model_gsi_keys(TestUser)
        self.assertIn("GSI1", gsi_keys)
        self.assertEqual(gsi_keys["GSI1"]["partition_key"], "email_index")
        self.assertEqual(gsi_keys["GSI1"]["sort_key"], "status_index")
    
    def test_attribute_decorator(self):
        """Test attribute decorator"""
        # Test regular attribute
        self.assertEqual(self.user.username, "testuser")
        
        # Test attribute with custom name
        self.assertEqual(self.user.email, "test@example.com")
    
    def test_default_value_decorator(self):
        """Test default value decorator"""
        # Test default value
        self.assertTrue(self.user.is_active)
        
        # Test overriding default value
        user = TestUser(
            id="123",
            username="inactive",
            email="inactive@example.com",
            is_active=False,
            status="inactive"
        )
        self.assertFalse(user.is_active)
    
    def test_auto_generate_decorator(self):
        """Test auto-generate decorator"""
        # created_at should be auto-generated if not provided
        user = TestUser(
            id="123",
            username="new",
            email="new@example.com",
            status="pending"
        )
        self.assertIsNotNone(user.created_at)
        
        # Should not override provided value
        specific_time = datetime(2023, 1, 1, 12, 0, 0)
        user = TestUser(
            id="123",
            username="specific",
            email="specific@example.com",
            created_at=specific_time,
            status="active"
        )
        self.assertEqual(user.created_at, specific_time)
    
    def test_validate_decorator(self):
        """Test validate decorator"""
        # Valid status
        user = TestUser(
            id="123",
            username="valid",
            email="valid@example.com",
            status="active"
        )
        self.assertEqual(user.status, "active")
        
        # Invalid status should raise ValueError
        with self.assertRaises(ValueError):
            user = TestUser(
                id="123",
                username="invalid",
                email="invalid@example.com",
                status="invalid-status"
            )


if __name__ == '__main__':
    unittest.main() 