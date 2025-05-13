"""
Tests for S3 utilities.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from src.common.s3 import create_presigned_upload_url, create_presigned_get_url, check_object_exists

@patch('src.common.s3.boto3.client')
def test_create_presigned_upload_url(mock_boto_client):
    # Setup
    mock_s3_client = MagicMock()
    mock_boto_client.return_value = mock_s3_client
    
    expected_url = "https://presigned-url-for-upload.example"
    mock_s3_client.generate_presigned_url.return_value = expected_url
    
    # Execute
    bucket = "test-bucket"
    key = "test/file.pdf"
    content_type = "application/pdf"
    result = create_presigned_upload_url(bucket, key, content_type)
    
    # Verify
    assert result == expected_url
    mock_boto_client.assert_called_once_with('s3')
    mock_s3_client.generate_presigned_url.assert_called_once_with(
        'put_object',
        Params={
            'Bucket': bucket,
            'Key': key,
            'ContentType': content_type
        },
        ExpiresIn=3600
    )

@patch('src.common.s3.boto3.client')
def test_create_presigned_get_url(mock_boto_client):
    # Setup
    mock_s3_client = MagicMock()
    mock_boto_client.return_value = mock_s3_client
    
    expected_url = "https://presigned-url-for-download.example"
    mock_s3_client.generate_presigned_url.return_value = expected_url
    
    # Execute
    bucket = "test-bucket"
    key = "test/file.pdf"
    result = create_presigned_get_url(bucket, key)
    
    # Verify
    assert result == expected_url
    mock_boto_client.assert_called_once_with('s3')
    mock_s3_client.generate_presigned_url.assert_called_once_with(
        'get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        },
        ExpiresIn=3600
    )

@patch('src.common.s3.boto3.client')
def test_check_object_exists_when_exists(mock_boto_client):
    # Setup
    mock_s3_client = MagicMock()
    mock_boto_client.return_value = mock_s3_client
    
    # Execute
    bucket = "test-bucket"
    key = "test/file.pdf"
    result = check_object_exists(bucket, key)
    
    # Verify
    assert result is True
    mock_boto_client.assert_called_once_with('s3')
    mock_s3_client.head_object.assert_called_once_with(Bucket=bucket, Key=key)

@patch('src.common.s3.boto3.client')
def test_check_object_exists_when_not_exists(mock_boto_client):
    # Setup
    from botocore.exceptions import ClientError
    mock_s3_client = MagicMock()
    mock_boto_client.return_value = mock_s3_client
    
    # Configure mock to raise ClientError with 404 code
    error_response = {'Error': {'Code': '404'}}
    mock_s3_client.head_object.side_effect = ClientError(error_response, 'HeadObject')
    
    # Execute
    bucket = "test-bucket"
    key = "test/file.pdf"
    result = check_object_exists(bucket, key)
    
    # Verify
    assert result is False
    mock_boto_client.assert_called_once_with('s3')
    mock_s3_client.head_object.assert_called_once_with(Bucket=bucket, Key=key) 