"""
Logger Utilities for SDIMS

This module provides extended logging utilities based on AWS Lambda Powertools.
"""

import os
import json
import traceback
from typing import Dict, Any, Optional, List
from aws_lambda_powertools import Logger as PowertoolsLogger
from aws_lambda_powertools.logging import correlation_paths

class Logger:
    """
    Extended logger based on AWS Lambda Powertools
    """
    
    def __init__(self, service: str, level: Optional[str] = None, 
                sampling_rate: float = 0.1, correlation_id_path: Optional[str] = None):
        """
        Initialize logger
        
        Args:
            service: Service name
            level: Log level (INFO, DEBUG, etc.)
            sampling_rate: Sampling rate for debug logs (0.0 to 1.0)
            correlation_id_path: Path to extract correlation ID
        """
        log_level = level or os.environ.get('LOG_LEVEL', 'INFO')
        
        # Setup correlation ID configuration
        if not correlation_id_path:
            correlation_id_path = correlation_paths.API_GATEWAY_REST
            
        self.sampling_rate = sampling_rate
        self.logger = PowertoolsLogger(
            service=service,
            level=log_level,
            correlation_id_path=correlation_id_path
        )
        
    def append_keys(self, **kwargs) -> None:
        """
        Append keys to logger context
        
        Args:
            **kwargs: Key-value pairs to add to the logger context
        """
        self.logger.append_keys(**kwargs)
        
    def remove_keys(self, keys: List[str]) -> None:
        """
        Remove keys from logger context
        
        Args:
            keys: List of keys to remove
        """
        for key in keys:
            self.logger.remove_keys(keys)
            
    def set_correlation_id(self, correlation_id: str) -> None:
        """
        Set correlation ID explicitly
        
        Args:
            correlation_id: Correlation ID to use
        """
        self.logger.set_correlation_id(correlation_id)
        
    def info(self, message: str, **kwargs) -> None:
        """
        Log info message with additional context
        
        Args:
            message: Log message
            **kwargs: Additional context as key-value pairs
        """
        self.logger.info(message, **kwargs)
        
    def error(self, message: str, exc: Optional[Exception] = None, **kwargs) -> None:
        """
        Log error message with exception details if provided
        
        Args:
            message: Error message
            exc: Exception object
            **kwargs: Additional context as key-value pairs
        """
        if exc:
            kwargs['exception_type'] = type(exc).__name__
            kwargs['exception'] = str(exc)
            kwargs['traceback'] = traceback.format_exc()
        self.logger.error(message, **kwargs)
        
    def warning(self, message: str, **kwargs) -> None:
        """
        Log warning message with additional context
        
        Args:
            message: Warning message
            **kwargs: Additional context as key-value pairs
        """
        self.logger.warning(message, **kwargs)
        
    def debug(self, message: str, **kwargs) -> None:
        """
        Log debug message with additional context
        
        Args:
            message: Debug message
            **kwargs: Additional context as key-value pairs
        """
        self.logger.debug(message, **kwargs)
        
    def critical(self, message: str, **kwargs) -> None:
        """
        Log critical message with additional context
        
        Args:
            message: Critical message
            **kwargs: Additional context as key-value pairs
        """
        self.logger.critical(message, **kwargs)
        
    def inject_lambda_context(self, lambda_handler):
        """
        Decorator to inject Lambda context info to logger
        
        Args:
            lambda_handler: Lambda handler function
            
        Returns:
            Decorated handler function
        """
        return self.logger.inject_lambda_context(lambda_handler)
        
    def log_event(self, event: Dict[str, Any], level: str = "DEBUG") -> None:
        """
        Log API Gateway event with appropriate sanitization
        
        Args:
            event: API Gateway event
            level: Log level
        """
        # Deep copy event to avoid modifying the original
        event_copy = json.loads(json.dumps(event))
        
        # Remove sensitive fields from headers if present
        headers = event_copy.get('headers', {})
        if headers and isinstance(headers, dict):
            for sensitive_header in ['authorization', 'x-api-key', 'x-amz-security-token']:
                if sensitive_header in headers:
                    headers[sensitive_header] = '[REDACTED]'
                    
        # Sanitize body if it contains sensitive information
        body = event_copy.get('body')
        if body and isinstance(body, str):
            try:
                body_json = json.loads(body)
                for sensitive_field in ['password', 'token', 'refreshToken', 'apiKey', 'secret']:
                    if sensitive_field in body_json:
                        body_json[sensitive_field] = '[REDACTED]'
                event_copy['body'] = json.dumps(body_json)
            except (json.JSONDecodeError, TypeError):
                # Body is not JSON or already parsed as JSON
                pass
                
        # Log the sanitized event
        if level == "INFO":
            self.logger.info("Received API Gateway event", event=event_copy)
        elif level == "DEBUG":
            self.logger.debug("Received API Gateway event", event=event_copy)
        elif level == "ERROR":
            self.logger.error("Received API Gateway event", event=event_copy)
            
    def log_response(self, response: Dict[str, Any], level: str = "DEBUG") -> None:
        """
        Log Lambda response with appropriate sanitization
        
        Args:
            response: Lambda response
            level: Log level
        """
        # Don't log binary responses or extremely large ones
        if response.get('isBase64Encoded', False):
            if level == "INFO":
                self.logger.info("Binary response (not logged)")
            elif level == "DEBUG":
                self.logger.debug("Binary response (not logged)")
            return
            
        # Deep copy response to avoid modifying the original
        response_copy = json.loads(json.dumps(response))
        
        # Sanitize body if it's very large
        body = response_copy.get('body')
        if body and isinstance(body, str) and len(body) > 1000:
            try:
                body_json = json.loads(body)
                # Keep structure but limit content
                if isinstance(body_json, list) and len(body_json) > 10:
                    response_copy['body'] = json.dumps({
                        'array_preview': body_json[:3],
                        'array_length': len(body_json),
                        'message': 'Array truncated for logging'
                    })
                elif isinstance(body_json, dict) and len(json.dumps(body_json)) > 1000:
                    # For large objects, only keep first level keys
                    preview = {k: '...' for k in body_json.keys()}
                    response_copy['body'] = json.dumps({
                        'object_preview': preview,
                        'message': 'Object content truncated for logging'
                    })
            except (json.JSONDecodeError, TypeError):
                # Body is not JSON or already parsed
                response_copy['body'] = f"Response body truncated ({len(body)} chars)"
                
        # Log the sanitized response
        if level == "INFO":
            self.logger.info("Lambda response", response=response_copy)
        elif level == "DEBUG":
            self.logger.debug("Lambda response", response=response_copy)
        elif level == "ERROR":
            self.logger.error("Lambda response", response=response_copy) 