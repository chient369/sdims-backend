"""
S3 Storage Provider Implementation

This module implements the StorageProvider interface for AWS S3.
"""

import os
import json
import uuid
import boto3
from typing import Dict, Any, List, Optional, Union, BinaryIO, Tuple
from io import BytesIO
from botocore.exceptions import ClientError
from botocore.config import Config

from common.storage.provider import StorageProvider
from common.storage.exceptions import (
    StorageError,
    StorageFileNotFoundError,
    StoragePermissionError,
    StorageUploadError,
    StorageDownloadError,
    StorageDeleteError,
    StorageConnectionError
)
from common.storage.file_operations import FileOperations
from common.logger import Logger


logger = Logger(service="s3-storage-provider")


class S3StorageProvider(StorageProvider):
    """
    AWS S3 implementation of the StorageProvider interface
    """
    
    def __init__(self, 
                bucket_name: Optional[str] = None,
                region: Optional[str] = None,
                endpoint_url: Optional[str] = None,
                aws_access_key_id: Optional[str] = None,
                aws_secret_access_key: Optional[str] = None):
        """
        Initialize the S3StorageProvider
        
        Args:
            bucket_name: S3 bucket name (if None, will use S3_BUCKET_NAME environment variable)
            region: AWS region (if None, will use AWS_REGION environment variable)
            endpoint_url: Custom endpoint URL for S3 (for testing or non-AWS S3 compatible services)
            aws_access_key_id: AWS access key ID (if None, will use AWS_ACCESS_KEY_ID environment variable)
            aws_secret_access_key: AWS secret access key (if None, will use AWS_SECRET_ACCESS_KEY environment variable)
            
        Raises:
            ValueError: If bucket name is not provided and not in environment
            StorageConnectionError: If connection to S3 fails
        """
        # Get bucket name
        self.bucket_name = bucket_name or os.environ.get('S3_BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("Bucket name must be provided or set as S3_BUCKET_NAME environment variable")
            
        # Get region
        self.region = region or os.environ.get('AWS_REGION', 'us-east-1')
        
        # Configure S3 client
        try:
            config = Config(
                region_name=self.region,
                signature_version='s3v4',
                retries={
                    'max_attempts': 3,
                    'mode': 'standard'
                }
            )
            
            self.s3_client = boto3.client(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                config=config
            )
            
            self.s3_resource = boto3.resource(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                config=config
            )
            
            self.bucket = self.s3_resource.Bucket(self.bucket_name)
            
            # Verify connection by getting bucket location
            self.s3_client.get_bucket_location(Bucket=self.bucket_name)
            
            logger.debug(f"Successfully initialized S3StorageProvider for bucket {self.bucket_name}")
        except ClientError as e:
            logger.error(f"Failed to initialize S3StorageProvider: {str(e)}", exc=e)
            raise StorageConnectionError(f"Failed to connect to S3 bucket {self.bucket_name}: {str(e)}")
    
    def upload(self, 
               file_data: Union[bytes, BinaryIO], 
               key: str, 
               content_type: Optional[str] = None,
               metadata: Optional[Dict[str, str]] = None) -> str:
        """
        Upload file data to S3
        
        Args:
            file_data: The file data as bytes or file-like object
            key: The S3 key where the file will be stored
            content_type: The content type (MIME type) of the file
            metadata: Additional metadata to associate with the file
            
        Returns:
            The S3 key where the file was stored
            
        Raises:
            StorageUploadError: If upload fails
            StoragePermissionError: If permission is denied
        """
        try:
            # Prepare extra args
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
                
            if metadata:
                # S3 only accepts string values for metadata
                string_metadata = {k: str(v) for k, v in metadata.items()}
                extra_args['Metadata'] = string_metadata
                
            # Add server-side encryption
            extra_args['ServerSideEncryption'] = 'AES256'
            
            # Upload file
            if isinstance(file_data, bytes):
                # Upload from bytes
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=file_data,
                    **extra_args
                )
            else:
                # Upload from file-like object
                self.s3_client.upload_fileobj(
                    Fileobj=file_data,
                    Bucket=self.bucket_name,
                    Key=key,
                    ExtraArgs=extra_args
                )
                
            logger.info(f"Successfully uploaded file to s3://{self.bucket_name}/{key}")
            return key
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'AccessDenied':
                logger.error(f"Permission denied when uploading to s3://{self.bucket_name}/{key}", exc=e)
                raise StoragePermissionError(f"Permission denied when uploading file: {str(e)}")
            else:
                logger.error(f"Failed to upload file to s3://{self.bucket_name}/{key}", exc=e)
                raise StorageUploadError(f"Failed to upload file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when uploading to s3://{self.bucket_name}/{key}", exc=e)
            raise StorageUploadError(f"Failed to upload file: {str(e)}")
    
    def download(self, key: str) -> bytes:
        """
        Download file from S3
        
        Args:
            key: The S3 key of the file
            
        Returns:
            The file data as bytes
            
        Raises:
            StorageDownloadError: If download fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        try:
            # Check if file exists
            if not self.file_exists(key):
                raise StorageFileNotFoundError(f"File with key '{key}' not found in bucket {self.bucket_name}")
                
            # Download file
            buffer = BytesIO()
            self.s3_client.download_fileobj(
                Bucket=self.bucket_name,
                Key=key,
                Fileobj=buffer
            )
            
            # Reset buffer position and convert to bytes
            buffer.seek(0)
            data = buffer.read()
            
            logger.info(f"Successfully downloaded file from s3://{self.bucket_name}/{key}")
            return data
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'NoSuchKey':
                logger.error(f"File not found: s3://{self.bucket_name}/{key}", exc=e)
                raise StorageFileNotFoundError(f"File with key '{key}' not found in bucket {self.bucket_name}")
            elif error_code == 'AccessDenied':
                logger.error(f"Permission denied when downloading s3://{self.bucket_name}/{key}", exc=e)
                raise StoragePermissionError(f"Permission denied when downloading file: {str(e)}")
            else:
                logger.error(f"Failed to download file from s3://{self.bucket_name}/{key}", exc=e)
                raise StorageDownloadError(f"Failed to download file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when downloading s3://{self.bucket_name}/{key}", exc=e)
            raise StorageDownloadError(f"Failed to download file: {str(e)}")
    
    def delete(self, key: str) -> bool:
        """
        Delete file from S3
        
        Args:
            key: The S3 key of the file
            
        Returns:
            True if file was deleted, False otherwise
            
        Raises:
            StorageDeleteError: If deletion fails
            StoragePermissionError: If permission is denied
        """
        try:
            # Check if file exists first
            if not self.file_exists(key):
                logger.warn(f"Attempting to delete non-existent file: s3://{self.bucket_name}/{key}")
                return False
                
            # Delete file
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            logger.info(f"Successfully deleted file from s3://{self.bucket_name}/{key}")
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'AccessDenied':
                logger.error(f"Permission denied when deleting s3://{self.bucket_name}/{key}", exc=e)
                raise StoragePermissionError(f"Permission denied when deleting file: {str(e)}")
            else:
                logger.error(f"Failed to delete file from s3://{self.bucket_name}/{key}", exc=e)
                raise StorageDeleteError(f"Failed to delete file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when deleting s3://{self.bucket_name}/{key}", exc=e)
            raise StorageDeleteError(f"Failed to delete file: {str(e)}")
    
    def list(self, prefix: str = "", delimiter: str = "", max_keys: int = 1000) -> List[Dict[str, Any]]:
        """
        List files in S3
        
        Args:
            prefix: Prefix to filter files
            delimiter: Delimiter for hierarchical listing
            max_keys: Maximum number of keys to return
            
        Returns:
            List of file information dictionaries
            
        Raises:
            StorageError: If listing fails
            StoragePermissionError: If permission is denied
        """
        try:
            # Prepare parameters
            params = {
                'Bucket': self.bucket_name,
                'MaxKeys': max_keys
            }
            
            if prefix:
                params['Prefix'] = prefix
                
            if delimiter:
                params['Delimiter'] = delimiter
                
            # Get list of objects
            response = self.s3_client.list_objects_v2(**params)
            
            # Extract file information
            files = []
            
            # Process files
            for obj in response.get('Contents', []):
                # Get object metadata
                try:
                    head = self.s3_client.head_object(
                        Bucket=self.bucket_name,
                        Key=obj['Key']
                    )
                    
                    file_info = {
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat(),
                        'etag': obj['ETag'].strip('"'),
                        'content_type': head.get('ContentType', 'application/octet-stream'),
                        'metadata': head.get('Metadata', {})
                    }
                    
                    files.append(file_info)
                except ClientError:
                    # Skip files we can't access for some reason
                    continue
                    
            # Process prefixes (directories)
            for prefix_obj in response.get('CommonPrefixes', []):
                files.append({
                    'key': prefix_obj['Prefix'],
                    'is_prefix': True
                })
                
            logger.info(f"Listed {len(files)} files in s3://{self.bucket_name}/{prefix}")
            return files
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'AccessDenied':
                logger.error(f"Permission denied when listing s3://{self.bucket_name}/{prefix}", exc=e)
                raise StoragePermissionError(f"Permission denied when listing files: {str(e)}")
            else:
                logger.error(f"Failed to list files in s3://{self.bucket_name}/{prefix}", exc=e)
                raise StorageError(f"Failed to list files: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when listing s3://{self.bucket_name}/{prefix}", exc=e)
            raise StorageError(f"Failed to list files: {str(e)}")
    
    def get_metadata(self, key: str) -> Dict[str, Any]:
        """
        Get metadata for a file in S3
        
        Args:
            key: The S3 key of the file
            
        Returns:
            Dictionary of metadata
            
        Raises:
            StorageError: If operation fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        try:
            # Get object metadata
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            # Extract metadata
            metadata = {
                'key': key,
                'size': response.get('ContentLength', 0),
                'last_modified': response.get('LastModified').isoformat() if response.get('LastModified') else None,
                'content_type': response.get('ContentType', 'application/octet-stream'),
                'etag': response.get('ETag', '').strip('"'),
                'custom_metadata': response.get('Metadata', {})
            }
            
            logger.info(f"Got metadata for s3://{self.bucket_name}/{key}")
            return metadata
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'NoSuchKey' or error_code == '404':
                logger.error(f"File not found: s3://{self.bucket_name}/{key}", exc=e)
                raise StorageFileNotFoundError(f"File with key '{key}' not found in bucket {self.bucket_name}")
            elif error_code == 'AccessDenied':
                logger.error(f"Permission denied when getting metadata for s3://{self.bucket_name}/{key}", exc=e)
                raise StoragePermissionError(f"Permission denied when getting file metadata: {str(e)}")
            else:
                logger.error(f"Failed to get metadata for s3://{self.bucket_name}/{key}", exc=e)
                raise StorageError(f"Failed to get file metadata: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when getting metadata for s3://{self.bucket_name}/{key}", exc=e)
            raise StorageError(f"Failed to get file metadata: {str(e)}")
    
    def update_metadata(self, key: str, metadata: Dict[str, str]) -> Dict[str, Any]:
        """
        Update metadata for a file in S3
        
        Args:
            key: The S3 key of the file
            metadata: Metadata to update
            
        Returns:
            Updated metadata dictionary
            
        Raises:
            StorageError: If operation fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        try:
            # Check if file exists
            if not self.file_exists(key):
                raise StorageFileNotFoundError(f"File with key '{key}' not found in bucket {self.bucket_name}")
                
            # Get current object metadata to preserve non-metadata attributes
            current = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            # Prepare copy source
            copy_source = {
                'Bucket': self.bucket_name,
                'Key': key
            }
            
            # Prepare metadata directive (replace all metadata)
            metadata_directive = 'REPLACE'
            
            # Convert metadata values to strings
            string_metadata = {k: str(v) for k, v in metadata.items()}
            
            # Copy object to itself with new metadata
            response = self.s3_client.copy_object(
                Bucket=self.bucket_name,
                Key=key,
                CopySource=copy_source,
                MetadataDirective=metadata_directive,
                Metadata=string_metadata,
                ContentType=current.get('ContentType', 'application/octet-stream'),
                ServerSideEncryption=current.get('ServerSideEncryption', 'AES256')
            )
            
            # Get updated metadata
            updated = self.get_metadata(key)
            
            logger.info(f"Updated metadata for s3://{self.bucket_name}/{key}")
            return updated
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'NoSuchKey':
                logger.error(f"File not found: s3://{self.bucket_name}/{key}", exc=e)
                raise StorageFileNotFoundError(f"File with key '{key}' not found in bucket {self.bucket_name}")
            elif error_code == 'AccessDenied':
                logger.error(f"Permission denied when updating metadata for s3://{self.bucket_name}/{key}", exc=e)
                raise StoragePermissionError(f"Permission denied when updating file metadata: {str(e)}")
            else:
                logger.error(f"Failed to update metadata for s3://{self.bucket_name}/{key}", exc=e)
                raise StorageError(f"Failed to update file metadata: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when updating metadata for s3://{self.bucket_name}/{key}", exc=e)
            raise StorageError(f"Failed to update file metadata: {str(e)}")
    
    def get_presigned_url(self, 
                        key: str, 
                        expires_in: int = 3600, 
                        response_content_type: Optional[str] = None,
                        response_content_disposition: Optional[str] = None) -> str:
        """
        Generate a pre-signed URL for direct access to a file in S3
        
        Args:
            key: The S3 key of the file
            expires_in: Expiration time in seconds
            response_content_type: Override content type in response
            response_content_disposition: Override content disposition in response
            
        Returns:
            Pre-signed URL for direct access
            
        Raises:
            StorageError: If generation fails
            StorageFileNotFoundError: If file is not found
            StoragePermissionError: If permission is denied
        """
        try:
            # Check if file exists
            if not self.file_exists(key):
                raise StorageFileNotFoundError(f"File with key '{key}' not found in bucket {self.bucket_name}")
                
            # Prepare parameters
            params = {
                'Bucket': self.bucket_name,
                'Key': key
            }
            
            # Add optional parameters
            if response_content_type:
                params['ResponseContentType'] = response_content_type
                
            if response_content_disposition:
                params['ResponseContentDisposition'] = response_content_disposition
                
            # Generate URL
            url = self.s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params=params,
                ExpiresIn=expires_in
            )
            
            logger.info(f"Generated presigned URL for s3://{self.bucket_name}/{key}, expires in {expires_in}s")
            return url
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '') if hasattr(e, 'response') else ''
            logger.error(f"Failed to generate presigned URL for s3://{self.bucket_name}/{key}", exc=e)
            raise StorageError(f"Failed to generate presigned URL: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when generating presigned URL for s3://{self.bucket_name}/{key}", exc=e)
            raise StorageError(f"Failed to generate presigned URL: {str(e)}")
    
    def get_upload_url(self, 
                      key: str, 
                      expires_in: int = 3600,
                      content_type: Optional[str] = None,
                      metadata: Optional[Dict[str, str]] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a pre-signed URL for direct upload to S3
        
        Args:
            key: The S3 key where the file will be stored
            expires_in: Expiration time in seconds
            content_type: Content type of the file to be uploaded
            metadata: Additional metadata for the file
            
        Returns:
            Tuple of (pre-signed URL, additional fields required for upload)
            
        Raises:
            StorageError: If generation fails
            StoragePermissionError: If permission is denied
        """
        try:
            # Prepare fields
            fields = {}
            
            # Add metadata if provided
            if metadata:
                for meta_key, meta_value in metadata.items():
                    fields[f'x-amz-meta-{meta_key}'] = str(meta_value)
                    
            # Add server-side encryption
            fields['x-amz-server-side-encryption'] = 'AES256'
            
            # Add content type if provided
            conditions = []
            if content_type:
                fields['Content-Type'] = content_type
                conditions.append(['eq', '$Content-Type', content_type])
                
            # Generate post presigned URL
            post = self.s3_client.generate_presigned_post(
                Bucket=self.bucket_name,
                Key=key,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expires_in
            )
            
            logger.info(f"Generated presigned POST URL for s3://{self.bucket_name}/{key}, expires in {expires_in}s")
            return post['url'], post['fields']
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '') if hasattr(e, 'response') else ''
            if error_code == 'AccessDenied':
                logger.error(f"Permission denied when generating upload URL for s3://{self.bucket_name}/{key}", exc=e)
                raise StoragePermissionError(f"Permission denied when generating upload URL: {str(e)}")
            else:
                logger.error(f"Failed to generate upload URL for s3://{self.bucket_name}/{key}", exc=e)
                raise StorageError(f"Failed to generate upload URL: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when generating upload URL for s3://{self.bucket_name}/{key}", exc=e)
            raise StorageError(f"Failed to generate upload URL: {str(e)}")
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename to be safe for S3
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        return FileOperations.sanitize_filename(filename)
    
    def file_exists(self, key: str) -> bool:
        """
        Check if a file exists in S3
        
        Args:
            key: The S3 key of the file
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True
        except ClientError as e:
            # If error code is 404, file doesn't exist
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == '404' or error_code == 'NoSuchKey':
                return False
            # For other errors, propagate exception
            raise
    
    def copy(self, source_key: str, destination_key: str, metadata: Optional[Dict[str, str]] = None) -> str:
        """
        Copy a file within S3
        
        Args:
            source_key: Source S3 key
            destination_key: Destination S3 key
            metadata: Optional new metadata to apply
            
        Returns:
            The destination key
            
        Raises:
            StorageError: If copy fails
            StorageFileNotFoundError: If source file is not found
            StoragePermissionError: If permission is denied
        """
        try:
            # Check if source file exists
            if not self.file_exists(source_key):
                raise StorageFileNotFoundError(f"Source file with key '{source_key}' not found in bucket {self.bucket_name}")
                
            # Prepare copy source
            copy_source = {
                'Bucket': self.bucket_name,
                'Key': source_key
            }
            
            # Prepare parameters
            params = {
                'Bucket': self.bucket_name,
                'Key': destination_key,
                'CopySource': copy_source,
                'ServerSideEncryption': 'AES256'
            }
            
            # Add metadata if provided
            if metadata:
                params['MetadataDirective'] = 'REPLACE'
                params['Metadata'] = {k: str(v) for k, v in metadata.items()}
            
            # Copy object
            self.s3_client.copy_object(**params)
            
            logger.info(f"Copied file from s3://{self.bucket_name}/{source_key} to s3://{self.bucket_name}/{destination_key}")
            return destination_key
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'NoSuchKey':
                logger.error(f"Source file not found: s3://{self.bucket_name}/{source_key}", exc=e)
                raise StorageFileNotFoundError(f"Source file with key '{source_key}' not found in bucket {self.bucket_name}")
            elif error_code == 'AccessDenied':
                logger.error(f"Permission denied when copying s3://{self.bucket_name}/{source_key}", exc=e)
                raise StoragePermissionError(f"Permission denied when copying file: {str(e)}")
            else:
                logger.error(f"Failed to copy file from s3://{self.bucket_name}/{source_key} to {destination_key}", exc=e)
                raise StorageError(f"Failed to copy file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error when copying s3://{self.bucket_name}/{source_key}", exc=e)
            raise StorageError(f"Failed to copy file: {str(e)}") 