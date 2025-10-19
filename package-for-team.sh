#!/bin/bash

# 🚀 HackWestTX Class Portfolio API - Package for Team Sharing
# This script creates a clean package of your API for team distribution

echo "📦 Packaging HackWestTX Class Portfolio API for team sharing..."

# Create a clean copy directory
PACKAGE_DIR="HackWestTX-For-Team"
rm -rf "$PACKAGE_DIR"
mkdir "$PACKAGE_DIR"

# Copy essential files
echo "📋 Copying project files..."
cp -r api/ "$PACKAGE_DIR/"
cp -r hackwesttx/ "$PACKAGE_DIR/"
cp manage.py "$PACKAGE_DIR/"
cp requirements.txt "$PACKAGE_DIR/"
cp README.md "$PACKAGE_DIR/"
cp SETUP-FOR-TEAM.md "$PACKAGE_DIR/"
cp QUICK-START.md "$PACKAGE_DIR/"
cp env.example "$PACKAGE_DIR/"

# Remove unnecessary files
echo "🧹 Cleaning up unnecessary files..."
rm -rf "$PACKAGE_DIR/api/__pycache__"
rm -rf "$PACKAGE_DIR/hackwesttx/__pycache__"
rm -rf "$PACKAGE_DIR/api/migrations/__pycache__"
rm -f "$PACKAGE_DIR/db.sqlite3"
rm -f "$PACKAGE_DIR/db 2.sqlite3"

# Create a simple .gitignore
echo "📝 Creating .gitignore..."
cat > "$PACKAGE_DIR/.gitignore" << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Database
db.sqlite3
*.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
EOF

# Create a team welcome file
echo "👋 Creating team welcome file..."
cat > "$PACKAGE_DIR/TEAM-WELCOME.md" << EOF
# 🎉 Welcome to HackWestTX Class Portfolio API!

## 🚀 **Quick Start**
1. Read `QUICK-START.md` for immediate setup
2. Read `SETUP-FOR-TEAM.md` for detailed instructions
3. Read `README.md` for complete API documentation

## 📋 **What You Have**
- Complete Django REST API backend
- 8 core features implemented
- Token-based authentication
- SQLite database
- Comprehensive documentation

## 🎯 **Your Mission**
Build an amazing frontend that connects to this API!

## 🔗 **API Base URL**
\`http://localhost:8000/api/\`

## 📞 **Need Help?**
- Check the documentation files
- Test endpoints with Postman
- Use the Django admin at \`http://localhost:8000/admin/\`

**Happy coding! 🚀**
EOF

echo "✅ Package created successfully!"
echo "📁 Package location: $PACKAGE_DIR"
echo ""
echo "📦 To share with your team:"
echo "1. Zip the '$PACKAGE_DIR' folder"
echo "2. Send it to your team members"
echo "3. They follow the setup instructions in SETUP-FOR-TEAM.md"
echo ""
echo "🎯 Your team can start building the frontend immediately!"
