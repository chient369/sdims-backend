from aws_lambda_powertools import Metrics
from typing import Optional, Dict, Any, List
import os

# Initialize metrics
metrics = Metrics(namespace="SDIMS", service="api")

class APIMetrics:
    def __init__(self):
        """Initialize API metrics handler"""
        self.metrics = metrics
        
    def add_metric(
        self,
        name: str,
        value: float = 1,
        unit: str = "Count",
        dimensions: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Add single metric
        
        Args:
            name: Metric name
            value: Metric value
            unit: CloudWatch metric unit
            dimensions: Optional metric dimensions
        """
        try:
            self.metrics.add_metric(
                name=name,
                value=value,
                unit=unit,
                dimensions=dimensions or {}
            )
        except Exception as e:
            # Log error but don't raise to avoid impacting main flow
            print(f"Error adding metric {name}: {str(e)}")
            
    def add_dimensions(self, **dimensions: Dict[str, str]) -> None:
        """
        Add dimensions to metrics
        
        Args:
            dimensions: Dimension key-value pairs
        """
        try:
            self.metrics.add_dimension(**dimensions)
        except Exception as e:
            print(f"Error adding dimensions: {str(e)}")
            
    def flush_metrics(self) -> None:
        """Flush metrics to CloudWatch"""
        try:
            self.metrics.flush_metrics()
        except Exception as e:
            print(f"Error flushing metrics: {str(e)}")

class RequestMetrics:
    def __init__(self):
        """Initialize request metrics handler"""
        self.api_metrics = APIMetrics()
        
    def record_request(
        self,
        path: str,
        method: str,
        status_code: int,
        duration: float
    ) -> None:
        """
        Record API request metrics
        
        Args:
            path: Request path
            method: HTTP method
            status_code: Response status code
            duration: Request duration in seconds
        """
        # Add request count
        self.api_metrics.add_metric(
            name="RequestCount",
            dimensions={
                "Path": path,
                "Method": method,
                "StatusCode": str(status_code)
            }
        )
        
        # Add latency
        self.api_metrics.add_metric(
            name="Latency",
            value=duration * 1000,  # Convert to milliseconds
            unit="Milliseconds",
            dimensions={
                "Path": path,
                "Method": method
            }
        )
        
        # Add error count if applicable
        if status_code >= 400:
            self.api_metrics.add_metric(
                name="ErrorCount",
                dimensions={
                    "Path": path,
                    "Method": method,
                    "StatusCode": str(status_code)
                }
            )
            
        # Flush metrics
        self.api_metrics.flush_metrics()
        
class BusinessMetrics:
    def __init__(self):
        """Initialize business metrics handler"""
        self.api_metrics = APIMetrics()
        
    def record_business_metric(
        self,
        name: str,
        value: float,
        unit: str,
        context: Dict[str, str]
    ) -> None:
        """
        Record business-specific metric
        
        Args:
            name: Metric name
            value: Metric value
            unit: CloudWatch metric unit
            context: Business context dimensions
        """
        self.api_metrics.add_metric(
            name=name,
            value=value,
            unit=unit,
            dimensions=context
        )
        self.api_metrics.flush_metrics()

# Create singleton instances
request_metrics = RequestMetrics()
business_metrics = BusinessMetrics() 