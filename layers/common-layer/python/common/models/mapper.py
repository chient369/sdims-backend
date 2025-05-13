"""
Model Mapper for DynamoDB

This module provides utilities for mapping between Python model objects and DynamoDB items.
"""

import inspect
import json
import decimal
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Set, get_type_hints

from aws_lambda_powertools import Logger

from common.models.converters import (
    BaseConverter, 
    StringConverter,
    NumberConverter,
    BooleanConverter,
    DateTimeConverter,
    UUIDConverter
)
from common.models.decorators import (
    _get_model_metadata,
    _get_all_property_metadata,
    _get_property_metadata,
    get_model_table_name,
    get_model_entity_type,
    get_model_keys,
    get_model_gsi_keys
)
from common.models.base_model import BaseModel

logger = Logger(service="model-mapper")

T = TypeVar('T', bound=BaseModel)

# Cache for converter instances to avoid creating new ones for each conversion
_converter_cache: Dict[Type[BaseConverter], BaseConverter] = {}

def _get_converter(converter_class: Type[BaseConverter]) -> BaseConverter:
    """
    Get or create converter instance
    
    Args:
        converter_class: The converter class
        
    Returns:
        Converter instance
    """
    if converter_class not in _converter_cache:
        _converter_cache[converter_class] = converter_class()
    
    return _converter_cache[converter_class]


def _get_attribute_converter(model_class: Type[T], prop_name: str) -> BaseConverter:
    """
    Get converter for a model attribute
    
    Args:
        model_class: The model class
        prop_name: The property name
        
    Returns:
        Converter for the attribute
    """
    metadata = _get_property_metadata(model_class, prop_name)
    converter_class = metadata.get('converter')
    
    # If no converter specified, try to determine from return type
    if not converter_class:
        # Get the property method
        prop_method = getattr(model_class, prop_name)
        
        # Get return type hint
        return_type = metadata.get('return_type')
        
        # Default to StringConverter if no type hint
        if not return_type or return_type is inspect.Signature.empty:
            converter_class = StringConverter
        else:
            # Get appropriate converter for return type
            converter_class = _get_converter_for_type(return_type)
    
    return _get_converter(converter_class)


def _get_converter_for_type(type_hint: Any) -> Type[BaseConverter]:
    """
    Get appropriate converter for a type hint
    
    Args:
        type_hint: The type hint
        
    Returns:
        Converter class for the type
    """
    # Handle primitive types
    if type_hint == str:
        return StringConverter
    elif type_hint == bool:
        return BooleanConverter
    elif type_hint in (int, float, decimal.Decimal):
        return NumberConverter
    elif type_hint == datetime:
        return DateTimeConverter
    
    # Default to string
    return StringConverter


def model_to_dynamodb_item(model: T, nested: bool = False) -> Dict[str, Any]:
    """
    Convert model to DynamoDB item
    
    Args:
        model: The model instance
        nested: Whether this is a nested conversion
        
    Returns:
        DynamoDB item
    """
    model_class = model.__class__
    result = {}
    
    # Get all properties
    for name, method in inspect.getmembers(model_class, predicate=inspect.isfunction):
        # Skip private and special methods
        if name.startswith('_') or name in ('to_dict', 'from_dict', 'is_dirty', 'get_dirty_fields', 'mark_clean'):
            continue
        
        # Get metadata for property
        metadata = _get_property_metadata(model_class, name)
        
        # Skip if not an attribute
        if not metadata.get('is_attribute', False) and not metadata.get('is_primary_key', False) and not metadata.get('is_sort_key', False):
            continue
        
        # Get attribute name in DynamoDB
        db_name = metadata.get('name', name)
        
        # Get property value
        try:
            value = getattr(model, name)
        except Exception as e:
            logger.warning(f"Error getting property {name} from {model_class.__name__}: {str(e)}")
            continue
        
        # Skip None values
        if value is None:
            continue
        
        # Get converter for property
        converter = _get_attribute_converter(model_class, name)
        
        # Convert value to DynamoDB format
        try:
            db_value = converter.to_dynamodb(value)
            # Add to result
            result[db_name] = db_value
        except Exception as e:
            logger.error(f"Error converting {name} to DynamoDB format: {str(e)}")
            raise ValueError(f"Error converting {name} to DynamoDB format: {str(e)}")
    
    # Add type indicator for entity type if not nested
    if not nested:
        entity_type = get_model_entity_type(model_class)
        result['entity_type'] = entity_type
    
    return result


