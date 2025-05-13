"""
Type Converters for Model Mapping

This module provides converters for transforming between Python types and DynamoDB representation.
"""

import uuid
import decimal
import json
from enum import Enum
from datetime import datetime, date, time
from typing import Any, Dict, List, Set, Optional, Type, TypeVar, Generic, Union, Callable

T = TypeVar('T')
S = TypeVar('S')

class BaseConverter(Generic[T, S]):
    """
    Base converter interface for converting between Python types and DynamoDB representation.
    
    Type parameters:
        T: The Python type
        S: The DynamoDB representation type
    """
    
    def to_dynamodb(self, value: T) -> S:
        """
        Convert Python value to DynamoDB representation
        
        Args:
            value: The Python value to convert
            
        Returns:
            The DynamoDB representation
            
        Raises:
            ValueError: If conversion fails
        """
        raise NotImplementedError("Subclasses must implement to_dynamodb")
    
    def from_dynamodb(self, value: S) -> T:
        """
        Convert DynamoDB representation to Python value
        
        Args:
            value: The DynamoDB representation to convert
            
        Returns:
            The Python value
            
        Raises:
            ValueError: If conversion fails
        """
        raise NotImplementedError("Subclasses must implement from_dynamodb")


class StringConverter(BaseConverter[str, str]):
    """Converter for string values"""
    
    def to_dynamodb(self, value: str) -> str:
        if value is None:
            return None
        return str(value)
    
    def from_dynamodb(self, value: str) -> str:
        return value


class NumberConverter(BaseConverter[Union[int, float, decimal.Decimal], str]):
    """Converter for number values (int, float, decimal)"""
    
    def __init__(self, target_type: Type = decimal.Decimal):
        """
        Initialize NumberConverter
        
        Args:
            target_type: The target Python type (int, float, decimal.Decimal)
        """
        self.target_type = target_type
    
    def to_dynamodb(self, value: Union[int, float, decimal.Decimal]) -> str:
        if value is None:
            return None
        return str(value)
    
    def from_dynamodb(self, value: str) -> Union[int, float, decimal.Decimal]:
        if value is None:
            return None
        try:
            if self.target_type == int:
                return int(value)
            elif self.target_type == float:
                return float(value)
            else:
                return decimal.Decimal(value)
        except (ValueError, decimal.InvalidOperation) as e:
            raise ValueError(f"Cannot convert '{value}' to {self.target_type.__name__}") from e


class BooleanConverter(BaseConverter[bool, bool]):
    """Converter for boolean values"""
    
    def to_dynamodb(self, value: bool) -> bool:
        if value is None:
            return None
        return bool(value)
    
    def from_dynamodb(self, value: bool) -> bool:
        return value


class UUIDConverter(BaseConverter[uuid.UUID, str]):
    """Converter for UUID values"""
    
    def to_dynamodb(self, value: uuid.UUID) -> str:
        if value is None:
            return None
        return str(value)
    
    def from_dynamodb(self, value: str) -> uuid.UUID:
        if value is None:
            return None
        try:
            return uuid.UUID(value)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Cannot convert '{value}' to UUID") from e


class DateTimeConverter(BaseConverter[datetime, str]):
    """Converter for datetime values"""
    
    def __init__(self, format_str: str = "%Y-%m-%dT%H:%M:%S.%fZ"):
        """
        Initialize DateTimeConverter
        
        Args:
            format_str: The datetime format string
        """
        self.format_str = format_str
    
    def to_dynamodb(self, value: datetime) -> str:
        if value is None:
            return None
        return value.strftime(self.format_str)
    
    def from_dynamodb(self, value: str) -> datetime:
        if value is None:
            return None
        try:
            return datetime.strptime(value, self.format_str)
        except ValueError as e:
            raise ValueError(f"Cannot convert '{value}' to datetime using format '{self.format_str}'") from e


class DateConverter(BaseConverter[date, str]):
    """Converter for date values"""
    
    def __init__(self, format_str: str = "%Y-%m-%d"):
        """
        Initialize DateConverter
        
        Args:
            format_str: The date format string
        """
        self.format_str = format_str
    
    def to_dynamodb(self, value: date) -> str:
        if value is None:
            return None
        return value.strftime(self.format_str)
    
    def from_dynamodb(self, value: str) -> date:
        if value is None:
            return None
        try:
            return datetime.strptime(value, self.format_str).date()
        except ValueError as e:
            raise ValueError(f"Cannot convert '{value}' to date using format '{self.format_str}'") from e


