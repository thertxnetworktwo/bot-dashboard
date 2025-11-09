#!/bin/bash

# Telegram Bot Dashboard Management Script
# This script handles all deployment and management operations

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
LOG_DIR="$BACKEND_DIR/logs"
BACKUP_DIR="$PROJECT_DIR/backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        return 1
    fi
    return 0
}

# Command functions
cmd_install() {
    log_info "Installing system dependencies..."
    
    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Update package list
        sudo apt-get update
        
        # Install Python 3.10+
        if ! check_command python3; then
            log_info "Installing Python 3..."
            sudo apt-get install -y python3 python3-pip python3-venv
        fi
        
        # Install Node.js 18+
        if ! check_command node; then
            log_info "Installing Node.js..."
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
        
        # Install PostgreSQL 14+
        if ! check_command psql; then
            log_info "Installing PostgreSQL..."
            sudo apt-get install -y postgresql postgresql-contrib
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
        fi
        
        # Install Git
        if ! check_command git; then
            log_info "Installing Git..."
            sudo apt-get install -y git
        fi
    else
        log_warning "Auto-install only supported on Linux. Please install dependencies manually:"
        log_info "- Python 3.10+"
        log_info "- Node.js 18+"
        log_info "- PostgreSQL 14+"
        log_info "- Git"
        exit 1
    fi
    
    # Install Python dependencies
    log_info "Installing Python dependencies..."
    cd "$BACKEND_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    
    # Install Node.js dependencies
    log_info "Installing Node.js dependencies..."
    cd "$FRONTEND_DIR"
    npm install
    
    log_success "Installation completed!"
}

cmd_setup() {
    log_info "Setting up the application..."
    
    # Create .env file if it doesn't exist
    if [ ! -f "$BACKEND_DIR/.env" ]; then
        log_info "Creating .env file..."
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        log_warning "Please update $BACKEND_DIR/.env with your configuration"
    fi
    
    if [ ! -f "$FRONTEND_DIR/.env" ]; then
        log_info "Creating frontend .env file..."
        cp "$FRONTEND_DIR/.env.example" "$FRONTEND_DIR/.env"
    fi
    
    # Create logs directory
    mkdir -p "$LOG_DIR"
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    
    # Setup PostgreSQL database
    log_info "Setting up PostgreSQL database..."
    
    # Load environment variables
    if [ -f "$BACKEND_DIR/.env" ]; then
        export $(cat "$BACKEND_DIR/.env" | grep -v '^#' | xargs)
    fi
    
    DB_USER="${DB_USER:-dashboard_user}"
    DB_PASSWORD="${DB_PASSWORD:-your_secure_password}"
    DB_NAME="${DB_NAME:-dashboard_db}"
    
    # Create user if it doesn't exist
    sudo -u postgres psql <<EOF
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;
EOF
    
    # Create database if it doesn't exist
    sudo -u postgres psql <<EOF
SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec
EOF
    
    # Grant all necessary privileges
    sudo -u postgres psql <<EOF
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
EOF
    
    # Run initial migrations
    log_info "Running database migrations..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    alembic upgrade head || log_warning "No migrations to apply or migration failed"
    deactivate
    
    log_success "Setup completed!"
}

cmd_migrate() {
    if [ -z "$1" ]; then
        log_error "Please provide a migration description"
        echo "Usage: ./dashboard.sh migrate \"description of changes\""
        exit 1
    fi
    
    log_info "Creating new migration: $1"
    cd "$BACKEND_DIR"
    source venv/bin/activate
    alembic revision --autogenerate -m "$1"
    deactivate
    log_success "Migration created!"
}

cmd_upgrade() {
    log_info "Applying pending migrations..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    alembic upgrade head
    deactivate
    log_success "Migrations applied!"
}

cmd_downgrade() {
    log_warning "Rolling back last migration..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    alembic downgrade -1
    deactivate
    log_success "Migration rolled back!"
}

cmd_migration_status() {
    log_info "Migration status:"
    cd "$BACKEND_DIR"
    source venv/bin/activate
    echo ""
    echo "Current version:"
    alembic current
    echo ""
    echo "Migration history:"
    alembic history
    deactivate
}

cmd_dev() {
    log_info "Starting development servers..."
    
    # Create logs directory
    mkdir -p "$LOG_DIR"
    
    # Start backend
    cd "$BACKEND_DIR"
    source venv/bin/activate
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > "$LOG_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$LOG_DIR/backend.pid"
    deactivate
    
    # Start frontend
    cd "$FRONTEND_DIR"
    npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$LOG_DIR/frontend.pid"
    
    log_success "Development servers started!"
    log_info "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
    log_info "Frontend: http://localhost:5173 (PID: $FRONTEND_PID)"
    log_info "API Docs: http://localhost:8000/docs"
    log_info ""
    log_info "Logs are being written to $LOG_DIR"
    log_info "Use './dashboard.sh logs' to view logs"
    log_info "Use './dashboard.sh stop' to stop servers"
}

