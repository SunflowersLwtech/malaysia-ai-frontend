#!/usr/bin/env python3
"""
Malaysia AI Travel Guide - Streamlit Frontend
Beautiful web interface for the Malaysia AI Travel Guide
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

# Page configuration
st.set_page_config(
    page_title="Malaysia AI Travel Guide",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API configuration
BACKEND_URL = "https://malaysia-ai-guide-api.onrender.com"

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #4ECDC4;
        background-color: #f0f2f6;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .ai-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .status-card {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .suggestion-button {
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        cursor: pointer;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

class MalaysiaAIFrontend:
    """Frontend application for Malaysia AI Travel Guide"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session_id = self._get_session_id()
        
    def _get_session_id(self) -> str:
        """Get or create session ID"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        return st.session_state.session_id
    
    def check_backend_status(self) -> Dict[str, Any]:
        """Check if backend is available"""
        try:
            response = requests.get(f"{self.backend_url}/api/status", timeout=10)
            if response.status_code == 200:
                return {"status": "online", "data": response.json()}
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "offline", "message": str(e)}
    
    def send_chat_message(self, message: str, location: Optional[str] = None) -> Dict[str, Any]:
        """Send message to backend AI"""
        try:
            payload = {
                "message": message,
                "user_id": self.session_id,
                "location": location
            }
            
            response = requests.post(
                f"{self.backend_url}/api/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "message": "Sorry, I'm having trouble connecting right now. Please try again!"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "message": "I'm experiencing connection issues. Please check your internet and try again!"
            }
    
    def get_knowledge_base(self) -> Dict[str, Any]:
        """Get knowledge base from backend"""
        try:
            response = requests.get(f"{self.backend_url}/api/knowledge", timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def send_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """Send feedback to backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/feedback",
                json=feedback_data,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

