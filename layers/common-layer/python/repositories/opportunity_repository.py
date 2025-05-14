import logging
import boto3
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from common.models.opportunity import Opportunity, OpportunityList
from common.errors import DatabaseError, NotFoundException, ValidationError

logger = logging.getLogger(__name__)

class OpportunityRepository:
    """Repository class for interacting with Opportunity data in DynamoDB"""
    
    def __init__(self, table_name: str, dynamodb_resource=None):
        """Initialize the repository with table name and optional DynamoDB resource"""
        self.table_name = table_name
        self.dynamodb = dynamodb_resource or boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        
    def _parse_filter_params(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate filter parameters"""
        valid_filters = {}
        
        # Status filter
        if 'status' in filters and filters['status']:
            valid_filters['status'] = filters['status']
            
        # Follow-up status filter
        if 'follow_up_status' in filters and filters['follow_up_status']:
            valid_filters['follow_up_status'] = filters['follow_up_status']
            
        # Assigned to filter
        if 'assigned_to' in filters and filters['assigned_to']:
            valid_filters['assigned_to'] = filters['assigned_to']
            
        # Customer name filter
        if 'customer_name' in filters and filters['customer_name']:
            valid_filters['customer_name'] = filters['customer_name']
            
        # Date range filters
        date_filters = ['created_after', 'created_before', 'updated_after', 
                       'updated_before', 'interaction_after', 'interaction_before']
        
        for date_filter in date_filters:
            if date_filter in filters and filters[date_filter]:
                try:
                    # Convert to datetime if it's a string
                    if isinstance(filters[date_filter], str):
                        valid_filters[date_filter] = datetime.fromisoformat(filters[date_filter])
                    else:
                        valid_filters[date_filter] = filters[date_filter]
                except ValueError:
                    raise ValidationError(f"Invalid date format for {date_filter}")
                    
        # Value range filters
        if 'min_value' in filters and filters['min_value'] is not None:
            try:
                valid_filters['min_value'] = float(filters['min_value'])
            except ValueError:
                raise ValidationError("min_value must be a number")
                
        if 'max_value' in filters and filters['max_value'] is not None:
            try:
                valid_filters['max_value'] = float(filters['max_value'])
            except ValueError:
                raise ValidationError("max_value must be a number")
                
        return valid_filters
    
    def _calculate_followup_status(self, opportunity: Dict[str, Any]) -> str:
        """Calculate the follow-up status based on opportunity data"""
        # Default days thresholds (these could be moved to system configuration)
        RED_THRESHOLD_DAYS = 7  # No interaction for 7+ days
        YELLOW_THRESHOLD_DAYS = 2  # Follow-up due in 2 days
        
        # Get last interaction date
        last_interaction = opportunity.get('last_interaction_date')
        if not last_interaction:
            # If no interaction recorded, consider as RED
            return "Red"
            
        # Convert to datetime if it's a string
        if isinstance(last_interaction, str):
            last_interaction = datetime.fromisoformat(last_interaction)
            
        # Calculate days since last interaction
        days_since_interaction = (datetime.now() - last_interaction).days
        
        # Get next follow-up date
        next_followup = opportunity.get('next_followup_date')
        if next_followup and isinstance(next_followup, str):
            next_followup = datetime.fromisoformat(next_followup)
        
        # RED: No interaction for too long
        if days_since_interaction >= RED_THRESHOLD_DAYS:
            return "Red"
            
        # YELLOW: Follow-up due soon
        if next_followup:
            days_to_followup = (next_followup - datetime.now()).days
            if days_to_followup <= YELLOW_THRESHOLD_DAYS and days_to_followup >= 0:
                return "Yellow"
                
        # Deal stage-based logic
        deal_stage = opportunity.get('deal_stage')
        if deal_stage in ['proposal', 'negotiation'] and days_since_interaction >= 3:
            return "Yellow"
            
        # Default: GREEN
        return "Green"
    
    def list_opportunities(
        self, 
        limit: int = 10, 
        next_token: Optional[str] = None,
        filters: Dict[str, Any] = None,
        search_term: Optional[str] = None,
        sort_by: str = 'updated_at',
        sort_order: str = 'desc'
    ) -> OpportunityList:
        """
        Retrieve a list of opportunities with pagination, filtering, and sorting
        
        Args:
            limit: Maximum number of items to return
            next_token: Token for pagination
            filters: Dictionary of filter parameters
            search_term: Text to search in name, description and customer_name
            sort_by: Field to sort by
            sort_order: Sort direction ('asc' or 'desc')
            
        Returns:
            OpportunityList with items, count and next_token
        """
        try:
            # Parse the next_token if provided
            exclusive_start_key = None
            if next_token:
                try:
                    exclusive_start_key = json.loads(next_token)
                except json.JSONDecodeError:
                    raise ValidationError("Invalid pagination token")
            
            # Parse and validate filters
            valid_filters = {}
            if filters:
                valid_filters = self._parse_filter_params(filters)
            
            # Determine which GSI to use based on filters and sort
            # Default to main table scan with filter expressions
            params = {
                'TableName': self.table_name,
                'Limit': limit
            }
            
            # If user's assigned_to filter is provided, use GSI3
            if valid_filters.get('assigned_to'):
                params['IndexName'] = 'GSI3'
                params['KeyConditionExpression'] = Key('GSI3PK').eq(f"SALES#{valid_filters['assigned_to']}")
                
            # If status filter is provided, use GSI2
            elif valid_filters.get('status'):
                params['IndexName'] = 'GSI2'
                params['KeyConditionExpression'] = Key('GSI2PK').eq(f"OPPORTUNITY_STAGE#{valid_filters['status']}")
                
            # Default query - scan with FilterExpression
            else:
                # Base filter for non-deleted opportunities
                filter_expr = Attr('PK').begins_with('OPPORTUNITY#') & Attr('is_deleted').ne(True)
                
                # Apply additional filters
                if valid_filters.get('customer_name'):
                    filter_expr = filter_expr & Attr('customer_name').contains(valid_filters['customer_name'])
                    
                if valid_filters.get('follow_up_status'):
                    filter_expr = filter_expr & Attr('followup_status').eq(valid_filters['follow_up_status'])
                    
                # Date range filters
                if valid_filters.get('created_after'):
                    created_after = valid_filters['created_after'].isoformat()
                    filter_expr = filter_expr & Attr('created_at').gte(created_after)
                    
                if valid_filters.get('created_before'):
                    created_before = valid_filters['created_before'].isoformat()
                    filter_expr = filter_expr & Attr('created_at').lte(created_before)
                    
                if valid_filters.get('updated_after'):
                    updated_after = valid_filters['updated_after'].isoformat()
                    filter_expr = filter_expr & Attr('updated_at').gte(updated_after)
                    
                if valid_filters.get('updated_before'):
                    updated_before = valid_filters['updated_before'].isoformat()
                    filter_expr = filter_expr & Attr('updated_at').lte(updated_before)
                    
                if valid_filters.get('interaction_after'):
                    interaction_after = valid_filters['interaction_after'].isoformat()
                    filter_expr = filter_expr & Attr('last_interaction_date').gte(interaction_after)
                    
                if valid_filters.get('interaction_before'):
                    interaction_before = valid_filters['interaction_before'].isoformat()
                    filter_expr = filter_expr & Attr('last_interaction_date').lte(interaction_before)
                    
                # Value range filters
                if valid_filters.get('min_value') is not None:
                    filter_expr = filter_expr & Attr('estimated_value_usd').gte(Decimal(str(valid_filters['min_value'])))
                    
                if valid_filters.get('max_value') is not None:
                    filter_expr = filter_expr & Attr('estimated_value_usd').lte(Decimal(str(valid_filters['max_value'])))
                    
                # Search term across multiple fields
                if search_term:
                    search_expr = (
                        Attr('name').contains(search_term) | 
                        Attr('description').contains(search_term) | 
                        Attr('customer_name').contains(search_term)
                    )
                    filter_expr = filter_expr & search_expr
                    
                params['FilterExpression'] = filter_expr
            
            # Add exclusive start key for pagination
            if exclusive_start_key:
                params['ExclusiveStartKey'] = exclusive_start_key
            
            # Execute the query or scan
            if 'KeyConditionExpression' in params:
                response = self.table.query(**params)
            else:
                response = self.table.scan(**params)
            
            # Process results
            items = []
            for item in response.get('Items', []):
                # Calculate follow-up status dynamically if not already set
                if 'followup_status' not in item:
                    item['followup_status'] = self._calculate_followup_status(item)
                    
                opportunity = Opportunity.from_dynamo_item(item)
                if opportunity:
                    items.append(opportunity)
            
            # Prepare pagination token for next request
            result = OpportunityList(
                items=items,
                count=len(items),
                next_token=json.dumps(response.get('LastEvaluatedKey')) if 'LastEvaluatedKey' in response else None
            )
            
            return result
            
        except ClientError as e:
            logger.error(f"DynamoDB error in list_opportunities: {str(e)}")
            raise DatabaseError(f"Failed to list opportunities: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in list_opportunities: {str(e)}")
            raise DatabaseError(f"Failed to list opportunities: {str(e)}")
    
    def get_opportunity_by_id(self, opportunity_id: str) -> Opportunity:
        """
        Retrieve a single opportunity by ID
        
        Args:
            opportunity_id: The ID of the opportunity to retrieve
            
        Returns:
            Opportunity object
            
        Raises:
            NotFoundException: If opportunity is not found
            DatabaseError: If there is a database error
        """
        try:
            response = self.table.get_item(
                Key={
                    'PK': f"OPPORTUNITY#{opportunity_id}",
                    'SK': f"METADATA#{opportunity_id}"
                }
            )
            
            item = response.get('Item')
            if not item:
                raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
                
            # Check if opportunity is deleted
            if item.get('is_deleted'):
                raise NotFoundException(f"Opportunity with ID {opportunity_id} not found or is deleted")
                
            # Calculate follow-up status dynamically if not already set
            if 'followup_status' not in item:
                item['followup_status'] = self._calculate_followup_status(item)
                
            return Opportunity.from_dynamo_item(item)
            
        except ClientError as e:
            logger.error(f"DynamoDB error in get_opportunity_by_id: {str(e)}")
            raise DatabaseError(f"Failed to get opportunity: {str(e)}")
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_opportunity_by_id: {str(e)}")
            raise DatabaseError(f"Failed to get opportunity: {str(e)}") 