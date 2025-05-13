"""
Example of using the API Validation Framework in a Lambda function.

This example demonstrates how to use the validation framework to validate 
requests to a create_employee API endpoint.
"""

import json
import os
import logging
from typing import Dict, Any

from common.validation import (
    validate_request, RequiredRule, StringRule, EmailRule, PhoneRule,
    CommonValidations, SchemaTemplates
)
from common.response import Response
from common.errors import BadRequestError, ResourceNotFoundError

# Set up logging
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

# Define validation schema
create_employee_schema = {
    "body": {
        "first_name": [RequiredRule(), StringRule(min_length=2, max_length=50)],
        "last_name": [RequiredRule(), StringRule(min_length=2, max_length=50)],
        "email": [RequiredRule(), EmailRule()],
        "position": [RequiredRule(), StringRule(max_length=100)],
        "team_id": [StringRule(pattern=r"^TEAM-[A-Z0-9]{8}$")], 
        "phone_number": [PhoneRule()],
        "address": [StringRule(max_length=255)],
        "employee_code": [RequiredRule(), StringRule(pattern=r"^EMP-[A-Z0-9]{6}$")]
    },
    "query_string": {
        "include_skills": [StringRule(enum=["true", "false"])]
    }
}

# Define schema using CommonValidations for get employee endpoint
get_employee_schema = {
    "path_parameters": {
        "employee_id": CommonValidations.required(CommonValidations.RESOURCE_ID)
    },
    "query_string": SchemaTemplates.combine(
        {
            "include_skills": [StringRule(enum=["true", "false"])],
            "include_projects": [StringRule(enum=["true", "false"])]
        }
    )
}

# Define schema for listing employees
list_employees_schema = {
    "query_string": SchemaTemplates.combine(
        SchemaTemplates.PAGINATION_PARAMS,
        SchemaTemplates.SEARCH_PARAMS,
        {
            "team_id": CommonValidations.string(pattern=r"^TEAM-[A-Z0-9]{8}$"),
            "status": CommonValidations.enum(["active", "inactive", "on_leave"]),
            "hire_date_from": CommonValidations.DATE,
            "hire_date_to": CommonValidations.DATE
        }
    )
}

@validate_request(schema=create_employee_schema, error_message="Dữ liệu nhân viên không hợp lệ")
def create_employee_handler(event, context):
    """
    Lambda handler for creating an employee.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Get validated data
        body = event.get("body", {})
        
        # Log employee creation
        logger.info(f"Creating employee with email: {body.get('email')}")
        
        # In a real implementation, you would save the employee to the database
        # For example:
        # employee_id = employee_service.create_employee(body)
        
        # For demo purposes, we'll just return success
        employee_id = "EMP-123456"
        
        return Response.success({
            "message": "Nhân viên đã được tạo thành công",
            "employee_id": employee_id
        }, status_code=201)
        
    except Exception as e:
        logger.error(f"Error creating employee: {str(e)}", exc_info=True)
        return Response.error(
            message="Có lỗi xảy ra khi tạo nhân viên",
            status_code=500,
            error_code="E6000"
        )

@validate_request(schema=get_employee_schema)
def get_employee_handler(event, context):
    """
    Lambda handler for getting an employee.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Get path parameters
        path_params = event.get("pathParameters", {})
        employee_id = path_params.get("employee_id")
        
        # Get query parameters
        query_params = event.get("queryStringParameters", {})
        include_skills = query_params.get("include_skills") == "true"
        include_projects = query_params.get("include_projects") == "true"
        
        # Log request
        logger.info(f"Getting employee with ID: {employee_id}")
        
        # In a real implementation, you would get the employee from the database
        # For example:
        # employee = employee_service.get_employee(employee_id, include_skills, include_projects)
        # if not employee:
        #     raise ResourceNotFoundError("Employee", employee_id)
        
        # For demo purposes, we'll just return dummy data
        employee = {
            "id": employee_id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": "Software Engineer",
            "team_id": "TEAM-12345678",
            "status": "active"
        }
        
        # Add skills if requested
        if include_skills:
            employee["skills"] = [
                {"id": "SKILL-1", "name": "Python", "level": 5},
                {"id": "SKILL-2", "name": "AWS Lambda", "level": 4}
            ]
            
        # Add projects if requested
        if include_projects:
            employee["projects"] = [
                {"id": "PROJ-1", "name": "Internal Management System", "role": "Developer"},
                {"id": "PROJ-2", "name": "Customer Portal", "role": "Lead"}
            ]
            
        return Response.success(employee)
        
    except ResourceNotFoundError as e:
        return Response.error(
            message=str(e),
            status_code=404,
            error_code=e.error_code
        )
    except Exception as e:
        logger.error(f"Error getting employee: {str(e)}", exc_info=True)
        return Response.error(
            message="Có lỗi xảy ra khi lấy thông tin nhân viên",
            status_code=500,
            error_code="E6000"
        )

@validate_request(schema=list_employees_schema)
def list_employees_handler(event, context):
    """
    Lambda handler for listing employees.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Get query parameters
        query_params = event.get("queryStringParameters", {})
        
        # Handle pagination
        page = int(query_params.get("page", "1"))
        size = int(query_params.get("size", "20"))
        
        # Handle other filters
        team_id = query_params.get("team_id")
        status = query_params.get("status")
        search_query = query_params.get("q")
        
        # Log request
        logger.info(f"Listing employees - page: {page}, size: {size}, filters: {query_params}")
        
        # In a real implementation, you would get employees from the database
        # For example:
        # employees, total = employee_service.list_employees(page, size, team_id, status, search_query)
        
        # For demo purposes, we'll just return dummy data
        employees = [
            {
                "id": "EMP-123456",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "position": "Software Engineer",
                "team_id": "TEAM-12345678",
                "status": "active"
            },
            {
                "id": "EMP-654321",
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "position": "Product Manager",
                "team_id": "TEAM-87654321",
                "status": "active"
            }
        ]
        
        total = 2  # Total number of employees matching the filters
        
        return Response.paginated(
            items=employees,
            count=total,
            page=page,
            page_size=size,
            has_more=(page * size < total)
        )
        
    except Exception as e:
        logger.error(f"Error listing employees: {str(e)}", exc_info=True)
        return Response.error(
            message="Có lỗi xảy ra khi lấy danh sách nhân viên",
            status_code=500,
            error_code="E6000"
        )

# Main handler that routes to the appropriate function based on the HTTP method
def handler(event, context):
    """
    Main Lambda handler that routes to the appropriate function.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    http_method = event.get("httpMethod", "").upper()
    resource = event.get("resource", "")
    
    try:
        # Route to the appropriate handler
        if http_method == "POST" and resource == "/api/v1/employees":
            return create_employee_handler(event, context)
        elif http_method == "GET" and resource == "/api/v1/employees/{employee_id}":
            return get_employee_handler(event, context)
        elif http_method == "GET" and resource == "/api/v1/employees":
            return list_employees_handler(event, context)
        else:
            return Response.error(
                message="Method not allowed",
                status_code=405,
                error_code="E6003"
            )
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return Response.error(
            message="Internal server error",
            status_code=500,
            error_code="E6000"
        ) 