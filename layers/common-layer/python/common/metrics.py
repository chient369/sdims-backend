"""
Metrics Module.

This module provides utilities for tracking metrics using aws_lambda_powertools.
"""

import time
from typing import Any, Dict, List, Optional
from aws_lambda_powertools import Metrics as PowertoolsMetrics
from aws_lambda_powertools.metrics import MetricUnit

class Metrics(PowertoolsMetrics):
    """
    Extended Metrics class with additional functionality.
    """
    
    def __init__(
        self,
        namespace: str = "API",
        service: str = "api-gateway",
        default_dimensions: Optional[Dict[str, str]] = None
    ):
        """
        Initialize metrics with standard configuration.
        
        Args:
            namespace: CloudWatch metrics namespace
            service: Service name for metrics context
            default_dimensions: Default dimensions for all metrics
        """
        super().__init__(
            namespace=namespace,
            service=service,
            default_dimensions=default_dimensions or {}
        )
        
    def track_api_metric(
        self,
        path: str,
        method: str,
        status_code: int,
        response_time: float
    ) -> None:
        """
        Track API request metrics.
        
        Args:
            path: Request path
            method: HTTP method
            status_code: Response status code
            response_time: Request processing time in milliseconds
        """
        # Add default dimensions
        self.add_dimension(name="Path", value=path)
        self.add_dimension(name="Method", value=method)
        self.add_dimension(name="StatusCode", value=str(status_code))
        
        # Track request count
        self.add_metric(
            name="RequestCount",
            unit=MetricUnit.Count,
            value=1
        )
        
        # Track response time
        self.add_metric(
            name="ResponseTime",
            unit=MetricUnit.Milliseconds,
            value=response_time
        )
        
        # Track errors if status code is 4xx or 5xx
        if status_code >= 400:
            self.add_metric(
                name="ErrorCount",
                unit=MetricUnit.Count,
                value=1
            )
            
        self.flush_metrics()
        
    def track_external_call(
        self,
        service: str,
        operation: str,
        success: bool,
        response_time: float
    ) -> None:
        """
        Track external service call metrics.
        
        Args:
            service: External service name
            operation: Operation being performed
            success: Whether the call succeeded
            response_time: Call duration in milliseconds
        """
        # Add dimensions for the external call
        self.add_dimension(name="Service", value=service)
        self.add_dimension(name="Operation", value=operation)
        
        # Track call count
        self.add_metric(
            name="ExternalCallCount",
            unit=MetricUnit.Count,
            value=1
        )
        
        # Track response time
        self.add_metric(
            name="ExternalCallResponseTime",
            unit=MetricUnit.Milliseconds,
            value=response_time
        )
        
        # Track success/failure
        if not success:
            self.add_metric(
                name="ExternalCallErrorCount",
                unit=MetricUnit.Count,
                value=1
            )
            
        self.flush_metrics()
        
    def track_business_metric(
        self,
        name: str,
        value: float,
        unit: MetricUnit,
        dimensions: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Track custom business metrics.
        
        Args:
            name: Metric name
            value: Metric value
            unit: Metric unit
            dimensions: Optional additional dimensions
        """
        if dimensions:
            for dim_name, dim_value in dimensions.items():
                self.add_dimension(name=dim_name, value=dim_value)
                
        self.add_metric(
            name=name,
            unit=unit,
            value=value
        )
        
        self.flush_metrics()
        
class MetricsTimer:
    """
    Context manager for timing operations.
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        
    @property
    def elapsed_time(self) -> float:
        """
        Get elapsed time in milliseconds.
        
        Returns:
            Elapsed time in milliseconds
        """
        if self.start_time is None:
            raise ValueError("Timer has not been started")
            
        end = self.end_time if self.end_time is not None else time.time()
        return (end - self.start_time) * 1000  # Convert to milliseconds 