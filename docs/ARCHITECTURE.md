# Architecture Documentation

## System Overview

The Telegram Bot Dashboard is a full-stack web application following a modern, scalable architecture with clear separation between frontend and backend.

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────┐
│  React Frontend │
│   (Port 5173)   │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐      ┌──────────────────┐
│  FastAPI Backend│◄────►│   PostgreSQL     │
│   (Port 8000)   │      │    Database      │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│ Phone Registry  │
│  External API   │
└─────────────────┘
```

## Backend Architecture

### Layered Structure

```
┌─────────────────────────────────┐
│         API Routes              │  ← HTTP endpoints
├─────────────────────────────────┤
│         Services                │  ← Business logic
├─────────────────────────────────┤
│      Models/Schemas             │  ← Data validation
├─────────────────────────────────┤
│    Database (SQLAlchemy)        │  ← Data persistence
└─────────────────────────────────┘
```

### Components

#### 1. API Routes (`app/api/routes/`)
- Handle HTTP requests/responses
- Input validation
- Route-specific logic
- Status code management

#### 2. Services (`app/services/`)
- Business logic implementation
- Data transformation
- External API communication
- Complex operations

#### 3. Models (`app/models/`)
- SQLAlchemy ORM models
- Database schema definition
- Relationships
- Database constraints

#### 4. Schemas (`app/schemas/`)
- Pydantic models
- Request/response validation
- Data serialization
- Type safety

#### 5. Core (`app/core/`)
- Configuration management
- Database connection
- Security utilities
- Shared dependencies

### Database Design

#### Products Table
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    bot_username VARCHAR(255),
    website_link VARCHAR(500),
    contract_months INTEGER NOT NULL,
    contract_start_date TIMESTAMP NOT NULL,
    contract_end_date TIMESTAMP NOT NULL,
    is_renewed BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) NOT NULL,
    customer_telegram VARCHAR(255),
    customer_link VARCHAR(500),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_customer ON products(customer_telegram);
CREATE INDEX idx_products_end_date ON products(contract_end_date);
```

### Async Architecture

The backend uses async/await throughout:

```python
# Async database sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Async route handlers
@router.get("/products")
async def list_products(db: AsyncSession = Depends(get_db)):
    products = await ProductService.get_products(db)
    return products

# Async external API calls
async def check_phone(phone_number: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(...)
```

## Frontend Architecture

### Component Structure

```
src/
├── components/
│   ├── ui/              # Reusable UI components (shadcn)
│   ├── layout/          # Layout components
│   ├── dashboard/       # Dashboard-specific components
│   ├── products/        # Product management components
│   └── phone-registry/  # Phone registry components
├── lib/
│   ├── api.ts          # API client
│   └── utils.ts        # Utility functions
├── pages/              # Page components
├── types/              # TypeScript types
└── App.tsx             # Main app component
```

### State Management

Using React Query for server state:

```typescript
// Fetching data
const { data, isLoading } = useQuery({
  queryKey: ['products'],
  queryFn: api.products.list,
})

// Mutations
const mutation = useMutation({
  mutationFn: api.products.create,
  onSuccess: () => {
    queryClient.invalidateQueries(['products'])
  },
})
```

### Routing

```typescript
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/products" element={<Products />} />
  <Route path="/phone-registry" element={<PhoneRegistry />} />
</Routes>
```

## Data Flow

### Product Creation Flow

```
1. User fills form → React Hook Form
2. Validation → Zod schema
3. Submit → useMutation
4. HTTP POST → axios
5. FastAPI route → products.create_product
6. Service layer → ProductService.create_product
7. Database → SQLAlchemy insert
8. Response → JSON serialization
9. Update UI → React Query cache invalidation
10. Toast notification → sonner
```

### Error Handling

#### Backend
```python
@router.get("/{id}")
async def get_product(id: UUID):
    product = await ProductService.get_product(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

#### Frontend
```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    toast.error(error.response?.data?.detail)
    return Promise.reject(error)
  }
)
```

## Database Migrations

Using Alembic for version control:

```
1. Model changes → SQLAlchemy models
2. Generate migration → alembic revision --autogenerate
3. Review migration → Check generated SQL
4. Apply migration → alembic upgrade head
5. Rollback if needed → alembic downgrade -1
```

## Performance Optimizations

### Backend
- Async I/O operations
- Database connection pooling
- Query optimization with indexes
- Pagination for large datasets
- Efficient filtering

### Frontend
- Code splitting (lazy loading)
- React Query caching
- Debounced search
- Optimistic updates
- Virtual scrolling (for large lists)

### Database
```sql
-- Indexes for common queries
CREATE INDEX idx_status ON products(status);
CREATE INDEX idx_end_date ON products(contract_end_date);
CREATE INDEX idx_customer ON products(customer_telegram);

-- Connection pooling
pool_size=20
max_overflow=10
```

## Security

### Backend
- Input validation (Pydantic)
- SQL injection prevention (ORM)
- CORS configuration
- API key authentication (phone registry)
- Environment-based secrets

### Frontend
- XSS prevention (React auto-escaping)
- HTTPS enforcement
- Secure headers
- Environment variables

## Deployment Architecture

### Development
```
Frontend (Vite dev) :5173
Backend (uvicorn)   :8000
PostgreSQL          :5432
```

### Production
```
Nginx (reverse proxy) :80/443
  ├─► Frontend (static) /
  └─► Backend API       /api
Backend (uvicorn)     :8000
PostgreSQL            :5432
```

## Monitoring & Logging

### Logs
```
backend/logs/
├── app.log          # Application logs
├── backend.log      # Backend server logs
└── frontend.log     # Frontend build logs
```

### Log Levels
- DEBUG: Development debugging
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical issues

## Scalability Considerations

### Horizontal Scaling
- Stateless API (can run multiple instances)
- Database connection pooling
- Load balancer ready
- Session storage (if needed)

### Vertical Scaling
- Worker process count (API_WORKERS)
- Database connection pool size
- Memory allocation

### Caching (Future)
- Redis for API responses
- Browser caching for static assets
- Database query caching
