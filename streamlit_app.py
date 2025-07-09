"""
Streamlit Frontend for AI Chat Application
A modern, responsive chat interface that connects to the FastAPI backend
"""

import streamlit as st
import requests
import json
from typing import List, Dict, Any
import time

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend configuration - works both locally and on Render
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
BACKEND_URL = API_BASE_URL

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
    }
    .status-success {
        color: #4caf50;
        font-weight: bold;
    }
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_health() -> bool:
    """Check if the backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def clean_display_text(text: str) -> str:
    """Clean text for better display"""
    if not text:
        return text
    
    # Remove excessive whitespace while preserving paragraph breaks
    import re
    
    # Replace multiple spaces with single space
    cleaned = re.sub(r' +', ' ', text)
    
    # Clean up line breaks - preserve intentional formatting
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    
    # Remove trailing/leading whitespace
    cleaned = cleaned.strip()
    
    return cleaned

def send_message(prompt: str, history: List[Dict[str, str]]) -> str:
    """Send message to backend and get streaming response"""
    try:
        # Get user-configured parameters or use defaults
        max_tokens = st.session_state.get("max_tokens", 8192)
        temperature = st.session_state.get("temperature", 0.7)
        
        # Enhanced payload to match Google Cloud Console parameters
        payload = {
            "message": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=60  # Increased timeout for longer responses
        )
        
        if response.status_code == 200:
            response_data = response.json()
            raw_response = response_data.get("response", "❌ No response from AI model")
            model_used = response_data.get("model_used", "unknown")
            
            # Store response info for debugging
            st.session_state["last_response_info"] = {
                "length": len(raw_response),
                "model": model_used,
                "temp": temperature,
                "max_tokens": max_tokens
            }
            
            # Minimal cleaning to preserve content quality
            cleaned_response = raw_response.strip() if raw_response else "❌ No response from AI model"
            return cleaned_response
        else:
            error_detail = response.text
            try:
                error_json = response.json()
                if "detail" in error_json:
                    error_detail = str(error_json["detail"])
            except:
                pass
            return f"❌ Error: {response.status_code} - {error_detail}"
            
    except requests.RequestException as e:
        return f"❌ Connection error: {str(e)}"

def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>🤖 AI Chat Assistant</h1>
        <p>Powered by Fine-tuned Gemini Model on Vertex AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 System Status")
        
        # Check backend status
        if check_backend_health():
            st.markdown('<p class="status-success">✅ Backend: Connected</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-error">❌ Backend: Disconnected</p>', unsafe_allow_html=True)
            st.error("Please ensure the backend server is running on http://localhost:8000")
            st.stop()
        
        st.markdown("### ⚙️ Settings")
        
        # Advanced settings
        with st.expander("🔧 Advanced Parameters"):
            max_tokens = st.slider("Max Tokens", 1000, 16384, 8192, 1000)
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            
            # Store in session state
            st.session_state["max_tokens"] = max_tokens
            st.session_state["temperature"] = temperature
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        # Model info with endpoint details
        st.markdown("### 🧠 Model Info")
        st.info("""
        **Model**: Fine-tuned Gemini (TourismMalaysia)  
        **Provider**: Google Vertex AI  
        **Endpoint**: 6528596580524621824  
        **Features**: Enhanced tourism knowledge, Multi-turn conversation
        """)
        
        # Last response debug info
        if "last_response_info" in st.session_state:
            info = st.session_state["last_response_info"]
            st.markdown("### 📊 Last Response")
            st.json({
                "Response Length": f"{info['length']} chars",
                "Model Used": info['model'],
                "Temperature": info['temp'],
                "Max Tokens": info['max_tokens']
            })
        
        # Instructions
        st.markdown("### 💡 How to Use")
        st.markdown("""
        1. Type your message in the chat input
        2. Press Enter to send
        3. Watch the AI respond in real-time
        4. Continue the conversation naturally
        """)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    st.markdown("### 💬 Chat Conversation")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare conversation history for backend
        history = []
        for msg in st.session_state.messages[:-1]:  # Exclude the current prompt
            if msg["role"] == "user":
                history.append({"role": "user", "content": msg["content"]})
            else:
                history.append({"role": "assistant", "content": msg["content"]})

        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Show thinking animation
            with st.spinner("🤔 AI is thinking..."):
                response = send_message(prompt, history)
            
            # Display response
            message_placeholder.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Auto-scroll to bottom
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🚀 Built with FastAPI + Streamlit | Powered by Google Vertex AI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 