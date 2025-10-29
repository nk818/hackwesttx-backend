# MongoDB Atlas Configuration - Complete Guide

## 📖 How Everything Works

### Current Architecture (MongoDB-Only Mode)

Your backend is now configured to use **MongoDB Atlas for everything**:

1. **Django ORM** → Uses `djongo` to store all Django models (Users, ClassPortfolio, etc.) in MongoDB Atlas
2. **Additional Data** → Uses `pymongo` directly for raw MongoDB operations (via `mongodb_utils.py`)

Both use the same MongoDB Atlas database, but through different interfaces.

---

## 🔄 Two Database Approaches Explained

### Option 1: **MongoDB-Only Mode** (Current Setup - Recommended)

```
┌─────────────────────────────────────────┐
│         MongoDB Atlas                   │
│  ┌──────────────────────────────────┐  │
│  │  Django ORM Data (via djongo)    │  │
│  │  - Users, ClassPortfolio, etc.   │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Additional Data (via pymongo)  │  │
│  │  - Custom collections, logs, etc.│  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**How it works:**
- **Django ORM**: All your Django models (User, ClassPortfolio, Quiz, etc.) are stored in MongoDB using `djongo`
- **Additional Data**: Your `mongodb_utils.py` functions use `pymongo` directly for custom operations
- **Both use the same database**: Everything is in `hackwesttx_db` on MongoDB Atlas

**Advantages:**
- ✅ Single database source of truth
- ✅ No SQLite file to manage
- ✅ Consistent data structure
- ✅ Easy to back up (just MongoDB Atlas)
- ✅ Works the same locally and in production

**Configuration:**
```python
# settings.py automatically uses MongoDB when:
USE_MONGODB_ONLY=True  # (default)

# This makes Django ORM use djongo to store models in MongoDB
DATABASES = {
    'default': {
        'ENGINE': 'djongo',  # <-- Makes Django models go to MongoDB
        'NAME': 'hackwesttx_db',
        'CLIENT': {
            'host': 'mongodb+srv://...',
            # SSL settings...
        }
    }
}
```

---

### Option 2: **Hybrid Mode** (SQLite + MongoDB)

```
┌──────────────────────┐     ┌──────────────────────────┐
│   SQLite (local)     │     │   MongoDB Atlas (cloud) │
│  ┌────────────────┐ │     │  ┌────────────────────┐  │
│  │ Django ORM Data │ │     │  │ Additional Data   │  │
│  │ - Users, etc.   │ │     │  │ - Custom stuff    │  │
│  └────────────────┘ │     │  └────────────────────┘  │
└──────────────────────┘     └──────────────────────────┘
```

**How it works:**
- **Django ORM**: Stores models in local `db.sqlite3` file
- **Additional Data**: Uses MongoDB Atlas via `pymongo` for custom collections
- **Two separate databases**: Different data in different places

**Advantages:**
- ✅ Faster local development (no network needed for Django ORM)
- ✅ Works offline for Django ORM
- ✅ No MongoDB connection needed for basic Django operations

**Disadvantages:**
- ❌ Two different databases to manage
- ❌ Data not consistent between local and production
- ❌ SQLite file can get corrupted
- ❌ Harder to sync data

**Configuration:**
```python
# Set this in .env or environment:
USE_MONGODB_ONLY=False

# This makes Django ORM use SQLite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # <-- SQLite
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# But mongodb_utils.py still uses MongoDB Atlas
```

---

## 🛠️ How Django ORM Works with MongoDB (djongo)

### What is djongo?

`djongo` is a bridge that translates Django ORM operations into MongoDB queries.

**Example:**
```python
# You write Django code:
user = User.objects.create(username='john', email='john@example.com')
users = User.objects.filter(role='student')

# djongo translates this to MongoDB:
# db.users.insert_one({username: 'john', email: 'john@example.com'})
# db.users.find({role: 'student'})
```

**How it works:**
1. You use Django models normally: `User.objects.all()`
2. `djongo` intercepts these calls
3. Converts Django ORM queries to MongoDB queries
4. Stores data in MongoDB collections
5. Returns results as Django model instances

**Collections created:**
- Each Django model becomes a MongoDB collection
- Example: `User` model → `api_user` collection
- Example: `ClassPortfolio` model → `api_classportfolio` collection

---

## 🔍 How to Verify Everything Works

### 1. Check Configuration

```bash
python3 manage.py shell
```

```python
from django.conf import settings
from django.db import connections

