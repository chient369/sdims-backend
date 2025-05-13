"""
S3 Utilities for SDIMS

This module provides utilities for working with Amazon S3.
"""

import os
import boto3
import json
import uuid
from typing import Dict, Any, List, Optional, Union, BinaryIO
from botocore.exceptions import ClientError

from common.logger import Logger

logger = Logger(service="s3-utils")

class S3Utils:
    """
    Utilities for working with Amazon S3
    """
    
    def __init__(self, bucket_name: Optional[str] = None):
        """
        Initialize S3 utilities
        
        Args:
            bucket_name: Optional bucket name, can also be set via environment variable
        """
        self.bucket_name = bucket_name or os.environ.get('S3_BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("Bucket name must be provided or set as S3_BUCKET_NAME environment variable")
            
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.bucket = self.s3_resource.Bucket(self.bucket_name)
        
        logger.debug(f"Initialized S3Utils for bucket {self.bucket_name}")
        
    def generate_presigned_url(self, 
                             key: str, 
                             expiration: int = 3600,
                             http_method: str = 'GET',
                             content_type: Optional[str] = None) -> str:
        """
        Generate a presigned URL for S3 object
        
        Args:
            key: S3 object key
            expiration: URL expiration time in seconds
            http_method: HTTP method (GET, PUT, etc.)
            content_type: Content type for PUT requests
                
        Returns:
            Presigned URL
            
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            params = {
                'Bucket': self.bucket_name,
                'Key': key
            }
            
            # For upload URLs, add content-type if provided
            if http_method == 'PUT' and content_type:
                params['ContentType'] = content_type
                
            url = self.s3_client.generate_presigned_url(
                ClientMethod=f'{http_method.lower()}_object',
                Params=params,
                ExpiresIn=expiration
            )
            
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL for {key}", exc=e)
            raise
            
    def upload_file(self, 
                  file_path: str, 
                  key: Optional[str] = None, 
                  content_type: Optional[str] = None,
                  metadata: Optional[Dict[str, str]] = None) -> str:
        """
        Upload a file to S3
        
        Args:
            file_path: Path to the file to upload
            key: S3 object key (if None, will use filename from file_path)
            content_type: Content type of the file
            metadata: Additional metadata for the object
                
        Returns:
            S3 object key
            
        Raises:
            ClientError: If there is an error with the S3 client
            FileNotFoundError: If the file is not found
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            if key is None:
                key = os.path.basename(file_path)
                
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
                
            if metadata:
                extra_args['Metadata'] = metadata
                
            self.bucket.upload_file(file_path, key, ExtraArgs=extra_args)
            logger.info(f"Uploaded file to s3://{self.bucket_name}/{key}")
            
            return key
        except (ClientError, FileNotFoundError) as e:
            logger.error(f"Error uploading file {file_path} to {key}", exc=e)
            raise
            
    def upload_fileobj(self, 
                     fileobj: BinaryIO, 
                     key: str, 
                     content_type: Optional[str] = None,
                     metadata: Optional[Dict[str, str]] = None) -> str:
        """
        Upload a file-like object to S3
        
        Args:
            fileobj: File-like object to upload
            key: S3 object key
            content_type: Content type of the file
            metadata: Additional metadata for the object
                
        Returns:
            S3 object key
            
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
                
            if metadata:
                extra_args['Metadata'] = metadata
                
            self.bucket.upload_fileobj(fileobj, key, ExtraArgs=extra_args)
            logger.info(f"Uploaded fileobj to s3://{self.bucket_name}/{key}")
            
            return key
        except ClientError as e:
            logger.error(f"Error uploading fileobj to {key}", exc=e)
            raise
            
    def download_file(self, key: str, destination_path: str) -> None:
        """
        Download a file from S3
        
        Args:
            key: S3 object key
            destination_path: Local path to save the file
                
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            self.bucket.download_file(key, destination_path)
            logger.info(f"Downloaded s3://{self.bucket_name}/{key} to {destination_path}")
        except ClientError as e:
            logger.error(f"Error downloading file {key} to {destination_path}", exc=e)
            raise
            
    def get_object(self, key: str) -> Dict[str, Any]:
        """
        Get S3 object
        
        Args:
            key: S3 object key
                
        Returns:
            S3 object data and metadata
            
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response
        except ClientError as e:
            logger.error(f"Error getting object {key}", exc=e)
            raise
            
    def get_object_metadata(self, key: str) -> Dict[str, Any]:
        """
        Get S3 object metadata
        
        Args:
            key: S3 object key
                
        Returns:
            S3 object metadata
            
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return response
        except ClientError as e:
            logger.error(f"Error getting object metadata for {key}", exc=e)
            raise
            
    def delete_object(self, key: str) -> None:
        """
        Delete S3 object
        
        Args:
            key: S3 object key
                
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            self.bucket.delete_objects(
                Delete={
                    'Objects': [
                        {
                            'Key': key
                        }
                    ]
                }
            )
            logger.info(f"Deleted s3://{self.bucket_name}/{key}")
        except ClientError as e:
            logger.error(f"Error deleting object {key}", exc=e)
            raise
            
    def delete_objects(self, keys: List[str]) -> None:
        """
        Delete multiple S3 objects
        
        Args:
            keys: List of S3 object keys
                
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            if not keys:
                return
                
            # S3 delete_objects has a limit of 1000 keys per request
            chunk_size = 1000
            for i in range(0, len(keys), chunk_size):
                chunk = keys[i:i + chunk_size]
                
                objects = [{'Key': key} for key in chunk]
                
                self.bucket.delete_objects(
                    Delete={
                        'Objects': objects
                    }
                )
                
            logger.info(f"Deleted {len(keys)} objects from s3://{self.bucket_name}/")
        except ClientError as e:
            logger.error(f"Error deleting objects", exc=e)
            raise
            
    def list_objects(self, prefix: str = '', delimiter: str = '', max_keys: int = 1000) -> Dict[str, Any]:
        """
        List objects in the S3 bucket
        
        Args:
            prefix: Filter by prefix
            delimiter: Delimiter for hierarchy
            max_keys: Maximum number of keys to return
                
        Returns:
            S3 list objects response
            
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            params = {
                'Bucket': self.bucket_name,
                'Prefix': prefix,
                'MaxKeys': max_keys
            }
            
            if delimiter:
                params['Delimiter'] = delimiter
                
            response = self.s3_client.list_objects_v2(**params)
            return response
        except ClientError as e:
            logger.error(f"Error listing objects with prefix {prefix}", exc=e)
            raise
            
    def object_exists(self, key: str) -> bool:
        """
        Check if an object exists in the S3 bucket
        
        Args:
            key: S3 object key
                
        Returns:
            True if object exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the object does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                return False
            else:
                logger.error(f"Error checking if object {key} exists", exc=e)
                raise
                
    def generate_unique_key(self, prefix: str = '', extension: Optional[str] = None) -> str:
        """
        Generate a unique S3 object key
        
        Args:
            prefix: Key prefix
            extension: File extension
                
        Returns:
            Unique S3 object key
        """
        unique_id = str(uuid.uuid4())
        if prefix:
            prefix = prefix.rstrip('/') + '/'
            
        key = f"{prefix}{unique_id}"
        
        if extension:
            if not extension.startswith('.'):
                extension = f".{extension}"
            key = f"{key}{extension}"
            
        return key
    
    def copy_object(self, source_key: str, destination_key: str, 
                  source_bucket: Optional[str] = None,
                  metadata: Optional[Dict[str, str]] = None,
                  metadata_directive: str = 'COPY') -> None:
        """
        Copy an object within S3
        
        Args:
            source_key: Source S3 object key
            destination_key: Destination S3 object key
            source_bucket: Source bucket name (if different from current bucket)
            metadata: New metadata to apply
            metadata_directive: COPY (preserve metadata) or REPLACE (replace with new metadata)
                
        Raises:
            ClientError: If there is an error with the S3 client
        """
        try:
            source_bucket = source_bucket or self.bucket_name
            copy_source = {
                'Bucket': source_bucket,
                'Key': source_key
            }
            
            copy_params = {
                'CopySource': copy_source,
                'MetadataDirective': metadata_directive
            }
            
            if metadata and metadata_directive == 'REPLACE':
                copy_params['Metadata'] = metadata
                
            self.s3_client.copy_object(
                Bucket=self.bucket_name,
                Key=destination_key,
                **copy_params
            )
            
            logger.info(f"Copied s3://{source_bucket}/{source_key} to s3://{self.bucket_name}/{destination_key}")
        except ClientError as e:
            logger.error(f"Error copying object from {source_key} to {destination_key}", exc=e)
            raise 