#!/usr/bin/env python3
"""
Web-friendly version of CareAgent for voice chat interface
"""
import logging
import os
import re
from dotenv import load_dotenv
from livekit.plugins import openai

load_dotenv()

logger = logging.getLogger("web-agent")
logger.setLevel(logging.INFO)

HELP_KEYWORDS = ("help", "ayuda", "emergency", "auxilio")
NEGATIVE_WORDS = ("sick", "dizzy", "pain", "cold", "alone", "sad", "mal", "tos", "dolor", "triste")

class WebCareAgent:
    def __init__(self, lang_pref: str = "en"):
        """Initialize the web-friendly care agent"""
        self.lang_pref = lang_pref
        self.language = "en"  # English only
        self.conversation_history = []
        
        # Initialize OpenAI LLM
        llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.llm = openai.LLM(model=llm_model)
        
        # Web-friendly instructions
        self.instructions = """
You are a caring AI health assistant designed for elder care check-ins. Your personality:

1) Be warm, empathetic, and genuinely caring - like a helpful family member
2) Keep responses short and clear (1-2 sentences usually)
3) Focus on health and wellness check-ins
4) Ask about medications, how they're feeling, if they need anything
5) Be encouraging and supportive
6) Adapt to the user's language (English/Spanish) naturally

Your conversation flow should be:
- Greet warmly and ask how they're feeling
- Ask about medications: "Did you take your medications today?"
- If they say yes: "That's great! Please take care and rest well."
- If they say no: "It's important to take them. Can you take them now?"
- Ask if they need anything or have any concerns
- Always end with caring words like "Take care" or "I'm here if you need me"

Remember: You're here to provide caring health check-ins, not casual chat.
"""
        
        logger.info("WebCareAgent initialized successfully")
    
    async def process_message(self, user_input: str) -> str:
        """Process user input and generate response"""
        try:
            # Detect language and update if needed
            self._detect_language(user_input)
            
            # Check for help/distress keywords
            if self._check_for_distress(user_input):
                return self._handle_distress()
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Generate response using LLM
            response = await self._generate_response(user_input)
            
            # Add response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep conversation history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            logger.info(f"Generated response for user input: {user_input[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return self._get_error_response()
    
    def _detect_language(self, text: str):
        """Language detection disabled - English only"""
        pass
    
    def _check_for_distress(self, text: str) -> bool:
        """Check if user needs help or is in distress"""
        text_lower = text.lower()
        return (any(keyword in text_lower for keyword in HELP_KEYWORDS) or
                any(word in text_lower for word in NEGATIVE_WORDS) or
                "emergency" in text_lower)
    
    def _handle_distress(self) -> str:
        """Handle distress situations with empathy"""
        return "I can hear that you might be going through something difficult. I'm here to listen and support you. Would you like to tell me more about how you're feeling?"
    
    async def _generate_response(self, user_input: str) -> str:
        """Generate response using rule-based logic"""
        try:
            # Simple rule-based responses for common medication-related inputs
            user_lower = user_input.lower()
            
            # Check for medication responses
            if any(word in user_lower for word in ["yes", "took", "taken", "already", "finished"]):
                return "That's wonderful! I'm so glad you took your medications. How are you feeling today?"
            
            elif any(word in user_lower for word in ["no", "not", "haven't", "didn't", "forgot"]):
                return "It's important to take your medications. Can you take them now? I'm here to support you."
            
            elif any(word in user_lower for word in ["good", "fine", "well", "okay", "great"]):
                return "OK, take care and I will call you back in a few hours."
            
            elif any(word in user_lower for word in ["bad", "sick", "pain", "hurt", "tired"]):
                return "I'm sorry to hear that. Would you like to tell me more about how you're feeling? I'm here to listen."
            
            else:
                # Default friendly response
                return "I understand. Is there anything specific I can help you with today? Take care of yourself."
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_error_response()
    
    def _get_error_response(self) -> str:
        """Get appropriate error response"""
        return "Sorry, I had a small hiccup there. Could you repeat what you said?"
    
    def get_greeting(self) -> str:
        """Get initial greeting message"""
        return "Hi there! How are you feeling today? Did you take your medications?"
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        self.language = "en"
        logger.info("Conversation reset")
