from typing import Optional, Dict, Any, TypeVar, Generic, List
from pydantic import BaseModel
from fastapi.responses import JSONResponse

T = TypeVar("T")

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int

class APIResponse(BaseModel, Generic[T]):
    status: str = "success"
    data: T
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    @staticmethod
    def success(
        data: Any,
        message: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create success response
        
        Args:
            data: Response data
            message: Optional success message
            meta: Optional metadata
            
        Returns:
            Dict containing formatted success response
        """
        return {
            "status": "success",
            "data": data,
            "message": message,
            "meta": meta
        }

    @staticmethod
    def paginated(
        data: List[Any],
        page: int,
        limit: int,
        total: int,
        message: Optional[str] = None,
        extra_meta: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create paginated response
        
        Args:
            data: List of items for current page
            page: Current page number
            limit: Items per page
            total: Total number of items
            message: Optional success message
            extra_meta: Additional metadata
            
        Returns:
            Dict containing formatted paginated response
        """
        total_pages = (total + limit - 1) // limit
        
        meta = {
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages
            }
        }
        
        if extra_meta:
            meta.update(extra_meta)
            
        return APIResponse.success(
            data=data,
            message=message,
            meta=meta
        )

def create_response(
    data: Any,
    message: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
    status_code: int = 200
) -> JSONResponse:
    """
    Create JSON response with standard format
    
    Args:
        data: Response data
        message: Optional message
        meta: Optional metadata
        status_code: HTTP status code
        
    Returns:
        JSONResponse with formatted data
    """
    return JSONResponse(
        status_code=status_code,
        content=APIResponse.success(
            data=data,
            message=message,
            meta=meta
        )
    ) 