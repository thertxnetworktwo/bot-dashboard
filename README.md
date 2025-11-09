# Telegram Bot Dashboard

A full-stack dashboard application for managing Telegram bot products with integrated phone registry API functionality.

⚠️ **Security Notice**: This dashboard currently does NOT include authentication. See [Authentication Guide](docs/AUTHENTICATION.md) for security recommendations.

## Features

- 📊 **Dashboard Analytics** - Track products, expiration dates, and key metrics
- 📦 **Products Management** - Full CRUD operations for bot products
- 📱 **Phone Registry Integration** - Check, register, and bulk manage phone numbers
- 🔄 **Database Migrations** - Alembic-powered schema versioning
- 🚀 **Easy Deployment** - Single script handles everything
- 📝 **Production Ready** - Async operations, proper indexing, error handling

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite for build tooling
- Tailwind CSS + shadcn/ui components
- React Query for data fetching
- React Hook Form + Zod for forms

### Backend
- FastAPI (Python)
- SQLAlchemy ORM (async)
- Alembic for migrations
- PostgreSQL database
- Pydantic for validation

## Documentation

- 🚀 [VPS Deployment Guide](docs/VPS_DEPLOYMENT.md) - Deploy to production server
- 🔒 [Authentication Guide](docs/AUTHENTICATION.md) - Secure your dashboard
- 📚 [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running)

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bot-dashboard
```

2. Install dependencies:
```bash
./dashboard.sh install
```

3. Setup the application:
```bash
./dashboard.sh setup
```

4. Configure environment variables:
```bash
# Edit backend/.env with your settings
nano backend/.env

# For VPS deployment, also configure frontend/.env
nano frontend/.env
# Set VITE_API_URL=http://YOUR_VPS_IP:8000
```

5. Start development servers:
```bash
./dashboard.sh dev
```

The application will be available at:
- Frontend: http://localhost:7082
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

**Note**: For VPS/production deployment with external access, see the [VPS Deployment Guide](docs/VPS_DEPLOYMENT.md).

## Dashboard Script Commands

The `dashboard.sh` script is the main control center for the application:

### Installation & Setup
```bash
./dashboard.sh install              # Install all dependencies
./dashboard.sh setup                # Initialize database and migrations
```

### Database Migrations
```bash
./dashboard.sh migrate "message"    # Create new migration
./dashboard.sh upgrade              # Apply pending migrations
./dashboard.sh downgrade            # Rollback last migration
./dashboard.sh migration-status     # Show migration status
```

### Development
```bash
./dashboard.sh dev                  # Start both frontend and backend
./dashboard.sh dev-frontend         # Start only frontend
./dashboard.sh dev-backend          # Start only backend
```

### Production
```bash
./dashboard.sh build                # Build production assets
./dashboard.sh start                # Start production server
./dashboard.sh stop                 # Stop all services
./dashboard.sh restart              # Restart services
```

### Auto-Start
```bash
./dashboard.sh autostart            # Enable systemd auto-start
./dashboard.sh disable-autostart    # Disable auto-start
```

### Monitoring & Maintenance
```bash
./dashboard.sh status               # Check service status
./dashboard.sh logs                 # View all logs
./dashboard.sh logs-backend         # View backend logs only
./dashboard.sh logs-frontend        # View frontend logs only
```

### Database Backup & Restore
```bash
./dashboard.sh backup               # Backup database
./dashboard.sh restore <file>       # Restore from backup
```

### Testing & Quality
```bash
./dashboard.sh test                 # Run tests
./dashboard.sh lint                 # Run linters
./dashboard.sh clean                # Clean build artifacts
```

## Configuration

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dashboard_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dashboard_db
DB_USER=dashboard_user
DB_PASSWORD=your_secure_password

# API
API_SECRET_KEY=your-secret-key-min-32-chars
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Phone Registry (External)
PHONE_REGISTRY_URL=http://localhost:8000
PHONE_REGISTRY_API_KEY=your-api-key

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Environment
ENV=development
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
telegram-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/          # API endpoints
│   │   │   └── deps.py          # Dependencies
│   │   ├── core/
│   │   │   ├── config.py        # Configuration
│   │   │   ├── database.py      # Database setup
│   │   │   └── security.py      # Security utilities
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── main.py              # FastAPI app
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Backend tests
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── lib/                 # Utilities
│   │   ├── pages/               # Page components
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── .env
├── docs/                        # Documentation
├── dashboard.sh                 # Main control script
├── .env.example
└── README.md
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for the interactive API documentation powered by Swagger/OpenAPI.

### Main Endpoints

#### Products
- `GET /api/products` - List products (with pagination, filters)
- `POST /api/products` - Create product
- `GET /api/products/{id}` - Get product details
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product
- `POST /api/products/{id}/renew` - Renew product
- `GET /api/products/stats` - Get dashboard statistics

#### Phone Registry
- `POST /api/phone/check` - Check phone number
- `POST /api/phone/register` - Register phone number
- `POST /api/phone/bulk-register` - Bulk register (up to 1000)
- `DELETE /api/phone/cleanup` - Cleanup old records

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
source venv/bin/activate
pytest tests/ -v

# Frontend tests (if configured)
cd frontend
npm test
```

### Database Migrations

Create a new migration:
```bash
./dashboard.sh migrate "add new field to products"
```

Apply migrations:
```bash
./dashboard.sh upgrade
```

Rollback migration:
```bash
./dashboard.sh downgrade
```

## Production Deployment

1. Build frontend:
```bash
./dashboard.sh build
```

2. Configure production environment:
```bash
# Update backend/.env
ENV=production
API_WORKERS=4
```

3. Start production server:
```bash
./dashboard.sh start
```

4. Enable auto-start (optional):
```bash
./dashboard.sh autostart
```

5. Serve frontend with nginx (recommended):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/bot-dashboard/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Check credentials in `backend/.env`
- Verify database exists: `sudo -u postgres psql -l`

### Migration Errors
- Check current status: `./dashboard.sh migration-status`
- Review migration files in `backend/alembic/versions/`
- Manually fix database if needed

### Port Already in Use
- Stop existing services: `./dashboard.sh stop`
- Kill any lingering processes: `pkill -f uvicorn`

### Frontend Not Connecting to Backend
- Check VITE_API_URL in `frontend/.env`
- Ensure backend is running: `./dashboard.sh status`
- Check CORS settings in `backend/app/main.py`

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `./dashboard.sh test`
4. Run linters: `./dashboard.sh lint`
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.
