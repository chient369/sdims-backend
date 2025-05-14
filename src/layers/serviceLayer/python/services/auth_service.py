import logging
import os
import jwt
from typing import Dict, Any, Optional
from datetime import datetime

from repositories.user_repository import UserRepository
from repositories.token_repository import TokenRepository
from repositories.role_repository import RoleRepository
from common.models.user import User
from common.models.role import Role
from common.utils.password_utils import verify_password
from common.utils.jwt_utils import create_token, create_refresh_token, DEFAULT_TOKEN_EXPIRY, verify_token, DEFAULT_REFRESH_TOKEN_EXPIRY
from common.errors import AuthenticationError, NotFoundException, DatabaseError, AccountLockedError

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AuthService:
    """
    Service for handling authentication operations.
    """
    
    def __init__(self, user_repository: Optional[UserRepository] = None, 
                token_repository: Optional[TokenRepository] = None,
                role_repository: Optional[RoleRepository] = None):
        """
        Initialize the auth service with dependencies.
        
        Args:
            user_repository: Repository for user operations
            token_repository: Repository for token operations
            role_repository: Repository for role operations
        """
        self.user_repository = user_repository or UserRepository()
        self.token_repository = token_repository or TokenRepository()
        self.role_repository = role_repository or RoleRepository()
        self.jwt_secret = os.environ.get("JWT_SECRET", "this_is_a_temporary_secret_key_replace_in_production")
    
    def login(self, username: str, password: str, remember_me: bool = False) -> Dict[str, Any]:
        """
        Authenticate a user and generate JWT tokens.
        
        Args:
            username: The username to authenticate
            password: The password to verify
            remember_me: Whether to extend token expiry time
            
        Returns:
            Dict: Authentication response with tokens and user info
            
        Raises:
            AuthenticationError: If authentication fails
            AccountLockedError: If account is locked
        """
        try:
            # Get user by username
            user_data = self.user_repository.get_by_username(username)
            
            # Check if user is active
            if not user_data.get("is_active", True):
                logger.warning(f"Login attempt for locked account: {username}")
                raise AccountLockedError("Tài khoản bị khóa")
            
            # Verify password
            stored_password_hash = user_data.get("password_hash")
            if not stored_password_hash or not verify_password(stored_password_hash, password):
                logger.warning(f"Failed login attempt for user: {username}")
                raise AuthenticationError("Sai tên đăng nhập hoặc mật khẩu")
            
            # Get user role and permissions
            role_data = self.user_repository.get_user_role(user_data["id"])
            permissions = role_data.get("permissions", [])
            
            # Create tokens
            token_expiry = DEFAULT_TOKEN_EXPIRY * 7 if remember_me else DEFAULT_TOKEN_EXPIRY
            access_token = create_token(
                user_id=user_data["id"],
                username=user_data["username"],
                permissions=permissions,
                secret_key=self.jwt_secret,
                expiry=token_expiry,
                additional_claims={
                    "email": user_data["email"],
                    "role": role_data["name"]
                }
            )
            
            refresh_token = create_refresh_token(
                user_id=user_data["id"],
                secret_key=self.jwt_secret
            )
            
            # Update last login timestamp
            self.user_repository.update_last_login(user_data["id"])
            
            # Create user model from data
            user = User.from_dict(user_data)
            role = Role.from_dict(role_data)
            
            # Return login response
            return {
                "token": access_token,
                "token_type": "Bearer",
                "expires_in": token_expiry,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": role.name,
                    "permissions": role.permissions
                }
            }
        except NotFoundException:
            logger.warning(f"Login attempt for non-existent user: {username}")
            raise AuthenticationError("Sai tên đăng nhập hoặc mật khẩu")
        except (AccountLockedError, AuthenticationError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login for user {username}: {str(e)}")
            raise AuthenticationError("Không thể xác thực người dùng") from e
            
    def logout(self, token: str) -> bool:
        """
        Invalidate a JWT token by adding it to a blacklist.
        
        Args:
            token: The JWT token to invalidate
            
        Returns:
            bool: True if the token was successfully invalidated
            
        Raises:
            AuthenticationError: If token is invalid
            DatabaseError: If a database error occurs
        """
        try:
            # Verify token is valid before blacklisting
            token_data = verify_token(token, self.jwt_secret)
            
            # Extract token ID and expiration
            jti = token_data.get("jti")
            exp = token_data.get("exp")
            user_id = token_data.get("sub")
            
            if not jti or not exp or not user_id:
                logger.warning("Attempted to logout with invalid token (missing claims)")
                raise AuthenticationError("Token không hợp lệ")
            
            # Add token to blacklist
            self.token_repository.add_to_blacklist(
                token_id=jti,
                user_id=user_id,
                expires_at=exp
            )
            
            logger.info(f"Successfully logged out user {user_id}")
            return True
        except jwt.InvalidTokenError:
            logger.warning("Attempted to logout with invalid token")
            raise AuthenticationError("Token không hợp lệ")
        except jwt.ExpiredSignatureError:
            # If token is already expired, no need to blacklist
            logger.info("Attempted to logout with expired token")
            return True
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            raise DatabaseError("Không thể đăng xuất") from e
            
    def get_current_user(self, token: str) -> Dict[str, Any]:
        """
        Get the current user information from a JWT token.
        
        Args:
            token: The JWT token
            
        Returns:
            Dict: User information with permissions
            
        Raises:
            AuthenticationError: If token is invalid or user is not found
            DatabaseError: If a database error occurs
        """
        try:
            # Verify token is valid
            token_data = verify_token(token, self.jwt_secret)
            
            # Check if token is blacklisted
            jti = token_data.get("jti")
            if jti and self.token_repository.is_token_blacklisted(jti):
                logger.warning(f"Attempt to use blacklisted token {jti}")
                raise AuthenticationError("Token đã hết hạn hoặc bị vô hiệu hóa")
            
            # Extract user ID from token
            user_id = token_data.get("sub")
            
            if not user_id:
                logger.warning("Token missing user ID")
                raise AuthenticationError("Token không hợp lệ")
            
            # Get user from database
            user_data = self.user_repository.get_by_id(user_id)
            
            # Check if user is active
            if not user_data.get("is_active", True):
                logger.warning(f"Attempt to use token for locked account: {user_id}")
                raise AccountLockedError("Tài khoản bị khóa")
            
            # Get user role and permissions
            role_data = self.role_repository.get_by_id(user_data.get("role_id"))
            
            # Create user model
            user = User.from_dict(user_data)
            role = Role.from_dict(role_data)
            
            # Return user information
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": role.name,
                "team_id": user_data.get("team_id"),
                "permissions": role.permissions
            }
        except jwt.ExpiredSignatureError:
            logger.warning("Attempt to use expired token")
            raise AuthenticationError("Token đã hết hạn")
        except jwt.InvalidTokenError:
            logger.warning("Attempt to use invalid token")
            raise AuthenticationError("Token không hợp lệ")
        except NotFoundException as e:
            logger.warning(f"User or role not found for token: {str(e)}")
            raise AuthenticationError("Không thể xác thực người dùng") from e
        except (AccountLockedError, AuthenticationError):
            raise
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting current user: {str(e)}")
            raise DatabaseError("Không thể lấy thông tin người dùng") from e
            
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an access token using a refresh token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            Dict: New access token and refresh token
            
        Raises:
            AuthenticationError: If refresh token is invalid
            DatabaseError: If a database error occurs
        """
        try:
            # Verify refresh token
            token_data = verify_token(refresh_token, self.jwt_secret)
            
            # Check if it's a refresh token
            if token_data.get("type") != "refresh":
                logger.warning("Attempted to use non-refresh token for refresh")
                raise AuthenticationError("Token không hợp lệ")
            
            # Check if token is blacklisted
            jti = token_data.get("jti")
            if jti and self.token_repository.is_token_blacklisted(jti):
                logger.warning(f"Attempt to use blacklisted refresh token {jti}")
                raise AuthenticationError("Refresh token đã hết hạn hoặc bị vô hiệu hóa")
            
            # Extract user ID
            user_id = token_data.get("sub")
            
            if not user_id:
                logger.warning("Refresh token missing user ID")
                raise AuthenticationError("Token không hợp lệ")
            
            # Get user from database
            user_data = self.user_repository.get_by_id(user_id)
            
            # Check if user is active
            if not user_data.get("is_active", True):
                logger.warning(f"Refresh token for locked account: {user_id}")
                raise AccountLockedError("Tài khoản bị khóa")
            
            # Get user role and permissions
            role_data = self.user_repository.get_user_role(user_id)
            permissions = role_data.get("permissions", [])
            
            # Blacklist the old refresh token
            self.token_repository.add_to_blacklist(
                token_id=jti,
                user_id=user_id,
                expires_at=token_data.get("exp", 0)
            )
            
            # Create new tokens
            new_access_token = create_token(
                user_id=user_id,
                username=user_data["username"],
                permissions=permissions,
                secret_key=self.jwt_secret,
                additional_claims={
                    "email": user_data["email"],
                    "role": role_data["name"]
                }
            )
            
            new_refresh_token = create_refresh_token(
                user_id=user_id,
                secret_key=self.jwt_secret
            )
            
            # Return token response
            return {
                "token": new_access_token,
                "token_type": "Bearer",
                "expires_in": DEFAULT_TOKEN_EXPIRY,
                "refresh_token": new_refresh_token
            }
        except jwt.ExpiredSignatureError:
            logger.warning("Attempted to use expired refresh token")
            raise AuthenticationError("Refresh token đã hết hạn")
        except jwt.InvalidTokenError:
            logger.warning("Attempted to use invalid refresh token")
            raise AuthenticationError("Refresh token không hợp lệ")
        except NotFoundException as e:
            logger.warning(f"User not found for refresh token: {str(e)}")
            raise AuthenticationError("Không thể xác thực người dùng") from e
        except (AccountLockedError, AuthenticationError):
            raise
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {str(e)}")
            raise DatabaseError("Không thể làm mới token") from e 