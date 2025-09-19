#!/usr/bin/env python3
"""
Debug test to check if the app is actually working
"""
import asyncio
import sys
import traceback
import logging
from dotenv import load_dotenv
import os

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("debug_test")

async def test_make_call_function():
    """Test the make_call function directly"""
    print("=== Testing make_call function ===")
    
    try:
        # Load environment
        load_dotenv()
        
        # Import the function
        from make_call import make_call
        
        # Test with demo phone number
        phone_number = os.getenv("DEMO_PHONE_NUMBER")
        print(f"Testing call to: {phone_number}")
        
        # Call the function
        await make_call(phone_number, reason="test", lang_pref="en", person_id="test-001")
        print("✓ make_call function executed successfully")
        
    except Exception as e:
        print(f"✗ make_call function failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_agent_import():
    """Test importing the CareAgent"""
    print("\n=== Testing CareAgent import ===")
    
    try:
        from calling_agent import CareAgent
        print("✓ CareAgent imported successfully")
        
        # Try to create an instance
        agent = CareAgent(lang_pref="en")
        print("✓ CareAgent instance created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ CareAgent test failed: {e}")
        traceback.print_exc()
        return False

def test_livekit_api():
    """Test LiveKit API connection"""
    print("\n=== Testing LiveKit API ===")
    
    try:
        from livekit import api
        load_dotenv()
        
        # Create API client
        lkapi = api.LiveKitAPI()
        print("✓ LiveKit API client created")
        
        # Test environment variables
        url = os.getenv("LIVEKIT_URL")
        key = os.getenv("LIVEKIT_API_KEY")
        secret = os.getenv("LIVEKIT_API_SECRET")
        
        if url and key and secret:
            print(f"✓ LiveKit credentials configured: {url[:30]}...")
        else:
            print("✗ LiveKit credentials missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ LiveKit API test failed: {e}")
        traceback.print_exc()
        return False

async def main():
    """Run all debug tests"""
    print("=== AI Voice Agent Debug Test ===\n")
    
    # Test 1: LiveKit API
    api_ok = test_livekit_api()
    
    # Test 2: Agent import
    agent_ok = test_agent_import()
    
    # Test 3: Make call function
    call_ok = await test_make_call_function()
    
    print("\n=== Debug Test Results ===")
    print(f"LiveKit API: {'PASS' if api_ok else 'FAIL'}")
    print(f"CareAgent: {'PASS' if agent_ok else 'FAIL'}")
    print(f"make_call: {'PASS' if call_ok else 'FAIL'}")
    
    if api_ok and agent_ok and call_ok:
        print("\n🎉 All debug tests passed! The app should be working.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return api_ok and agent_ok and call_ok

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