cmd_dev_frontend() {
    log_info "Starting frontend development server..."
    cd "$FRONTEND_DIR"
    npm run dev
}

cmd_dev_backend() {
    log_info "Starting backend development server..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    deactivate
}

cmd_build() {
    log_info "Building production assets..."
    
    # Build frontend
    cd "$FRONTEND_DIR"
    npm run build
    
    log_success "Build completed! Assets are in $FRONTEND_DIR/dist"
}

cmd_start() {
    log_info "Starting production servers..."
    
    mkdir -p "$LOG_DIR"
    
    # Load environment variables
    if [ -f "$BACKEND_DIR/.env" ]; then
        export $(cat "$BACKEND_DIR/.env" | grep -v '^#' | xargs)
    fi
    
    API_HOST="${API_HOST:-0.0.0.0}"
    API_PORT="${API_PORT:-8000}"
    API_WORKERS="${API_WORKERS:-4}"
    
    # Start backend with production settings
    cd "$BACKEND_DIR"
    source venv/bin/activate
    uvicorn app.main:app --host $API_HOST --port $API_PORT --workers $API_WORKERS > "$LOG_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$LOG_DIR/backend.pid"
    deactivate
    
    log_success "Production server started!"
    log_info "Backend: http://$API_HOST:$API_PORT (PID: $BACKEND_PID)"
    log_info "Serve frontend from: $FRONTEND_DIR/dist"
}

cmd_stop() {
    log_info "Stopping servers..."
    
    # Stop backend
    if [ -f "$LOG_DIR/backend.pid" ]; then
        BACKEND_PID=$(cat "$LOG_DIR/backend.pid")
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill $BACKEND_PID
            rm "$LOG_DIR/backend.pid"
            log_success "Backend stopped (PID: $BACKEND_PID)"
        fi
    fi
    
    # Stop frontend
    if [ -f "$LOG_DIR/frontend.pid" ]; then
        FRONTEND_PID=$(cat "$LOG_DIR/frontend.pid")
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill $FRONTEND_PID
            rm "$LOG_DIR/frontend.pid"
            log_success "Frontend stopped (PID: $FRONTEND_PID)"
        fi
    fi
    
    # Kill any remaining uvicorn processes
    pkill -f "uvicorn app.main:app" 2>/dev/null || true
    
    log_success "All servers stopped!"
}

cmd_restart() {
    cmd_stop
    sleep 2
    cmd_start
}

cmd_autostart() {
    log_info "Configuring systemd service for auto-start..."
    
    SERVICE_FILE="/etc/systemd/system/telegram-dashboard.service"
    CURRENT_USER=$(whoami)
    
    sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Telegram Bot Dashboard
After=network.target postgresql.service

[Service]
Type=forking
User=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/dashboard.sh start
ExecStop=$PROJECT_DIR/dashboard.sh stop
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable telegram-dashboard.service
    
    log_success "Systemd service configured!"
    log_info "Use 'sudo systemctl start telegram-dashboard' to start"
    log_info "Use 'sudo systemctl status telegram-dashboard' to check status"
}

cmd_disable_autostart() {
    log_info "Disabling auto-start..."
    
    sudo systemctl disable telegram-dashboard.service || true
    sudo systemctl stop telegram-dashboard.service || true
    
    log_success "Auto-start disabled!"
}

cmd_logs() {
    log_info "Viewing logs (Ctrl+C to exit)..."
    tail -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log" 2>/dev/null || log_warning "No logs found"
}

cmd_logs_backend() {
    log_info "Viewing backend logs (Ctrl+C to exit)..."
    tail -f "$LOG_DIR/backend.log" 2>/dev/null || log_warning "No backend logs found"
}

cmd_logs_frontend() {
    log_info "Viewing frontend logs (Ctrl+C to exit)..."
    tail -f "$LOG_DIR/frontend.log" 2>/dev/null || log_warning "No frontend logs found"
}

cmd_backup() {
    log_info "Backing up database..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Load environment variables
    if [ -f "$BACKEND_DIR/.env" ]; then
        export $(cat "$BACKEND_DIR/.env" | grep -v '^#' | xargs)
    fi
    
    DB_NAME="${DB_NAME:-dashboard_db}"
    BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
    
    sudo -u postgres pg_dump $DB_NAME > "$BACKUP_FILE"
    
    log_success "Database backed up to $BACKUP_FILE"
}

