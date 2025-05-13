"""
ValidationResult Class

This module defines the ValidationResult class for validation framework.
"""

from typing import List, Dict, Any
from .validation_error import ValidationError

class ValidationResult:
    """
    Class to hold validation results and errors
    """
    
    def __init__(self):
        """
        Initialize an empty validation result
        """
        self.errors: List[ValidationError] = []
    
    def add_error(self, field: str, message: str, code: str = None) -> None:
        """
        Add a validation error
        
        Args:
            field: The field name that failed validation
            message: The error message
            code: Optional error code
        """
        self.errors.append(ValidationError(field, message, code))
    
    def add_errors(self, errors: List[ValidationError]) -> None:
        """
        Add multiple validation errors
        
        Args:
            errors: List of ValidationError objects
        """
        self.errors.extend(errors)
    
    def merge(self, other_result: 'ValidationResult') -> None:
        """
        Merge another ValidationResult with this one
        
        Args:
            other_result: Another ValidationResult instance
        """
        self.add_errors(other_result.errors)
    
    @property
    def is_valid(self) -> bool:
        """
        Check if validation passed
        
        Returns:
            True if no errors, False otherwise
        """
        return len(self.errors) == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert validation result to dictionary format
        
        Returns:
            Dictionary with the validation errors
        """
        return {
            "valid": self.is_valid,
            "errors": [error.to_dict() for error in self.errors]
        }
    
    def get_error_messages(self) -> Dict[str, List[str]]:
        """
        Get error messages grouped by field
        
        Returns:
            Dictionary with field names as keys and lists of error messages as values
        """
        result: Dict[str, List[str]] = {}
        for error in self.errors:
            if error.field not in result:
                result[error.field] = []
            result[error.field].append(error.message)
        return result
    
    def get_errors_list(self) -> List[Dict[str, str]]:
        """
        Get errors as a list of field-message pairs
        
        Returns:
            List of dictionaries with 'field' and 'message' keys
        """
        return [error.to_dict() for error in self.errors] 