# Setup Guide

## System Requirements

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- 2GB RAM minimum
- 10GB disk space

## Detailed Installation Steps

### 1. Install System Dependencies

#### Ubuntu/Debian
```bash
# Update package list
sudo apt-get update

# Install Python
sudo apt-get install -y python3 python3-pip python3-venv

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Install Git
sudo apt-get install -y git
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.10 node postgresql git
brew services start postgresql
```

### 2. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd bot-dashboard

# Run installation script
./dashboard.sh install
```

### 3. Database Setup

The setup script will automatically create the database, but if you need to do it manually:

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE USER dashboard_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE dashboard_db OWNER dashboard_user;
GRANT ALL PRIVILEGES ON DATABASE dashboard_db TO dashboard_user;
\q
```

### 4. Configuration

Edit `backend/.env`:
```bash
nano backend/.env
```

Update these critical settings:
- `DATABASE_URL` - Your PostgreSQL connection string
- `API_SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `PHONE_REGISTRY_URL` - External phone registry API URL
- `PHONE_REGISTRY_API_KEY` - Your API key

### 5. Initialize Database

```bash
./dashboard.sh setup
```

This will:
- Create necessary tables
- Run initial migrations
- Set up logging directories

### 6. Development Mode

```bash
./dashboard.sh dev
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 7. Production Deployment

1. Build frontend:
```bash
./dashboard.sh build
```

2. Update environment to production:
```bash
# In backend/.env
ENV=production
```

3. Start production server:
```bash
./dashboard.sh start
```

4. Setup nginx (recommended):
```bash
sudo apt-get install nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/bot-dashboard
```

Add:
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
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/bot-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

5. Enable auto-start:
```bash
./dashboard.sh autostart
```

## Verification

Test the installation:

```bash
# Check status
./dashboard.sh status

# Run tests
./dashboard.sh test

# View logs
./dashboard.sh logs
```

## Troubleshooting

### PostgreSQL Connection Failed

1. Check PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

2. Test connection:
```bash
psql -U dashboard_user -d dashboard_db -h localhost
```

3. Check pg_hba.conf for local connections

### Port Already in Use

```bash
# Find and kill process
sudo lsof -i :8000
sudo kill -9 <PID>

# Or use the stop command
./dashboard.sh stop
```

### Migration Errors

```bash
# Check migration status
./dashboard.sh migration-status

# If stuck, manually fix in PostgreSQL:
sudo -u postgres psql dashboard_db
# Then run:
DELETE FROM alembic_version;
# Exit and try again:
./dashboard.sh upgrade
```

## Security Checklist

- [ ] Change default database password
- [ ] Generate strong API_SECRET_KEY
- [ ] Configure firewall (ufw/iptables)
- [ ] Enable SSL/TLS with Let's Encrypt
- [ ] Set up regular backups
- [ ] Configure fail2ban
- [ ] Restrict database access
- [ ] Use environment variables for secrets
