"""
Decorators for Model Mapping

This module provides decorators for defining the mapping between Python models and DynamoDB.
"""

import inspect
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Callable, Union, get_type_hints
from functools import wraps

from common.models.converters import BaseConverter, StringConverter

# Model registry to store metadata about models
_model_registry: Dict[Type, Dict[str, Any]] = {}

# Property registry to store metadata about model properties
_property_registry: Dict[Type, Dict[str, Dict[str, Any]]] = {}


def _register_model(cls: Type, **kwargs) -> None:
    """
    Register model class with metadata
    
    Args:
        cls: The model class
        **kwargs: Additional metadata
    """
    if cls not in _model_registry:
        _model_registry[cls] = {}
    
    _model_registry[cls].update(kwargs)


def _register_property(cls: Type, prop_name: str, **kwargs) -> None:
    """
    Register property metadata
    
    Args:
        cls: The model class
        prop_name: The property name
        **kwargs: Additional metadata
    """
    if cls not in _property_registry:
        _property_registry[cls] = {}
    
    if prop_name not in _property_registry[cls]:
        _property_registry[cls][prop_name] = {}
    
    _property_registry[cls][prop_name].update(kwargs)


def _get_model_metadata(cls: Type) -> Dict[str, Any]:
    """
    Get model metadata
    
    Args:
        cls: The model class
        
    Returns:
        Model metadata
    """
    return _model_registry.get(cls, {})


def _get_property_metadata(cls: Type, prop_name: str) -> Dict[str, Any]:
    """
    Get property metadata
    
    Args:
        cls: The model class
        prop_name: The property name
        
    Returns:
        Property metadata
    """
    class_registry = _property_registry.get(cls, {})
    return class_registry.get(prop_name, {})


def _get_all_property_metadata(cls: Type) -> Dict[str, Dict[str, Any]]:
    """
    Get all property metadata for a class
    
    Args:
        cls: The model class
        
    Returns:
        All property metadata
    """
    return _property_registry.get(cls, {})


def dynamodb_model(table_name: str, entity_type: Optional[str] = None):
    """
    Decorator to mark a class as a DynamoDB model
    
    Args:
        table_name: The DynamoDB table name
        entity_type: The entity type identifier (used in PK/SK)
        
    Returns:
        Decorator function
    """
    def decorator(cls):
        # Register model metadata
        _register_model(
            cls,
            table_name=table_name,
            entity_type=entity_type or cls.__name__.upper()
        )
        
        return cls
    
    return decorator


def attribute(name: Optional[str] = None, 
              converter: Optional[Type[BaseConverter]] = None,
              auto_generate: Optional[Callable] = None,
              default_value: Any = None):
    """
    Decorator to mark a property as a DynamoDB attribute
    
    Args:
        name: The attribute name in DynamoDB (if different from property name)
        converter: The converter to use for this attribute
        auto_generate: Function to auto-generate value if None
        default_value: Default value for this attribute
        
    Returns:
        Decorator function
    """
    def decorator(func):
        prop_name = func.__name__
        
        # Get the return type hint
        func_signature = inspect.signature(func)
        return_type = func_signature.return_annotation
        if return_type is inspect.Signature.empty:
            return_type = None
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Check for auto-generate if value is None
            attr_name = f"_{prop_name}"
            if not hasattr(self, attr_name) or getattr(self, attr_name) is None:
                # First check if we need to auto-generate
                if auto_generate is not None:
                    setattr(self, attr_name, auto_generate())
                # Then check for default value
                elif default_value is not None:
                    setattr(self, attr_name, default_value)
            
            return func(self, *args, **kwargs)
        
        # Register property metadata
        _register_property(
            func.__qualname__.split('.')[0],
            prop_name,
            name=name or prop_name,
            is_attribute=True,
            converter=converter,
            return_type=return_type,
            auto_generate=auto_generate,
            default_value=default_value
        )
        
        return wrapper
    
    return decorator


def primary_key(func):
    """
    Decorator to mark a property as the primary key
    
    Returns:
        Decorator function
    """
    prop_name = func.__name__
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    
    # Register property metadata
    _register_property(
        func.__qualname__.split('.')[0],
        prop_name,
        is_primary_key=True
    )
    
    return wrapper


def sort_key(func):
    """
    Decorator to mark a property as the sort key
    
    Returns:
        Decorator function
    """
    prop_name = func.__name__
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    
    # Register property metadata
    _register_property(
        func.__qualname__.split('.')[0],
        prop_name,
        is_sort_key=True
    )
    
    return wrapper


def gsi_partition_key(index_name: str):
    """
    Decorator to mark a property as a GSI partition key
    
    Args:
        index_name: The GSI name
        
    Returns:
        Decorator function
    """
    def decorator(func):
        prop_name = func.__name__
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        
        # Register property metadata
        _register_property(
            func.__qualname__.split('.')[0],
            prop_name,
            is_gsi_partition_key=True,
            gsi_name=index_name
        )
        
        return wrapper
    
    return decorator


