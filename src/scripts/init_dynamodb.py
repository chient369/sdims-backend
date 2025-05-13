#!/usr/bin/env python3
"""
Script để khởi tạo dữ liệu ban đầu cho DynamoDB table.
Sử dụng khi triển khai lần đầu hoặc khi cần reset dữ liệu.
"""

import os
import sys
import json
import logging
import argparse
import boto3
from datetime import datetime
from pathlib import Path

# Thêm thư mục src vào sys.path để import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.dynamodb import dynamodb_repo, create_initial_data

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Initialize DynamoDB table with initial data')
    parser.add_argument('--stage', default='dev', help='Deployment stage (dev, staging, prod)')
    parser.add_argument('--create-table', action='store_true', help='Create DynamoDB table if it does not exist')
    parser.add_argument('--force', action='store_true', help='Force data initialization even if table already has data')
    parser.add_argument('--seed-file', help='Path to JSON seed file with additional data')
    return parser.parse_args()

def check_table_exists(table_name):
    """Check if DynamoDB table exists."""
    dynamodb = boto3.client('dynamodb')
    try:
        dynamodb.describe_table(TableName=table_name)
        return True
    except Exception:
        return False

def create_table(table_name):
    """Create DynamoDB table with required schema."""
    logger.info(f"Creating DynamoDB table: {table_name}")
    
    dynamodb = boto3.client('dynamodb')
    
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI1SK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI2PK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI2SK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI3PK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI3SK', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'GSI1',
                    'KeySchema': [
                        {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                        {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'GSI2',
                    'KeySchema': [
                        {'AttributeName': 'GSI2PK', 'KeyType': 'HASH'},
                        {'AttributeName': 'GSI2SK', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'GSI3',
                    'KeySchema': [
                        {'AttributeName': 'GSI3PK', 'KeyType': 'HASH'},
                        {'AttributeName': 'GSI3SK', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
            SSESpecification={
                'Enabled': True
            }
        )
        logger.info(f"DynamoDB table created: {table_name}")
        
        # Đợi cho table có trạng thái ACTIVE
        dynamodb.get_waiter('table_exists').wait(TableName=table_name)
        logger.info(f"Table {table_name} is now active and ready to use")
        
        return True
    except Exception as e:
        logger.error(f"Error creating DynamoDB table: {e}")
        return False

def check_table_is_empty():
    """Check if DynamoDB table is empty."""
    try:
        response = dynamodb_repo.scan(limit=1)
        return len(response.get('Items', [])) == 0
    except Exception as e:
        logger.error(f"Error checking if table is empty: {e}")
        return False

def load_seed_data(seed_file):
    """Load and import seed data from JSON file."""
    try:
        if not os.path.exists(seed_file):
            logger.error(f"Seed file does not exist: {seed_file}")
            return False
        
        with open(seed_file, 'r') as f:
            seed_data = json.load(f)
        
        if not isinstance(seed_data, list):
            logger.error("Seed data must be a list of items")
            return False
        
        logger.info(f"Loading {len(seed_data)} items from seed file")
        
        # Chia thành các batch nhỏ (25 items mỗi batch - giới hạn của batch_write)
        batch_size = 25
        for i in range(0, len(seed_data), batch_size):
            batch = seed_data[i:i+batch_size]
            dynamodb_repo.batch_write(batch)
            logger.info(f"Loaded batch {i//batch_size + 1}/{(len(seed_data)-1)//batch_size + 1}")
        
        return True
    except Exception as e:
        logger.error(f"Error loading seed data: {e}")
        return False

def main():
    """Main function to initialize DynamoDB table."""
    args = parse_args()
    
    # Thiết lập stage nếu không được đặt trong biến môi trường
    if 'STAGE' not in os.environ:
        os.environ['STAGE'] = args.stage
    
    # Xác định tên table dựa trên stage
    table_name = f"SDIMS-Main-{os.environ.get('STAGE', 'dev')}"
    os.environ['DYNAMODB_TABLE'] = table_name
    
    logger.info(f"Initializing DynamoDB table: {table_name} for stage: {os.environ.get('STAGE', 'dev')}")
    
    # Kiểm tra table tồn tại
    table_exists = check_table_exists(table_name)
    
    # Tạo table nếu cần
    if not table_exists:
        if args.create_table:
            table_created = create_table(table_name)
            if not table_created:
                logger.error("Failed to create DynamoDB table")
                return 1
        else:
            logger.error(f"Table {table_name} does not exist. Use --create-table to create it.")
            return 1
    
    # Kiểm tra table trống hoặc force được thiết lập
    if not check_table_is_empty() and not args.force:
        logger.warning("Table is not empty. Use --force to initialize data anyway.")
        return 0
    
    # Tạo dữ liệu ban đầu
    logger.info("Creating initial data...")
    if not create_initial_data():
        logger.error("Failed to create initial data")
        return 1
    
    # Tải dữ liệu thêm từ seed file nếu có
    if args.seed_file:
        logger.info(f"Loading seed data from {args.seed_file}...")
        if not load_seed_data(args.seed_file):
            logger.error("Failed to load seed data")
            return 1
    
    logger.info("DynamoDB initialization completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 