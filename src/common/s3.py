"""
S3 utilities for SDIMS backend.
"""
from typing import Any, Dict, List, Optional, BinaryIO, Union
import os
import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger

logger = Logger(service="s3-utils")

class S3Repository:
    """
    Repository class for S3 operations.
    Implements common operations for S3 buckets.
    """
    
    def __init__(self, bucket_name: str):
        """
        Initialize S3 repository.
        
        Args:
            bucket_name: Name of the S3 bucket
        """
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')
        logger.info(f"Initialized S3 repository for bucket: {bucket_name}")
    
    def upload_file(
        self, 
        file_path: str, 
        object_key: str, 
        metadata: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to S3.
        
        Args:
            file_path: Path to the file to upload
            object_key: S3 object key (path in bucket)
            metadata: Optional metadata for the object
            content_type: Content type of the file
            
        Returns:
            Response from S3
            
        Raises:
            FileNotFoundError: If file not found
            Exception: If S3 operation fails
        """
        try:
            extra_args = {}
            
            if metadata:
                extra_args['Metadata'] = metadata
                
            if content_type:
                extra_args['ContentType'] = content_type
                
            self.s3.upload_file(
                Filename=file_path,
                Bucket=self.bucket_name,
                Key=object_key,
                ExtraArgs=extra_args
            )
            
            logger.info(f"Successfully uploaded file to {self.bucket_name}/{object_key}")
            return {'bucket': self.bucket_name, 'key': object_key}
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            raise
    
    def upload_fileobj(
        self, 
        file_obj: BinaryIO, 
        object_key: str, 
        metadata: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file object to S3.
        
        Args:
            file_obj: File object to upload
            object_key: S3 object key (path in bucket)
            metadata: Optional metadata for the object
            content_type: Content type of the file
            
        Returns:
            Response from S3
            
        Raises:
            Exception: If S3 operation fails
        """
        try:
            extra_args = {}
            
            if metadata:
                extra_args['Metadata'] = metadata
                
            if content_type:
                extra_args['ContentType'] = content_type
                
            self.s3.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.bucket_name,
                Key=object_key,
                ExtraArgs=extra_args
            )
            
            logger.info(f"Successfully uploaded file object to {self.bucket_name}/{object_key}")
            return {'bucket': self.bucket_name, 'key': object_key}
        except Exception as e:
            logger.error(f"Error uploading file object to S3: {str(e)}")
            raise
    
    def download_file(self, object_key: str, file_path: str) -> None:
        """
        Download a file from S3.
        
        Args:
            object_key: S3 object key (path in bucket)
            file_path: Path to save the downloaded file
            
        Raises:
            Exception: If S3 operation fails
        """
        try:
            self.s3.download_file(
                Bucket=self.bucket_name,
                Key=object_key,
                Filename=file_path
            )
            
            logger.info(f"Successfully downloaded file from {self.bucket_name}/{object_key}")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.error(f"Object {object_key} not found in bucket {self.bucket_name}")
            else:
                logger.error(f"Error downloading file from S3: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error downloading file from S3: {str(e)}")
            raise
    
    def get_object(self, object_key: str) -> Dict[str, Any]:
        """
        Get an object from S3.
        
        Args:
            object_key: S3 object key (path in bucket)
            
        Returns:
            Response from S3 containing the object
            
        Raises:
            Exception: If S3 operation fails
        """
        try:
            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            
            logger.info(f"Successfully retrieved object from {self.bucket_name}/{object_key}")
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error(f"Object {object_key} not found in bucket {self.bucket_name}")
            else:
                logger.error(f"Error getting object from S3: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error getting object from S3: {str(e)}")
            raise
    
    def delete_object(self, object_key: str) -> Dict[str, Any]:
        """
        Delete an object from S3.
        
        Args:
            object_key: S3 object key (path in bucket)
            
        Returns:
            Response from S3
            
        Raises:
            Exception: If S3 operation fails
        """
        try:
            response = self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            
            logger.info(f"Successfully deleted object from {self.bucket_name}/{object_key}")
            return response
        except Exception as e:
            logger.error(f"Error deleting object from S3: {str(e)}")
            raise
    
    def create_presigned_url(
        self, 
        object_key: str, 
        expiration: int = 3600, 
        http_method: str = 'GET'
    ) -> str:
        """
        Create a presigned URL for an S3 object.
        
        Args:
            object_key: S3 object key (path in bucket)
            expiration: Expiration time in seconds
            http_method: HTTP method for the URL
            
        Returns:
            Presigned URL
            
        Raises:
            Exception: If S3 operation fails
        """
        try:
            url = self.s3.generate_presigned_url(
                ClientMethod=f'{http_method.lower()}_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key,
                },
                ExpiresIn=expiration
            )
            
            logger.info(f"Successfully created presigned URL for {self.bucket_name}/{object_key}")
            return url
        except Exception as e:
            logger.error(f"Error creating presigned URL: {str(e)}")
            raise

# Utility functions for presigned URLs
def create_presigned_upload_url(bucket: str, key: str, content_type: str, expires_in: int = 3600) -> str:
    """
    Create presigned URL for uploading a file to S3
    
    Args:
        bucket: Name of the bucket
        key: Object key (file path)
        content_type: MIME type of the file
        expires_in: Expiration time in seconds, default is 3600
        
    Returns:
        str: Presigned URL
        
    Raises:
        Exception: If there is an error creating the presigned URL
    """
    try:
        s3_client = boto3.client('s3')
        
        params = {
            'Bucket': bucket,
            'Key': key,
            'ContentType': content_type
        }
        
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params=params,
            ExpiresIn=expires_in
        )
        
        logger.info(f"Successfully created presigned upload URL for {bucket}/{key}")
        return presigned_url
    except Exception as e:
        logger.exception(f"Error creating presigned upload URL for {bucket}/{key}")
        raise

def create_presigned_get_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    """
    Create presigned URL for downloading a file from S3
    
    Args:
        bucket: Name of the bucket
        key: Object key (file path)
        expires_in: Expiration time in seconds, default is 3600
        
    Returns:
        str: Presigned URL
        
    Raises:
        Exception: If there is an error creating the presigned URL
    """
    try:
        s3_client = boto3.client('s3')
        
        params = {
            'Bucket': bucket,
            'Key': key
        }
        
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params=params,
            ExpiresIn=expires_in
        )
        
        logger.info(f"Successfully created presigned get URL for {bucket}/{key}")
        return presigned_url
    except Exception as e:
        logger.exception(f"Error creating presigned get URL for {bucket}/{key}")
        raise

def check_object_exists(bucket: str, key: str) -> bool:
    """
    Check if an object exists in the S3 bucket
    
    Args:
        bucket: Name of the bucket
        key: Object key (file path)
        
    Returns:
        bool: True if object exists, False otherwise
    """
    try:
        s3_client = boto3.client('s3')
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            logger.error(f"Error checking if object exists: {str(e)}")
            raise
    except Exception as e:
        logger.error(f"Error checking if object exists: {str(e)}")
        raise 