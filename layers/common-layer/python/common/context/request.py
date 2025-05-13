from fastapi import Request
from typing import Optional, Dict, Any
from aws_lambda_powertools import Logger
import json
import os

logger = Logger(service="request_context")

class RequestContext:
    def __init__(self, request: Request):
        """
        Initialize request context
        
        Args:
            request: FastAPI request object
        """
        self.request = request
        self._event: Optional[Dict[str, Any]] = None
        self._context: Optional[Dict[str, Any]] = None
        
    @property
    async def event(self) -> Dict[str, Any]:
        """
        Get Lambda event data
        
        Returns:
            Dict containing Lambda event data
        """
        if not self._event:
            self._event = await self._get_event()
        return self._event
        
    @property
    async def context(self) -> Dict[str, Any]:
        """
        Get Lambda context data
        
        Returns:
            Dict containing Lambda context data
        """
        if not self._context:
            self._context = await self._get_context()
        return self._context
        
    async def _get_event(self) -> Dict[str, Any]:
        """
        Extract Lambda event data from request state
        
        Returns:
            Dict containing event data
        """
        try:
            return self.request.scope.get("aws.event", {})
        except Exception as e:
            logger.warning("Error getting Lambda event data", exc_info=e)
            return {}
            
    async def _get_context(self) -> Dict[str, Any]:
        """
        Extract Lambda context data from request state
        
        Returns:
            Dict containing context data
        """
        try:
            return self.request.scope.get("aws.context", {})
        except Exception as e:
            logger.warning("Error getting Lambda context data", exc_info=e)
            return {}
            
    @property
    def trace_id(self) -> Optional[str]:
        """Get X-Ray trace ID if available"""
        try:
            return os.getenv("_X_AMZN_TRACE_ID")
        except:
            return None
            
    @property
    def request_id(self) -> Optional[str]:
        """Get request ID from event"""
        try:
            return self.request.headers.get("x-request-id")
        except:
            return None
            
    @property
    def source_ip(self) -> Optional[str]:
        """Get source IP address"""
        try:
            return self.request.client.host
        except:
            return None
            
    @property
    def user_agent(self) -> Optional[str]:
        """Get user agent string"""
        try:
            return self.request.headers.get("user-agent")
        except:
            return None
            
    def get_header(self, name: str) -> Optional[str]:
        """
        Get request header value
        
        Args:
            name: Header name
            
        Returns:
            Header value if present
        """
        try:
            return self.request.headers.get(name)
        except:
            return None
            
    async def get_body(self) -> Dict[str, Any]:
        """
        Get request body as dict
        
        Returns:
            Dict containing request body data
        """
        try:
            body = await self.request.body()
            return json.loads(body)
        except:
            return {}

async def get_request_context(request: Request) -> RequestContext:
    """
    FastAPI dependency for getting request context
    
    Args:
        request: FastAPI request object
        
    Returns:
        Initialized RequestContext instance
    """
    return RequestContext(request) 