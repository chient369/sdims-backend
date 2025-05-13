"""
Model Mapping Utilities for SDIMS

This package provides utilities for mapping between DynamoDB items and Python model objects.
"""

from common.models.base_model import BaseModel
from common.models.decorators import (
    dynamodb_model,
    attribute,
    primary_key,
    sort_key,
    gsi_partition_key,
    gsi_sort_key,
    auto_generate,
    validate,
    default_value
) 