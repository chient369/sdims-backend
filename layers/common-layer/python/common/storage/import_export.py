"""
Import/Export Utilities

This module provides utilities for importing and exporting data from files.
"""

import csv
import json
import tempfile
import os
from typing import Dict, List, Any, Optional, Union, Callable, BinaryIO, Tuple
from io import BytesIO, StringIO

import pandas as pd
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

from common.logger import Logger
from common.storage.exceptions import StorageError


logger = Logger(service="file-import-export")


class ValidationResult:
    """Class for storing validation results"""
    
    def __init__(self, is_valid: bool = True, errors: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize validation result
        
        Args:
            is_valid: Whether the data is valid
            errors: List of error dictionaries
        """
        self.is_valid = is_valid
        self.errors = errors or []
        self.valid_items = []
        self.invalid_items = []
        
    @property
    def valid_count(self) -> int:
        """Get count of valid items"""
        return len(self.valid_items)
        
    @property
    def invalid_count(self) -> int:
        """Get count of invalid items"""
        return len(self.invalid_items)
        
    def add_error(self, row: Optional[int] = None, field: Optional[str] = None, message: str = ""):
        """
        Add an error to the validation result
        
        Args:
            row: Row number (optional)
            field: Field name (optional)
            message: Error message
        """
        self.is_valid = False
        error = {"message": message}
        if row is not None:
            error["row"] = row
        if field:
            error["field"] = field
            
        self.errors.append(error)
        
    def add_item_result(self, item: Dict[str, Any], is_valid: bool, row: Optional[int] = None):
        """
        Add an item validation result
        
        Args:
            item: The data item
            is_valid: Whether the item is valid
            row: Row number (optional)
        """
        if row is not None:
            item["_row_number"] = row
            
        if is_valid:
            self.valid_items.append(item)
        else:
            self.invalid_items.append(item)
            
        # If at least one item is invalid, the whole result is invalid
        if not is_valid:
            self.is_valid = False


class DataValidator:
    """Base class for data validators"""
    
    def __init__(self):
        """Initialize the data validator"""
        pass
        
    def validate(self, data: Dict[str, Any], row: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate a single data item
        
        Args:
            data: The data item to validate
            row: Row number for error reporting
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Base implementation just returns valid
        return True, None
        
    def validate_bulk(self, data_list: List[Dict[str, Any]]) -> ValidationResult:
        """
        Validate a list of data items
        
        Args:
            data_list: List of data items to validate
            
        Returns:
            ValidationResult object
        """
        result = ValidationResult()
        
        for i, item in enumerate(data_list):
            # Add row number if not present
            row = item.get("_row_number", i + 1)
            
            # Validate item
            is_valid, error_message = self.validate(item, row)
            
            # Add result
            result.add_item_result(item, is_valid, row)
            
            # Add error if invalid
            if not is_valid and error_message:
                result.add_error(row=row, message=error_message)
                
        return result


class EmployeeDataValidator(DataValidator):
    """Validator for employee data"""
    
    def validate(self, data: Dict[str, Any], row: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate employee data
        
        Args:
            data: Employee data
            row: Row number for error reporting
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        # Required fields
        required_fields = ["first_name", "last_name", "employee_code", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing required field: {field}")
                
        # Email format
        if "email" in data and data["email"]:
            email = data["email"]
            if "@" not in email or "." not in email:
                errors.append("Invalid email format")
                
        # Check if employee code is unique (this would need database access in real implementation)
        if "employee_code" in data and data["employee_code"]:
            # Placeholder for checking uniqueness
            pass
            
        # Return validation result
        is_valid = len(errors) == 0
        error_message = "; ".join(errors) if errors else None
        
        return is_valid, error_message


class FileParser:
    """Base class for file parsers"""
    
    def __init__(self, file_data: Union[bytes, BinaryIO, str] = None, url: str = None):
        """
        Initialize the file parser
        
        Args:
            file_data: File data as bytes, file-like object, or file path
            url: URL to download file from
            
        Raises:
            ValueError: If neither file_data nor url is provided
        """
        if not file_data and not url:
            raise ValueError("Either file_data or url must be provided")
            
        self.file_data = file_data
        self.url = url
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse the file
        
        Returns:
            Parsed data
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("parse() method must be implemented by subclass")


class CSVParser(FileParser):
    """Parser for CSV files"""
    
    def __init__(self, file_data: Union[bytes, BinaryIO, str] = None, url: str = None, 
                encoding: str = 'utf-8', delimiter: str = ','):
        """
        Initialize the CSV parser
        
        Args:
            file_data: CSV file data as bytes, file-like object, or file path
            url: URL to download CSV from
            encoding: Character encoding
            delimiter: CSV delimiter
        """
        super().__init__(file_data, url)
        self.encoding = encoding
        self.delimiter = delimiter
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse the CSV file
        
        Returns:
            Dictionary with 'data' key containing list of row dictionaries
            
        Raises:
            StorageError: If parsing fails
        """
        try:
            # Get file data
            if self.url:
                import requests
                response = requests.get(self.url)
                content = response.content
            elif isinstance(self.file_data, str) and os.path.isfile(self.file_data):
                with open(self.file_data, 'rb') as f:
                    content = f.read()
            elif isinstance(self.file_data, bytes):
                content = self.file_data
            elif hasattr(self.file_data, 'read'):
                content = self.file_data.read()
                if hasattr(self.file_data, 'seek'):
                    self.file_data.seek(0)
            else:
                raise ValueError("Unable to read file data")
                
            # Convert to string
            if isinstance(content, bytes):
                content_str = content.decode(self.encoding)
            else:
                content_str = content
                
            # Parse CSV
            csv_reader = csv.DictReader(StringIO(content_str), delimiter=self.delimiter)
            rows = list(csv_reader)
            
            # Add row numbers
            for i, row in enumerate(rows):
                row['_row_number'] = i + 2  # +2 because row 1 is headers
                
            return {'data': rows}
        except Exception as e:
            logger.error("CSV parsing failed", exc=e)
            raise StorageError(f"Failed to parse CSV file: {str(e)}")


class ExcelParser(FileParser):
    """Parser for Excel files"""
    
    def __init__(self, file_data: Union[bytes, BinaryIO, str] = None, url: str = None):
        """
        Initialize the Excel parser
        
        Args:
            file_data: Excel file data as bytes, file-like object, or file path
            url: URL to download Excel from
        """
        super().__init__(file_data, url)
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse all sheets in the Excel file
        
        Returns:
            Dictionary with sheet names as keys and sheet data as values
            
        Raises:
            StorageError: If parsing fails
        """
        try:
            # Create temporary file if needed
            if self.url:
                import requests
                response = requests.get(self.url)
                temp_file = BytesIO(response.content)
            elif isinstance(self.file_data, str) and os.path.isfile(self.file_data):
                temp_file = self.file_data
            elif isinstance(self.file_data, bytes):
                temp_file = BytesIO(self.file_data)
            elif hasattr(self.file_data, 'read'):
                # Create a copy of the file-like object
                if hasattr(self.file_data, 'seek'):
                    self.file_data.seek(0)
                temp_file = BytesIO(self.file_data.read())
                if hasattr(self.file_data, 'seek'):
                    self.file_data.seek(0)
            else:
                raise ValueError("Unable to read file data")
                
            # Read Excel file with pandas
            excel_data = {}
            xls = pd.ExcelFile(temp_file)
            
            for sheet_name in xls.sheet_names:
                # Read sheet
                df = pd.read_excel(xls, sheet_name)
                
                # Convert to list of dictionaries
                records = df.to_dict('records')
                
                # Add row numbers
                for i, record in enumerate(records):
                    record['_row_number'] = i + 2  # +2 because row 1 is headers
                    
                excel_data[sheet_name] = records
                
            return excel_data
        except Exception as e:
            logger.error("Excel parsing failed", exc=e)
            raise StorageError(f"Failed to parse Excel file: {str(e)}")
            
    def parse_sheet(self, sheet_name: str) -> List[Dict[str, Any]]:
        """
        Parse a specific sheet in the Excel file
        
        Args:
            sheet_name: Name of the sheet to parse
            
        Returns:
            List of row dictionaries for the sheet
            
        Raises:
            StorageError: If parsing fails
            KeyError: If sheet does not exist
        """
        excel_data = self.parse()
        
        if sheet_name not in excel_data:
            raise KeyError(f"Sheet '{sheet_name}' not found in Excel file")
            
        return excel_data[sheet_name]


class JSONParser(FileParser):
    """Parser for JSON files"""
    
    def __init__(self, file_data: Union[bytes, BinaryIO, str] = None, url: str = None):
        """
        Initialize the JSON parser
        
        Args:
            file_data: JSON file data as bytes, file-like object, or file path
            url: URL to download JSON from
        """
        super().__init__(file_data, url)
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse the JSON file
        
        Returns:
            Parsed JSON data
            
        Raises:
            StorageError: If parsing fails
        """
        try:
            # Get file data
            if self.url:
                import requests
                response = requests.get(self.url)
                content = response.content
            elif isinstance(self.file_data, str) and os.path.isfile(self.file_data):
                with open(self.file_data, 'rb') as f:
                    content = f.read()
            elif isinstance(self.file_data, bytes):
                content = self.file_data
            elif hasattr(self.file_data, 'read'):
                content = self.file_data.read()
                if hasattr(self.file_data, 'seek'):
                    self.file_data.seek(0)
            else:
                raise ValueError("Unable to read file data")
                
            # Parse JSON
            if isinstance(content, bytes):
                json_data = json.loads(content.decode('utf-8'))
            else:
                json_data = json.loads(content)
                
            return json_data
        except Exception as e:
            logger.error("JSON parsing failed", exc=e)
            raise StorageError(f"Failed to parse JSON file: {str(e)}")


class DataExporter:
    """Base class for data exporters"""
    
    def export(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> bytes:
        """
        Export data to file format
        
        Args:
            data: Data to export
            
        Returns:
            Exported file as bytes
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("export() method must be implemented by subclass")


class CSVExporter(DataExporter):
    """Exporter for CSV files"""
    
    def __init__(self, encoding: str = 'utf-8', delimiter: str = ','):
        """
        Initialize the CSV exporter
        
        Args:
            encoding: Character encoding
            delimiter: CSV delimiter
        """
        self.encoding = encoding
        self.delimiter = delimiter
        
    def export(self, data: List[Dict[str, Any]]) -> bytes:
        """
        Export data to CSV
        
        Args:
            data: List of dictionaries to export
            
        Returns:
            CSV file as bytes
            
        Raises:
            StorageError: If export fails
            ValueError: If data is not a list of dictionaries
        """
        try:
            if not isinstance(data, list):
                raise ValueError("Data must be a list of dictionaries")
                
            # Create CSV output
            output = StringIO()
            
            # Get field names from the first row
            fieldnames = list(data[0].keys()) if data else []
            
            # Remove internal fields
            if "_row_number" in fieldnames:
                fieldnames.remove("_row_number")
                
            # Create CSV writer
            writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=self.delimiter)
            
            # Write header
            writer.writeheader()
            
            # Write rows
            for item in data:
                # Create a copy without internal fields
                row = {k: v for k, v in item.items() if k != "_row_number"}
                writer.writerow(row)
                
            # Get CSV as bytes
            return output.getvalue().encode(self.encoding)
        except Exception as e:
            logger.error("CSV export failed", exc=e)
            raise StorageError(f"Failed to export CSV file: {str(e)}")


class ExcelExporter(DataExporter):
    """Exporter for Excel files"""
    
    def export(self, data: Dict[str, List[Dict[str, Any]]]) -> bytes:
        """
        Export data to Excel
        
        Args:
            data: Dictionary with sheet names as keys and lists of row dictionaries as values
            
        Returns:
            Excel file as bytes
            
        Raises:
            StorageError: If export fails
            ValueError: If data is not a dictionary of lists
        """
        try:
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary with sheet names as keys")
                
            # Create Excel output
            output = BytesIO()
            
            # Create Excel writer
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for sheet_name, sheet_data in data.items():
                    # Create DataFrame from sheet data
                    df = pd.DataFrame(sheet_data)
                    
                    # Remove internal fields
                    if "_row_number" in df.columns:
                        df = df.drop(columns=["_row_number"])
                        
                    # Write sheet
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    
            # Get Excel as bytes
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            logger.error("Excel export failed", exc=e)
            raise StorageError(f"Failed to export Excel file: {str(e)}")
            
    def export_single_sheet(self, data: List[Dict[str, Any]], sheet_name: str = "Sheet1") -> bytes:
        """
        Export data to a single Excel sheet
        
        Args:
            data: List of dictionaries to export
            sheet_name: Name of the sheet
            
        Returns:
            Excel file as bytes
            
        Raises:
            StorageError: If export fails
            ValueError: If data is not a list of dictionaries
        """
        if not isinstance(data, list):
            raise ValueError("Data must be a list of dictionaries")
            
        return self.export({sheet_name: data})


class JSONExporter(DataExporter):
    """Exporter for JSON files"""
    
    def __init__(self, pretty: bool = False, encoding: str = 'utf-8'):
        """
        Initialize the JSON exporter
        
        Args:
            pretty: Whether to format the JSON with indentation
            encoding: Character encoding
        """
        self.pretty = pretty
        self.encoding = encoding
        
    def export(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> bytes:
        """
        Export data to JSON
        
        Args:
            data: Data to export (list or dictionary)
            
        Returns:
            JSON file as bytes
            
        Raises:
            StorageError: If export fails
        """
        try:
            # Create JSON output
            indent = 2 if self.pretty else None
            json_str = json.dumps(data, indent=indent)
            
            # Get JSON as bytes
            return json_str.encode(self.encoding)
        except Exception as e:
            logger.error("JSON export failed", exc=e)
            raise StorageError(f"Failed to export JSON file: {str(e)}") 