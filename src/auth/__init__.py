"""
Authentication module for SDIMS backend.
This package contains lambda functions for authentication and authorization.
"""
from src.auth.auth import login_handler, me_handler
from src.auth.logout import handler as logout_handler
from src.auth.authorizer import handler as authorizer_handler
from src.auth.auth_handler import handler as combined_auth_handler

__version__ = "0.1.0" 