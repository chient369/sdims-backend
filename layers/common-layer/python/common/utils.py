"""
Common Utilities Module.

This module provides common utility functions used across the application.
"""

import json
import uuid
import base64
import hashlib
import datetime
from typing import Any, Dict, List, Optional, Union

def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID with optional prefix.
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Unique ID string
    """
    unique_id = str(uuid.uuid4())
    return f"{prefix}{unique_id}" if prefix else unique_id

def parse_json(json_str: str) -> Dict[str, Any]:
    """
    Safely parse JSON string.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed JSON as dictionary
        
    Raises:
        ValueError: If JSON is invalid
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")

def format_datetime(dt: datetime.datetime, format: str = "%Y-%m-%dT%H:%M:%S.%fZ") -> str:
    """
    Format datetime object to string.
    
    Args:
        dt: Datetime object
        format: Optional datetime format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format)

def parse_datetime(dt_str: str, format: str = "%Y-%m-%dT%H:%M:%S.%fZ") -> datetime.datetime:
    """
    Parse datetime string to datetime object.
    
    Args:
        dt_str: Datetime string
        format: Optional datetime format string
        
    Returns:
        Datetime object
        
    Raises:
        ValueError: If datetime string is invalid
    """
    try:
        return datetime.datetime.strptime(dt_str, format)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {str(e)}")

def hash_string(value: str, algorithm: str = "sha256") -> str:
    """
    Hash a string using specified algorithm.
    
    Args:
        value: String to hash
        algorithm: Hash algorithm (default: sha256)
        
    Returns:
        Hashed string
        
    Raises:
        ValueError: If algorithm is not supported
    """
    try:
        hasher = hashlib.new(algorithm)
        hasher.update(value.encode())
        return hasher.hexdigest()
    except ValueError as e:
        raise ValueError(f"Unsupported hash algorithm: {str(e)}")

def encode_base64(data: Union[str, bytes]) -> str:
    """
    Encode data to base64 string.
    
    Args:
        data: String or bytes to encode
        
    Returns:
        Base64 encoded string
    """
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(data).decode()

def decode_base64(data: str) -> bytes:
    """
    Decode base64 string to bytes.
    
    Args:
        data: Base64 string to decode
        
    Returns:
        Decoded bytes
        
    Raises:
        ValueError: If input is not valid base64
    """
    try:
        return base64.b64decode(data)
    except Exception as e:
        raise ValueError(f"Invalid base64 data: {str(e)}")

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size.
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if (
            key in result and
            isinstance(result[key], dict) and
            isinstance(value, dict)
        ):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
            
    return result

def filter_dict(
    data: Dict[str, Any],
    include_keys: Optional[List[str]] = None,
    exclude_keys: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Filter dictionary keys.
    
    Args:
        data: Dictionary to filter
        include_keys: Keys to include (if None, include all)
        exclude_keys: Keys to exclude
        
    Returns:
        Filtered dictionary
    """
    result = {}
    
    for key, value in data.items():
        if exclude_keys and key in exclude_keys:
            continue
            
        if include_keys is None or key in include_keys:
            result[key] = value
            
    return result

def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r"^\+?[0-9]{10,15}$"
    return bool(re.match(pattern, phone))

def sanitize_string(value: str) -> str:
    """
    Sanitize string by removing special characters.
    
    Args:
        value: String to sanitize
        
    Returns:
        Sanitized string
    """
    import re
    return re.sub(r'[^a-zA-Z0-9\s-]', '', value)

def truncate_string(value: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        value: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(value) <= max_length:
        return value
        
    return value[:max_length - len(suffix)] + suffix

def format_currency(
    amount: float,
    currency: str = "USD",
    locale: str = "en_US"
) -> str:
    """
    Format currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
        locale: Locale code
        
    Returns:
        Formatted currency string
    """
    import locale as loc
    loc.setlocale(loc.LC_ALL, locale)
    return loc.currency(amount, currency, grouping=True)

def parse_bool(value: Union[str, bool]) -> bool:
    """
    Parse boolean value from string.
    
    Args:
        value: Value to parse
        
    Returns:
        Boolean value
        
    Raises:
        ValueError: If value cannot be parsed as boolean
    """
    if isinstance(value, bool):
        return value
        
    value = str(value).lower()
    if value in ('true', '1', 'yes', 'on'):
        return True
    elif value in ('false', '0', 'no', 'off'):
        return False
        
    raise ValueError(f"Cannot parse as boolean: {value}")

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Retry decorator for functions.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts in seconds
        backoff: Multiplier for delay between attempts
        exceptions: Tuple of exceptions to catch
        
    Returns:
        Decorated function
    """
    import time
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
                        
            raise last_exception
            
        return wrapper
    return decorator 