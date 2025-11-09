# Authentication & Security

## Current Status

⚠️ **Important**: The current version of the dashboard does NOT have built-in authentication. This means anyone who can access the URL can view and modify data.

## Recommended Authentication Solutions

### Option 1: Basic HTTP Authentication (Quick & Simple)

Use Nginx basic auth to protect the entire dashboard:

1. Install apache2-utils:
```bash
sudo apt install apache2-utils
```

2. Create password file:
```bash
sudo htpasswd -c /etc/nginx/.htpasswd admin
# Enter password when prompted
```

3. Update Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Basic authentication
    auth_basic "Bot Dashboard";
    auth_basic_user_file /etc/nginx/.htpasswd;

    # ... rest of your configuration
}
```

4. Reload Nginx:
```bash
sudo systemctl reload nginx
```

### Option 2: OAuth2 Proxy (Google/GitHub Authentication)

Use OAuth2 Proxy to add authentication via Google, GitHub, or other providers:

1. Install OAuth2 Proxy:
```bash
wget https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.5.0/oauth2-proxy-v7.5.0.linux-amd64.tar.gz
tar -xzf oauth2-proxy-v7.5.0.linux-amd64.tar.gz
sudo mv oauth2-proxy-v7.5.0.linux-amd64/oauth2-proxy /usr/local/bin/
```

2. Configure OAuth2 Proxy for your provider (Google, GitHub, etc.)
3. Update Nginx to proxy through OAuth2

See: https://oauth2-proxy.github.io/oauth2-proxy/

### Option 3: IP Whitelisting (VPN/Office Network)

Restrict access to specific IP addresses in Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Allow specific IPs only
    allow 192.168.1.0/24;  # Your office network
    allow 1.2.3.4;         # Specific IP
    deny all;

    # ... rest of configuration
}
```

### Option 4: VPN Access Only

1. Set up a VPN (OpenVPN, WireGuard)
2. Configure firewall to only allow access from VPN:
```bash
sudo ufw deny 80/tcp
sudo ufw deny 8000/tcp
sudo ufw deny 7082/tcp
# Allow VPN interface
sudo ufw allow in on tun0
```

### Option 5: Custom Authentication (Development Required)

To add custom authentication to the application itself, you'll need to:

1. **Backend**: Add FastAPI authentication
   - JWT tokens
   - Session-based auth
   - API keys

2. **Frontend**: Add login page
   - Login form
   - Protected routes
   - Token storage

**Example FastAPI Authentication Setup:**

```python
# backend/app/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "your-password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# backend/app/main.py - Add to routes
from app.core.auth import get_current_user

@app.get("/api/products")
async def get_products(current_user: str = Depends(get_current_user)):
    # Protected route
    pass
```

## Interim Security Measures

Until you implement proper authentication:

1. **Use Firewall**: Only allow access from trusted IPs
```bash
sudo ufw allow from YOUR_IP to any port 80
sudo ufw allow from YOUR_IP to any port 8000
sudo ufw allow from YOUR_IP to any port 7082
```

2. **Use VPN**: Access dashboard only through VPN

3. **Use Basic Auth**: Quick Nginx basic authentication (see Option 1)

4. **Change Default Ports**: Use non-standard ports
```bash
# In vite.config.ts
server: {
  port: 34567  # Random high port
}

# In backend/.env
API_PORT=45678  # Random high port
```

5. **Monitor Access Logs**:
```bash
sudo tail -f /var/log/nginx/access.log
./dashboard.sh logs-backend
```

## Recommended Approach

For production use, we recommend:

1. **Immediate**: Use Nginx Basic Authentication (Option 1) - takes 5 minutes
2. **Short-term**: Implement IP whitelisting (Option 3)
3. **Long-term**: Develop custom authentication (Option 5) with user management

## Environment Variables for Secrets

Never hardcode credentials in your code. Use environment variables:

```bash
# backend/.env
API_SECRET_KEY=your-very-long-secret-key-change-this
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password-here
JWT_SECRET=another-very-long-secret-key
```

## Additional Security Recommendations

1. **HTTPS**: Always use HTTPS in production (Let's Encrypt is free)
2. **CORS**: Configure CORS properly (don't use `allow_origins=["*"]` in production)
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Input Validation**: All inputs are validated (already done with Pydantic)
5. **SQL Injection**: Using SQLAlchemy ORM prevents SQL injection (already safe)
6. **XSS Protection**: React escapes content by default (already safe)
7. **CSRF**: Implement CSRF tokens if using cookies
8. **Security Headers**: Add security headers in Nginx

### Nginx Security Headers

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## Summary

**Current State**: ❌ No authentication

**Quick Fix** (5 min): ✅ Nginx Basic Auth

**Recommended**: ✅ OAuth2 Proxy or Custom JWT Authentication

**Security Level**: 
- Without auth: 🔴 Low
- With Basic Auth: 🟡 Medium
- With OAuth2/JWT + HTTPS: 🟢 High
