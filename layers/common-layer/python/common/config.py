"""
Configuration Management Module.

This module provides utilities for managing application configuration
using environment variables and AWS Parameter Store.
"""

import os
import json
from typing import Any, Dict, Optional
import boto3
from botocore.exceptions import ClientError
from .errors import ConfigurationError

class Config:
    """
    Configuration management class.
    """
    
    def __init__(
        self,
        env: str = None,
        parameter_path: str = None,
        use_ssm: bool = True
    ):
        """
        Initialize configuration manager.
        
        Args:
            env: Environment name (dev, staging, prod)
            parameter_path: SSM parameter path prefix
            use_ssm: Whether to use AWS Parameter Store
        """
        self.env = env or os.getenv('ENVIRONMENT', 'dev')
        self.parameter_path = parameter_path or f"/sdims/{self.env}"
        self.use_ssm = use_ssm
        self._config_cache: Dict[str, Any] = {}
        
        if use_ssm:
            self.ssm_client = boto3.client('ssm')
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        # Check environment variables first
        env_key = key.upper().replace('.', '_')
        value = os.getenv(env_key)
        if value is not None:
            return self._parse_value(value)
            
        # Check cache
        if key in self._config_cache:
            return self._config_cache[key]
            
        # Check Parameter Store if enabled
        if self.use_ssm:
            ssm_value = self._get_ssm_parameter(key)
            if ssm_value is not None:
                self._config_cache[key] = ssm_value
                return ssm_value
                
        return default
        
    def require(self, key: str) -> Any:
        """
        Get required configuration value.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
            
        Raises:
            ConfigurationError: If key not found
        """
        value = self.get(key)
        if value is None:
            raise ConfigurationError(f"Required configuration key not found: {key}")
        return value
        
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config_cache[key] = value
        
    def _get_ssm_parameter(self, key: str) -> Optional[Any]:
        """
        Get parameter from AWS Parameter Store.
        
        Args:
            key: Parameter key
            
        Returns:
            Parameter value if found, None otherwise
        """
        try:
            parameter_name = f"{self.parameter_path}/{key}"
            response = self.ssm_client.get_parameter(
                Name=parameter_name,
                WithDecryption=True
            )
            return self._parse_value(response['Parameter']['Value'])
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterNotFound':
                return None
            raise ConfigurationError(f"Error getting SSM parameter: {str(e)}")
            
    def _parse_value(self, value: str) -> Any:
        """
        Parse configuration value.
        
        Args:
            value: String value to parse
            
        Returns:
            Parsed value
        """
        # Try parsing as JSON
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
            
        # Parse boolean values
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False
            
        # Parse numeric values
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
            
        # Return as string
        return value
        
    def load_json(self, json_str: str) -> None:
        """
        Load configuration from JSON string.
        
        Args:
            json_str: JSON configuration string
            
        Raises:
            ConfigurationError: If JSON is invalid
        """
        try:
            config = json.loads(json_str)
            self._config_cache.update(config)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON configuration: {str(e)}")
            
    def load_file(self, file_path: str) -> None:
        """
        Load configuration from JSON file.
        
        Args:
            file_path: Path to JSON configuration file
            
        Raises:
            ConfigurationError: If file cannot be read or has invalid JSON
        """
        try:
            with open(file_path, 'r') as f:
                self.load_json(f.read())
        except (IOError, OSError) as e:
            raise ConfigurationError(f"Error reading configuration file: {str(e)}")
            
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Dictionary of all configuration values
        """
        return self._config_cache.copy()
        
    def clear(self) -> None:
        """Clear configuration cache."""
        self._config_cache.clear()
        
    def reload(self) -> None:
        """Reload configuration from all sources."""
        self.clear()
        if self.use_ssm:
            try:
                # Get all parameters under path
                paginator = self.ssm_client.get_paginator('get_parameters_by_path')
                for page in paginator.paginate(
                    Path=self.parameter_path,
                    Recursive=True,
                    WithDecryption=True
                ):
                    for parameter in page['Parameters']:
                        name = parameter['Name'].replace(f"{self.parameter_path}/", '')
                        value = self._parse_value(parameter['Value'])
                        self._config_cache[name] = value
            except ClientError as e:
                raise ConfigurationError(f"Error reloading SSM parameters: {str(e)}")
                
# Global configuration instance
config = Config() 