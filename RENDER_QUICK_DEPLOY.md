# Quick Render Deployment Guide

## 🚀 Deploy Your Django Backend to Render

### Step 1: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select: `HackWestTX-Complete-Backend`

### Step 2: Configure Your Service

**Basic Settings:**
- **Name**: `hackwesttx-backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python manage.py migrate && gunicorn hackwesttx.wsgi:application --bind 0.0.0.0:$PORT`

### Step 3: Environment Variables

Add these environment variables:

```
DEBUG=False
SECRET_KEY=django-insecure-change-this-in-production-$(date +%s)
MONGODB_ENABLED=True
MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
RENDER=true
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for deployment (2-5 minutes)
3. Your backend will be available at: `https://your-app-name.onrender.com`

### Step 5: Test Your Deployment

```bash
python3 check_status.py https://your-app-name.onrender.com
```

### Expected Results

✅ **Backend**: UP and running
✅ **SQLite**: Connected with tables  
✅ **MongoDB Atlas**: Connected
✅ **All endpoints**: Working

### Troubleshooting

**If gunicorn error occurs:**
- Make sure `gunicorn==21.2.0` is in requirements.txt
- Use the correct start command with gunicorn

**If database errors:**
- Check environment variables are set correctly
- Verify MongoDB URI is correct

Your Django backend should work perfectly on Render! 🎉
