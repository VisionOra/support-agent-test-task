# Thoughtful AI Customer Support Agent

An intelligent customer support AI agent built for Thoughtful AI that uses GPT-3.5-turbo with Retrieval Augmented Generation (RAG) to answer questions about their automation agents (EVA, CAM, and PHIL). The agent combines a curated knowledge base with the power of large language models to provide accurate, conversational responses.

![Thoughtful AI Support Agent](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Features

- 🤖 **AI-Powered Responses**: Uses GPT-3.5-turbo for intelligent, conversational responses
- 📚 **RAG Architecture**: Retrieval Augmented Generation with predefined knowledge base
- 💬 **Conversational UI**: Clean, modern chat interface built with Streamlit
- 🎯 **Context-Aware**: Automatically retrieves relevant information from knowledge base
- 🛡️ **Error Handling**: Robust error handling for invalid inputs and edge cases
- 🔄 **Graceful Fallback**: Works with or without OpenAI API key (limited functionality)

## Predefined Knowledge Base

The agent can answer questions about:

- **EVA (Eligibility Verification Agent)**: Automates patient eligibility verification
- **CAM (Claims Processing Agent)**: Streamlines claims submission and management
- **PHIL (Payment Posting Agent)**: Automates payment posting to patient accounts
- **General Benefits**: Information about Thoughtful AI's agent benefits

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd ta
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. **Choose your deployment method**:

#### Option A: Local Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

#### Option B: Docker Deployment (Recommended)

```bash
# Build the Docker image
docker build -t thoughtful-ai-agent .

# Run the container
docker run -p 8501:8501 -e OPENAI_API_KEY=your_api_key_here thoughtful-ai-agent
```

4. **Access the application**:
   - Open your browser and navigate to `http://localhost:8501`

## Usage

1. **Ask Questions**: Type your question in the chat input at the bottom of the page
2. **View Responses**: The agent will respond with the most relevant answer
3. **Sample Questions**: Click on sample questions in the sidebar for quick testing
4. **Clear History**: Use the "Clear Chat History" button to start fresh

### Example Questions

- "What does EVA do?"
- "Tell me about the claims processing agent"
- "How does PHIL work?"
- "What are the benefits of using Thoughtful AI's agents?"

## Project Structure

```
ta/
├── app.py                 # Main Streamlit application
├── data.json             # Predefined Q&A dataset
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Architecture

### Core Components

1. **ThoughtfulAIAgent Class**:
   - Loads and manages predefined Q&A data
   - Implements semantic similarity matching
   - Handles fallback to OpenAI API
   - Provides confidence scoring

2. **Similarity Matching Algorithm**:
   - Uses `SequenceMatcher` for text similarity
   - Implements keyword boosting for better accuracy
   - Configurable threshold (default: 40%)

3. **Streamlit UI**:
   - Modern chat interface with custom CSS
   - Session state management for chat history
   - Sidebar with helpful information and quick actions

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for fallback responses (optional but recommended)

### Customization

To modify the predefined Q&A dataset, edit `data.json`:

```json
{
    "questions": [
        {
            "question": "Your question here",
            "answer": "Your answer here"
        }
    ]
}
```

## Error Handling

The application includes comprehensive error handling for:

- Missing or invalid data files
- Invalid JSON format
- OpenAI API errors
- Empty or invalid user inputs
- Network connectivity issues

## Technical Details

### Dependencies

- **streamlit**: Web UI framework
- **openai**: OpenAI API client for fallback responses

### RAG (Retrieval Augmented Generation) Architecture

The agent uses a sophisticated RAG approach:

1. **Context Retrieval**: Finds relevant Q&A pairs from the knowledge base using semantic similarity
2. **Context Injection**: Provides top matching context to the LLM
3. **AI Generation**: GPT-3.5-turbo generates natural, conversational responses based on the context
4. **Graceful Fallback**: If no relevant context is found, provides general helpful responses

This approach combines the accuracy of predefined knowledge with the flexibility of AI.

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements.txt

# Run the application in development mode
streamlit run app.py --server.runOnSave true
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

### Common Issues

**Issue**: "Data file not found"
- **Solution**: Ensure `data.json` is in the same directory as `app.py`

**Issue**: OpenAI API errors
- **Solution**: Check that your API key is valid and has sufficient credits

**Issue**: Port 8501 already in use
- **Solution**: Stop other Streamlit instances or use a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

## Performance

- **Response Time**: < 1 second for predefined answers
- **Fallback Time**: 1-3 seconds for OpenAI responses
- **Memory Usage**: ~50MB base + session data

## Security Considerations

- API keys should be stored in environment variables, never in code
- The `.env` file is excluded from version control
- Input validation prevents injection attacks

## License

This project is created for the Thoughtful AI technical assessment.

## Contact

For questions or issues, please contact the development team.

---

Built with ❤️ for Thoughtful AI

