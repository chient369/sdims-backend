"""
ValidationError Class

This module defines the ValidationError class for validation framework.
"""

class ValidationError:
    """
    Class to represent a validation error for a specific field
    """
    
    def __init__(self, field: str, message: str, code: str = None):
        """
        Initialize a validation error
        
        Args:
            field: The field name that failed validation
            message: The error message
            code: Optional error code (for more specific error handling)
        """
        self.field = field
        self.message = message
        self.code = code
    
    def to_dict(self):
        """
        Convert the error to a dictionary representation
        
        Returns:
            Dictionary with field and message
        """
        result = {
            "field": self.field,
            "message": self.message
        }
        
        if self.code:
            result["code"] = self.code
            
        return result 