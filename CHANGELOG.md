# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-09

### Added
- Initial release of Telegram Bot Dashboard
- Full-stack application with React frontend and FastAPI backend
- Product management system with CRUD operations
- Dashboard analytics and statistics
- Phone registry API integration
- Database migrations with Alembic
- Comprehensive `dashboard.sh` management script
- Complete documentation (README, API docs, Setup guide, Architecture)
- Production-ready deployment configuration
- Systemd service configuration for auto-start
- Database backup and restore functionality
- Development and production modes
- PostgreSQL database with proper indexing
- Async/await throughout backend
- React Query for frontend data management
- Tailwind CSS + shadcn/ui components
- Responsive design for mobile devices

### Features
- **Products Management**
  - Create, read, update, delete products
  - Auto-calculated expiration dates
  - Status indicators (Active, Expired, Expiring Soon)
  - Product renewal functionality
  - Search and filtering
  - Pagination

- **Dashboard**
  - Total products count
  - Active vs Expired products metrics
  - Products expiring in 7/30 days
  - Visual statistics cards

- **Phone Registry**
  - Check phone number existence
  - Register single phone numbers
  - Bulk register up to 1000 numbers
  - Cleanup old records

- **Database Migrations**
  - Create new migrations
  - Apply pending migrations
  - Rollback migrations
  - Migration status checking

- **Management Script**
  - One-command installation
  - Database setup automation
  - Development server management
  - Production deployment
  - Auto-start configuration
  - Log viewing
  - Backup/restore
  - Clean build artifacts
  - Service status checking
  - Testing and linting

### Documentation
- Comprehensive README with quick start guide
- Detailed API documentation
- Step-by-step setup guide
- Architecture documentation
- Contributing guidelines
- Code examples and best practices

### Technical Stack
- Frontend: React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui
- Backend: FastAPI, SQLAlchemy 2.0, Alembic, asyncpg
- Database: PostgreSQL 14+
- Tools: React Query, React Hook Form, Zod, Axios

[1.0.0]: https://github.com/thertxnetworktwo/bot-dashboard/releases/tag/v1.0.0
