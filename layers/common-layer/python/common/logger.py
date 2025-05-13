"""
Logging Module.

This module provides a standardized logging setup using aws_lambda_powertools.
"""

import json
from typing import Any, Dict, Optional
from aws_lambda_powertools import Logger as PowertoolsLogger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

class Logger(PowertoolsLogger):
    """
    Extended Logger class with additional functionality.
    """
    
    def __init__(
        self,
        service: str = "api-gateway",
        level: str = "INFO",
        sample_rate: float = 0.1,
        stream_name: Optional[str] = None
    ):
        """
        Initialize logger with standard configuration.
        
        Args:
            service: Service name for logging context
            level: Log level (default: INFO)
            sample_rate: Sampling rate for debug logs (default: 0.1)
            stream_name: Optional CloudWatch Logs stream name
        """
        super().__init__(
            service=service,
            level=level,
            sample_rate=sample_rate,
            stream_name=stream_name,
            correlation_id_path=correlation_paths.API_GATEWAY_REST
        )
        
    def inject_lambda_context(self, lambda_handler):
        """
        Decorator to inject Lambda context and correlation ID.
        
        Args:
            lambda_handler: Lambda handler function
            
        Returns:
            Decorated handler function
        """
        return super().inject_lambda_context(
            lambda_handler,
            correlation_id_path=correlation_paths.API_GATEWAY_REST
        )
        
    def log_event(self, event: Dict[str, Any], context: LambdaContext) -> None:
        """
        Log Lambda event and context details.
        
        Args:
            event: Lambda event
            context: Lambda context
        """
        # Remove sensitive information
        sanitized_event = self._sanitize_event(event)
        
        self.debug(
            "Lambda event",
            extra={
                "event": sanitized_event,
                "function_name": context.function_name,
                "function_version": context.function_version,
                "memory_limit": context.memory_limit_in_mb,
                "aws_request_id": context.aws_request_id
            }
        )
        
    def _sanitize_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove sensitive information from event before logging.
        
        Args:
            event: Event to sanitize
            
        Returns:
            Sanitized event dictionary
        """
        if not isinstance(event, dict):
            return event
            
        sanitized = event.copy()
        
        # Remove sensitive headers
        if 'headers' in sanitized:
            headers = sanitized['headers']
            if isinstance(headers, dict):
                for sensitive_header in ['Authorization', 'Cookie', 'X-Api-Key']:
                    if sensitive_header in headers:
                        headers[sensitive_header] = '[REDACTED]'
                        
        # Remove sensitive fields from body
        if 'body' in sanitized:
            try:
                body = (
                    json.loads(sanitized['body'])
                    if isinstance(sanitized['body'], str)
                    else sanitized['body']
                )
                if isinstance(body, dict):
                    for sensitive_field in ['password', 'token', 'api_key', 'secret']:
                        if sensitive_field in body:
                            body[sensitive_field] = '[REDACTED]'
                    sanitized['body'] = (
                        json.dumps(body)
                        if isinstance(sanitized['body'], str)
                        else body
                    )
            except json.JSONDecodeError:
                pass
                
        return sanitized
        
    def log_api_event(
        self,
        method: str,
        path: str,
        status_code: int,
        response_time: float,
        error: Optional[Exception] = None
    ) -> None:
        """
        Log API request details.
        
        Args:
            method: HTTP method
            path: Request path
            status_code: Response status code
            response_time: Request processing time in milliseconds
            error: Optional exception if request failed
        """
        extra = {
            "http_method": method,
            "path": path,
            "status_code": status_code,
            "response_time_ms": response_time
        }
        
        if error:
            extra["error"] = str(error)
            extra["error_type"] = error.__class__.__name__
            self.error(f"API request failed: {path}", extra=extra)
        else:
            self.info("API request processed", extra=extra)
            
    def log_external_call(
        self,
        service: str,
        operation: str,
        success: bool,
        response_time: float,
        error: Optional[Exception] = None
    ) -> None:
        """
        Log external service call details.
        
        Args:
            service: External service name
            operation: Operation being performed
            success: Whether the call succeeded
            response_time: Call duration in milliseconds
            error: Optional exception if call failed
        """
        extra = {
            "service": service,
            "operation": operation,
            "success": success,
            "response_time_ms": response_time
        }
        
        if error:
            extra["error"] = str(error)
            extra["error_type"] = error.__class__.__name__
            self.error(f"External service call failed: {service}.{operation}", extra=extra)
        else:
            self.info(f"External service call completed: {service}.{operation}", extra=extra) 