# Quick Fix for API Connection & CORS Errors on VPS

## Problem 1: ERR_CONNECTION_REFUSED
You're seeing: `ERR_CONNECTION_REFUSED` when accessing `http://141.136.42.249:7082/`

The frontend is trying to connect to `localhost:8000` instead of your VPS IP.

## Solution for Connection Refused (2 minutes)

### Step 1: Configure Frontend API URL

Edit `frontend/.env`:
```bash
nano frontend/.env
```

Add this line (replace with YOUR actual VPS IP):
```bash
VITE_API_URL=http://141.136.42.249:8000
```

### Step 2: Configure Backend CORS

Edit `backend/.env`:
```bash
nano backend/.env
```

Add this line (replace with YOUR actual VPS IP):
```bash
CORS_ORIGINS=http://141.136.42.249:7082,http://localhost:7082
```

### Step 3: Rebuild Frontend

```bash
cd frontend
npm install  # If node_modules don't exist
npm run build
```

### Step 4: Restart Backend

```bash
cd ..
./dashboard.sh stop
./dashboard.sh start
```

### Step 5: Restart Frontend Server

If using Python HTTP server:
```bash
cd frontend/dist
python3 -m http.server 7082 --bind 0.0.0.0
```

## Problem 2: CORS Blocked

You're seeing: `Access to XMLHttpRequest has been blocked by CORS policy`

This means the backend doesn't allow requests from your frontend origin.

## Solution for CORS (1 minute)

### Quick Fix - Add Your Frontend URL to CORS Origins

1. Edit `backend/.env`:
```bash
nano backend/.env
```

2. Add or update CORS_ORIGINS:
```bash
CORS_ORIGINS=http://141.136.42.249:7082,http://localhost:7082
```

3. Restart backend:
```bash
./dashboard.sh stop
./dashboard.sh start
```

### Alternative - Allow All (DEV ONLY)

⚠️ **Not recommended for production!**

```bash
# In backend/.env
CORS_ORIGINS=*
```

Then restart backend.

## Verify It Works

1. Open browser: `http://141.136.42.249:7082`
2. Open browser console (F12)
3. Should see API requests going to `http://141.136.42.249:8000` instead of `localhost:8000`
4. Should NOT see CORS errors
5. Dashboard should load data successfully

## Still Having Issues?

### Check Backend is Running
```bash
cd /path/to/bot-dashboard
./dashboard.sh status
```

If backend is not running:
```bash
./dashboard.sh start
```

### Check Firewall
```bash
sudo ufw status
# Should allow port 8000 and 7082
sudo ufw allow 8000/tcp
sudo ufw allow 7082/tcp
```

### Check Backend Logs
```bash
./dashboard.sh logs-backend
```

## Security Warning

⚠️ **No authentication!** Anyone with your IP can access the dashboard.

**Quick security fix (5 minutes):**

See `docs/AUTHENTICATION.md` for Nginx Basic Auth setup.

Or restrict to your IP only:
```bash
sudo ufw delete allow 7082/tcp
sudo ufw delete allow 8000/tcp
sudo ufw allow from YOUR_HOME_IP to any port 7082
sudo ufw allow from YOUR_HOME_IP to any port 8000
```

## Full Guides

- **Deployment**: `docs/VPS_DEPLOYMENT.md`
- **Security**: `docs/AUTHENTICATION.md`
