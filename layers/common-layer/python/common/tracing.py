"""
Tracing Module.

This module provides utilities for distributed tracing using aws_lambda_powertools.
"""

from typing import Any, Dict, Optional
from aws_lambda_powertools import Tracer as PowertoolsTracer
from aws_lambda_powertools.tracing import annotation, capture_method

class Tracer(PowertoolsTracer):
    """
    Extended Tracer class with additional functionality.
    """
    
    def __init__(
        self,
        service: str = "api-gateway",
        disabled: bool = False,
        auto_patch: bool = True
    ):
        """
        Initialize tracer with standard configuration.
        
        Args:
            service: Service name for tracing context
            disabled: Whether tracing is disabled
            auto_patch: Whether to auto-patch supported libraries
        """
        super().__init__(
            service=service,
            disabled=disabled,
            auto_patch=auto_patch
        )
        
    def trace_api_request(
        self,
        path: str,
        method: str,
        request_id: str,
        user_id: Optional[str] = None
    ) -> None:
        """
        Add API request details to current trace.
        
        Args:
            path: Request path
            method: HTTP method
            request_id: Unique request ID
            user_id: Optional user ID
        """
        self.put_annotation(key="Path", value=path)
        self.put_annotation(key="Method", value=method)
        self.put_annotation(key="RequestId", value=request_id)
        
        if user_id:
            self.put_annotation(key="UserId", value=user_id)
            
    def trace_api_response(
        self,
        status_code: int,
        error: Optional[Exception] = None
    ) -> None:
        """
        Add API response details to current trace.
        
        Args:
            status_code: Response status code
            error: Optional exception if request failed
        """
        self.put_annotation(key="StatusCode", value=str(status_code))
        
        if error:
            self.put_annotation(key="Error", value=str(error))
            self.put_annotation(key="ErrorType", value=error.__class__.__name__)
            
    def trace_external_call(
        self,
        service: str,
        operation: str,
        success: bool,
        error: Optional[Exception] = None
    ) -> None:
        """
        Add external service call details to current trace.
        
        Args:
            service: External service name
            operation: Operation being performed
            success: Whether the call succeeded
            error: Optional exception if call failed
        """
        self.put_annotation(key="ExternalService", value=service)
        self.put_annotation(key="Operation", value=operation)
        self.put_annotation(key="Success", value=str(success))
        
        if error:
            self.put_annotation(key="Error", value=str(error))
            self.put_annotation(key="ErrorType", value=error.__class__.__name__)
            
    def trace_business_event(
        self,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """
        Add business event details to current trace.
        
        Args:
            event_type: Type of business event
            event_data: Event data dictionary
        """
        self.put_annotation(key="EventType", value=event_type)
        
        # Add event data as metadata
        self.put_metadata(
            key=event_type,
            value=event_data,
            namespace="BusinessEvents"
        )
        
def trace_handler(name: Optional[str] = None):
    """
    Decorator for tracing Lambda handlers.
    
    Args:
        name: Optional name for the trace segment
        
    Returns:
        Decorated handler function
    """
    def decorator(handler):
        tracer = Tracer()
        
        @tracer.capture_lambda_handler
        def wrapper(event, context):
            return handler(event, context)
            
        return wrapper
    return decorator
    
def trace_method(name: Optional[str] = None):
    """
    Decorator for tracing methods.
    
    Args:
        name: Optional name for the trace segment
        
    Returns:
        Decorated method
    """
    return capture_method(name=name) 