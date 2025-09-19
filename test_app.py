#!/usr/bin/env python3
"""
Test script to verify the AI voice agent app is working properly
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        # Basic imports
        import asyncio
        import logging
        from dotenv import load_dotenv
        print("✓ Basic Python imports successful")
        
        # LiveKit core
        from livekit import api
        print("✓ LiveKit API imported")
        
        # LiveKit agents
        from livekit.agents import JobContext, WorkerOptions, cli
        from livekit.agents.voice import Agent, AgentSession
        print("✓ LiveKit agents imported")
        
        # LiveKit plugins
        from livekit.plugins import openai, silero, deepgram, rime
        print("✓ LiveKit plugins imported")
        
        # AssemblyAI plugin
        from livekit.plugins import assemblyai as aai
        print("✓ AssemblyAI plugin imported")
        
        # Other dependencies
        import requests
        import json
        import re
        print("✓ Additional dependencies imported")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\nTesting environment variables...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'LIVEKIT_URL',
            'LIVEKIT_API_KEY', 
            'LIVEKIT_API_SECRET',
            'OPENAI_API_KEY',
            'ASSEMBLYAI_API_KEY',
            'RIME_API_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if value:
                print(f"✓ {var}: {'*' * min(len(value), 10)}...")
            else:
                print(f"✗ {var}: Not set")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"Missing environment variables: {missing_vars}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Environment test error: {e}")
        return False

def test_agent_creation():
    """Test creating the CareAgent"""
    print("\nTesting agent creation...")
    
    try:
        # Import the CareAgent class
        sys.path.append(str(Path(__file__).parent))
        from calling_agent import CareAgent
        
        # Try to create an agent instance
        agent = CareAgent(lang_pref="en")
        print("✓ CareAgent created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent creation error: {e}")
        return False

def test_api_connection():
    """Test LiveKit API connection"""
    print("\nTesting LiveKit API connection...")
    
    try:
        from livekit import api
        from dotenv import load_dotenv
        load_dotenv()
        
        # Create API client
        lkapi = api.LiveKitAPI()
        print("✓ LiveKit API client created")
        
        return True
        
    except Exception as e:
        print(f"✗ API connection error: {e}")
        return False

def main():
    """Run all tests"""
    print("=== AI Voice Agent App Test ===\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment), 
        ("Agent Creation Test", test_agent_creation),
        ("API Connection Test", test_api_connection)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n=== Test Results ===")
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The app should work correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
