"""
Test script for Thoughtful AI Support Agent
"""
import json
import os
from app import ThoughtfulAIAgent

def test_agent():
    """Test the AI agent functionality"""
    print("🧪 Testing Thoughtful AI Support Agent")
    print("=" * 50)
    
    # Initialize agent
    agent = ThoughtfulAIAgent()
    
    # Test cases
    test_cases = [
        {
            "question": "What does EVA do?",
            "expected_source": "ai_agent",
            "description": "Direct question about EVA (should use knowledge base)"
        },
        {
            "question": "Tell me about CAM",
            "expected_source": "ai_agent",
            "description": "Question about CAM (should use knowledge base)"
        },
        {
            "question": "How does PHIL work?",
            "expected_source": "ai_agent",
            "description": "Question about PHIL (should use knowledge base)"
        },
        {
            "question": "What are the benefits?",
            "expected_source": "ai_agent",
            "description": "Question about benefits (should use knowledge base)"
        },
        {
            "question": "Tell me about the agents",
            "expected_source": "ai_agent",
            "description": "General question about agents (should use knowledge base)"
        },
        {
            "question": "",
            "expected_source": "validation",
            "description": "Empty input validation"
        },
        {
            "question": "What's the weather today?",
            "expected_source": "ai_general",
            "description": "Unrelated question (general AI response)"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['description']}")
        print(f"   Question: '{test['question']}'")
        
        response = agent.get_response(test['question'])
        
        print(f"   Source: {response['source']}")
        print(f"   Answer: {response['answer'][:100]}...")
        
        if response['source'] == test['expected_source']:
            print("   ✅ PASSED")
            passed += 1
        else:
            print(f"   ❌ FAILED (expected {test['expected_source']}, got {response['source']})")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = test_agent()
    exit(0 if success else 1)

