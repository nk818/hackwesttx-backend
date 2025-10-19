# MongoDB Atlas Connection

This document provides a simple guide for connecting to MongoDB Atlas.

## 🔗 Connection String

Your MongoDB Atlas connection string is:

```
mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

## 🧪 Test Connection

To test your MongoDB Atlas connection, run:

```bash
python3 test_mongodb.py
```

This will:
- ✅ Test the connection to MongoDB Atlas
- ✅ Create a test database connection
- ✅ Insert and retrieve a test document
- ✅ Clean up test data

## 📊 Database Information

- **Database Name**: `hackwesttx_db`
- **Cluster**: `cluster0.bn7mgbx.mongodb.net`
- **User**: `noahkueng1_db_user`

## 🔧 Usage in Your Applications

### Python with PyMongo

```python
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import ssl

# Connection string
uri = "mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create client
client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)

# Test connection
client.admin.command('ping')

# Use database
db = client['hackwesttx_db']
collection = db['your_collection_name']

# Insert document
result = collection.insert_one({"key": "value"})
print(f"Inserted document with ID: {result.inserted_id}")

# Find documents
documents = collection.find()
for doc in documents:
    print(doc)
```

### Node.js with MongoDB Driver

```javascript
const { MongoClient } = require('mongodb');

const uri = "mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

async function connectToMongoDB() {
    const client = new MongoClient(uri);
    
    try {
        await client.connect();
        console.log("Connected to MongoDB Atlas!");
        
        const db = client.db('hackwesttx_db');
        const collection = db.collection('your_collection_name');
        
        // Insert document
        const result = await collection.insertOne({key: "value"});
        console.log(`Inserted document with ID: ${result.insertedId}`);
        
    } finally {
        await client.close();
    }
}

connectToMongoDB();
```

## 🚨 Troubleshooting

### SSL Certificate Issues (macOS)

If you encounter SSL certificate issues on macOS, the connection string in `test_mongodb.py` includes `tlsAllowInvalidCertificates=True` to bypass this issue.

### Common Issues

1. **Connection timeout**: Check your IP address is whitelisted in MongoDB Atlas
2. **Authentication failed**: Verify your username and password
3. **Network issues**: Check your internet connection

## 📚 Resources

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Node.js Driver](https://docs.mongodb.com/drivers/node/)

Your MongoDB Atlas connection is ready to use! 🎉
