#!/usr/bin/env python3
"""
FastAPI server for voice chat with WebCareAgent
"""
import asyncio
import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from web_agent import WebCareAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice_chat_server")

app = FastAPI(title="Voice Chat with AI Agent")

# Store active agent sessions
active_sessions: Dict[str, WebCareAgent] = {}

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main chat interface"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <head><title>Voice Chat</title></head>
            <body>
                <h1>Voice Chat Interface</h1>
                <p>Please make sure index.html is in the same directory as this server.</p>
            </body>
        </html>
        """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time voice chat"""
    await websocket.accept()
    session_id = id(websocket)
    
    # Create new agent session
    agent = WebCareAgent(lang_pref="auto")
    active_sessions[session_id] = agent
    
    logger.info(f"New WebSocket connection: {session_id}")
    
    try:
        # Send initial greeting
        greeting = agent.get_greeting()
        await websocket.send_text(json.dumps({
            "type": "agent_response",
            "message": greeting,
            "language": agent.language
        }))
        
        # Handle incoming messages
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                if message_data["type"] == "user_message":
                    user_input = message_data["message"]
                    logger.info(f"Received user message: {user_input[:50]}...")
                    
                    # Process message with agent
                    response = await agent.process_message(user_input)
                    
                    # Send response back to client
                    await websocket.send_text(json.dumps({
                        "type": "agent_response",
                        "message": response,
                        "language": agent.language
                    }))
                    
                elif message_data["type"] == "reset_conversation":
                    # Reset the conversation
                    agent.reset_conversation()
                    greeting = agent.get_greeting()
                    await websocket.send_text(json.dumps({
                        "type": "agent_response",
                        "message": greeting,
                        "language": agent.language
                    }))
                    logger.info(f"Reset conversation for session: {session_id}")
                    
            except json.JSONDecodeError:
                logger.error("Invalid JSON received from client")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid message format"
                }))
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Clean up session
        if session_id in active_sessions:
            del active_sessions[session_id]
        logger.info(f"Cleaned up session: {session_id}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_sessions": len(active_sessions),
        "message": "Voice chat server is running"
    }

@app.get("/stats")
async def get_stats():
    """Get server statistics"""
    return {
        "active_sessions": len(active_sessions),
        "session_ids": list(active_sessions.keys())
    }

# Serve static files (CSS, JS)
try:
    app.mount("/static", StaticFiles(directory="."), name="static")
except Exception:
    logger.warning("Could not mount static files directory")

if __name__ == "__main__":
    print("🚀 Starting Voice Chat Server...")
    print("📱 Open your browser to: http://localhost:8000")
    print("🎤 Make sure to allow microphone access when prompted")
    print("💬 Click 'Start Talking' to begin voice conversation")
    print("\n" + "="*50)
    
    uvicorn.run(
        "voice_chat_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
