#!/usr/bin/env python3
"""
Script to generate sample data for DynamoDB.
Generate fake data for different entity types to use in dev/test environment.
"""

import json
import uuid
import random
from datetime import datetime, timedelta
import os
from pathlib import Path

# Create seeds directory if it doesn't exist
SEEDS_DIR = Path(__file__).parent.parent.parent / 'seeds'
SEEDS_DIR.mkdir(exist_ok=True)

def generate_iso_date(days_ago=0):
    """Generate ISO 8601 date string."""
    dt = datetime.now() - timedelta(days=days_ago)
    return dt.strftime('%Y-%m-%d')

def generate_iso_datetime(days_ago=0, hours_ago=0):
    """Generate ISO 8601 datetime string."""
    dt = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
    return dt.isoformat()

def generate_user(index, is_admin=False):
    """Generate a user entity."""
    user_id = str(uuid.uuid4())
    username = f"user{index}" if not is_admin else "admin"
    email = f"{username}@sdims.example.com"
    
    return {
        'PK': f'USER#{user_id}',
        'SK': f'METADATA#{user_id}',
        'GSI1PK': 'USER',
        'GSI1SK': username,
        'GSI2PK': 'USER',
        'GSI2SK': email,
        'id': user_id,
        'username': username,
        'password_hash': '$2b$12$B8oCZu9i/6Q5XVXzIdxjJ.YiYBSLNL6NUAgUZLKGT0BhRcDDRpMK2',  # "Admin@123"
        'email': email,
        'full_name': f"User {index}" if not is_admin else "System Administrator",
        'role_id': 'ADMIN_ROLE_ID' if is_admin else 'USER_ROLE_ID',
        'is_active': True,
        'last_login_at': generate_iso_datetime(random.randint(0, 10)),
        'created_at': generate_iso_datetime(30),
        'updated_at': generate_iso_datetime(random.randint(0, 5))
    }

def generate_employee(index, team_id):
    """Generate an employee entity."""
    employee_id = str(uuid.uuid4())
    first_name = f"First{index}"
    last_name = f"Last{index}"
    employee_code = f"EMP{1000 + index}"
    
    statuses = ['Available', 'Allocated', 'EndingSoon', 'OnLeave', 'Resigned']
    current_status = random.choice(statuses)
    
    return {
        'PK': f'EMPLOYEE#{employee_id}',
        'SK': f'METADATA#{employee_id}',
        'GSI1PK': 'EMPLOYEE',
        'GSI1SK': employee_code,
        'GSI2PK': f'EMPLOYEE_STATUS#{current_status}',
        'GSI2SK': f'{last_name}#{first_name}',
        'GSI3PK': f'EMPLOYEE_TEAM#{team_id}',
        'GSI3SK': f'{last_name}#{first_name}',
        'id': employee_id,
        'employee_code': employee_code,
        'first_name': first_name,
        'last_name': last_name,
        'full_name': f"{first_name} {last_name}",
        'birth_date': generate_iso_date(random.randint(8000, 12000)),  # ~25-35 years ago
        'hire_date': generate_iso_date(random.randint(30, 1000)),
        'company_email': f"{first_name.lower()}.{last_name.lower()}@sdims.example.com",
        'internal_account': f"{first_name[0].lower()}{last_name.lower()}",
        'address': f"{index} Example Street, City",
        'phone_number': f"+1555{index:06d}",
        'position': random.choice(['Developer', 'Tester', 'Analyst', 'Manager', 'Designer']),
        'team_id': team_id,
        'current_status': current_status,
        'allocation_percentage': random.randint(0, 100),
        'current_project_id': None if current_status != 'Allocated' else f'PROJECT_{random.randint(1, 5)}',
        'current_project_name': None if current_status != 'Allocated' else f'Project {random.randint(1, 5)}',
        'created_at': generate_iso_datetime(random.randint(30, 1000)),
        'updated_at': generate_iso_datetime(random.randint(0, 30))
    }

def generate_team(index):
    """Generate a team entity."""
    team_id = str(uuid.uuid4())
    team_name = f"Team {index}"
    
    return {
        'PK': f'TEAM#{team_id}',
        'SK': f'METADATA#{team_id}',
        'GSI1PK': 'TEAM',
        'GSI1SK': team_name,
        'GSI2PK': f'DIVISION#DIV{index % 3 + 1}',
        'GSI2SK': f'TEAM#{team_name}',
        'id': team_id,
        'name': team_name,
        'description': f"Description for {team_name}",
        'leader': {
            'id': str(uuid.uuid4()),
            'name': f"Leader {index}"
        },
        'division_id': f'DIV{index % 3 + 1}',
        'created_at': generate_iso_datetime(random.randint(100, 500)),
        'updated_at': generate_iso_datetime(random.randint(0, 100))
    }

def generate_skill_category(index):
    """Generate a skill category entity."""
    category_id = str(uuid.uuid4())
    category_name = f"Skill Category {index}"
    
    return {
        'PK': f'SKILL_CATEGORY#{category_id}',
        'SK': f'METADATA#{category_id}',
        'GSI1PK': 'SKILL_CATEGORY',
        'GSI1SK': category_name,
        'id': category_id,
        'name': category_name,
        'description': f"Description for {category_name}",
        'display_order': index,
        'created_at': generate_iso_datetime(random.randint(100, 500)),
        'updated_at': generate_iso_datetime(random.randint(0, 100))
    }

