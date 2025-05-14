from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator, field_validator
from enum import Enum


class DealStage(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"
    CLOSED = "closed"


class DealSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"


class FollowupStatus(str, Enum):
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"


class CustomerDetails(BaseModel):
    contact: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class Opportunity(BaseModel):
    id: str
    code: Optional[str] = None
    hubspot_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    customer_name: str
    customer_details: Optional[CustomerDetails] = None
    estimated_value: Optional[float] = None
    currency: Optional[str] = None
    estimated_value_usd: Optional[float] = None
    deal_size: Optional[DealSize] = None
    deal_stage: DealStage
    previous_stage: Optional[str] = None
    stage_change_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    closing_probability: Optional[float] = None
    source: Optional[str] = None
    created_by_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    team_id: Optional[str] = None
    division_id: Optional[str] = None
    related_contract_id: Optional[str] = None
    last_interaction_date: Optional[datetime] = None
    next_followup_date: Optional[datetime] = None
    followup_status: Optional[FollowupStatus] = None
    onsite_priority: Optional[bool] = False
    requirements: Optional[List[Dict[str, str]]] = None
    skills_required: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    hubspot_created_at: Optional[datetime] = None
    hubspot_last_updated_at: Optional[datetime] = None
    sync_status: Optional[str] = None
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    external_id: Optional[str] = None
    is_deleted: Optional[bool] = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
    
    # Calculated fields - not stored in DynamoDB
    days_since_last_interaction: Optional[int] = None
    
    @field_validator('days_since_last_interaction', mode='always')
    def calculate_days_since_last_interaction(cls, v, values):
        last_interaction = values.get('last_interaction_date')
        if not last_interaction:
            return None
        return (datetime.now() - last_interaction).days

    def to_dynamo_item(self) -> Dict[str, Any]:
        """Convert Opportunity object to DynamoDB item format"""
        item = {
            'PK': f"OPPORTUNITY#{self.id}",
            'SK': f"METADATA#{self.id}",
            'GSI1PK': f"HUBSPOT_OPPORTUNITY#{self.hubspot_id}" if self.hubspot_id else f"OPPORTUNITY#{self.id}",
            'GSI1SK': self.name,
            'GSI2PK': f"OPPORTUNITY_STAGE#{self.deal_stage.value}",
            'GSI2SK': self.last_interaction_date.isoformat() if self.last_interaction_date else "",
            'GSI3PK': f"SALES#{self.assigned_to_id}" if self.assigned_to_id else "SALES#UNASSIGNED",
            'GSI3SK': f"OPPORTUNITY#{self.followup_status.value if self.followup_status else 'NONE'}#{self.name}",
            'id': self.id,
            'name': self.name,
            'deal_stage': self.deal_stage.value,
            'created_at': self.created_at.isoformat()
        }
        
        # Add optional fields if they exist
        optional_fields = [
            'code', 'hubspot_id', 'description', 'customer_name', 
            'estimated_value', 'currency', 'estimated_value_usd', 
            'previous_stage', 'closing_probability', 'source', 
            'created_by_id', 'assigned_to_id', 'team_id', 'division_id',
            'related_contract_id', 'onsite_priority', 'requirements',
            'skills_required', 'tags', 'external_id', 'is_deleted'
        ]
        
        for field in optional_fields:
            value = getattr(self, field)
            if value is not None:
                item[field] = value
                
        # Handle enum fields
        if self.deal_size:
            item['deal_size'] = self.deal_size.value
            
        if self.followup_status:
            item['followup_status'] = self.followup_status.value
            
        # Handle datetime fields
        datetime_fields = [
            'stage_change_date', 'closing_date', 'last_interaction_date',
            'next_followup_date', 'hubspot_created_at', 'hubspot_last_updated_at',
            'last_sync_at', 'updated_at', 'deleted_at'
        ]
        
        for field in datetime_fields:
            value = getattr(self, field)
            if value:
                item[field] = value.isoformat()
                
        # Handle nested object
        if self.customer_details:
            item['customer_details'] = self.customer_details.model_dump(exclude_none=True)
            
        return item
    
    @classmethod
    def from_dynamo_item(cls, item: Dict[str, Any]) -> 'Opportunity':
        """Create Opportunity object from DynamoDB item"""
        if not item:
            return None
            
        # Handle datetime fields
        datetime_fields = [
            'stage_change_date', 'closing_date', 'last_interaction_date',
            'next_followup_date', 'hubspot_created_at', 'hubspot_last_updated_at',
            'last_sync_at', 'created_at', 'updated_at', 'deleted_at'
        ]
        
        for field in datetime_fields:
            if field in item and item[field]:
                if isinstance(item[field], str):
                    item[field] = datetime.fromisoformat(item[field])
        
        # Handle enum fields
        if 'deal_stage' in item:
            item['deal_stage'] = DealStage(item['deal_stage'])
            
        if 'deal_size' in item:
            item['deal_size'] = DealSize(item['deal_size'])
            
        if 'followup_status' in item:
            item['followup_status'] = FollowupStatus(item['followup_status'])
            
        # Handle nested object
        if 'customer_details' in item and item['customer_details']:
            item['customer_details'] = CustomerDetails(**item['customer_details'])
            
        # Remove DynamoDB-specific keys
        dynamo_keys = ['PK', 'SK', 'GSI1PK', 'GSI1SK', 'GSI2PK', 'GSI2SK', 'GSI3PK', 'GSI3SK']
        for key in dynamo_keys:
            if key in item:
                del item[key]
                
        return cls(**item)


class OpportunityList(BaseModel):
    items: List[Opportunity]
    next_token: Optional[str] = None
    count: int 