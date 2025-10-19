# 🚀 Simple Backend Deployment (No Node.js Needed!)

## Option 1: Render (Recommended - Easiest)

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Upload all your backend files to the repository

### Step 2: Deploy on Render
1. Go to https://render.com
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `hackwesttx-backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python manage.py runserver 0.0.0.0:$PORT`
6. Click "Deploy"

### Step 3: Set Environment Variables
In Render dashboard, go to Environment tab and add:
```
DJANGO_SETTINGS_MODULE=hackwesttx.settings
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

## Option 2: Railway (Also Easy)

### Step 1: Go to Railway
1. Visit https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect it's a Python/Django app

### Step 2: Set Variables
In Railway dashboard, add these environment variables:
```
DJANGO_SETTINGS_MODULE=hackwesttx.settings
DEBUG=False
MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

## Option 3: Heroku (Traditional)

### Step 1: Create Heroku App
1. Go to https://heroku.com
2. Create new app
3. Connect GitHub repository
4. Enable automatic deploys

### Step 2: Set Config Vars
In Heroku dashboard → Settings → Config Vars:
```
DJANGO_SETTINGS_MODULE=hackwesttx.settings
DEBUG=False
MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

## 🎯 Your Backend Will Be Available At:
- **API Root**: `https://your-app.onrender.com/`
- **Health Check**: `https://your-app.onrender.com/api/health/`
- **Calendar Events**: `https://your-app.onrender.com/api/calendar-events/`
- **User Registration**: `https://your-app.onrender.com/api/auth/register/`

## 🧪 Test Your Deployed Backend
```bash
curl https://your-app.onrender.com/api/health/
```

**No Node.js needed! Just upload your files and deploy! 🎉**
