# VPS Deployment Guide

## Production Deployment on VPS

This guide explains how to deploy the Telegram Bot Dashboard on a VPS server.

### Prerequisites
- VPS with Ubuntu/Debian
- Root or sudo access
- Domain name (optional, but recommended)

### Step 1: Environment Configuration

1. **Backend Configuration** (`backend/.env`):
```bash
# Database
DATABASE_URL=postgresql+asyncpg://dashboard_user:your_password@localhost:5432/dashboard_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dashboard_db
DB_USER=dashboard_user
DB_PASSWORD=your_secure_password

# API Configuration
API_SECRET_KEY=your-secret-key-min-32-chars-change-in-production
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Environment
ENV=production
```

2. **Frontend Configuration** (`frontend/.env`):

For VPS deployment, you need to set the backend API URL:

```bash
# Set this to your VPS IP and backend port
VITE_API_URL=http://YOUR_VPS_IP:8000

# Example:
# VITE_API_URL=http://141.136.42.249:8000
```

**Important**: Replace `YOUR_VPS_IP` with your actual VPS IP address.

### Step 2: Build and Deploy

1. Install dependencies:
```bash
./dashboard.sh install
```

2. Setup database:
```bash
./dashboard.sh setup
```

3. Build frontend for production:
```bash
./dashboard.sh build
```

This creates optimized production files in `frontend/dist/`

### Step 3: Serve the Application

#### Option A: Using the Dashboard Script (Simple)

Start the backend:
```bash
./dashboard.sh start
```

Serve the frontend using a simple HTTP server:
```bash
cd frontend/dist
python3 -m http.server 7082 --bind 0.0.0.0
```

#### Option B: Using Nginx (Recommended)

1. Install Nginx:
```bash
sudo apt install nginx
```

2. Create Nginx configuration (`/etc/nginx/sites-available/bot-dashboard`):
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your VPS IP

    # Frontend
    location / {
        root /path/to/bot-dashboard/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Backend health check
    location /health {
        proxy_pass http://localhost:8000/health;
    }

    # API docs
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }
}
```

3. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/bot-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

4. Update frontend `.env` for Nginx setup:
```bash
# Leave empty to use relative URLs (Nginx will proxy)
VITE_API_URL=
```

5. Rebuild frontend:
```bash
cd frontend
npm run build
```

### Step 4: Configure Firewall

Allow necessary ports:
```bash
sudo ufw allow 80/tcp    # HTTP (if using Nginx)
sudo ufw allow 8000/tcp  # Backend API (if direct access)
sudo ufw allow 7082/tcp  # Frontend (if not using Nginx)
sudo ufw enable
```

### Step 5: Enable Auto-Start (Optional)

```bash
./dashboard.sh autostart
```

This creates a systemd service that starts the backend automatically on boot.

For the frontend, add to the systemd service or use PM2:
```bash
# Install PM2
sudo npm install -g pm2

# Start frontend server (if not using Nginx)
cd frontend/dist
pm2 start "python3 -m http.server 7082 --bind 0.0.0.0" --name bot-dashboard-frontend
pm2 save
pm2 startup
```

### Access URLs

#### Without Nginx (Direct Access)
- Frontend: `http://YOUR_VPS_IP:7082`
- Backend API: `http://YOUR_VPS_IP:8000`
- API Docs: `http://YOUR_VPS_IP:8000/docs`

#### With Nginx
- Frontend: `http://YOUR_VPS_IP` or `http://your-domain.com`
- Backend API: `http://YOUR_VPS_IP/api/` or `http://your-domain.com/api/`
- API Docs: `http://YOUR_VPS_IP/docs` or `http://your-domain.com/docs`

### Troubleshooting

#### Connection Refused Errors

If you see `ERR_CONNECTION_REFUSED` for API calls:

1. Check if backend is running:
```bash
./dashboard.sh status
```

2. Verify the `VITE_API_URL` in `frontend/.env` matches your deployment:
   - For direct access: `VITE_API_URL=http://YOUR_VPS_IP:8000`
   - For Nginx: `VITE_API_URL=` (empty)

3. Rebuild the frontend after changing `.env`:
```bash
cd frontend
npm run build
```

#### CORS Issues

If you get CORS errors, update `backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Security Recommendations

1. **Use HTTPS**: Set up SSL/TLS with Let's Encrypt
2. **Add Authentication**: Implement user authentication (see Authentication section)
3. **Firewall**: Only open necessary ports
4. **Environment Variables**: Never commit `.env` files
5. **Database Security**: Use strong passwords, restrict database access

### Monitoring

Check logs:
```bash
./dashboard.sh logs          # View all logs
./dashboard.sh logs-backend  # Backend only
./dashboard.sh logs-frontend # Frontend only
```

Check service status:
```bash
./dashboard.sh status
```

### Backup and Restore

Backup database:
```bash
./dashboard.sh backup
```

Restore from backup:
```bash
./dashboard.sh restore backups/backup_YYYYMMDD_HHMMSS.sql
```
