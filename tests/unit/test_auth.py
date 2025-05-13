"""
Unit tests for authentication module.
"""
import json
import unittest
from unittest.mock import patch, MagicMock

from src.auth import auth
from src.common.auth import AuthUtility


class TestAuth(unittest.TestCase):
    """Test cases for authentication module."""

    def setUp(self):
        """Set up test cases."""
        self.auth_util_mock = MagicMock()
        self.auth_util_mock.generate_token.return_value = {
            "token": "mock-token",
            "refresh_token": "mock-refresh-token",
            "expires_in": 3600
        }

    @patch('src.auth.auth.auth_util')
    def test_login_success(self, auth_util_mock):
        """Test successful login."""
        # Setup
        auth_util_mock.generate_token.return_value = {
            "token": "mock-token",
            "refresh_token": "mock-refresh-token",
            "expires_in": 3600
        }
        
        event = {
            "body": json.dumps({
                "username": "admin",
                "password": "password"
            })
        }
        
        # Execute
        response = auth.login_handler(event, {})
        
        # Assert
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["token"], "mock-token")
        self.assertEqual(body["refresh_token"], "mock-refresh-token")
        self.assertEqual(body["expires_in"], 3600)
        self.assertEqual(body["user"]["username"], "admin")
        self.assertEqual(body["user"]["role"], "admin")
        
        # Verify mock was called
        auth_util_mock.generate_token.assert_called_once()

    @patch('src.auth.auth.auth_util')
    def test_login_missing_credentials(self, auth_util_mock):
        """Test login with missing credentials."""
        # Setup
        event = {
            "body": json.dumps({
                "username": "admin"
                # Missing password
            })
        }
        
        # Execute
        response = auth.login_handler(event, {})
        
        # Assert
        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertEqual(body["error"]["code"], "VALIDATION_ERROR")
        
        # Verify mock was not called
        auth_util_mock.generate_token.assert_not_called()

    @patch('src.auth.auth.auth_util')
    def test_login_invalid_credentials(self, auth_util_mock):
        """Test login with invalid credentials."""
        # Setup
        event = {
            "body": json.dumps({
                "username": "invalid",
                "password": "invalid"
            })
        }
        
        # Execute
        response = auth.login_handler(event, {})
        
        # Assert
        self.assertEqual(response["statusCode"], 401)
        body = json.loads(response["body"])
        self.assertEqual(body["error"]["code"], "UNAUTHORIZED")
        
        # Verify mock was not called
        auth_util_mock.generate_token.assert_not_called()

    def test_logout(self):
        """Test logout."""
        # Setup
        event = {}
        
        # Execute
        response = auth.logout_handler(event, {})
        
        # Assert
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["message"], "Successfully logged out")


if __name__ == '__main__':
    unittest.main() 