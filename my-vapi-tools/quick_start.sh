#!/bin/bash

# Quick Start Script for Vapi Tools
# This script helps you set up and test the Vapi tools

set -e

echo "🚀 Quick Start Script for Vapi Tools"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your actual credentials:"
    echo "   - SEARCHAPI_API_KEY: Your SearchAPI key"
    echo ""
    echo "   You can get this from:"
    echo "   - SearchAPI: https://www.searchapi.io/"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
else
    echo "✅ .env file already exists"
fi

# Check if SearchAPI key is configured
if ! grep -q "SEARCHAPI_API_KEY=.*[^[:space:]]" .env 2>/dev/null || grep -q "SEARCHAPI_API_KEY=your-searchapi-key-here" .env; then
    echo "❌ SEARCHAPI_API_KEY not configured in .env file"
    echo "Please add your SearchAPI key to the .env file"
    exit 1
fi

echo ""
echo "🧪 Testing the symptom search tool..."

# Run the test script
if python test_symptom_search.py; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Deploy the symptom_search_server.py to a cloud platform"
    echo "   - See DEPLOYMENT_GUIDE.md for detailed instructions"
    echo "   - Recommended: Render, Railway, or Heroku"
    echo ""
    echo "2. Create the tool in Vapi:"
    echo "   - Go to https://dashboard.vapi.ai"
    echo "   - Navigate to Tools section"
    echo "   - Create a new Function tool"
    echo "   - Use the webhook URL from your deployed server"
    echo ""
    echo "3. Add the tool to your assistant:"
    echo "   - Go to your Assistant in Vapi dashboard"
    echo "   - Add the symptom_search_tool"
    echo "   - Test with voice conversations"
    echo ""
    echo "📚 Documentation:"
    echo "   - README.md - This file"
    echo "   - SYMPTOM_SEARCH_README.md - Detailed setup guide"
    echo "   - DEPLOYMENT_GUIDE.md - Deployment instructions"
    echo ""
    echo "🔗 Useful Links:"
    echo "   - Vapi Dashboard: https://dashboard.vapi.ai"
    echo "   - SearchAPI: https://www.searchapi.io/"
    echo "   - Vapi Docs: https://docs.vapi.ai"
    echo ""
else
    echo ""
    echo "❌ Tests failed. Please check the errors above and try again."
    echo ""
    echo "Common issues:"
    echo "1. SEARCHAPI_API_KEY not configured correctly"
    echo "2. Internet connection issues"
    echo "3. SearchAPI service temporarily unavailable"
    echo ""
    exit 1
fi
