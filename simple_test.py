#!/usr/bin/env python3
"""
Simple test without Unicode characters
"""
import asyncio
import sys
import traceback
from dotenv import load_dotenv
import os

async def test_everything():
    """Test all components"""
    print("=== AI Voice Agent Test ===")
    
    # Load environment
    load_dotenv()
    
    # Test 1: Basic imports
    print("\n1. Testing imports...")
    try:
        from livekit import api
        from livekit.agents import JobContext, WorkerOptions, cli
        from livekit.plugins import openai, silero, deepgram, rime
        from livekit.plugins import assemblyai as aai
        print("   OK - All imports successful")
    except Exception as e:
        print(f"   ERROR - Import failed: {e}")
        return False
    
    # Test 2: Environment variables
    print("\n2. Testing environment...")
    required_vars = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET', 'OPENAI_API_KEY']
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"   ERROR - Missing variables: {missing}")
        return False
    else:
        print("   OK - All environment variables set")
    
    # Test 3: LiveKit API
    print("\n3. Testing LiveKit API...")
    try:
        lkapi = api.LiveKitAPI()
        print("   OK - LiveKit API client created")
    except Exception as e:
        print(f"   ERROR - LiveKit API failed: {e}")
        return False
    
    # Test 4: CareAgent
    print("\n4. Testing CareAgent...")
    try:
        from calling_agent import CareAgent
        agent = CareAgent(lang_pref="en")
        print("   OK - CareAgent created successfully")
    except Exception as e:
        print(f"   ERROR - CareAgent failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 5: make_call function
    print("\n5. Testing make_call function...")
    try:
        from make_call import make_call
        phone_number = os.getenv("DEMO_PHONE_NUMBER", "+18556066468")
        print(f"   Testing call to: {phone_number}")
        await make_call(phone_number, reason="test", lang_pref="en", person_id="test-001")
        print("   OK - make_call executed successfully")
    except Exception as e:
        print(f"   ERROR - make_call failed: {e}")
        traceback.print_exc()
        return False
    
    print("\n=== All Tests Passed! ===")
    print("The AI voice agent app is working correctly!")
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_everything())
        if result:
            print("\nSUCCESS: App is ready to use!")
        else:
            print("\nFAILED: App has issues that need to be fixed.")
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
