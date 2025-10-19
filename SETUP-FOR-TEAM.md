# 🚀 HackWestTX Class Portfolio API - Team Setup Guide

## 📋 **What You're Getting**
A complete Django REST API backend for a Class Portfolio management system with 8 core features:

1. **Smart Syllabus Scanner** - Upload and extract important dates
2. **Interactive Learning Space** - Flashcards, quizzes, and study materials
3. **Class Performance Tracker** - Grade analytics and projections
4. **End-of-Class Review & Archive** - Student reviews and ratings
5. **Marketplace & Sharing** - Share portfolios and resources
6. **Class Creation & Collaboration** - Create and collaborate on portfolios
7. **Community & Networking** - Study groups and Q&A
8. **Mobile & Notifications** - Push notifications and reminders

## 🛠️ **Quick Setup (5 minutes)**

### **Prerequisites**
- Python 3.8+ installed
- Git (optional, for version control)

### **Step 1: Navigate to Project**
```bash
cd HackWestTX
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Run Database Migrations**
```bash
python manage.py migrate
```

### **Step 5: Start the Server**
```bash
python manage.py runserver
```

**🎉 Success!** Your API is now running at `http://localhost:8000/api/`

## 🔗 **API Endpoints Overview**

### **Base URL**: `http://localhost:8000/api/`

### **Authentication**
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `GET /api/auth/me/` - Get current user info

### **Core Features**
- `GET /api/portfolios/` - List class portfolios
- `POST /api/portfolios/` - Create new portfolio
- `GET /api/materials/` - List lecture materials
- `POST /api/materials/` - Upload materials
- `GET /api/grades/` - List grades
- `POST /api/grades/` - Add grades
- `GET /api/study-groups/` - List study groups
- `POST /api/study-groups/` - Create study group

### **Health Check**
- `GET /api/health/` - Check if API is running

## 🔑 **Authentication**

The API uses **Token Authentication**. Here's how to use it:

### **1. Register a User**
```javascript
fetch('http://localhost:8000/api/auth/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    email: 'test@example.com',
    password: 'password123',
    password_confirm: 'password123',
    first_name: 'Test',
    last_name: 'User',
    phone: '+1234567890',
    university: 'HackWestTX University',
    graduation_year: 2025,
    major: 'Computer Science'
  })
})
```

### **2. Login**
```javascript
fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    password: 'password123'
  })
})
```

### **3. Use Token for Authenticated Requests**
```javascript
fetch('http://localhost:8000/api/portfolios/', {
  headers: {
    'Authorization': 'Token YOUR_TOKEN_HERE',
    'Content-Type': 'application/json'
  }
})
```

## 📚 **Frontend Development Examples**

### **React/JavaScript Example**
```javascript
// API base URL
const API_BASE = 'http://localhost:8000/api';

// Register user
const registerUser = async (userData) => {
  const response = await fetch(`${API_BASE}/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  return response.json();
};

// Login user
const loginUser = async (credentials) => {
  const response = await fetch(`${API_BASE}/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  const data = await response.json();
  localStorage.setItem('token', data.token); // Save token
  return data;
};

// Get portfolios (authenticated)
const getPortfolios = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE}/portfolios/`, {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};
```

## 🗂️ **Project Structure**
```
HackWestTX/
├── api/                    # Main API app
│   ├── models.py          # Database models
│   ├── serializers.py     # API serializers
│   ├── views.py          # API views
│   ├── urls.py           # URL patterns
│   └── admin.py          # Admin interface
├── hackwesttx/           # Django project settings
│   ├── settings.py       # Main settings
│   └── urls.py          # Root URL config
├── requirements.txt      # Python dependencies
├── README.md            # Detailed API documentation
├── manage.py            # Django management script
└── db.sqlite3          # SQLite database (created after migration)
```

## 🧪 **Testing the API**

### **Using Postman**
1. Import the API endpoints
2. Test registration and login
3. Use the token for authenticated requests

### **Using curl**
```bash
# Health check
curl http://localhost:8000/api/health/

# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123", "password_confirm": "password123"}'
```

## 🚨 **Troubleshooting**

### **Port Already in Use**
```bash
# Kill existing server
pkill -f "python manage.py runserver"
# Then restart
python manage.py runserver
```

### **Database Issues**
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

### **Virtual Environment Issues**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📖 **Full Documentation**

See `README.md` for complete API documentation with all endpoints, request/response examples, and detailed feature descriptions.

## 🎯 **Next Steps**

1. **Start the server**: `python manage.py runserver`
2. **Test the API**: Use Postman or curl
3. **Build the frontend**: Connect to `http://localhost:8000/api/`
4. **Read the docs**: Check `README.md` for detailed API specs

## 💡 **Pro Tips**

- Keep the server running while developing frontend
- Use the Django admin at `http://localhost:8000/admin/` to manage data
- Check the terminal for API request logs
- All endpoints return JSON responses
- Use proper error handling in your frontend code

---

**Happy coding! 🚀** Your Class Portfolio API is ready for frontend development!
