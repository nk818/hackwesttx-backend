#!/bin/bash

# 🚀 Railway Deployment Setup Script
# This script prepares your backend for Railway deployment

echo "🚀 Setting up HackWestTX Backend for Railway Deployment"
echo "=================================================="

# Initialize Git repository
echo "📁 Initializing Git repository..."
git init

# Add all files
echo "📝 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: HackWestTX Backend API with Railway deployment"

echo ""
echo "✅ Git repository initialized!"
echo ""
echo "📋 Next Steps:"
echo "1. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: hackwesttx-backend"
echo "   - Make it PUBLIC (required for Railway free tier)"
echo "   - Click 'Create repository'"
echo ""
echo "2. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/hackwesttx-backend.git"
echo "   git push -u origin main"
echo ""
echo "3. Deploy on Railway:"
echo "   - Go to https://railway.app"
echo "   - Sign up with GitHub"
echo "   - Click 'Deploy from GitHub repo'"
echo "   - Select your hackwesttx-backend repository"
echo ""
echo "4. Set Environment Variables in Railway:"
echo "   DJANGO_SETTINGS_MODULE=hackwesttx.settings"
echo "   DEBUG=False"
echo "   ALLOWED_HOSTS=*.railway.app"
echo "   MONGODB_URI=mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
echo ""
echo "🎉 Your backend will be live at: https://hackwesttx-backend-production.railway.app/"
echo ""
echo "📚 For detailed instructions, see: RAILWAY_DEPLOYMENT.md"