cmd_restore() {
    if [ -z "$1" ]; then
        log_error "Please provide a backup file"
        echo "Available backups:"
        ls -lh "$BACKUP_DIR"/*.sql 2>/dev/null || echo "No backups found"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        log_error "Backup file not found: $1"
        exit 1
    fi
    
    log_warning "Restoring database from $1"
    read -p "This will overwrite the current database. Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Restore cancelled"
        exit 0
    fi
    
    # Load environment variables
    if [ -f "$BACKEND_DIR/.env" ]; then
        export $(cat "$BACKEND_DIR/.env" | grep -v '^#' | xargs)
    fi
    
    DB_NAME="${DB_NAME:-dashboard_db}"
    
    sudo -u postgres psql $DB_NAME < "$1"
    
    log_success "Database restored from $1"
}

cmd_clean() {
    log_info "Cleaning build artifacts and cache..."
    
    # Clean Python cache
    find "$BACKEND_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$BACKEND_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Clean frontend build
    rm -rf "$FRONTEND_DIR/dist"
    rm -rf "$FRONTEND_DIR/node_modules/.vite"
    
    # Clean logs
    rm -f "$LOG_DIR"/*.log
    
    log_success "Cleaned build artifacts and cache!"
}

cmd_status() {
    log_info "Checking service status..."
    echo ""
    
    # Check backend
    if [ -f "$LOG_DIR/backend.pid" ]; then
        BACKEND_PID=$(cat "$LOG_DIR/backend.pid")
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            log_success "Backend is running (PID: $BACKEND_PID)"
        else
            log_warning "Backend PID file exists but process is not running"
        fi
    else
        log_warning "Backend is not running"
    fi
    
    # Check frontend
    if [ -f "$LOG_DIR/frontend.pid" ]; then
        FRONTEND_PID=$(cat "$LOG_DIR/frontend.pid")
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            log_success "Frontend is running (PID: $FRONTEND_PID)"
        else
            log_warning "Frontend PID file exists but process is not running"
        fi
    else
        log_warning "Frontend is not running"
    fi
    
    echo ""
    
    # Check PostgreSQL
    if sudo systemctl is-active --quiet postgresql; then
        log_success "PostgreSQL is running"
    else
        log_warning "PostgreSQL is not running"
    fi
}

cmd_test() {
    log_info "Running tests..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    pytest tests/ -v
    deactivate
    
    log_success "Tests completed!"
}

cmd_lint() {
    log_info "Running linters..."
    
    # Lint backend (if tools are available)
    if check_command black; then
        log_info "Running black on backend..."
        cd "$BACKEND_DIR"
        source venv/bin/activate
        black app/ --check || true
        deactivate
    fi
    
    # Lint frontend
    log_info "Running eslint on frontend..."
    cd "$FRONTEND_DIR"
    npm run lint || true
    
    log_success "Linting completed!"
}

cmd_help() {
    cat <<EOF
Telegram Bot Dashboard - Management Script

Usage: ./dashboard.sh [command]

Commands:
  install              Install all dependencies (Python, Node.js, PostgreSQL)
  setup                Initialize database, create tables, run initial migrations
  migrate <message>    Create new database migration
  upgrade              Apply pending migrations to database
  downgrade            Rollback last migration
  migration-status     Show current migration status
  dev                  Start development servers (frontend + backend)
  dev-frontend         Start only frontend dev server
  dev-backend          Start only backend dev server
  build                Build production assets
  start                Start production servers
  stop                 Stop all running services
  restart              Restart all services
  autostart            Configure systemd service for auto-start on boot
  disable-autostart    Disable systemd auto-start
  logs                 View application logs (tail -f)
  logs-backend         View only backend logs
  logs-frontend        View only frontend logs
  backup               Backup PostgreSQL database
  restore <file>       Restore database from backup
  clean                Clean build artifacts and cache
  status               Check status of all services
  test                 Run all tests
  lint                 Run linters and formatters
  help                 Show this help message

Examples:
  ./dashboard.sh install
  ./dashboard.sh setup
  ./dashboard.sh migrate "add user table"
  ./dashboard.sh dev
  ./dashboard.sh backup
  ./dashboard.sh restore backups/backup_20231109_120000.sql

For more information, see the README.md file.
EOF
}

# Main command dispatcher
case "$1" in
    install)
        cmd_install
        ;;
    setup)
        cmd_setup
        ;;
    migrate)
        cmd_migrate "$2"
        ;;
    upgrade)
        cmd_upgrade
        ;;
    downgrade)
        cmd_downgrade
        ;;
    migration-status)
        cmd_migration_status
        ;;
    dev)
        cmd_dev
        ;;
    dev-frontend)
        cmd_dev_frontend
        ;;
    dev-backend)
        cmd_dev_backend
        ;;
    build)
        cmd_build
        ;;
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_restart
        ;;
    autostart)
        cmd_autostart
        ;;
    disable-autostart)
        cmd_disable_autostart
        ;;
    logs)
        cmd_logs
        ;;
    logs-backend)
        cmd_logs_backend
        ;;
    logs-frontend)
        cmd_logs_frontend
        ;;
    backup)
        cmd_backup
        ;;
    restore)
        cmd_restore "$2"
        ;;
    clean)
        cmd_clean
        ;;
    status)
        cmd_status
        ;;
    test)
        cmd_test
        ;;
    lint)
        cmd_lint
        ;;
    help|--help|-h|"")
        cmd_help
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        cmd_help
        exit 1
        ;;
esac
