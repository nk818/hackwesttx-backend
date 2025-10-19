# Deploy to Render (Free Tier)

## 🚀 Quick Deploy Steps

### 1. Create Render Account
Go to: https://render.com

### 2. Connect GitHub Repository
1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Select "Web Service"

### 3. Configure Build Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python manage.py runserver 0.0.0.0:$PORT`

### 4. Set Environment Variables
```
DJANGO_SETTINGS_MODULE=hackwesttx.settings
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### 5. Deploy
Click "Deploy" and wait for build to complete.

## 🎯 Your Deployed URLs Will Be:
- **API Root**: `https://your-app.onrender.com/`
- **Health Check**: `https://your-app.onrender.com/api/health/`
- **Admin**: `https://your-app.onrender.com/admin/`
