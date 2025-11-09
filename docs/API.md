# API Documentation

## Overview

The Telegram Bot Dashboard API is built with FastAPI and provides RESTful endpoints for managing bot products and phone registry operations.

Base URL: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication for product management endpoints. Phone registry endpoints require an API key configured in the environment.

## Products API

### List Products

```http
GET /api/products
```

Query Parameters:
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 50, max: 100) - Items per page
- `status` (string, optional) - Filter by status: Active, Expired, ExpiringSoon
- `search` (string, optional) - Search in name, description, customer

Response:
```json
{
  "total": 100,
  "page": 1,
  "per_page": 50,
  "products": [...]
}
```

### Create Product

```http
POST /api/products
```

Request Body:
```json
{
  "name": "Bot Name",
  "description": "Bot description",
  "bot_username": "mybot",
  "website_link": "https://example.com",
  "contract_months": 6,
  "customer_telegram": "@customer",
  "customer_link": "https://t.me/customer"
}
```

### Get Product

```http
GET /api/products/{id}
```

### Update Product

```http
PUT /api/products/{id}
```

Request Body: (all fields optional)
```json
{
  "name": "Updated Name",
  "contract_months": 12
}
```

### Delete Product

```http
DELETE /api/products/{id}
```

### Renew Product

```http
POST /api/products/{id}/renew?months=3
```

Query Parameters:
- `months` (integer, required, 1-12) - Number of months to extend

### Dashboard Statistics

```http
GET /api/products/stats
```

Response:
```json
{
  "total_products": 50,
  "active_products": 40,
  "expired_products": 5,
  "expiring_soon_7_days": 3,
  "expiring_soon_30_days": 8
}
```

## Phone Registry API

### Check Phone Number

```http
POST /api/phone/check
```

Request Body:
```json
{
  "phone_number": "+1234567890"
}
```

### Register Phone Number

```http
POST /api/phone/register
```

Request Body:
```json
{
  "phone_number": "+1234567890",
  "metadata": {}
}
```

### Bulk Register

```http
POST /api/phone/bulk-register
```

Request Body:
```json
{
  "phone_numbers": ["+1234567890", "+0987654321"],
  "metadata": {}
}
```

Maximum 1000 phone numbers per request.

### Cleanup Old Records

```http
DELETE /api/phone/cleanup
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- 200: Success
- 201: Created
- 204: No Content (successful deletion)
- 400: Bad Request
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

Error Response Format:
```json
{
  "detail": "Error message"
}
```

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation with interactive API testing.