def main():
    """Main application function"""
    app = MalaysiaAIFrontend()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🇲🇾 Malaysia AI Travel Guide</h1>
        <p>Discover the best food, destinations, and experiences in Malaysia!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Quick Actions")
        
        # Backend status check
        status = app.check_backend_status()
        if status["status"] == "online":
            st.markdown("""
            <div class="status-card">
                <strong>✅ AI Guide Online</strong><br>
                Ready to help you explore Malaysia!
            </div>
            """, unsafe_allow_html=True)
            
            backend_data = status.get("data", {})
            st.write(f"🤖 Knowledge Items: {backend_data.get('knowledge_items', 'N/A')}")
            st.write(f"🧠 AI Status: {'Active' if backend_data.get('has_ai') else 'Fallback Mode'}")
            
        else:
            st.error(f"❌ Backend Status: {status['status']}")
            st.write("Please check your connection or try again later.")
        
        st.markdown("---")
        
        # Location input
        st.markdown("### 📍 Your Location (Optional)")
        user_location = st.text_input(
            "Where are you visiting?",
            placeholder="e.g., Kuala Lumpur, Penang, Langkawi"
        )
        
        st.markdown("---")
        
        # Knowledge explorer
        st.markdown("### 📚 Knowledge Explorer")
        knowledge = app.get_knowledge_base()
        
        if knowledge:
            categories = knowledge.get("categories", {})
            for category, items in categories.items():
                with st.expander(f"{category.title()} ({len(items)} items)"):
                    for item in items[:3]:  # Show first 3 items
                        st.write(f"• {item['content'][:100]}...")
        
        st.markdown("---")
        
        # Feedback section
        st.markdown("### 💭 Feedback")
        if st.button("📝 Give Feedback"):
            st.session_state.show_feedback = True

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        st.markdown("### 💬 Chat with Malaysia AI")
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Suggested questions
        st.markdown("**💡 Try asking about:**")
        suggestions = [
            "What are the best Malaysian dishes to try?",
            "Top destinations to visit in Malaysia",
            "Best street food in Penang",
            "Things to do in Kuala Lumpur",
            "Malaysian desserts I should try"
        ]
        
        # Create suggestion buttons
        cols = st.columns(3)
        for i, suggestion in enumerate(suggestions):
            with cols[i % 3]:
                if st.button(suggestion, key=f"suggestion_{i}"):
                    st.session_state.user_input = suggestion
        
        # Chat input
        user_input = st.text_input(
            "Ask me anything about Malaysia:",
            placeholder="e.g., What's the best food in Penang?",
            key="chat_input"
        )
        
        # Handle suggestion clicks
        if hasattr(st.session_state, 'user_input'):
            user_input = st.session_state.user_input
            delattr(st.session_state, 'user_input')
        
        # Send message
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                "type": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            
            # Show loading
            with st.spinner("🤔 Thinking about your question..."):
                # Get AI response
                response = app.send_chat_message(user_input, user_location)
            
            # Add AI response to history
            ai_message = response.get("message", "I'm sorry, I couldn't process your request right now.")
            st.session_state.chat_history.append({
                "type": "ai",
                "content": ai_message,
                "sources": response.get("sources", []),
                "suggestions": response.get("suggestions", []),
                "timestamp": datetime.now()
            })
            
            # Clear input
            st.rerun()
        
        # Display chat history
        for i, chat in enumerate(reversed(st.session_state.chat_history[-10:])):  # Show last 10 messages
            if chat["type"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑 You:</strong><br>
                    {chat["content"]}
                </div>
                """, unsafe_allow_html=True)
            
            else:  # AI message
                st.markdown(f"""
                <div class="chat-message ai-message">
                    <strong>🤖 Malaysia AI Guide:</strong><br>
                    {chat["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Show sources if available
                if chat.get("sources"):
                    with st.expander("📚 Sources"):
                        for source in chat["sources"]:
                            st.write(f"• {source.get('content', 'N/A')}")
                
                # Show suggestions if available
                if chat.get("suggestions"):
                    st.markdown("**💡 Related questions:**")
                    for suggestion in chat["suggestions"]:
                        if st.button(suggestion, key=f"followup_{i}_{hash(suggestion)}"):
                            st.session_state.user_input = suggestion
                            st.rerun()

    with col2:
        # Quick info panel
        st.markdown("### 🇲🇾 Malaysia Quick Facts")
        
        quick_facts = [
            "🏛️ **Capital**: Kuala Lumpur",
            "🗣️ **Languages**: Malay, English, Chinese, Tamil",
            "💰 **Currency**: Malaysian Ringgit (MYR)",
            "🌡️ **Climate**: Tropical, hot and humid",
            "🍜 **Famous For**: Street food, diverse cuisine",
            "🏝️ **Top Islands**: Langkawi, Penang, Perhentian"
        ]
        
        for fact in quick_facts:
            st.markdown(fact)
        
        st.markdown("---")
        
        # Weather info (placeholder)
        st.markdown("### 🌤️ Weather Tips")
        st.info("Malaysia has a tropical climate year-round. Pack light, breathable clothing and don't forget an umbrella for sudden rain showers!")
        
        st.markdown("---")
        
        # Travel tips
        st.markdown("### ✈️ Travel Tips")
        tips = [
            "Try hawker centers for authentic local food",
            "Learn basic Malay greetings",
            "Respect local customs and dress codes",
            "Use Grab for convenient transportation",
            "Bargain at markets but not in malls"
        ]
        
        for tip in tips:
            st.write(f"💡 {tip}")

    # Feedback modal
    if st.session_state.get("show_feedback"):
        with st.form("feedback_form"):
            st.markdown("### 📝 Share Your Feedback")
            
            rating = st.slider("How helpful was the AI guide?", 1, 5, 5)
            feedback_text = st.text_area("Tell us about your experience:")
            
            submitted = st.form_submit_button("Submit Feedback")
            
            if submitted:
                feedback_data = {
                    "rating": rating,
                    "feedback_text": feedback_text,
                    "timestamp": datetime.now().isoformat(),
                    "session_id": app.session_id
                }
                
                if app.send_feedback(feedback_data):
                    st.success("Thank you for your feedback! 🙏")
                    st.session_state.show_feedback = False
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Failed to send feedback. Please try again.")

if __name__ == "__main__":
    main() 