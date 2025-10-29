# MongoDB Atlas Setup Guide

This guide will help you configure MongoDB Atlas to work with your HackWestTX backend.

## Quick Setup

### 1. Get Your MongoDB Atlas Connection String

1. Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Go to your cluster and click **Connect**
3. Choose **Connect your application**
4. Copy the connection string (it will look like):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   ```

### 2. Configure Network Access

1. In MongoDB Atlas, go to **Network Access**
2. Click **Add IP Address**
3. For local development, add `0.0.0.0/0` (allows all IPs - use only for development)
4. For production, add specific IP addresses or your Render deployment IP

### 3. Set Up Environment Variables

#### Option A: Using .env file (Local Development)

Create a `.env` file in the project root:

```env
# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGODB_DATABASE=hackwesttx_db
MONGODB_ENABLED=True
MONGODB_TIMEOUT=10

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Other optional configurations
OPENAI_API_KEY=your-openai-key-here
```

#### Option B: Using Environment Variables (Production)

Set these environment variables in your hosting platform (Render, Railway, etc.):

```bash
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGODB_DATABASE=hackwesttx_db
MONGODB_ENABLED=True
MONGODB_TIMEOUT=10
RENDER=true  # Set to 'true' if deploying on Render
```

## Testing the Connection

### Method 1: Using the Test Script

```bash
python test_mongodb_atlas_final.py
```

This will:
- Check your configuration
- Test the MongoDB connection
- Perform read/write operations
- Verify everything is working

### Method 2: Using Django Shell

```bash
python manage.py shell
```

Then run:
```python
from api.mongodb_utils import test_mongodb_connection
result = test_mongodb_connection()
print(result)
```

### Method 3: Using the API Endpoint

If your server is running, visit:
```
GET /api/health/status/
```

This endpoint includes MongoDB connection status.

## Configuration Details

### MongoDB URI Format

The connection string should include:
- `retryWrites=true` - Enables retryable writes
- `w=majority` - Write concern for data durability
- `appName=Cluster0` - Application identifier

Example:
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### Environment Variable Priority

Settings are loaded in this order:
1. Environment variables (highest priority)
2. `.env` file
3. Default values in `settings.py` (lowest priority)

### Database Configuration

- **Local Development**: Uses SQLite for Django ORM, MongoDB Atlas for additional data storage
- **Production (Render)**: Uses MongoDB Atlas as the primary database via djongo

## Troubleshooting

### Connection Timeout

If you're experiencing connection timeouts:

1. Check your internet connection
2. Verify MongoDB Atlas cluster is running
3. Check Network Access settings in MongoDB Atlas
4. Increase timeout: `MONGODB_TIMEOUT=30`

### SSL/TLS Errors

SSL/TLS is automatically handled. If you see SSL errors:
- Make sure your connection string uses `mongodb+srv://` (not `mongodb://`)
- Check that your IP is whitelisted in MongoDB Atlas Network Access

### Authentication Errors

If you see authentication errors:
- Verify your username and password in the connection string
- Make sure the database user has proper permissions
- Check if the user exists in MongoDB Atlas

### Connection Refused

If connection is refused:
- Verify Network Access allows your IP
- Check if the cluster is paused (free tier clusters pause after inactivity)
- Ensure the connection string is correct

## Production Deployment

### On Render

1. Set `RENDER=true` in environment variables
2. Set `MONGODB_URI` with your Atlas connection string
3. Set `MONGODB_ENABLED=True`
4. The backend will automatically use MongoDB Atlas as the primary database

### Database Name

The default database name is `hackwesttx_db`. You can change it using:
```env
MONGODB_DATABASE=your_database_name
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: In production, use platform environment variables, not `.env` files
3. **Restrict network access**: Only allow necessary IP addresses
4. **Use strong passwords**: Create strong passwords for database users
5. **Rotate credentials**: Regularly update database passwords

## Support

If you encounter issues:
1. Check the test script output: `python test_mongodb_atlas_final.py`
2. Review MongoDB Atlas logs in the Atlas dashboard
3. Check Django logs for detailed error messages
4. Verify all environment variables are set correctly

