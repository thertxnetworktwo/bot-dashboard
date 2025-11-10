# Django Migration Notes

## Migration from FastAPI to Django

This project has been migrated from FastAPI to Django + Django REST Framework while maintaining full API compatibility with the existing frontend.

### Key Changes

1. **Backend Framework**: FastAPI → Django 5.2 + Django REST Framework
2. **ORM**: SQLAlchemy (async) → Django ORM
3. **Migrations**: Alembic → Django Migrations
4. **Server**: Uvicorn → Django Development Server / Gunicorn (production)

### API Compatibility

All API endpoints remain the same:
- `GET /api/health` - Health check
- `GET /api/products/` - List products
- `POST /api/products/` - Create product
- `GET /api/products/{id}/` - Get product
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `POST /api/products/{id}/renew/` - Renew product
- `GET /api/products/stats/` - Dashboard statistics
- Phone registry endpoints remain unchanged

Response formats are identical to ensure frontend compatibility.

### Dashboard Script Changes

The `dashboard.sh` script has been simplified:
- **Reduced from 688 lines to ~350 lines** (50% reduction)
- **Improved Vite process management** with proper process group handling
- **Removed commands**: autostart, backup/restore, separate dev servers, alembic-specific commands
- **Kept essential commands**: install, setup, migrate, dev, build, start, stop, restart, logs, status, test, clean

### Database Configuration

The application now uses:
- **PostgreSQL** for production (configured via .env)
- **SQLite** for testing when PostgreSQL is unavailable (set `USE_SQLITE=true`)

### Migration Command Changes

**Old (Alembic)**:
```bash
./dashboard.sh migrate "description"  # Create migration
./dashboard.sh upgrade                 # Apply migrations
./dashboard.sh downgrade              # Rollback
```

**New (Django)**:
```bash
./dashboard.sh migrate                # Create and apply migrations
```

Django migrations are automatic and simpler to use.

### Old Files

The original FastAPI implementation has been backed up to:
- `backend/old_fastapi_backup/` (gitignored)

This can be deleted once the migration is confirmed working.

### Testing

Run tests with:
```bash
./dashboard.sh test
```

Tests use SQLite automatically for isolated testing.
