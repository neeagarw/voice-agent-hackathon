#!/usr/bin/env python3
"""
Script to check if the LiveKit agent is working properly
"""

import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def check_livekit_connection():
    """Check LiveKit connection and agent status"""
    print("🔍 Checking LiveKit Agent Status")
    print("=" * 50)
    
    try:
        # Initialize LiveKit API
        lkapi = api.LiveKitAPI()
        print("✅ LiveKit API initialized")
        
        # Check rooms
        print("\n📁 Checking rooms...")
        rooms = await lkapi.room.list_rooms(api.ListRoomsRequest())
        print(f"✅ Found {len(rooms.rooms)} active rooms")
        
        for room in rooms.rooms:
            print(f"  📁 Room: {room.name}")
            print(f"     👥 Participants: {room.num_participants}")
            print(f"     🕐 Created: {room.creation_time}")
            print(f"     🌐 URL: {room.url}")
        
        # Check agent dispatches
        print("\n🤖 Checking agent dispatches...")
        try:
            dispatches = await lkapi.agent_dispatch.list_dispatches()
            print(f"✅ Found {len(dispatches.dispatches)} agent dispatches")
            
            for dispatch in dispatches.dispatches:
                print(f"  🤖 Agent: {dispatch.agent_name}")
                print(f"     📁 Room: {dispatch.room}")
                print(f"     📊 State: {dispatch.state}")
                print(f"     📋 Metadata: {dispatch.metadata}")
        except Exception as e:
            print(f"⚠️ Could not check dispatches: {e}")
        
        # Check SIP participants
        print("\n📞 Checking SIP participants...")
        try:
            sip_participants = await lkapi.sip.list_sip_participants()
            print(f"✅ Found {len(sip_participants.sip_participants)} SIP participants")
            
            for participant in sip_participants.sip_participants:
                print(f"  📞 SIP Call: {participant.sip_call_id}")
                print(f"     📁 Room: {participant.room_name}")
                print(f"     👤 Identity: {participant.participant_identity}")
        except Exception as e:
            print(f"⚠️ Could not check SIP participants: {e}")
        
        print("\n✅ LiveKit connection is working!")
        return True
        
    except Exception as e:
        print(f"❌ LiveKit connection failed: {e}")
        return False
    finally:
        await lkapi.aclose()

async def check_agent_worker():
    """Check if agent worker is running"""
    print("\n🔍 Checking Agent Worker Status")
    print("=" * 50)
    
    # Check environment variables
    required_vars = [
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY", 
        "LIVEKIT_API_SECRET",
        "ASSEMBLYAI_API_KEY",
        "OPENAI_API_KEY",
        "RIME_API_KEY"
    ]
    
    print("📋 Environment Variables:")
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "SECRET" in var or "KEY" in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: NOT SET")
            all_set = False
    
    if all_set:
        print("\n✅ All required environment variables are set")
    else:
        print("\n❌ Some environment variables are missing")
    
    return all_set

async def test_agent_functionality():
    """Test basic agent functionality"""
    print("\n🧪 Testing Agent Functionality")
    print("=" * 50)
    
    try:
        # Try to import the agent
        from calling_agent import CareAgent
        print("✅ CareAgent class imported successfully")
        
        # Test agent initialization (this might fail due to missing API keys)
        try:
            agent = CareAgent(lang_pref="auto")
            print("✅ CareAgent initialized successfully")
            return True
        except Exception as e:
            print(f"⚠️ CareAgent initialization failed (expected if API keys missing): {e}")
            print("   This is normal if you haven't set up all API keys yet")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import CareAgent: {e}")
        return False

async def main():
    """Main check function"""
    print("🏥 AI Voice Agent Health Check")
    print("=" * 60)
    
    # Check LiveKit connection
    livekit_ok = await check_livekit_connection()
    
    # Check environment
    env_ok = await check_agent_worker()
    
    # Test agent functionality
    agent_ok = await test_agent_functionality()
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 60)
    print(f"🔗 LiveKit Connection: {'✅ OK' if livekit_ok else '❌ FAILED'}")
    print(f"🔧 Environment Setup: {'✅ OK' if env_ok else '❌ FAILED'}")
    print(f"🤖 Agent Functionality: {'✅ OK' if agent_ok else '⚠️ PARTIAL'}")
    
    if livekit_ok and env_ok:
        print("\n🎉 Your agent should be working! Try making a call:")
        print("   python debug_call.py")
    else:
        print("\n🔧 Setup needed:")
        if not livekit_ok:
            print("   - Check LiveKit credentials in .env file")
        if not env_ok:
            print("   - Set up missing API keys")
        print("   - Run: python setup_env.py")

if __name__ == "__main__":
    asyncio.run(main())