def generate_skill(index, category_id):
    """Generate a skill entity."""
    skill_id = str(uuid.uuid4())
    skill_name = f"Skill {index}"
    
    return {
        'PK': f'SKILL#{skill_id}',
        'SK': f'METADATA#{skill_id}',
        'GSI1PK': f'SKILL_CATEGORY#{category_id}',
        'GSI1SK': skill_name,
        'id': skill_id,
        'category_id': category_id,
        'name': skill_name,
        'description': f"Description for {skill_name}",
        'display_order': index,
        'created_at': generate_iso_datetime(random.randint(100, 500)),
        'updated_at': generate_iso_datetime(random.randint(0, 100))
    }

def generate_contract(index):
    """Generate a contract entity."""
    contract_id = str(uuid.uuid4())
    contract_name = f"Contract {index}"
    contract_code = f"CTR-{2023}-{index:03d}"
    
    start_date = generate_iso_date(random.randint(0, 365))
    end_date = generate_iso_date(random.randint(365, 730))
    
    status_options = ['Draft', 'InReview', 'Approved', 'Active', 'InProgress', 'OnHold', 'Completed', 'Terminated', 'Expired', 'Cancelled']
    status = random.choice(status_options)
    
    return {
        'PK': f'CONTRACT#{contract_id}',
        'SK': f'METADATA#{contract_id}',
        'GSI1PK': f'CONTRACT_CODE#{contract_code}',
        'GSI1SK': contract_name,
        'GSI2PK': f'CONTRACT_STATUS#{status}',
        'GSI2SK': end_date,
        'GSI3PK': f'CUSTOMER#Customer {index % 10 + 1}',
        'GSI3SK': start_date,
        'id': contract_id,
        'contract_code': contract_code,
        'name': contract_name,
        'description': f"Description for {contract_name}",
        'customer_name': f"Customer {index % 10 + 1}",
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'total_value': random.randint(10000, 1000000),
        'total_value_usd': random.randint(10000, 1000000),
        'currency': 'USD',
        'created_at': generate_iso_datetime(random.randint(100, 500)),
        'updated_at': generate_iso_datetime(random.randint(0, 100))
    }

def generate_seed_data(num_users=10, num_teams=5, num_employees=20, num_skill_categories=3, num_skills_per_category=5, num_contracts=10):
    """Generate sample seed data for all entity types."""
    seed_data = []
    
    # Generate teams
    teams = []
    for i in range(1, num_teams + 1):
        team = generate_team(i)
        teams.append(team)
        seed_data.append(team)
    
    # Generate skill categories and skills
    skill_categories = []
    skills = []
    for i in range(1, num_skill_categories + 1):
        category = generate_skill_category(i)
        skill_categories.append(category)
        seed_data.append(category)
        
        # Skills for this category
        for j in range(1, num_skills_per_category + 1):
            skill_index = (i - 1) * num_skills_per_category + j
            skill = generate_skill(skill_index, category['id'])
            skills.append(skill)
            seed_data.append(skill)
    
    # Generate users
    users = []
    admin_user = generate_user(0, is_admin=True)
    users.append(admin_user)
    seed_data.append(admin_user)
    
    for i in range(1, num_users + 1):
        user = generate_user(i)
        users.append(user)
        seed_data.append(user)
    
    # Generate employees
    employees = []
    for i in range(1, num_employees + 1):
        team_id = teams[i % len(teams)]['id']
        employee = generate_employee(i, team_id)
        employees.append(employee)
        seed_data.append(employee)
    
    # Generate contracts
    contracts = []
    for i in range(1, num_contracts + 1):
        contract = generate_contract(i)
        contracts.append(contract)
        seed_data.append(contract)
    
    # Generate some employee-skill relationships
    for employee in employees:
        # Assign 2-5 random skills to each employee
        num_skills = random.randint(2, 5)
        selected_skills = random.sample(skills, num_skills)
        
        for skill in selected_skills:
            employee_skill = {
                'PK': employee['PK'],
                'SK': f"SKILL#{skill['id']}",
                'GSI1PK': f"SKILL#{skill['id']}",
                'GSI1SK': employee['PK'],
                'GSI2PK': f"SKILL#{skill['id']}",
                'GSI2SK': str(random.randint(1, 10)),  # Years of experience
                'id': str(uuid.uuid4()),
                'employee_id': employee['id'],
                'skill_id': skill['id'],
                'years_experience': random.randint(1, 10),
                'self_assessment_level': random.choice(['Basic', 'Intermediate', 'Advanced', 'Expert']),
                'leader_assessment_level': random.choice(['Basic', 'Intermediate', 'Advanced', 'Expert']),
                'level': random.randint(1, 5),
                'is_verified': random.choice([True, False]),
                'created_at': generate_iso_datetime(random.randint(0, 180)),
                'updated_at': generate_iso_datetime(random.randint(0, 30))
            }
            seed_data.append(employee_skill)
    
    return seed_data

def main():
    """Main function to generate and save seed data."""
    seed_data = generate_seed_data()
    
    # Lưu dữ liệu vào file JSON
    output_file = SEEDS_DIR / 'sample_data.json'
    with open(output_file, 'w') as f:
        json.dump(seed_data, f, indent=2)
    
    print(f"Generated {len(seed_data)} sample entities in {output_file}")

if __name__ == "__main__":
    main() 