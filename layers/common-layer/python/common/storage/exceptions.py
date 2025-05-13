"""
Exceptions for storage module
"""

from common.errors import BaseError


class StorageError(BaseError):
    """Base exception for all storage related errors"""
    error_code = "STORAGE_ERROR"
    status_code = 500
    default_message = "An error occurred when accessing the storage system"


class StorageFileNotFoundError(StorageError):
    """Raised when a file is not found in storage"""
    error_code = "STORAGE_FILE_NOT_FOUND"
    status_code = 404
    default_message = "The requested file was not found in storage"


class StoragePermissionError(StorageError):
    """Raised when a user does not have permission to access a file"""
    error_code = "STORAGE_PERMISSION_DENIED"
    status_code = 403
    default_message = "You do not have permission to access this file"


class StorageFileTypeError(StorageError):
    """Raised when a file type is not supported or allowed"""
    error_code = "STORAGE_FILE_TYPE_ERROR"
    status_code = 400
    default_message = "The file type is not supported or allowed"


class StorageFileSizeError(StorageError):
    """Raised when a file exceeds the maximum allowed size"""
    error_code = "STORAGE_FILE_SIZE_ERROR"
    status_code = 400
    default_message = "The file size exceeds the maximum allowed size"


class StorageQuotaExceededError(StorageError):
    """Raised when storage quota is exceeded"""
    error_code = "STORAGE_QUOTA_EXCEEDED"
    status_code = 400
    default_message = "Storage quota exceeded"


class StorageUploadError(StorageError):
    """Raised when there is an error during file upload"""
    error_code = "STORAGE_UPLOAD_ERROR"
    status_code = 500
    default_message = "An error occurred while uploading the file"


class StorageDownloadError(StorageError):
    """Raised when there is an error during file download"""
    error_code = "STORAGE_DOWNLOAD_ERROR"
    status_code = 500
    default_message = "An error occurred while downloading the file"


class StorageDeleteError(StorageError):
    """Raised when there is an error during file deletion"""
    error_code = "STORAGE_DELETE_ERROR"
    status_code = 500
    default_message = "An error occurred while deleting the file"


class StorageConnectionError(StorageError):
    """Raised when there is an error connecting to storage service"""
    error_code = "STORAGE_CONNECTION_ERROR"
    status_code = 500
    default_message = "Could not connect to storage service" 