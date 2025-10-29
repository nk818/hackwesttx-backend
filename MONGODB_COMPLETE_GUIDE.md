# MongoDB Atlas Complete Setup Guide

## ✅ Current Configuration Status

Your backend is now configured to use **MongoDB Atlas** as the primary database. Here's how everything works:

---

## 🏗️ Architecture Overview

### **MongoDB-Only Mode** (Current Default)

```
┌─────────────────────────────────────────────────────────┐
│              MongoDB Atlas (Cloud)                      │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Django ORM Data (via djongo)                      │ │
│  │  - Uses djongo to translate Django ORM → MongoDB │ │
│  │  - Models: User, ClassPortfolio, Quiz, etc.       │ │
│  │  - Stored in collections: api_user, api_class...  │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Additional Data (via pymongo)                     │ │
│  │  - Direct MongoDB operations                       │ │
│  │  - Custom collections, logs, analytics              │ │
│  │  - Accessed via mongodb_utils.py                   │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Key Point:** Everything goes to MongoDB Atlas, but through two different interfaces:
1. **Django ORM** → Uses `djongo` (Django model → MongoDB collection)
2. **Direct Access** → Uses `pymongo` (raw MongoDB operations)

---

## 🔧 How It Works

### 1. Django ORM → MongoDB (via djongo)

**What is djongo?**
- A bridge that converts Django ORM queries into MongoDB operations
- Allows you to use Django models normally, but stores data in MongoDB

**Example Flow:**
```python
# Your Django code:
user = User.objects.create(username='john', email='john@example.com')
users = User.objects.filter(role='student')

# What djongo does:
# 1. Intercepts Django ORM calls
# 2. Translates to MongoDB queries:
#    db.api_user.insert_one({username: 'john', ...})
#    db.api_user.find({role: 'student'})
# 3. Returns Django model instances
```

**Configuration:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'djongo',  # <-- This makes Django use MongoDB
        'NAME': 'hackwesttx_db',
        'CLIENT': {
            'host': 'mongodb+srv://...',  # Your Atlas connection string
        }
    }
}
```

**Collections Created:**
- Each Django model → MongoDB collection
- `User` → `api_user` collection
- `ClassPortfolio` → `api_classportfolio` collection
- Django migrations tracked in `django_migrations` collection

### 2. Direct MongoDB Access (via pymongo)

**What is pymongo?**
- Python driver for direct MongoDB operations
- Used by `mongodb_utils.py` for custom operations

**Example Flow:**
```python
# Using mongodb_utils.py:
from api.mongodb_utils import store_additional_data

# Stores directly in MongoDB (not through Django ORM)
result_id = store_additional_data('custom_logs', {
    'action': 'user_login',
    'timestamp': '2025-01-28'
})
```

**Configuration:**
```python
# settings.py
MONGODB_URI = 'mongodb+srv://...'  # Same Atlas connection
MONGODB_DATABASE = 'hackwesttx_db'
MONGODB_ENABLED = True
```

---

## 🆚 SQLite + MongoDB (Hybrid Mode)

### When Would You Use This?

If you want:
- ✅ Faster local development (no network for Django ORM)
- ✅ Work offline for Django operations
- ✅ Use MongoDB only for custom data

### How It Works:

```
┌─────────────────────┐     ┌──────────────────────────┐
│  SQLite (Local)     │     │  MongoDB Atlas (Cloud)  │
│  Django ORM Data    │     │  Additional Data         │
│  - User models      │     │  - Custom collections    │
│  - Django tables    │     │  - Analytics            │
└─────────────────────┘     └──────────────────────────┘
```

**Configuration:**
```python
# Set in .env:
USE_MONGODB_ONLY=False

# Then Django uses SQLite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# But mongodb_utils.py still uses MongoDB Atlas
```

**Advantages:**
- Fast local development (no network latency for Django ORM)
- Works completely offline

**Disadvantages:**
- Two databases to manage
- Data not consistent between local and production
- Need to migrate data when deploying

---

## ✅ Configuration Check

### Current Setup (MongoDB-Only)

```python
# settings.py automatically uses MongoDB when:
USE_MONGODB_ONLY=True  # (default)

# This makes:
# - Django ORM → MongoDB Atlas (via djongo)
# - Additional Data → MongoDB Atlas (via pymongo)
```

### Verify Your Configuration

```bash
python3 manage.py shell
```

