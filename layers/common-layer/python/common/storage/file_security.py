"""
File Security Utilities

This module provides utilities for file security, including
permission management and access control.
"""

import json
from typing import Dict, List, Optional, Set, Union, Any

from common.errors import ForbiddenError, UnauthorizedError
from common.storage.exceptions import StoragePermissionError
from common.logger import Logger
from common.auth import current_user


logger = Logger(service="file-security")


class FilePermissionManager:
    """
    Manager for file permissions and access control
    """
    
    def __init__(self):
        """Initialize the FilePermissionManager"""
        pass
    
    def check_file_access(self, 
                        entity_type: str, 
                        entity_id: str, 
                        required_permission: str,
                        user_id: Optional[str] = None) -> bool:
        """
        Check if a user has permission to access a file
        
        Args:
            entity_type: The type of entity the file is related to (e.g., contract, employee)
            entity_id: The ID of the entity
            required_permission: The permission required to access the file (e.g., 'contract:read')
            user_id: Optional user ID to check (if None, current authenticated user is used)
            
        Returns:
            True if user has permission, False otherwise
            
        Raises:
            UnauthorizedError: If no user is authenticated
        """
        # If no user ID provided, use current user
        if not user_id:
            try:
                user = current_user.get_user()
                user_id = user.id
            except Exception as e:
                logger.error("No authenticated user found when checking file access", exc=e)
                raise UnauthorizedError("Authentication required to access files")
            
        try:
            # Different logic based on entity type
            if entity_type == "contract":
                return self._check_contract_file_access(entity_id, required_permission, user_id)
            elif entity_type == "employee":
                return self._check_employee_file_access(entity_id, required_permission, user_id)
            elif entity_type == "opportunity":
                return self._check_opportunity_file_access(entity_id, required_permission, user_id)
            else:
                # Default check for other entity types
                return self._check_generic_file_access(entity_type, entity_id, required_permission, user_id)
        except Exception as e:
            logger.error(f"Error checking file access for {entity_type}/{entity_id}", exc=e)
            # Default to denying access on error
            return False
    
    def _check_contract_file_access(self, contract_id: str, required_permission: str, user_id: str) -> bool:
        """
        Check access to contract files
        
        Args:
            contract_id: Contract ID
            required_permission: Required permission
            user_id: User ID
            
        Returns:
            True if user has permission, False otherwise
        """
        # Get user permissions
        user_permissions = self._get_user_permissions(user_id)
        
        # Check if user has admin/all access
        if f"{required_permission}:all" in user_permissions:
            return True
            
        # Check if user is the owner/manager of the contract
        if self._is_contract_owner(contract_id, user_id):
            if f"{required_permission}:own" in user_permissions:
                return True
                
        # Check if user is assigned to the contract
        if self._is_assigned_to_contract(contract_id, user_id):
            if f"{required_permission}:assigned" in user_permissions:
                return True
                
        return False
    
    def _check_employee_file_access(self, employee_id: str, required_permission: str, user_id: str) -> bool:
        """
        Check access to employee files
        
        Args:
            employee_id: Employee ID
            required_permission: Required permission
            user_id: User ID
            
        Returns:
            True if user has permission, False otherwise
        """
        # Get user permissions
        user_permissions = self._get_user_permissions(user_id)
        
        # Check if user has admin/all access
        if f"{required_permission}:all" in user_permissions:
            return True
            
        # Check if user is accessing their own file
        if employee_id == user_id:
            if f"{required_permission}:own" in user_permissions:
                return True
                
        # Check if user is leader of the employee's team
        if self._is_team_leader(employee_id, user_id):
            if f"{required_permission}:team" in user_permissions:
                return True
                
        return False
    
    def _check_opportunity_file_access(self, opportunity_id: str, required_permission: str, user_id: str) -> bool:
        """
        Check access to opportunity files
        
        Args:
            opportunity_id: Opportunity ID
            required_permission: Required permission
            user_id: User ID
            
        Returns:
            True if user has permission, False otherwise
        """
        # Get user permissions
        user_permissions = self._get_user_permissions(user_id)
        
        # Check if user has admin/all access
        if f"{required_permission}:all" in user_permissions:
            return True
            
        # Check if user created the opportunity
        if self._is_opportunity_creator(opportunity_id, user_id):
            if f"{required_permission}:own" in user_permissions:
                return True
                
        # Check if user is assigned to the opportunity
        if self._is_assigned_to_opportunity(opportunity_id, user_id):
            if f"{required_permission}:assigned" in user_permissions:
                return True
                
        return False
    
    def _check_generic_file_access(self, entity_type: str, entity_id: str, required_permission: str, user_id: str) -> bool:
        """
        Generic file access check for other entity types
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            required_permission: Required permission
            user_id: User ID
            
        Returns:
            True if user has permission, False otherwise
        """
        # Get user permissions
        user_permissions = self._get_user_permissions(user_id)
        
        # Check for different permission scopes
        for scope in ["all", "own", "team", "assigned"]:
            permission = f"{required_permission}:{scope}"
            if permission in user_permissions:
                # Additional checks based on scope
                if scope == "all":
                    return True
                elif scope == "own" and self._is_entity_owner(entity_type, entity_id, user_id):
                    return True
                elif scope == "team" and self._is_in_same_team(entity_type, entity_id, user_id):
                    return True
                elif scope == "assigned" and self._is_assigned_to_entity(entity_type, entity_id, user_id):
                    return True
                    
        return False
    
    def _get_user_permissions(self, user_id: str) -> Set[str]:
        """
        Get permissions for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Set of permission strings
        """
        try:
            # In a real implementation, this would query the database or auth system
            # For now, we'll use the current_user if user_id matches
            user = current_user.get_user()
            if user and user.id == user_id:
                return set(user.permissions)
                
            # Placeholder - in real implementation, would query user permissions from DB
            # This is a simplified implementation for demonstration
            return set()
        except Exception as e:
            logger.error(f"Error getting permissions for user {user_id}", exc=e)
            return set()
    
    def _is_contract_owner(self, contract_id: str, user_id: str) -> bool:
        """Check if user is the owner of a contract"""
        # Placeholder - in real implementation, would query contract from DB
        # This is a simplified implementation for demonstration
        return False
    
    def _is_assigned_to_contract(self, contract_id: str, user_id: str) -> bool:
        """Check if user is assigned to a contract"""
        # Placeholder - in real implementation, would query contract assignments from DB
        # This is a simplified implementation for demonstration
        return False
    
    def _is_team_leader(self, employee_id: str, user_id: str) -> bool:
        """Check if user is the leader of employee's team"""
        # Placeholder - in real implementation, would query team and leader info from DB
        # This is a simplified implementation for demonstration
        return False
    
    def _is_opportunity_creator(self, opportunity_id: str, user_id: str) -> bool:
        """Check if user created the opportunity"""
        # Placeholder - in real implementation, would query opportunity from DB
        # This is a simplified implementation for demonstration
        return False
    
    def _is_assigned_to_opportunity(self, opportunity_id: str, user_id: str) -> bool:
        """Check if user is assigned to an opportunity"""
        # Placeholder - in real implementation, would query opportunity assignments from DB
        # This is a simplified implementation for demonstration
        return False
    
    def _is_entity_owner(self, entity_type: str, entity_id: str, user_id: str) -> bool:
        """Generic check if user is the owner of an entity"""
        # Placeholder - in real implementation, would query entity from DB
        # This is a simplified implementation for demonstration
        return False
    
    def _is_in_same_team(self, entity_type: str, entity_id: str, user_id: str) -> bool:
        """Check if user is in the same team as the entity"""
        # Placeholder - in real implementation, would query team relations from DB
        # This is a simplified implementation for demonstration
        return False
    
    def _is_assigned_to_entity(self, entity_type: str, entity_id: str, user_id: str) -> bool:
        """Check if user is assigned to an entity"""
        # Placeholder - in real implementation, would query assignments from DB
        # This is a simplified implementation for demonstration
        return False


