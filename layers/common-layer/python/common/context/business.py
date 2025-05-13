from fastapi import Request, Depends
from typing import Optional, Dict, Any, List
from aws_lambda_powertools import Logger
from ..api.errors import AuthenticationError, AuthorizationError
import jwt
import os

logger = Logger(service="business_context")

class BusinessContext:
    def __init__(self, request: Request):
        """
        Initialize business context with request
        
        Args:
            request: FastAPI request object
        """
        self.request = request
        self.user: Optional[Dict[str, Any]] = None
        self.permissions: List[str] = []
        self._loaded = False
        
    async def load(self) -> None:
        """
        Load user and permissions data
        """
        if not self._loaded:
            await self._load_user()
            await self._load_permissions()
            self._loaded = True
    
    async def _load_user(self) -> None:
        """
        Load user data from JWT token
        """
        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationError("Token không được cung cấp")
            
        token = auth_header.split(" ")[1]
        try:
            # Verify and decode JWT token
            secret_key = os.getenv("JWT_SECRET_KEY")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            
            # Get user data from token claims
            self.user = {
                "id": payload["sub"],
                "username": payload["username"],
                "email": payload.get("email"),
                "role_id": payload.get("role_id")
            }
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token đã hết hạn")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Token không hợp lệ")
        except Exception as e:
            logger.exception("Error loading user data")
            raise AuthenticationError("Lỗi xác thực người dùng")
    
    async def _load_permissions(self) -> None:
        """
        Load user permissions from database
        """
        if not self.user:
            return
            
        try:
            # TODO: Load permissions from DynamoDB based on role_id
            # For now, using mock permissions
            self.permissions = ["employee:list", "employee:read"]
            
        except Exception as e:
            logger.exception("Error loading permissions")
            self.permissions = []
    
    def require_permissions(self, required_permissions: List[str]) -> None:
        """
        Check if user has required permissions
        
        Args:
            required_permissions: List of required permission codes
            
        Raises:
            AuthorizationError: If user lacks any required permission
        """
        if not all(p in self.permissions for p in required_permissions):
            raise AuthorizationError()
    
    @property
    def user_id(self) -> Optional[str]:
        """Get current user ID"""
        return self.user["id"] if self.user else None
    
    @property
    def username(self) -> Optional[str]:
        """Get current username"""
        return self.user["username"] if self.user else None
    
    @property
    def role_id(self) -> Optional[str]:
        """Get current user role ID"""
        return self.user["role_id"] if self.user else None

async def get_business_context(request: Request) -> BusinessContext:
    """
    FastAPI dependency for getting business context
    
    Args:
        request: FastAPI request object
        
    Returns:
        Initialized BusinessContext instance
    """
    context = BusinessContext(request)
    await context.load()
    return context 