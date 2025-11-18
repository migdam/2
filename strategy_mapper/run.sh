#!/bin/bash

echo "🚀 Starting Strategy Mapper..."
echo ""

# Check if database exists
if [ ! -f "strategy_mapper.db" ]; then
    echo "⚙️  Database not found. Initializing..."
    python db/init_db.py
    echo ""
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY environment variable is not set!"
    echo "Please set it using:"
    echo "  export OPENAI_API_KEY='your-key-here'"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🌟 Launching Streamlit app..."
streamlit run app.py
