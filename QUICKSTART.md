# Quick Start Guide

Get up and running with the Telegram Bot Dashboard in minutes!

## 🚀 Installation (5 minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/thertxnetworktwo/bot-dashboard.git
cd bot-dashboard
```

### Step 2: Validate Setup
```bash
./validate.sh
```
This checks if you have all required dependencies.

### Step 3: Install Dependencies
```bash
./dashboard.sh install
```
This installs Python, Node.js, PostgreSQL and all dependencies automatically.

### Step 4: Setup Application
```bash
./dashboard.sh setup
```
This creates the database, runs migrations, and initializes the system.

### Step 5: Configure Environment
```bash
# Edit backend/.env with your settings
nano backend/.env
```
Update at minimum:
- `DB_PASSWORD` - Your PostgreSQL password
- `API_SECRET_KEY` - Generate with: `openssl rand -hex 32`

### Step 6: Start Development Servers
```bash
./dashboard.sh dev
```

## 🎯 Access the Application

Once started, you can access:

- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Using the Dashboard

### Dashboard Page
View analytics and statistics:
- Total products count
- Active/Expired products
- Products expiring soon

### Products Page
Manage your bot products:
- View all products in cards/list
- Create new products
- Edit existing products
- Delete products
- Renew subscriptions
- Search and filter

### Phone Registry Page
Manage phone numbers:
- Check if a phone exists
- Register single number
- Bulk register up to 1000 numbers
- Cleanup old records

## ��️ Common Commands

### Development
```bash
./dashboard.sh dev              # Start both frontend & backend
./dashboard.sh dev-frontend     # Start only frontend
./dashboard.sh dev-backend      # Start only backend
./dashboard.sh stop             # Stop all services
```

### Database
```bash
./dashboard.sh migrate "add new field"  # Create migration
./dashboard.sh upgrade                   # Apply migrations
./dashboard.sh backup                    # Backup database
./dashboard.sh status                    # Check service status
```

### Production
```bash
./dashboard.sh build            # Build frontend
./dashboard.sh start            # Start production
./dashboard.sh autostart        # Enable auto-start
```

### Maintenance
```bash
./dashboard.sh logs             # View logs
./dashboard.sh clean            # Clean build files
./dashboard.sh test             # Run tests
```

## 🎨 Customization

### Add Sample Data
```bash
cd backend
source venv/bin/activate
python seed_data.py
```

### Modify Colors/Theme
Edit `frontend/src/index.css` for custom colors.

### Configure API
Edit `backend/.env` for API settings.

## 🔧 Troubleshooting

### Port Already in Use
```bash
./dashboard.sh stop
# or manually:
sudo lsof -i :8000
kill -9 <PID>
```

### Database Connection Failed
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### Migration Errors
```bash
./dashboard.sh migration-status
./dashboard.sh downgrade
./dashboard.sh upgrade
```

### Frontend Build Errors
```bash
cd frontend
npm install
npm run build
```

## 📖 Next Steps

1. Read the [README.md](README.md) for comprehensive documentation
2. Check [API.md](docs/API.md) for API reference
3. Review [ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand the system
4. See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## 🆘 Getting Help

- Check logs: `./dashboard.sh logs`
- Run validation: `./validate.sh`
- Check status: `./dashboard.sh status`
- View help: `./dashboard.sh help`

## 🎯 Production Deployment

Ready to deploy to production?

1. Update `backend/.env` with production settings
2. Build frontend: `./dashboard.sh build`
3. Start services: `./dashboard.sh start`
4. Enable auto-start: `./dashboard.sh autostart`
5. Setup nginx (see [SETUP.md](docs/SETUP.md))

---

**Need help?** Open an issue on GitHub or check the documentation!
