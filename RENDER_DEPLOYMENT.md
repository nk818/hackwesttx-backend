# Render Deployment Guide

## 🚀 Deploy Your Django Backend to Render

### Prerequisites
- ✅ PostgreSQL database created on Render
- ✅ GitHub repository with your code

### Step 1: Connect Your Repository

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your repository: `HackWestTX-Complete-Backend`

### Step 2: Configure Your Service

**Basic Settings:**
- **Name**: `hackwesttx-backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (or `/` if needed)

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`

### Step 3: Environment Variables

Add these environment variables in Render:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
MONGODB_ENABLED=False
RENDER=true
ALLOWED_HOSTS=your-app-name.onrender.com
```

**Database Variables** (from your PostgreSQL service):
```
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=5432
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Wait for deployment to complete (usually 2-5 minutes)

### Step 5: Test Your Deployment

Your backend will be available at: `https://your-app-name.onrender.com`

Test endpoints:
- **Health Check**: `https://your-app-name.onrender.com/api/health/`
- **API Root**: `https://your-app-name.onrender.com/`
- **Admin**: `https://your-app-name.onrender.com/admin/`

### Step 6: Connect to Your PostgreSQL Database

1. Go to your PostgreSQL service on Render
2. Copy the connection details
3. Add them as environment variables in your web service

### Expected Results

✅ **Working Endpoints:**
- `/` - API Root
- `/api/health/` - Health Check
- `/api/` - API Documentation
- `/admin/` - Django Admin

✅ **Database:**
- PostgreSQL connection working
- Migrations run automatically
- All database tables created

### Troubleshooting

**If deployment fails:**
1. Check build logs in Render dashboard
2. Verify all environment variables are set
3. Ensure PostgreSQL service is running

**If database connection fails:**
1. Verify database environment variables
2. Check PostgreSQL service status
3. Ensure database is accessible

### Benefits of Render vs Railway

✅ **Render Advantages:**
- Better PostgreSQL integration
- More reliable migrations
- Better static file handling
- More predictable deployments
- Better logging and monitoring

Your Django backend should work perfectly on Render! 🎉