class EnumConverter(BaseConverter[Enum, str]):
    """Converter for Enum values"""
    
    def __init__(self, enum_class: Type[Enum], use_name: bool = True):
        """
        Initialize EnumConverter
        
        Args:
            enum_class: The Enum class
            use_name: Whether to use the enum name (True) or value (False)
        """
        self.enum_class = enum_class
        self.use_name = use_name
    
    def to_dynamodb(self, value: Enum) -> str:
        if value is None:
            return None
        if self.use_name:
            return value.name
        return str(value.value)
    
    def from_dynamodb(self, value: str) -> Enum:
        if value is None:
            return None
        try:
            if self.use_name:
                return self.enum_class[value]
            
            for item in self.enum_class:
                if str(item.value) == value:
                    return item
            
            raise ValueError(f"No enum value '{value}' found in {self.enum_class.__name__}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Cannot convert '{value}' to enum {self.enum_class.__name__}") from e


class ListConverter(BaseConverter[List[T], List[S]]):
    """Converter for list values"""
    
    def __init__(self, item_converter: BaseConverter[T, S]):
        """
        Initialize ListConverter
        
        Args:
            item_converter: Converter for list items
        """
        self.item_converter = item_converter
    
    def to_dynamodb(self, value: List[T]) -> List[S]:
        if value is None:
            return None
        return [self.item_converter.to_dynamodb(item) for item in value]
    
    def from_dynamodb(self, value: List[S]) -> List[T]:
        if value is None:
            return None
        return [self.item_converter.from_dynamodb(item) for item in value]


class SetConverter(BaseConverter[Set[T], List[S]]):
    """Converter for set values"""
    
    def __init__(self, item_converter: BaseConverter[T, S]):
        """
        Initialize SetConverter
        
        Args:
            item_converter: Converter for set items
        """
        self.item_converter = item_converter
    
    def to_dynamodb(self, value: Set[T]) -> List[S]:
        if value is None:
            return None
        return [self.item_converter.to_dynamodb(item) for item in value]
    
    def from_dynamodb(self, value: List[S]) -> Set[T]:
        if value is None:
            return None
        return {self.item_converter.from_dynamodb(item) for item in value}


class MapConverter(BaseConverter[Dict[str, T], Dict[str, S]]):
    """Converter for map/dictionary values"""
    
    def __init__(self, value_converter: BaseConverter[T, S]):
        """
        Initialize MapConverter
        
        Args:
            value_converter: Converter for dictionary values
        """
        self.value_converter = value_converter
    
    def to_dynamodb(self, value: Dict[str, T]) -> Dict[str, S]:
        if value is None:
            return None
        return {k: self.value_converter.to_dynamodb(v) for k, v in value.items()}
    
    def from_dynamodb(self, value: Dict[str, S]) -> Dict[str, T]:
        if value is None:
            return None
        return {k: self.value_converter.from_dynamodb(v) for k, v in value.items()}


class JsonConverter(BaseConverter[Any, str]):
    """Converter for serializing complex objects to JSON"""
    
    def to_dynamodb(self, value: Any) -> str:
        if value is None:
            return None
        try:
            return json.dumps(value)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Cannot serialize value to JSON: {value}") from e
    
    def from_dynamodb(self, value: str) -> Any:
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Cannot deserialize JSON value: {value}") from e


class ModelConverter(BaseConverter[Any, Dict[str, Any]]):
    """Converter for embedded model objects"""
    
    def __init__(self, model_class: Type):
        """
        Initialize ModelConverter
        
        Args:
            model_class: The model class to convert to/from
        """
        self.model_class = model_class
    
    def to_dynamodb(self, value: Any) -> Dict[str, Any]:
        if value is None:
            return None
        # This will rely on model_to_dynamodb from mapper.py
        from common.models.mapper import model_to_dynamodb_item
        return model_to_dynamodb_item(value, nested=True)
    
    def from_dynamodb(self, value: Dict[str, Any]) -> Any:
        if value is None:
            return None
        # This will rely on dynamodb_to_model from mapper.py
        from common.models.mapper import dynamodb_item_to_model
        return dynamodb_item_to_model(self.model_class, value, nested=True) 