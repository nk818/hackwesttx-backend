# Deploy to Railway (Free & Easy)

## 🚀 Quick Deploy Steps

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login to Railway
```bash
railway login
```

### 3. Initialize Project
```bash
railway init
```

### 4. Set Environment Variables
```bash
# Set Django settings
railway variables set DJANGO_SETTINGS_MODULE=hackwesttx.settings
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=*.railway.app

# Set MongoDB connection
railway variables set MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### 5. Deploy
```bash
railway up
```

### 6. Get Your URL
```bash
railway domain
```

## 📋 Create Railway Config Files

### Procfile
```
web: python manage.py runserver 0.0.0.0:$PORT
```

### railway.json
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py runserver 0.0.0.0:$PORT",
    "healthcheckPath": "/api/health/"
  }
}
```

## 🔧 Update Django Settings for Production

Add to `hackwesttx/settings.py`:
```python
import os

# Production settings
ALLOWED_HOSTS = ['*']  # For Railway
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Database (Railway provides PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_URL', ''),
    }
}
```

## 🎯 Your Deployed URLs Will Be:
- **API Root**: `https://your-app.railway.app/`
- **Health Check**: `https://your-app.railway.app/api/health/`
- **Admin**: `https://your-app.railway.app/admin/`