```python
from django.conf import settings
from django.db import connections

# Check database engine
print(connections['default'].settings_dict['ENGINE'])
# Should show: djongo

# Check MongoDB settings
print(settings.MONGODB_URI[:50])
print(settings.MONGODB_ENABLED)  # Should be True
```

---

## 🧪 Testing

### Test 1: MongoDB Connection

```bash
python3 test_mongodb_atlas_final.py
```

This tests:
- ✅ Configuration
- ✅ Connection to MongoDB Atlas
- ✅ Read/Write operations
- ✅ Direct MongoDB access

### Test 2: Django ORM with MongoDB

```bash
python3 manage.py shell
```

```python
from api.models import User

# Count users (stored in MongoDB)
count = User.objects.count()
print(f"Users in MongoDB: {count}")

# These are stored in MongoDB via djongo
```

### Test 3: Direct MongoDB Access

```python
from api.mongodb_utils import get_mongodb_database, test_mongodb_connection

# Test connection
result = test_mongodb_connection()
print(result)

# Access database directly
db = get_mongodb_database()
collections = db.list_collection_names()
print(f"Collections: {collections}")
```

---

## 🔍 Where Is Your Data?

### In MongoDB Atlas Dashboard:

1. Go to your cluster → **Browse Collections**
2. Select database: `hackwesttx_db`
3. You'll see:

**Django ORM Collections** (via djongo):
- `api_user` - User models
- `api_classportfolio` - ClassPortfolio models
- `api_quiz` - Quiz models
- `django_migrations` - Django migration history
- ... (one collection per Django model)

**Custom Collections** (via pymongo):
- `connection_test` - Test documents
- Any collections created by `mongodb_utils.py`

---

## 🔄 Data Flow Examples

### Creating a User (Django ORM → MongoDB)

```
1. Code: User.objects.create_user(...)
          ↓
2. Django ORM processes the model
          ↓
3. djongo converts to MongoDB operation
          ↓
4. MongoDB Atlas: db.api_user.insert_one({...})
          ↓
5. Returns: User Django model instance
```

### Storing Custom Data (pymongo → MongoDB)

```
1. Code: store_additional_data('logs', {...})
          ↓
2. pymongo client connects to Atlas
          ↓
3. MongoDB Atlas: db.logs.insert_one({...})
          ↓
4. Returns: Document ID
```

---

## 📊 Summary

### MongoDB-Only Mode (Recommended)

**What:** Everything in MongoDB Atlas
- Django ORM → MongoDB (via djongo)
- Additional Data → MongoDB (via pymongo)

**Configuration:**
```env
USE_MONGODB_ONLY=True  # Default
MONGODB_URI=your_atlas_connection_string
MONGODB_DATABASE=hackwesttx_db
MONGODB_ENABLED=True
```

**When to Use:**
- ✅ Production deployments
- ✅ Want consistent data everywhere
- ✅ Need cloud-based database
- ✅ Easier backups and scaling

### Hybrid Mode (Optional)

**What:** SQLite for Django ORM + MongoDB for additional data
- Django ORM → SQLite (local file)
- Additional Data → MongoDB Atlas (cloud)

**Configuration:**
```env
USE_MONGODB_ONLY=False
MONGODB_URI=your_atlas_connection_string
MONGODB_ENABLED=True
```

**When to Use:**
- ✅ Fast local development
- ✅ Work offline for Django operations
- ✅ Testing without network

---

## 🎯 Quick Reference

### Check Current Mode:
```bash
# Look for this message when Django starts:
# "🍃 Using MongoDB Atlas as primary database" = MongoDB-only
# "🏠 Hybrid mode - SQLite + MongoDB" = Hybrid mode
```

### Switch Modes:
```env
# MongoDB-only (default)
USE_MONGODB_ONLY=True

# Hybrid mode
USE_MONGODB_ONLY=False
```

### Test Connection:
```bash
python3 test_mongodb_atlas_final.py
```

### View Data:
- MongoDB Atlas Dashboard → Browse Collections
- Database: `hackwesttx_db`
- Collections: `api_user`, `api_classportfolio`, etc.

---

## 🚀 Next Steps

1. ✅ Configuration is complete
2. ✅ MongoDB Atlas connection working
3. ✅ Ready to use MongoDB for all data

**Your backend now uses MongoDB Atlas as the primary database!**

All Django models (User, ClassPortfolio, etc.) will be stored in MongoDB Atlas, and you can also use `mongodb_utils.py` for additional custom data operations.