class FileSecurityUtils:
    """
    Utilities for file security, encryption, and secure handling
    """
    
    @staticmethod
    def generate_policy_document(entity_type: str, 
                               entity_id: str,
                               permissions: List[str],
                               user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a policy document for S3 bucket policy or similar
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            permissions: List of permission strings
            user_id: Optional user ID (if None, current authenticated user is used)
            
        Returns:
            Policy document as dictionary
        """
        # If no user ID provided, use current user
        if not user_id:
            try:
                user = current_user.get_user()
                user_id = user.id
            except Exception:
                user_id = "anonymous"
                
        # Create a policy document (e.g., for S3 bucket policies)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": f"arn:aws:iam::*:user/{user_id}"
                    },
                    "Action": [],
                    "Resource": [
                        f"arn:aws:s3:::${{BucketName}}/{entity_type}/{entity_id}/*"
                    ],
                    "Condition": {
                        "StringEquals": {
                            "s3:ExistingObjectTag/entity_type": entity_type,
                            "s3:ExistingObjectTag/entity_id": entity_id
                        }
                    }
                }
            ]
        }
        
        # Map permissions to S3 actions
        actions = []
        for permission in permissions:
            if permission == "read":
                actions.append("s3:GetObject")
            elif permission == "write":
                actions.append("s3:PutObject")
            elif permission == "delete":
                actions.append("s3:DeleteObject")
            elif permission == "list":
                actions.append("s3:ListBucket")
                
        policy["Statement"][0]["Action"] = actions
        
        return policy
    
    @staticmethod
    def validate_file_permissions(entity_type: str, 
                                entity_id: str, 
                                required_permission: str,
                                raise_exception: bool = True) -> bool:
        """
        Validate if current user has permission to access a file
        
        Args:
            entity_type: The type of entity the file is related to (e.g., contract, employee)
            entity_id: The ID of the entity
            required_permission: The permission required to access the file (e.g., 'contract:read')
            raise_exception: Whether to raise an exception on permission failure
            
        Returns:
            True if user has permission, False otherwise
            
        Raises:
            StoragePermissionError: If user doesn't have permission and raise_exception is True
        """
        # Create permission manager
        permission_manager = FilePermissionManager()
        
        # Check permissions
        has_permission = permission_manager.check_file_access(
            entity_type=entity_type,
            entity_id=entity_id,
            required_permission=required_permission
        )
        
        if not has_permission and raise_exception:
            raise StoragePermissionError(
                f"You don't have permission to {required_permission.split(':')[1]} "
                f"files for this {entity_type}"
            )
            
        return has_permission 