"""
Tests for BaseModel module
"""

import unittest
import json
from datetime import datetime

from common.models.base_model import BaseModel
from common.models.decorators import attribute, primary_key, sort_key, dynamodb_model
from common.models.converters import StringConverter, DateTimeConverter


@dynamodb_model(table_name="TEST_TABLE")
class TestModel(BaseModel):
    @primary_key
    @attribute(converter=StringConverter)
    def id(self) -> str:
        return f"TEST#{self._id}"
    
    @sort_key
    @attribute(converter=StringConverter)
    def metadata(self) -> str:
        return "METADATA"
    
    @attribute(converter=StringConverter)
    def name(self) -> str:
        return self._name
    
    @attribute(converter=DateTimeConverter)
    def created_at(self) -> datetime:
        return self._created_at


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now()
        self.model = TestModel(
            id="123",
            name="Test Model",
            created_at=self.now
        )
        
    def test_attribute_access(self):
        """Test accessing model attributes"""
        self.assertEqual(self.model.id, "TEST#123")
        self.assertEqual(self.model.metadata, "METADATA")
        self.assertEqual(self.model.name, "Test Model")
        self.assertEqual(self.model.created_at, self.now)
    
    def test_dirty_tracking(self):
        """Test change tracking"""
        # Initially not dirty
        self.assertFalse(self.model.is_dirty())
        self.assertEqual(self.model.get_dirty_fields(), set())
        
        # Update name
        self.model._name = "Updated Name"
        self.assertTrue(self.model.is_dirty())
        self.assertEqual(self.model.get_dirty_fields(), {'name'})
        
        # Update multiple fields
        self.model._id = "456"
        self.assertEqual(self.model.get_dirty_fields(), {'name', 'id'})
        
        # Mark clean
        self.model.mark_clean()
        self.assertFalse(self.model.is_dirty())
        self.assertEqual(self.model.get_dirty_fields(), set())
    
    def test_to_dict(self):
        """Test to_dict method"""
        result = self.model.to_dict()
        expected = {
            'id': "TEST#123",
            'metadata': "METADATA",
            'name': "Test Model",
            'created_at': self.now
        }
        self.assertEqual(result, expected)
    
    def test_to_json(self):
        """Test to_json method"""
        json_str = self.model.to_json()
        data = json.loads(json_str)
        
        # Check id
        self.assertEqual(data['id'], "TEST#123")
        self.assertEqual(data['metadata'], "METADATA")
        self.assertEqual(data['name'], "Test Model")
        
        # Created_at is converted to string in JSON
        self.assertTrue('created_at' in data)
    
    def test_from_dict(self):
        """Test from_dict method"""
        data = {
            'id': "789",
            'name': "Another Model",
            'created_at': self.now.isoformat()
        }
        
        model = TestModel.from_dict(data)
        self.assertEqual(model.id, "TEST#789")
        self.assertEqual(model.metadata, "METADATA")
        self.assertEqual(model.name, "Another Model")
        
        # Should be clean after creation
        self.assertFalse(model.is_dirty())
    
    def test_equality(self):
        """Test equality comparison"""
        model1 = TestModel(id="123", name="Test Model", created_at=self.now)
        model2 = TestModel(id="123", name="Test Model", created_at=self.now)
        model3 = TestModel(id="456", name="Different Model", created_at=self.now)
        
        self.assertEqual(model1, model2)
        self.assertNotEqual(model1, model3)
        self.assertNotEqual(model2, model3)


if __name__ == '__main__':
    unittest.main() 