from typing import Dict, List, Any, Optional


class APIResponse:
    """
    Standard API response format for the application.
    Used to ensure consistent response structure across all API endpoints.
    """
    
    @staticmethod
    def success(status_code: int = 200, data: Any = None, message: str = None) -> Dict[str, Any]:
        """
        Create a success response.
        
        Args:
            status_code: HTTP status code
            data: Response data
            message: Optional success message
            
        Returns:
            Dict: Formatted success response
        """
        response = {
            "status": "success",
            "code": status_code
        }
        
        if data is not None:
            response["data"] = data
            
        if message:
            response["message"] = message
            
        return response
    
    @staticmethod
    def error(status_code: int = 400, message: str = "An error occurred", 
              error_code: str = "UNKNOWN_ERROR", errors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Create an error response.
        
        Args:
            status_code: HTTP status code
            message: Error message
            error_code: Application-specific error code
            errors: List of validation errors or details
            
        Returns:
            Dict: Formatted error response
        """
        response = {
            "status": "error",
            "code": error_code,
            "message": message
        }
        
        if errors:
            response["errors"] = errors
            
        return response 