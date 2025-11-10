#!/bin/bash

# Telegram Bot Dashboard Management Script (Django Version)
# Minimal script with proper Vite process management

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
LOG_DIR="$BACKEND_DIR/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Install dependencies
cmd_install() {
    log_info "Installing dependencies..."
    
    # Install Python dependencies
    cd "$BACKEND_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    
    # Install Node.js dependencies
    cd "$FRONTEND_DIR"
    npm install
    
    log_success "Installation completed!"
}

# Setup database
cmd_setup() {
    log_info "Setting up database..."
    
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
    
    # Run Django migrations
    cd "$BACKEND_DIR"
    source venv/bin/activate
    python manage.py migrate
    deactivate
    
    log_success "Setup completed!"
}

# Start development servers
cmd_dev() {
    log_info "Starting development servers..."
    
    # Stop any existing servers
    cmd_stop
    
    mkdir -p "$LOG_DIR"
    
    # Start Django backend
    cd "$BACKEND_DIR"
    source venv/bin/activate
    nohup python manage.py runserver 0.0.0.0:8000 > "$LOG_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$LOG_DIR/backend.pid"
    deactivate
    
    # Start Vite frontend in its own process group
    cd "$FRONTEND_DIR"
    # Use setsid to create new session and process group for proper cleanup
    setsid npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$LOG_DIR/frontend.pid"
    
    sleep 2
    
    log_success "Development servers started!"
    log_info "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
    log_info "Frontend: http://localhost:7082 (PID: $FRONTEND_PID)"
    log_info "Admin: http://localhost:8000/admin"
    log_info ""
    log_info "Logs: $LOG_DIR"
    log_info "Stop: ./dashboard.sh stop"
}

# Build production assets
cmd_build() {
    log_info "Building production assets..."
    
    cd "$FRONTEND_DIR"
    npm run build
    
    log_success "Build completed! Assets are in $FRONTEND_DIR/dist"
}

# Start production server
cmd_start() {
    log_info "Starting production server..."
    
    cmd_stop
    
    mkdir -p "$LOG_DIR"
    
    # Collect static files
    cd "$BACKEND_DIR"
    source venv/bin/activate
    python manage.py collectstatic --noinput
    
    # Start Django with gunicorn (install if needed)
    if ! command -v gunicorn &> /dev/null; then
        log_info "Installing gunicorn..."
        pip install gunicorn
    fi
    
    nohup gunicorn dashboard.wsgi:application --bind 0.0.0.0:8000 --workers 4 > "$LOG_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$LOG_DIR/backend.pid"
    deactivate
    
    sleep 2
    
    log_success "Production server started!"
    log_info "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
    log_info "Serve frontend from: $FRONTEND_DIR/dist with nginx"
}

# Stop all servers
cmd_stop() {
    log_info "Stopping servers..."
    
    STOPPED=0
    
    # Stop backend
    if [ -f "$LOG_DIR/backend.pid" ]; then
        BACKEND_PID=$(cat "$LOG_DIR/backend.pid")
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill $BACKEND_PID 2>/dev/null || true
            sleep 1
            kill -9 $BACKEND_PID 2>/dev/null || true
            log_success "Backend stopped (PID: $BACKEND_PID)"
            STOPPED=1
        fi
        rm -f "$LOG_DIR/backend.pid"
    fi
    
    # Stop frontend - kill entire process group for proper Vite cleanup
    if [ -f "$LOG_DIR/frontend.pid" ]; then
        FRONTEND_PID=$(cat "$LOG_DIR/frontend.pid")
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            # Kill the entire process group (negative PID)
            kill -- -$FRONTEND_PID 2>/dev/null || kill $FRONTEND_PID 2>/dev/null || true
            sleep 1
            # Force kill if still running
            kill -9 -- -$FRONTEND_PID 2>/dev/null || kill -9 $FRONTEND_PID 2>/dev/null || true
            log_success "Frontend stopped (PID: $FRONTEND_PID)"
            STOPPED=1
        fi
        rm -f "$LOG_DIR/frontend.pid"
    fi
    
    # Cleanup any lingering processes
    pkill -f "manage.py runserver" 2>/dev/null && STOPPED=1 || true
    pkill -f "gunicorn dashboard.wsgi" 2>/dev/null && STOPPED=1 || true
    pkill -f "vite.*--port.*7082" 2>/dev/null && STOPPED=1 || true
    pkill -f "npm.*run.*dev" 2>/dev/null && STOPPED=1 || true
    
    if [ $STOPPED -eq 1 ]; then
        log_success "All servers stopped!"
    else
        log_info "No running servers found"
    fi
}

# Restart servers
cmd_restart() {
    cmd_stop
    sleep 2
    cmd_start
}

# View logs
cmd_logs() {
    log_info "Viewing logs (Ctrl+C to exit)..."
    tail -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log" 2>/dev/null || log_warning "No logs found"
}

# Check status
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
}

# Database migrations
cmd_migrate() {
    log_info "Creating new migration..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    python manage.py makemigrations
    python manage.py migrate
    deactivate
    log_success "Migrations completed!"
}

# Run tests
cmd_test() {
    log_info "Running tests..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    pytest tests/ -v
    deactivate
    log_success "Tests completed!"
}

# Clean build artifacts
cmd_clean() {
    log_info "Cleaning build artifacts..."
    
    # Clean Python cache
    find "$BACKEND_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$BACKEND_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Clean frontend build
    rm -rf "$FRONTEND_DIR/dist"
    rm -rf "$FRONTEND_DIR/node_modules/.vite"
    
    # Clean logs
    rm -f "$LOG_DIR"/*.log
    
    log_success "Cleaned build artifacts!"
}

# Help message
cmd_help() {
    cat <<EOF
Telegram Bot Dashboard - Management Script (Django)

Usage: ./dashboard.sh [command]

Commands:
  install     Install all dependencies
  setup       Initialize database and run migrations
  migrate     Create and apply database migrations
  dev         Start development servers (Django + Vite)
  build       Build production frontend assets
  start       Start production server
  stop        Stop all running services
  restart     Restart all services
  logs        View application logs (tail -f)
  status      Check status of all services
  test        Run tests
  clean       Clean build artifacts and cache
  help        Show this help message

Examples:
  ./dashboard.sh install
  ./dashboard.sh setup
  ./dashboard.sh dev
  ./dashboard.sh stop

For more information, see the README.md file.
EOF
}

# Command dispatcher
case "$1" in
    install) cmd_install ;;
    setup) cmd_setup ;;
    migrate) cmd_migrate ;;
    dev) cmd_dev ;;
    build) cmd_build ;;
    start) cmd_start ;;
    stop) cmd_stop ;;
    restart) cmd_restart ;;
    logs) cmd_logs ;;
    status) cmd_status ;;
    test) cmd_test ;;
    clean) cmd_clean ;;
    help|--help|-h|"") cmd_help ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        cmd_help
        exit 1
        ;;
esac