# Check database engine
print("Database Engine:", connections['default'].settings_dict['ENGINE'])
# Should show: djongo

# Check MongoDB settings
print("MongoDB URI:", settings.MONGODB_URI[:50] + "...")
print("MongoDB Database:", settings.MONGODB_DATABASE)
print("MongoDB Enabled:", settings.MONGODB_ENABLED)
```

### 2. Test Django ORM (stored in MongoDB)

```python
from api.models import User

# Create a test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)
print("✅ User created in MongoDB:", user.id)

# Query users
users = User.objects.all()
print(f"✅ Found {users.count()} users in MongoDB")
```

### 3. Test Direct MongoDB Access

```python
from api.mongodb_utils import get_mongodb_database

db = get_mongodb_database()
collections = db.list_collection_names()
print("✅ Collections in MongoDB:", collections)

# Should see Django model collections:
# - api_user (from User model)
# - api_classportfolio (from ClassPortfolio model)
# - etc.
```

### 4. Verify Data is in MongoDB Atlas

1. Go to MongoDB Atlas dashboard
2. Browse Collections → `hackwesttx_db` database
3. You should see collections like:
   - `api_user` - Your Django User models
   - `api_classportfolio` - Your ClassPortfolio models
   - `django_migrations` - Django migration tracking
   - Any custom collections from `mongodb_utils.py`

---

## 🔧 Environment Variables

### For MongoDB-Only Mode (Recommended)

```env
# Use MongoDB Atlas for Django ORM
USE_MONGODB_ONLY=True

# MongoDB Atlas Connection
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGODB_DATABASE=hackwesttx_db
MONGODB_ENABLED=True
MONGODB_TIMEOUT=10
```

### For Hybrid Mode

```env
# Use SQLite for Django ORM
USE_MONGODB_ONLY=False

# MongoDB Atlas still used for additional data
MONGODB_URI=mongodb+srv://...
MONGODB_DATABASE=hackwesttx_db
MONGODB_ENABLED=True
```

---

## 📊 Data Flow

### When You Create a User:

```
1. Code: User.objects.create_user(...)
          ↓
2. Django ORM: Processes the model
          ↓
3. djongo: Converts to MongoDB operation
          ↓
4. MongoDB Atlas: Stores in 'api_user' collection
          ↓
5. Returns: User model instance
```

### When You Use mongodb_utils:

```
1. Code: store_additional_data('logs', {...})
          ↓
2. pymongo: Direct MongoDB client
          ↓
3. MongoDB Atlas: Stores in 'logs' collection
          ↓
4. Returns: Document ID
```

---

## 🚀 Migration from SQLite to MongoDB-Only

If you previously used SQLite and want to migrate:

### Option A: Fresh Start (Recommended for development)

1. Backup your SQLite data (if needed)
2. Set `USE_MONGODB_ONLY=True`
3. Run migrations: `python3 manage.py migrate`
4. Recreate test data

### Option B: Import Data

1. Export SQLite data to JSON:
   ```python
   python3 manage.py dumpdata > backup.json
   ```

2. Switch to MongoDB:
   ```env
   USE_MONGODB_ONLY=True
   ```

3. Run migrations:
   ```bash
   python3 manage.py migrate
   ```

4. Load data:
   ```python
   python3 manage.py loaddata backup.json
   ```

---

## ✅ Testing Your Setup

Run the comprehensive test:

```bash
python3 test_mongodb_atlas_final.py
```

This tests:
- ✅ Configuration
- ✅ Connection
- ✅ Django ORM access (via djongo)
- ✅ Direct MongoDB access (via pymongo)
- ✅ Read/Write operations

---

## 🎯 Summary

**Current Setup (MongoDB-Only):**
- ✅ Django ORM → MongoDB Atlas (via djongo)
- ✅ Additional Data → MongoDB Atlas (via pymongo)
- ✅ Everything in one place
- ✅ Consistent across environments

**Configuration:**
- Set `USE_MONGODB_ONLY=True` (or leave default)
- Set `MONGODB_URI` with your Atlas connection string
- Everything else is automatic!

**Why This is Better:**
- Single source of truth
- No file-based database to manage
- Same setup locally and in production
- Easier backups and scaling

