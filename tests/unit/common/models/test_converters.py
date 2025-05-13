"""
Tests for converters module
"""

import unittest
import uuid
import decimal
import json
from enum import Enum
from datetime import datetime, date

from common.models.converters import (
    StringConverter,
    NumberConverter,
    BooleanConverter,
    UUIDConverter,
    DateTimeConverter,
    DateConverter,
    EnumConverter,
    ListConverter,
    SetConverter,
    MapConverter,
    JsonConverter
)


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class TestConverters(unittest.TestCase):
    def test_string_converter(self):
        """Test StringConverter"""
        converter = StringConverter()
        
        # Test to_dynamodb
        self.assertEqual(converter.to_dynamodb("test"), "test")
        self.assertEqual(converter.to_dynamodb("123"), "123")
        self.assertIsNone(converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(converter.from_dynamodb("test"), "test")
        self.assertEqual(converter.from_dynamodb("123"), "123")
        self.assertIsNone(converter.from_dynamodb(None))
    
    def test_number_converter(self):
        """Test NumberConverter"""
        # Test with int
        int_converter = NumberConverter(target_type=int)
        self.assertEqual(int_converter.to_dynamodb(123), "123")
        self.assertEqual(int_converter.from_dynamodb("123"), 123)
        
        # Test with float
        float_converter = NumberConverter(target_type=float)
        self.assertEqual(float_converter.to_dynamodb(123.45), "123.45")
        self.assertEqual(float_converter.from_dynamodb("123.45"), 123.45)
        
        # Test with decimal
        decimal_converter = NumberConverter(target_type=decimal.Decimal)
        self.assertEqual(decimal_converter.to_dynamodb(decimal.Decimal("123.45")), "123.45")
        self.assertEqual(decimal_converter.from_dynamodb("123.45"), decimal.Decimal("123.45"))
        
        # Test None handling
        self.assertIsNone(int_converter.to_dynamodb(None))
        self.assertIsNone(int_converter.from_dynamodb(None))
        
        # Test invalid values
        with self.assertRaises(ValueError):
            int_converter.from_dynamodb("not-a-number")
    
    def test_boolean_converter(self):
        """Test BooleanConverter"""
        converter = BooleanConverter()
        
        # Test to_dynamodb
        self.assertEqual(converter.to_dynamodb(True), True)
        self.assertEqual(converter.to_dynamodb(False), False)
        self.assertIsNone(converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(converter.from_dynamodb(True), True)
        self.assertEqual(converter.from_dynamodb(False), False)
        self.assertIsNone(converter.from_dynamodb(None))
    
    def test_uuid_converter(self):
        """Test UUIDConverter"""
        converter = UUIDConverter()
        uuid_value = uuid.uuid4()
        uuid_str = str(uuid_value)
        
        # Test to_dynamodb
        self.assertEqual(converter.to_dynamodb(uuid_value), uuid_str)
        self.assertIsNone(converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(converter.from_dynamodb(uuid_str), uuid_value)
        self.assertIsNone(converter.from_dynamodb(None))
        
        # Test invalid UUID
        with self.assertRaises(ValueError):
            converter.from_dynamodb("not-a-uuid")
    
    def test_datetime_converter(self):
        """Test DateTimeConverter"""
        converter = DateTimeConverter()
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Test to_dynamodb
        self.assertEqual(converter.to_dynamodb(now), now_str)
        self.assertIsNone(converter.to_dynamodb(None))
        
        # Custom format
        custom_converter = DateTimeConverter(format_str="%Y-%m-%d %H:%M:%S")
        custom_str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(custom_converter.to_dynamodb(now), custom_str)
        
        # Test from_dynamodb
        dt1 = converter.from_dynamodb(now_str)
        dt2 = datetime.strptime(now_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(dt1, dt2)
        
        self.assertIsNone(converter.from_dynamodb(None))
        
        # Test invalid datetime
        with self.assertRaises(ValueError):
            converter.from_dynamodb("not-a-datetime")
    
    def test_date_converter(self):
        """Test DateConverter"""
        converter = DateConverter()
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")
        
        # Test to_dynamodb
        self.assertEqual(converter.to_dynamodb(today), today_str)
        self.assertIsNone(converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(converter.from_dynamodb(today_str), today)
        self.assertIsNone(converter.from_dynamodb(None))
        
        # Test invalid date
        with self.assertRaises(ValueError):
            converter.from_dynamodb("not-a-date")
    
    def test_enum_converter(self):
        """Test EnumConverter"""
        # Test with name (default)
        name_converter = EnumConverter(UserStatus)
        
        # Test to_dynamodb
        self.assertEqual(name_converter.to_dynamodb(UserStatus.ACTIVE), "ACTIVE")
        self.assertIsNone(name_converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(name_converter.from_dynamodb("ACTIVE"), UserStatus.ACTIVE)
        self.assertIsNone(name_converter.from_dynamodb(None))
        
        # Test with value
        value_converter = EnumConverter(UserStatus, use_name=False)
        
        # Test to_dynamodb
        self.assertEqual(value_converter.to_dynamodb(UserStatus.ACTIVE), "active")
        
        # Test from_dynamodb
        self.assertEqual(value_converter.from_dynamodb("active"), UserStatus.ACTIVE)
        
        # Test invalid enum
        with self.assertRaises(ValueError):
            name_converter.from_dynamodb("INVALID")
    
    def test_list_converter(self):
        """Test ListConverter"""
        string_converter = StringConverter()
        list_converter = ListConverter(string_converter)
        
        # Test to_dynamodb
        self.assertEqual(list_converter.to_dynamodb(["a", "b", "c"]), ["a", "b", "c"])
        self.assertIsNone(list_converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(list_converter.from_dynamodb(["a", "b", "c"]), ["a", "b", "c"])
        self.assertIsNone(list_converter.from_dynamodb(None))
        
        # Test with number converter
        number_converter = NumberConverter(target_type=int)
        number_list_converter = ListConverter(number_converter)
        
        self.assertEqual(number_list_converter.to_dynamodb([1, 2, 3]), ["1", "2", "3"])
        self.assertEqual(number_list_converter.from_dynamodb(["1", "2", "3"]), [1, 2, 3])
    
    def test_set_converter(self):
        """Test SetConverter"""
        string_converter = StringConverter()
        set_converter = SetConverter(string_converter)
        
        # Test to_dynamodb
        self.assertEqual(set_converter.to_dynamodb({"a", "b", "c"}), ["a", "b", "c"])
        self.assertIsNone(set_converter.to_dynamodb(None))
        
        # Test from_dynamodb
        result = set_converter.from_dynamodb(["a", "b", "c"])
        self.assertIsInstance(result, set)
        self.assertEqual(result, {"a", "b", "c"})
        self.assertIsNone(set_converter.from_dynamodb(None))
    
    def test_map_converter(self):
        """Test MapConverter"""
        string_converter = StringConverter()
        map_converter = MapConverter(string_converter)
        
        # Test to_dynamodb
        self.assertEqual(
            map_converter.to_dynamodb({"a": "1", "b": "2"}),
            {"a": "1", "b": "2"}
        )
        self.assertIsNone(map_converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(
            map_converter.from_dynamodb({"a": "1", "b": "2"}),
            {"a": "1", "b": "2"}
        )
        self.assertIsNone(map_converter.from_dynamodb(None))
        
        # Test with number converter
        number_converter = NumberConverter(target_type=int)
        number_map_converter = MapConverter(number_converter)
        
        self.assertEqual(
            number_map_converter.to_dynamodb({"a": 1, "b": 2}),
            {"a": "1", "b": "2"}
        )
        self.assertEqual(
            number_map_converter.from_dynamodb({"a": "1", "b": "2"}),
            {"a": 1, "b": 2}
        )
    
    def test_json_converter(self):
        """Test JsonConverter"""
        converter = JsonConverter()
        data = {"name": "Test", "values": [1, 2, 3]}
        json_str = json.dumps(data)
        
        # Test to_dynamodb
        self.assertEqual(converter.to_dynamodb(data), json_str)
        self.assertIsNone(converter.to_dynamodb(None))
        
        # Test from_dynamodb
        self.assertEqual(converter.from_dynamodb(json_str), data)
        self.assertIsNone(converter.from_dynamodb(None))
        
        # Test invalid JSON
        with self.assertRaises(ValueError):
            converter.from_dynamodb("not-json")


if __name__ == '__main__':
    unittest.main() 