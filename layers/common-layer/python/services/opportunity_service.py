import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

from repositories.opportunity_repository import OpportunityRepository
from common.models.opportunity import Opportunity, OpportunityList
from common.errors import ValidationError, NotFoundException, DatabaseError

logger = logging.getLogger(__name__)

class OpportunityService:
    """Service class for opportunity business logic"""
    
    def __init__(self, table_name: Optional[str] = None):
        """
        Initialize the service with repositories
        
        Args:
            table_name: Optional DynamoDB table name, defaults to os.environ.get('TABLE_NAME')
        """
        self.table_name = table_name or os.environ.get('TABLE_NAME')
        if not self.table_name:
            raise ValueError("DynamoDB table name is required")
            
        self.opportunity_repository = OpportunityRepository(self.table_name)
        
    def list_opportunities(
        self,
        page_size: int = 10,
        next_token: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        search_term: Optional[str] = None,
        sort_by: str = 'updated_at',
        sort_order: str = 'desc'
    ) -> OpportunityList:
        """
        List opportunities with pagination, filtering, and search
        
        Args:
            page_size: Number of items per page
            next_token: Token for pagination
            filters: Dictionary of filter parameters
            search_term: Text to search across multiple fields
            sort_by: Field to sort by
            sort_order: Sort direction ('asc' or 'desc')
            
        Returns:
            OpportunityList with items, count and next_token
        """
        # Validate input parameters
        if page_size < 1 or page_size > 100:
            raise ValidationError("Page size must be between 1 and 100")
            
        if sort_order not in ['asc', 'desc']:
            raise ValidationError("Sort order must be 'asc' or 'desc'")
            
        valid_sort_fields = [
            'created_at', 'updated_at', 'last_interaction_date',
            'name', 'customer_name', 'estimated_value',
            'closing_date', 'deal_stage'
        ]
        
        if sort_by not in valid_sort_fields:
            raise ValidationError(f"Sort field must be one of: {', '.join(valid_sort_fields)}")
            
        # Delegate to repository
        return self.opportunity_repository.list_opportunities(
            limit=page_size,
            next_token=next_token,
            filters=filters or {},
            search_term=search_term,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
    def get_opportunity(self, opportunity_id: str) -> Opportunity:
        """
        Get a single opportunity by ID
        
        Args:
            opportunity_id: Opportunity ID
            
        Returns:
            Opportunity object
            
        Raises:
            NotFoundException: If opportunity is not found
        """
        if not opportunity_id:
            raise ValidationError("Opportunity ID is required")
            
        return self.opportunity_repository.get_opportunity_by_id(opportunity_id) 