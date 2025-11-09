#!/bin/bash

# Validation Script - Checks if the project is properly set up
# Run this to verify your installation

echo "🔍 Validating Telegram Bot Dashboard Setup..."
echo ""

ERRORS=0
WARNINGS=0

# Check if we're in the project root
if [ ! -f "dashboard.sh" ]; then
    echo "❌ Error: Not in project root directory"
    exit 1
fi

# Check backend structure
echo "📦 Checking Backend..."
if [ -d "backend/app" ]; then
    echo "  ✅ Backend directory exists"
else
    echo "  ❌ Backend directory missing"
    ERRORS=$((ERRORS+1))
fi

if [ -f "backend/requirements.txt" ]; then
    echo "  ✅ requirements.txt exists"
else
    echo "  ❌ requirements.txt missing"
    ERRORS=$((ERRORS+1))
fi

if [ -f "backend/alembic.ini" ]; then
    echo "  ✅ Alembic configured"
else
    echo "  ❌ Alembic not configured"
    ERRORS=$((ERRORS+1))
fi

# Check frontend structure
echo ""
echo "🎨 Checking Frontend..."
if [ -d "frontend/src" ]; then
    echo "  ✅ Frontend directory exists"
else
    echo "  ❌ Frontend directory missing"
    ERRORS=$((ERRORS+1))
fi

if [ -f "frontend/package.json" ]; then
    echo "  ✅ package.json exists"
else
    echo "  ❌ package.json missing"
    ERRORS=$((ERRORS+1))
fi

if [ -f "frontend/vite.config.ts" ]; then
    echo "  ✅ Vite configured"
else
    echo "  ❌ Vite not configured"
    ERRORS=$((ERRORS+1))
fi

# Check documentation
echo ""
echo "📚 Checking Documentation..."
if [ -f "README.md" ]; then
    echo "  ✅ README.md exists"
else
    echo "  ❌ README.md missing"
    ERRORS=$((ERRORS+1))
fi

if [ -f "docs/API.md" ]; then
    echo "  ✅ API documentation exists"
else
    echo "  ⚠️  API documentation missing"
    WARNINGS=$((WARNINGS+1))
fi

# Check configuration files
echo ""
echo "⚙️  Checking Configuration..."
if [ -f "backend/.env.example" ]; then
    echo "  ✅ Backend .env.example exists"
else
    echo "  ❌ Backend .env.example missing"
    ERRORS=$((ERRORS+1))
fi

if [ -f "backend/.env" ]; then
    echo "  ✅ Backend .env configured"
else
    echo "  ⚠️  Backend .env not configured (run ./dashboard.sh setup)"
    WARNINGS=$((WARNINGS+1))
fi

if [ -f "frontend/.env.example" ]; then
    echo "  ✅ Frontend .env.example exists"
else
    echo "  ❌ Frontend .env.example missing"
    ERRORS=$((ERRORS+1))
fi

# Check Python environment
echo ""
echo "🐍 Checking Python Environment..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "  ✅ Python installed (version $PYTHON_VERSION)"
else
    echo "  ❌ Python not installed"
    ERRORS=$((ERRORS+1))
fi

if [ -d "backend/venv" ]; then
    echo "  ✅ Virtual environment exists"
else
    echo "  ⚠️  Virtual environment not created (run ./dashboard.sh install)"
    WARNINGS=$((WARNINGS+1))
fi

# Check Node.js
echo ""
echo "📦 Checking Node.js Environment..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "  ✅ Node.js installed (version $NODE_VERSION)"
else
    echo "  ❌ Node.js not installed"
    ERRORS=$((ERRORS+1))
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "  ✅ npm installed (version $NPM_VERSION)"
else
    echo "  ❌ npm not installed"
    ERRORS=$((ERRORS+1))
fi

if [ -d "frontend/node_modules" ]; then
    echo "  ✅ Node modules installed"
else
    echo "  ⚠️  Node modules not installed (run ./dashboard.sh install)"
    WARNINGS=$((WARNINGS+1))
fi

# Check PostgreSQL
echo ""
echo "🐘 Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "  ✅ PostgreSQL client installed"
else
    echo "  ⚠️  PostgreSQL client not found"
    WARNINGS=$((WARNINGS+1))
fi

if sudo systemctl is-active --quiet postgresql 2>/dev/null; then
    echo "  ✅ PostgreSQL service is running"
else
    echo "  ⚠️  PostgreSQL service not running or not accessible"
    WARNINGS=$((WARNINGS+1))
fi

# Check dashboard.sh
echo ""
echo "🔧 Checking Management Script..."
if [ -x "dashboard.sh" ]; then
    echo "  ✅ dashboard.sh is executable"
else
    echo "  ❌ dashboard.sh is not executable (run: chmod +x dashboard.sh)"
    ERRORS=$((ERRORS+1))
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ All checks passed! Your setup is complete."
    echo ""
    echo "Next steps:"
    echo "  1. Configure backend/.env with your settings"
    echo "  2. Run: ./dashboard.sh setup"
    echo "  3. Run: ./dashboard.sh dev"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  Setup is mostly complete with $WARNINGS warning(s)"
    echo ""
    echo "You can proceed but should address the warnings above."
    exit 0
else
    echo "❌ Setup incomplete: $ERRORS error(s), $WARNINGS warning(s)"
    echo ""
    echo "Please fix the errors above before proceeding."
    echo "Run './dashboard.sh install' to install dependencies."
    exit 1
fi
