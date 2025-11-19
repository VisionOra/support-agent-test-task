#!/bin/bash

# Thoughtful AI Support Agent - Quick Start Script

echo "🤖 Thoughtful AI Support Agent"
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your OpenAI API key"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the application
echo ""
echo "🚀 Starting Thoughtful AI Support Agent..."
echo "📍 The app will open at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py

