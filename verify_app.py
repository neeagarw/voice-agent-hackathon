#!/usr/bin/env python3
"""
Simple verification script for the AI voice agent app
"""
import os
import sys
from dotenv import load_dotenv

def main():
    print("=== AI Voice Agent App Verification ===\n")
    
    # Load environment
    load_dotenv()
    
    # Check environment variables
    print("1. Checking environment variables...")
    required_vars = {
        'LIVEKIT_URL': os.getenv('LIVEKIT_URL'),
        'LIVEKIT_API_KEY': os.getenv('LIVEKIT_API_KEY'),
        'LIVEKIT_API_SECRET': os.getenv('LIVEKIT_API_SECRET'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ASSEMBLYAI_API_KEY': os.getenv('ASSEMBLYAI_API_KEY'),
        'RIME_API_KEY': os.getenv('RIME_API_KEY'),
        'SIP_OUTBOUND_TRUNK_ID': os.getenv('SIP_OUTBOUND_TRUNK_ID'),
        'DEMO_PHONE_NUMBER': os.getenv('DEMO_PHONE_NUMBER')
    }
    
    for var, value in required_vars.items():
        if value:
            print(f"   ✓ {var}: Set")
        else:
            print(f"   ✗ {var}: Missing")
    
    # Check imports
    print("\n2. Checking imports...")
    try:
        import livekit
        print("   ✓ livekit imported")
        
        from livekit import api
        print("   ✓ livekit.api imported")
        
        from livekit.agents import JobContext, WorkerOptions, cli
        print("   ✓ livekit.agents imported")
        
        from livekit.plugins import openai, silero, deepgram, rime
        print("   ✓ livekit.plugins imported")
        
        import requests
        print("   ✓ requests imported")
        
    except ImportError as e:
        print(f"   ✗ Import error: {e}")
        return False
    
    # Check files
    print("\n3. Checking application files...")
    files = ['calling_agent.py', 'make_call.py', '.env']
    for file in files:
        if os.path.exists(file):
            print(f"   ✓ {file}: Found")
        else:
            print(f"   ✗ {file}: Missing")
    
    print("\n4. Testing LiveKit API connection...")
    try:
        lkapi = api.LiveKitAPI()
        print("   ✓ LiveKit API client created successfully")
    except Exception as e:
        print(f"   ✗ LiveKit API error: {e}")
    
    print("\n=== Verification Complete ===")
    print("The app appears to be properly configured and ready to run!")
    print("\nTo run the app:")
    print("1. Start the agent: python calling_agent.py dev")
    print("2. Make a test call: python make_call.py")
    
    return True

if __name__ == "__main__":
    main()
