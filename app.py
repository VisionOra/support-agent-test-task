import streamlit as st
import json
import os
from openai import OpenAI
from difflib import SequenceMatcher
from pathlib import Path

# Load environment variables from .env file
def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

# Page configuration
st.set_page_config(
    page_title="Thoughtful AI Support Agent",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .agent-message {
        background-color: #f1f8e9;
        border-left: 4px solid #8bc34a;
    }
    .header-title {
        color: #1976d2;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

class ThoughtfulAIAgent:
    """AI Agent for Thoughtful AI customer support"""
    
    def __init__(self, data_path="data.json"):
        """Initialize the agent with predefined Q&A data"""
        self.qa_data = self._load_data(data_path)
        self.openai_client = None
        self._initialize_openai()
    
    def _load_data(self, data_path):
        """Load predefined Q&A data from JSON file"""
        try:
            with open(data_path, 'r') as f:
                data = json.load(f)
                return data.get('questions', [])
        except FileNotFoundError:
            st.error(f"Error: Data file '{data_path}' not found.")
            return []
        except json.JSONDecodeError:
            st.error(f"Error: Invalid JSON format in '{data_path}'.")
            return []
    
    def _initialize_openai(self):
        """Initialize OpenAI client for AI responses"""
        api_key = os.environ.get('OPENAI_API_KEY')
        
        if not api_key:
            st.error("⚠️ No OpenAI API key found. Please set OPENAI_API_KEY in .env file.")
            return
            
        try:
            # Initialize with minimal parameters to avoid compatibility issues
            self.openai_client = OpenAI(api_key=api_key)
            # Test the connection
            st.success("✅ OpenAI client initialized successfully!")
        except TypeError as e:
            if 'proxies' in str(e):
                # Fallback for older OpenAI versions
                try:
                    import openai
                    openai.api_key = api_key
                    self.openai_client = openai
                    st.success("✅ OpenAI client initialized (legacy mode)!")
                except Exception as e2:
                    st.error(f"❌ OpenAI initialization failed: {str(e2)}")
                    self.openai_client = None
            else:
                st.error(f"❌ OpenAI initialization error: {str(e)}")
                self.openai_client = None
        except Exception as e:
            st.error(f"❌ OpenAI initialization error: {str(e)}")
            self.openai_client = None
    
    def _calculate_similarity(self, text1, text2):
        """Calculate similarity score between two texts"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _find_best_match(self, user_question, threshold=0.5):
        """
        Find the best matching answer from predefined Q&A
        
        Args:
            user_question: User's input question
            threshold: Minimum similarity score to consider a match
            
        Returns:
            Tuple of (answer, confidence_score) or (None, 0) if no match
        """
        if not self.qa_data:
            return None, 0
        
        best_match = None
        best_score = 0
        
        user_question_lower = user_question.lower()
        
        for qa in self.qa_data:
            question = qa.get('question', '')
            answer = qa.get('answer', '')
            
            # Calculate similarity score
            score = self._calculate_similarity(user_question_lower, question)
            
            # Also check for keyword matching to improve accuracy
            keywords = ['eva', 'cam', 'phil', 'eligibility', 'claims', 'payment', 
                       'verification', 'processing', 'posting', 'agents', 'benefits', 
                       'thoughtful']
            
            keyword_boost = 0
            for keyword in keywords:
                if keyword in user_question_lower and keyword in question.lower():
                    keyword_boost += 0.15
            
            total_score = min(score + keyword_boost, 1.0)
            
            if total_score > best_score:
                best_score = total_score
                best_match = answer
        
        if best_score >= threshold:
            return best_match, best_score
        
        return None, 0
    
    def _get_fallback_response(self, user_question):
        """Get response from OpenAI when no predefined answer matches"""
        if not self.openai_client:
            return ("I apologize, but I don't have specific information about that topic. "
                   "I'm specialized in answering questions about Thoughtful AI's automation agents "
                   "(EVA, CAM, and PHIL). Could you please rephrase your question or ask about "
                   "our agents?")
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant. "
                     "Provide concise, friendly responses to user questions."},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return (f"I encountered an issue processing your question. "
                   f"Please try asking about Thoughtful AI's agents (EVA, CAM, or PHIL).")
    
    def _get_relevant_context(self, user_question):
        """
        Get relevant context from predefined Q&A for RAG
        
        Args:
            user_question: User's input question
            
        Returns:
            String with relevant context or None
        """
        if not self.qa_data:
            return None
        
        # Find top matching Q&A pairs
        matches = []
        user_question_lower = user_question.lower()
        
        for qa in self.qa_data:
            question = qa.get('question', '')
            answer = qa.get('answer', '')
            
            # Calculate similarity score
            score = self._calculate_similarity(user_question_lower, question)
            
            # Keyword boosting
            keywords = ['eva', 'cam', 'phil', 'eligibility', 'claims', 'payment', 
                       'verification', 'processing', 'posting', 'agents', 'benefits', 
                       'thoughtful']
            
            keyword_boost = 0
            for keyword in keywords:
                if keyword in user_question_lower and keyword in question.lower():
                    keyword_boost += 0.15
            
            total_score = min(score + keyword_boost, 1.0)
            
            if total_score > 0.3:  # Lower threshold for context retrieval
                matches.append({
                    'question': question,
                    'answer': answer,
                    'score': total_score
                })
        
        # Sort by score and take top 3
        matches.sort(key=lambda x: x['score'], reverse=True)
        top_matches = matches[:3]
        
        if not top_matches:
            return None
        
        # Format context
        context = "Here is relevant information from our knowledge base:\n\n"
        for i, match in enumerate(top_matches, 1):
            context += f"{i}. Q: {match['question']}\n   A: {match['answer']}\n\n"
        
        return context
    
    def _get_llm_response(self, user_question, context=None):
        """
        Get response from LLM with optional context
        
        Args:
            user_question: User's input question
            context: Optional context from knowledge base
            
        Returns:
            String response from LLM
        """
        if not self.openai_client:
            # If no OpenAI client, fall back to direct matching
            answer, confidence = self._find_best_match(user_question, threshold=0.5)
            if answer:
                return answer
            return ("I apologize, but I need an OpenAI API key to provide intelligent responses. "
                   "Please set the OPENAI_API_KEY environment variable.")
        
        try:
            # Build system message
            system_message = (
                "You are a helpful customer support AI agent for Thoughtful AI, a company that provides "
                "AI-powered automation agents for healthcare processes. "
                "Your role is to assist users with questions about Thoughtful AI's products and services. "
                "Be friendly, professional, and concise in your responses."
            )
            
            if context:
                system_message += f"\n\n{context}"
                system_message += (
                    "\nUse the above information to answer questions about Thoughtful AI's agents. "
                    "If the question is about our agents (EVA, CAM, PHIL), use the provided information. "
                    "For other questions, provide helpful general responses."
                )
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback to direct matching if LLM fails
            answer, confidence = self._find_best_match(user_question, threshold=0.5)
            if answer:
                return answer
            return (f"I'm having trouble processing your question right now. "
                   f"Please try asking about Thoughtful AI's agents (EVA, CAM, or PHIL).")
    
    def get_response(self, user_question):
        """
        Get response for user question using LLM with RAG
        
        Args:
            user_question: User's input question
            
        Returns:
            Dictionary with response and metadata
        """
        if not user_question or not user_question.strip():
            return {
                "answer": "Please ask me a question about Thoughtful AI's agents!",
                "source": "validation",
                "confidence": 0
            }
        
        # Get relevant context from knowledge base
        context = self._get_relevant_context(user_question)
        
        # Determine if this is about Thoughtful AI's agents
        is_about_agents = context is not None
        
        # Get LLM response with context
        answer = self._get_llm_response(user_question, context)
        
        return {
            "answer": answer,
            "source": "ai_agent" if is_about_agents else "ai_general",
            "confidence": 1.0 if is_about_agents else 0.5
        }

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'agent' not in st.session_state:
        st.session_state.agent = ThoughtfulAIAgent()

def display_chat_message(role, content, metadata=None):
    """Display a chat message with styling"""
    if role == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br/>
                {content}
            </div>
        """, unsafe_allow_html=True)
    else:
        source_badge = ""
        if metadata:
            source = metadata.get('source', '')
            if source == 'ai_agent':
                source_badge = " <small>🎯 (Using Knowledge Base)</small>"
            elif source == 'ai_general':
                source_badge = " <small>💭 (General Response)</small>"
        
        st.markdown(f"""
            <div class="chat-message agent-message">
                <strong>🤖 Thoughtful AI Agent:</strong>{source_badge}<br/>
                {content}
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="header-title">🤖 Thoughtful AI Support Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Powered by GPT - Ask me anything about our AI-powered automation agents!</div>', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(
            message['role'], 
            message['content'],
            message.get('metadata')
        )
    
    # Chat input
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get agent response
        with st.spinner("Thinking..."):
            response = st.session_state.agent.get_response(user_input)
        
        # Add agent response to chat history
        st.session_state.messages.append({
            "role": "agent",
            "content": response['answer'],
            "metadata": {
                "source": response['source'],
                "confidence": response['confidence']
            }
        })
        
        # Rerun to display new messages
        st.rerun()
    
    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.info(
            "This AI agent helps answer questions about Thoughtful AI's automation agents:\n\n"
            "- **EVA**: Eligibility Verification Agent\n"
            "- **CAM**: Claims Processing Agent\n"
            "- **PHIL**: Payment Posting Agent"
        )
        
        st.header("Sample Questions")
        sample_questions = [
            "What does EVA do?",
            "Tell me about CAM",
            "How does PHIL work?",
            "What are the benefits of using Thoughtful AI's agents?"
        ]
        
        for question in sample_questions:
            if st.button(question, key=question):
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })
                response = st.session_state.agent.get_response(question)
                st.session_state.messages.append({
                    "role": "agent",
                    "content": response['answer'],
                    "metadata": {
                        "source": response['source'],
                        "confidence": response['confidence']
                    }
                })
                st.rerun()
        
        st.divider()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()

