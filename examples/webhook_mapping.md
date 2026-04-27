# CRM Webhook Mapping

This file shows how cleaned lead records can move into CRM systems such as **ReSimpli** or **GoHighLevel**.

## Clean lead schema

The cleaned output in [`sample_output.csv`](sample_output.csv) contains:

- `agent_name`
- `brokerage`
- `email`
- `mobile_phone`
- `city`
- `state`
- `source_platform`
- `source_url`
- `crm_status`

## ReSimpli-style mapping

| Lead field | CRM field |
| --- | --- |
| `agent_name` | contact full name |
| `email` | email |
| `mobile_phone` | phone |
| `city` | city |
| `state` | state |
| `brokerage` | custom field: brokerage |
| `source_platform` | lead source |
| `source_url` | custom field: source URL |
| `crm_status` | pipeline stage or review queue |

## GoHighLevel-style mapping

| Lead field | CRM field |
| --- | --- |
| `agent_name` | `firstName` + `lastName` |
| `email` | `email` |
| `mobile_phone` | `phone` |
| `city` | `city` |
| `state` | `state` |
| `source_platform` | `source` |
| `brokerage` | `customFields.brokerage` |
| `source_url` | `customFields.source_url` |
| `crm_status` | tag or custom field |

## Posting rule

Only records with `crm_status=ready_for_crm` should be posted automatically. Records marked `needs_review` should stay in a manual review queue until missing fields are resolved.

## Example webhook payload shape

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "city": "Los Angeles",
  "state": "CA",
  "source": "Realtor.com",
  "tags": ["ca-agent", "off-market-outreach", "ready-for-crm"],
  "customFields": {
    "brokerage": "ABC Realty",
    "source_url": "https://www.realtor.com/profile/johndoe",
    "crm_status": "ready_for_crm"
  }
}
```

## Operational notes

- split names before exporting to CRMs that store first and last names separately
- normalize phone numbers before posting
- keep source URLs for auditability and follow-up
- route incomplete records into a review bucket instead of sending them automatically
