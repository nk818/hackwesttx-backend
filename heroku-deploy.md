# Deploy to Heroku

## 🚀 Quick Deploy Steps

### 1. Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
heroku create your-app-name
```

### 4. Set Environment Variables
```bash
heroku config:set DJANGO_SETTINGS_MODULE=hackwesttx.settings
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### 5. Create Procfile
```
web: python manage.py runserver 0.0.0.0:$PORT
```

### 6. Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 7. Run Migrations
```bash
heroku run python manage.py migrate
```

### 8. Create Superuser
```bash
heroku run python manage.py createsuperuser
```

## 🎯 Your Deployed URLs Will Be:
- **API Root**: `https://your-app-name.herokuapp.com/`
- **Health Check**: `https://your-app-name.herokuapp.com/api/health/`
- **Admin**: `https://your-app-name.herokuapp.com/admin/`
