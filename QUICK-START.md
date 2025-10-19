# 🚀 Quick Start Commands

## **One-Line Setup**
```bash
cd HackWestTX && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
```

## **Step-by-Step Setup**
```bash
# 1. Navigate to project
cd HackWestTX

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver
```

## **Test the API**
```bash
# Health check
curl http://localhost:8000/api/health/

# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123", "password_confirm": "password123", "first_name": "Test", "last_name": "User"}'
```

## **API Base URL**
`http://localhost:8000/api/`

## **Admin Interface**
`http://localhost:8000/admin/`

## **Stop Server**
Press `Ctrl+C` in the terminal where the server is running
