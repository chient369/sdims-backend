"""
Lambda handlers for opportunity management
"""
import json
import logging
import os
from typing import Dict, Any, Optional

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.parser import parse_qs
from aws_lambda_powertools.event_handler import content_types
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError

# Add common layer to path
import sys
import os
sys.path.append('/opt/python')

from services.opportunity_service import OpportunityService
from common.errors import ValidationError, NotFoundException, DatabaseError
from common.response import build_response, build_error_response

logger = Logger(service="opportunities")
tracer = Tracer(service="opportunities")
app = ApiGatewayResolver(proxy_type="api_gateway_proxy")

# Initialize services
opportunity_service = OpportunityService()

@app.get("/api/v1/opportunities")
@tracer.capture_method
def list_opportunities():
    """
    Handler for GET /api/v1/opportunities
    List opportunities with filtering, pagination, and sorting
    """
    try:
        # Parse query string parameters
        query_params = app.current_event.query_string_parameters or {}
        
        # Pagination
        page_size = int(query_params.get('page_size', '10'))
        next_token = query_params.get('next_token')
        
        # Sorting
        sort_by = query_params.get('sort_by', 'updated_at')
        sort_order = query_params.get('sort_order', 'desc')
        
        # Search
        search_term = query_params.get('search')
        
        # Filters
        filters = {}
        filter_params = [
            'status', 'follow_up_status', 'assigned_to', 'customer_name',
            'created_after', 'created_before', 'updated_after', 'updated_before',
            'interaction_after', 'interaction_before', 'min_value', 'max_value'
        ]
        
        for param in filter_params:
            if param in query_params and query_params[param]:
                filters[param] = query_params[param]
                
        # Call service
        result = opportunity_service.list_opportunities(
            page_size=page_size,
            next_token=next_token,
            filters=filters,
            search_term=search_term,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Return response
        return build_response(
            status_code=200,
            body={
                "items": [item.dict(exclude_none=True) for item in result.items],
                "next_token": result.next_token,
                "count": result.count
            }
        )
        
    except ValidationError as e:
        logger.warning(f"Validation error in list_opportunities: {str(e)}")
        return build_error_response(status_code=400, error_code="E2000", message=str(e))
        
    except DatabaseError as e:
        logger.error(f"Database error in list_opportunities: {str(e)}")
        return build_error_response(status_code=500, error_code="E6001", message="An error occurred while retrieving opportunities")
        
    except Exception as e:
        logger.exception(f"Unexpected error in list_opportunities: {str(e)}")
        return build_error_response(status_code=500, error_code="E6000", message="An unexpected error occurred")

@app.get("/api/v1/opportunities/<opportunity_id>")
@tracer.capture_method
def get_opportunity(opportunity_id: str):
    """
    Handler for GET /api/v1/opportunities/{opportunity_id}
    Get a single opportunity by ID
    """
    try:
        # Call service
        opportunity = opportunity_service.get_opportunity(opportunity_id)
        
        # Return response
        return build_response(
            status_code=200,
            body=opportunity.dict(exclude_none=True)
        )
        
    except NotFoundException as e:
        logger.warning(f"Not found error in get_opportunity: {str(e)}")
        return build_error_response(status_code=404, error_code="E3002", message=str(e))
        
    except ValidationError as e:
        logger.warning(f"Validation error in get_opportunity: {str(e)}")
        return build_error_response(status_code=400, error_code="E2000", message=str(e))
        
    except DatabaseError as e:
        logger.error(f"Database error in get_opportunity: {str(e)}")
        return build_error_response(status_code=500, error_code="E6001", message="An error occurred while retrieving the opportunity")
        
    except Exception as e:
        logger.exception(f"Unexpected error in get_opportunity: {str(e)}")
        return build_error_response(status_code=500, error_code="E6000", message="An unexpected error occurred")

def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda handler for Opportunity APIs
    """
    logger.debug(f"Received event: {json.dumps(event)}")
    
    # Forward event to ApiGatewayResolver
    return app.resolve(event, context) 