def dynamodb_item_to_model(model_class: Type[T], item: Dict[str, Any], nested: bool = False) -> T:
    """
    Convert DynamoDB item to model
    
    Args:
        model_class: The model class
        item: The DynamoDB item
        nested: Whether this is a nested conversion
        
    Returns:
        Model instance
    """
    kwargs = {}
    
    # Get all properties
    metadata = _get_all_property_metadata(model_class)
    
    # Process each property
    for prop_name, prop_meta in metadata.items():
        # Get attribute name in DynamoDB
        db_name = prop_meta.get('name', prop_name)
        
        # Skip if not in item
        if db_name not in item:
            continue
        
        # Get raw value from DynamoDB
        db_value = item[db_name]
        
        # Skip None values
        if db_value is None:
            continue
        
        # Get converter for property
        converter = _get_attribute_converter(model_class, prop_name)
        
        # Convert value to Python format
        try:
            python_value = converter.from_dynamodb(db_value)
            # Add to kwargs with private attribute name (without '_')
            kwargs[prop_name] = python_value
        except Exception as e:
            logger.error(f"Error converting {db_name} from DynamoDB format: {str(e)}")
            raise ValueError(f"Error converting {db_name} from DynamoDB format: {str(e)}")
    
    # Create and return model instance
    try:
        instance = model_class(**kwargs)
        instance.mark_clean()  # Mark as clean initially
        return instance
    except Exception as e:
        logger.error(f"Error creating {model_class.__name__} instance: {str(e)}")
        raise ValueError(f"Error creating {model_class.__name__} instance: {str(e)}")


def generate_key(model: T) -> Dict[str, Any]:
    """
    Generate DynamoDB key for a model
    
    Args:
        model: The model instance
        
    Returns:
        DynamoDB key (PK and SK)
    """
    model_class = model.__class__
    key_map = get_model_keys(model_class)
    result = {}
    
    # Get primary key
    pk_prop = key_map.get('primary_key')
    if pk_prop:
        pk_value = getattr(model, pk_prop)
        pk_meta = _get_property_metadata(model_class, pk_prop)
        pk_name = pk_meta.get('name', pk_prop)
        result[pk_name] = pk_value
    
    # Get sort key if available
    sk_prop = key_map.get('sort_key')
    if sk_prop:
        sk_value = getattr(model, sk_prop)
        sk_meta = _get_property_metadata(model_class, sk_prop)
        sk_name = sk_meta.get('name', sk_prop)
        result[sk_name] = sk_value
    
    return result


def generate_gsi_keys(model: T, index_name: str) -> Dict[str, Any]:
    """
    Generate GSI keys for a model
    
    Args:
        model: The model instance
        index_name: The GSI index name
        
    Returns:
        GSI keys for the index
    """
    model_class = model.__class__
    gsi_keys = get_model_gsi_keys(model_class)
    
    if index_name not in gsi_keys:
        raise ValueError(f"GSI {index_name} not defined for {model_class.__name__}")
    
    index_keys = gsi_keys[index_name]
    result = {}
    
    # Get GSI partition key
    pk_prop = index_keys.get('partition_key')
    if pk_prop:
        pk_value = getattr(model, pk_prop)
        pk_meta = _get_property_metadata(model_class, pk_prop)
        pk_name = pk_meta.get('name', pk_prop)
        result[pk_name] = pk_value
    
    # Get GSI sort key if available
    sk_prop = index_keys.get('sort_key')
    if sk_prop:
        sk_value = getattr(model, sk_prop)
        sk_meta = _get_property_metadata(model_class, sk_prop)
        sk_name = sk_meta.get('name', sk_prop)
        result[sk_name] = sk_value
    
    return result


class ModelMapper:
    """
    Utility class for mapping between models and DynamoDB items
    """
    
    @staticmethod
    def to_dynamodb_item(model: T) -> Dict[str, Any]:
        """
        Convert model to DynamoDB item
        
        Args:
            model: The model instance
            
        Returns:
            DynamoDB item
        """
        return model_to_dynamodb_item(model)
    
    @staticmethod
    def from_dynamodb_item(model_class: Type[T], item: Dict[str, Any]) -> T:
        """
        Convert DynamoDB item to model
        
        Args:
            model_class: The model class
            item: The DynamoDB item
            
        Returns:
            Model instance
        """
        return dynamodb_item_to_model(model_class, item)
    
    @staticmethod
    def generate_key(model: T) -> Dict[str, Any]:
        """
        Generate DynamoDB key for a model
        
        Args:
            model: The model instance
            
        Returns:
            DynamoDB key (PK and SK)
        """
        return generate_key(model)
    
    @staticmethod
    def generate_gsi_keys(model: T, index_name: str) -> Dict[str, Any]:
        """
        Generate GSI keys for a model
        
        Args:
            model: The model instance
            index_name: The GSI index name
            
        Returns:
            GSI keys for the index
        """
        return generate_gsi_keys(model, index_name) 