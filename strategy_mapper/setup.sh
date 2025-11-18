#!/bin/bash

echo "📦 Strategy Mapper Setup"
echo "========================"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo ""

# Initialize database
echo "🗄️  Initializing database..."
python db/init_db.py
echo ""

# Make run script executable
chmod +x run.sh

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Set your OpenAI API key:"
echo "     export OPENAI_API_KEY='your-key-here'"
echo ""
echo "  2. Run the app:"
echo "     ./run.sh"
echo ""
