# Opportunity Management APIs

This module provides APIs for managing business opportunities in the SDIMS system.

## APIs

### List Opportunities

**Endpoint:** GET `/api/v1/opportunities`

**Description:** Retrieves a list of business opportunities with filtering, sorting, and pagination support.

**Query Parameters:**
- `page_size` (optional): Number of items per page (default: 10, max: 100)
- `next_token` (optional): Pagination token for getting the next set of results
- `sort_by` (optional): Field to sort by (default: 'updated_at', options: created_at, updated_at, last_interaction_date, name, customer_name, estimated_value, closing_date, deal_stage)
- `sort_order` (optional): Sort direction (default: 'desc', options: asc, desc)
- `search` (optional): Search term to find in name, description, and customer_name
- `status` (optional): Filter by deal stage (e.g., new, contacted, qualified, proposal, negotiation, won, lost, closed)
- `follow_up_status` (optional): Filter by follow-up status (Red, Yellow, Green)
- `assigned_to` (optional): Filter by assigned user ID
- `customer_name` (optional): Filter by customer name
- `created_after`, `created_before` (optional): Filter by creation date range (ISO8601 format)
- `updated_after`, `updated_before` (optional): Filter by update date range (ISO8601 format)
- `interaction_after`, `interaction_before` (optional): Filter by last interaction date range (ISO8601 format)
- `min_value`, `max_value` (optional): Filter by estimated value range

**Response:**
```json
{
  "items": [
    {
      "id": "123",
      "name": "Test Opportunity",
      "customer_name": "Test Customer",
      "deal_stage": "qualified",
      "followup_status": "Green",
      ...
    }
  ],
  "next_token": "eyJQSyI6Ik9QUE9SVFVOSVRZIzk5OSIsIlNLIjoiTUVUQURBVEEjOTk5In0=",
  "count": 1
}
```

### Get Opportunity

**Endpoint:** GET `/api/v1/opportunities/{opportunity_id}`

**Description:** Retrieves detailed information about a specific opportunity.

**Path Parameters:**
- `opportunity_id`: ID of the opportunity to retrieve

**Response:**
```json
{
  "id": "123",
  "name": "Test Opportunity",
  "description": "Opportunity description",
  "customer_name": "Test Customer",
  "customer_details": {
    "contact": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "website": "https://example.com",
    "industry": "Technology"
  },
  "estimated_value": 10000.0,
  "currency": "USD",
  "estimated_value_usd": 10000.0,
  "deal_stage": "qualified",
  "previous_stage": "contacted",
  "stage_change_date": "2025-04-15T00:00:00",
  "closing_date": "2025-06-30T00:00:00",
  "assigned_to_id": "user123",
  "last_interaction_date": "2025-05-01T00:00:00",
  "next_followup_date": "2025-05-15T00:00:00",
  "followup_status": "Green",
  "days_since_last_interaction": 5,
  "onsite_priority": false,
  ...
}
```

## Follow-up Status Calculation

The follow-up status is calculated based on the following rules:

1. **Red**: 
   - No last interaction recorded
   - Last interaction is more than 7 days ago

2. **Yellow**:
   - Next follow-up date is within the next 2 days
   - Deal is in proposal or negotiation stage with no interaction in the last 3 days

3. **Green**:
   - Recent interaction and not meeting any of the above conditions 