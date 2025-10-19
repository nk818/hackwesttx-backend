# 🚀 Railway Deployment Guide

## 📋 Pre-Deployment Checklist

✅ **Files Ready:**
- `manage.py` - Django server
- `requirements.txt` - Dependencies
- `Procfile` - Server startup
- `railway.json` - Railway config
- `railway.toml` - Railway settings
- `.gitignore` - Git ignore rules

✅ **MongoDB Connection:**
- Connection string ready
- Database: `hackwesttx_db`
- Cluster: `cluster0.bn7mgbx.mongodb.net`

## 🚀 Deployment Steps

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `hackwesttx-backend`
3. Description: `HackWestTX Class Portfolio Backend API`
4. Make it **Public** (required for Railway free tier)
5. Click "Create repository"

### Step 2: Upload Code to GitHub
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: HackWestTX Backend API"

# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hackwesttx-backend.git

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your `hackwesttx-backend` repository
5. Railway will automatically detect it's a Python/Django app

### Step 4: Set Environment Variables
In Railway dashboard → Variables tab, add:

```
DJANGO_SETTINGS_MODULE=hackwesttx.settings
DEBUG=False
ALLOWED_HOSTS=*.railway.app
MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### Step 5: Deploy
1. Click "Deploy" in Railway dashboard
2. Wait for build to complete (2-3 minutes)
3. Get your live URL!

## 🎯 Your Live URLs

After deployment, you'll get:
- **Main API**: `https://hackwesttx-backend-production.railway.app/`
- **Health Check**: `https://hackwesttx-backend-production.railway.app/api/health/`
- **Calendar Events**: `https://hackwesttx-backend-production.railway.app/api/calendar-events/`
- **User Registration**: `https://hackwesttx-backend-production.railway.app/api/auth/register/`

## 🧪 Test Your Deployment

```bash
# Test health endpoint
curl https://hackwesttx-backend-production.railway.app/api/health/

# Test API root
curl https://hackwesttx-backend-production.railway.app/

# Register a user
curl -X POST https://hackwesttx-backend-production.railway.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

## 🔧 Railway Dashboard Features

- **Logs**: View real-time server logs
- **Metrics**: Monitor CPU, memory, requests
- **Variables**: Manage environment variables
- **Domains**: Custom domain setup
- **Deployments**: View deployment history

## 🎉 Success!

Your Django backend will be live on Railway with:
- ✅ Automatic deployments from GitHub
- ✅ MongoDB Atlas integration
- ✅ All API endpoints working
- ✅ Health monitoring
- ✅ Free tier (no credit card needed)

**Ready to deploy! 🚀**