def gsi_sort_key(index_name: str):
    """
    Decorator to mark a property as a GSI sort key
    
    Args:
        index_name: The GSI name
        
    Returns:
        Decorator function
    """
    def decorator(func):
        prop_name = func.__name__
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        
        # Register property metadata
        _register_property(
            func.__qualname__.split('.')[0],
            prop_name,
            is_gsi_sort_key=True,
            gsi_name=index_name
        )
        
        return wrapper
    
    return decorator


def auto_generate(generator: Callable = None):
    """
    Decorator to auto-generate a value for a property
    
    Args:
        generator: Function to generate the value
        
    Returns:
        Decorator function
    """
    def decorator(func):
        prop_name = func.__name__
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            attr_name = f"_{prop_name}"
            if not hasattr(self, attr_name) or getattr(self, attr_name) is None:
                if generator:
                    setattr(self, attr_name, generator())
                elif prop_name == "id" or prop_name.endswith("_id"):
                    setattr(self, attr_name, str(uuid.uuid4()))
                elif "time" in prop_name or "date" in prop_name:
                    setattr(self, attr_name, datetime.now())
            
            return func(self, *args, **kwargs)
        
        # Register property metadata
        _register_property(
            func.__qualname__.split('.')[0],
            prop_name,
            auto_generate=generator or True
        )
        
        return wrapper
    
    return decorator


def default_value(value: Any):
    """
    Decorator to set a default value for a property
    
    Args:
        value: The default value
        
    Returns:
        Decorator function
    """
    def decorator(func):
        prop_name = func.__name__
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            attr_name = f"_{prop_name}"
            if not hasattr(self, attr_name):
                setattr(self, attr_name, value)
            
            return func(self, *args, **kwargs)
        
        # Register property metadata
        _register_property(
            func.__qualname__.split('.')[0],
            prop_name,
            default_value=value
        )
        
        return wrapper
    
    return decorator


def validate(validator: Callable[[Any], bool], error_message: Optional[str] = None):
    """
    Decorator to validate a property value
    
    Args:
        validator: Function to validate the value (returns bool)
        error_message: Error message if validation fails
        
    Returns:
        Decorator function
    """
    def decorator(func):
        prop_name = func.__name__
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            value = func(self, *args, **kwargs)
            
            if value is not None and not validator(value):
                msg = error_message or f"Validation failed for {prop_name}"
                raise ValueError(msg)
            
            return value
        
        # Register property metadata
        _register_property(
            func.__qualname__.split('.')[0],
            prop_name,
            validator=validator,
            error_message=error_message
        )
        
        return wrapper
    
    return decorator


# Helper functions for metadata access
def get_model_table_name(cls: Type) -> str:
    """
    Get the DynamoDB table name for a model
    
    Args:
        cls: The model class
        
    Returns:
        The table name
    """
    metadata = _get_model_metadata(cls)
    return metadata.get('table_name')


def get_model_entity_type(cls: Type) -> str:
    """
    Get the entity type for a model
    
    Args:
        cls: The model class
        
    Returns:
        The entity type
    """
    metadata = _get_model_metadata(cls)
    return metadata.get('entity_type', cls.__name__.upper())


def get_model_keys(cls: Type) -> Dict[str, str]:
    """
    Get the primary and sort keys for a model
    
    Args:
        cls: The model class
        
    Returns:
        Dictionary with 'primary_key' and 'sort_key'
    """
    result = {'primary_key': None, 'sort_key': None}
    properties = _get_all_property_metadata(cls)
    
    for prop_name, metadata in properties.items():
        if metadata.get('is_primary_key'):
            result['primary_key'] = prop_name
        elif metadata.get('is_sort_key'):
            result['sort_key'] = prop_name
    
    return result


def get_model_gsi_keys(cls: Type) -> Dict[str, Dict[str, str]]:
    """
    Get the GSI keys for a model
    
    Args:
        cls: The model class
        
    Returns:
        Dictionary mapping GSI names to {'partition_key', 'sort_key'}
    """
    result = {}
    properties = _get_all_property_metadata(cls)
    
    for prop_name, metadata in properties.items():
        if metadata.get('is_gsi_partition_key'):
            gsi_name = metadata.get('gsi_name')
            if gsi_name not in result:
                result[gsi_name] = {'partition_key': None, 'sort_key': None}
            result[gsi_name]['partition_key'] = prop_name
            
        elif metadata.get('is_gsi_sort_key'):
            gsi_name = metadata.get('gsi_name')
            if gsi_name not in result:
                result[gsi_name] = {'partition_key': None, 'sort_key': None}
            result[gsi_name]['sort_key'] = prop_name
    
    return result 