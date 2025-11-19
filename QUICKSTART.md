# Quick Start Guide

Get the Thoughtful AI Support Agent running in under 2 minutes!

## 🚀 Option 1: Using the Run Script (Easiest)

```bash
./run.sh
```

That's it! The script will:
- Create a virtual environment
- Install dependencies
- Start the application at http://localhost:8501

## 🐳 Option 2: Using Docker (Recommended for Production)

### Build and Run with Docker

```bash
# Build the image
docker build -t thoughtful-ai-agent .

# Run the container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_api_key_here \
  thoughtful-ai-agent
```

### Or use Docker Compose

```bash
# Make sure .env file has your API key
docker-compose up -d
```

## 💻 Option 3: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variable (optional)
export OPENAI_API_KEY=your_api_key_here

# 5. Run the app
streamlit run app.py
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
source venv/bin/activate
python test_agent.py
```

## 📝 Sample Questions to Try

Once the app is running, try these questions:

- "What does EVA do?"
- "Tell me about the claims processing agent"
- "How does PHIL work?"
- "What are the benefits of using Thoughtful AI's agents?"
- "Tell me about Thoughtful AI's Agents"

## 🔧 Troubleshooting

**Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

**Need to stop Docker container?**
```bash
docker-compose down
```

**Clear Streamlit cache?**
```bash
streamlit cache clear
```

## 📚 More Information

See [README.md](README.md) for detailed documentation.

