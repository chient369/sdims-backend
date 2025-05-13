"""
Base Model for DynamoDB Mapping

This module provides the BaseModel class which is the foundation for all model classes.
"""

import inspect
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Set, ClassVar, get_type_hints

from common.models.converters import BaseConverter, StringConverter


class BaseModel:
    """
    Base class for all DynamoDB models
    
    Provides common functionality for serialization, deserialization, and tracking changes.
    """
    
    # Class variable to track all model fields
    _model_fields: ClassVar[Set[str]] = set()
    
    def __init__(self, **kwargs):
        """
        Initialize model with provided values
        
        Args:
            **kwargs: Initial values for model attributes
        """
        # Set initial attribute values
        for key, value in kwargs.items():
            attr_name = f"_{key}"
            setattr(self, attr_name, value)
        
        # Initialize change tracking
        self._dirty_fields: Set[str] = set()
        self._initialized = True
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        Override setattr to track changes to model fields
        
        Args:
            name: Attribute name
            value: Attribute value
        """
        # Call the parent setattr
        super().__setattr__(name, value)
        
        # If it's a model field (private attribute with leading underscore)
        # and not an internal attribute (double underscore)
        if name.startswith('_') and not name.startswith('__') and not name == '_dirty_fields':
            field_name = name[1:]  # Remove leading underscore
            
            # Track changes if model is already initialized
            if hasattr(self, '_initialized') and self._initialized:
                self._dirty_fields.add(field_name)
    
    def is_dirty(self) -> bool:
        """
        Check if the model has been modified
        
        Returns:
            True if the model has been modified, False otherwise
        """
        return len(self._dirty_fields) > 0
    
    def get_dirty_fields(self) -> Set[str]:
        """
        Get the names of fields that have been modified
        
        Returns:
            Set of modified field names
        """
        return self._dirty_fields.copy()
    
    def mark_clean(self) -> None:
        """Mark the model as clean (not modified)"""
        self._dirty_fields.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary representation
        
        Returns:
            Dictionary with model attributes
        """
        result = {}
        
        # Get all properties
        for name, method in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            # Skip private and special methods
            if name.startswith('_') or name in ('to_dict', 'from_dict', 'is_dirty', 'get_dirty_fields', 'mark_clean'):
                continue
            
            # Get value using property
            value = getattr(self, name)
            
            # Add to result dictionary
            if value is not None:
                result[name] = value
        
        return result
    
    def to_json(self) -> str:
        """
        Convert model to JSON string
        
        Returns:
            JSON string representation of the model
        """
        def json_encoder(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        return json.dumps(self.to_dict(), default=json_encoder)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """
        Create model instance from dictionary
        
        Args:
            data: Dictionary with attribute values
            
        Returns:
            New model instance
        """
        kwargs = {}
        
        # Get attribute metadata
        from common.models.decorators import _get_all_property_metadata
        metadata = _get_all_property_metadata(cls)
        
        # Process attributes based on metadata
        for prop_name, prop_meta in metadata.items():
            # Get the attribute name in the dictionary
            attr_name = prop_meta.get('name', prop_name)
            
            # Check if the attribute exists in the data
            if attr_name in data:
                # Store with private attribute name (_name)
                kwargs[prop_name] = data[attr_name]
        
        # Create and return instance
        instance = cls(**kwargs)
        instance.mark_clean()  # Mark as clean initially
        return instance
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """
        Create model instance from JSON string
        
        Args:
            json_str: JSON string with attribute values
            
        Returns:
            New model instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __str__(self) -> str:
        """
        String representation of the model
        
        Returns:
            String representation
        """
        class_name = self.__class__.__name__
        props = []
        
        # Get all properties
        for name, method in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            # Skip private and special methods
            if name.startswith('_') or name in ('to_dict', 'from_dict', 'is_dirty', 'get_dirty_fields', 'mark_clean'):
                continue
            
            # Get value using property
            try:
                value = getattr(self, name)
                props.append(f"{name}={repr(value)}")
            except Exception:
                props.append(f"{name}=<error>")
        
        return f"{class_name}({', '.join(props)})"
    
    def __repr__(self) -> str:
        """
        Representation of the model
        
        Returns:
            Representation string
        """
        return self.__str__()
    
    def __eq__(self, other):
        """
        Compare two model instances
        
        Args:
            other: Other model instance
            
        Returns:
            True if equal, False otherwise
        """
        if not isinstance(other, self.__class__):
            return False
        
        # Get all properties
        for name, method in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
            # Skip private and special methods
            if name.startswith('_') or name in ('to_dict', 'from_dict', 'is_dirty', 'get_dirty_fields', 'mark_clean'):
                continue
            
            # Compare property values
            if getattr(self, name) != getattr(other, name):
                return False
        
        return True 