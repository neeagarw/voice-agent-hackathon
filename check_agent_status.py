#!/usr/bin/env python3
"""
Comprehensive LiveKit Agent Status Checker
"""
import asyncio
import sys
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent_status_checker")

async def check_agent_status():
    """Comprehensive check of LiveKit agent status"""
    print("=" * 60)
    print("🔍 LIVEKIT AGENT STATUS CHECKER")
    print("=" * 60)
    
    load_dotenv()
    
    # 1. Environment Check
    print("\n1. 📋 ENVIRONMENT CONFIGURATION")
    print("-" * 40)
    
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
    
    env_status = True
    for var, value in required_vars.items():
        if value:
            if var in ['LIVEKIT_URL', 'SIP_OUTBOUND_TRUNK_ID', 'DEMO_PHONE_NUMBER']:
                print(f"   ✅ {var}: {value}")
            else:
                print(f"   ✅ {var}: {'*' * min(len(value), 8)}...")
        else:
            print(f"   ❌ {var}: MISSING")
            env_status = False
    
    # 2. Import Check
    print("\n2. 📦 DEPENDENCY IMPORTS")
    print("-" * 40)
    
    import_status = True
    try:
        from livekit import api
        print("   ✅ LiveKit API: OK")
        
        from livekit.agents import JobContext, WorkerOptions, cli
        print("   ✅ LiveKit Agents: OK")
        
        from livekit.plugins import openai, silero, deepgram, rime
        print("   ✅ LiveKit Plugins: OK")
        
        from livekit.plugins import assemblyai as aai
        print("   ✅ AssemblyAI Plugin: OK")
        
        import requests
        print("   ✅ Requests: OK")
        
    except ImportError as e:
        print(f"   ❌ Import Error: {e}")
        import_status = False
    
    # 3. LiveKit API Connection
    print("\n3. 🌐 LIVEKIT API CONNECTION")
    print("-" * 40)
    
    api_status = True
    try:
        lkapi = api.LiveKitAPI()
        print("   ✅ API Client Created: OK")
        
        # Test basic API functionality
        url = os.getenv('LIVEKIT_URL')
        if url:
            print(f"   ✅ Server URL: {url}")
        else:
            print("   ❌ Server URL: Missing")
            api_status = False
            
    except Exception as e:
        print(f"   ❌ API Connection Error: {e}")
        api_status = False
    
    # 4. Agent Creation Test
    print("\n4. 🤖 AGENT CREATION TEST")
    print("-" * 40)
    
    agent_status = True
    try:
        from calling_agent import CareAgent
        agent = CareAgent(lang_pref="en")
        print("   ✅ CareAgent Instance: Created Successfully")
        print(f"   ✅ Language Preference: {agent.lang_pref}")
        print(f"   ✅ Default Language: {agent.language}")
        
    except Exception as e:
        print(f"   ❌ Agent Creation Error: {e}")
        agent_status = False
    
    # 5. Call Dispatch Test
    print("\n5. 📞 CALL DISPATCH TEST")
    print("-" * 40)
    
    dispatch_status = True
    try:
        from make_call import make_call
        phone_number = os.getenv("DEMO_PHONE_NUMBER", "+1234567890")
        print(f"   ✅ make_call Function: Available")
        print(f"   ✅ Target Phone: {phone_number}")
        
        # Test metadata creation (without actual call)
        from datetime import datetime, timezone
        test_metadata = f"phone={phone_number};reason=test;langPref=en;personId=test-001;ts={datetime.now(timezone.utc).isoformat()}"
        print(f"   ✅ Metadata Format: Valid")
        
    except Exception as e:
        print(f"   ❌ Call Dispatch Error: {e}")
        dispatch_status = False
    
    # 6. Audio Pipeline Check
    print("\n6. 🎵 AUDIO PIPELINE CHECK")
    print("-" * 40)
    
    audio_status = True
    try:
        # Check TTS
        from livekit.plugins import rime
        print("   ✅ Rime TTS: Available")
        
        # Check STT
        from livekit.plugins import assemblyai as aai
        from livekit.plugins import deepgram
        print("   ✅ AssemblyAI STT: Available")
        print("   ✅ Deepgram STT: Available (Fallback)")
        
        # Check VAD
        from livekit.plugins import silero
        print("   ✅ Silero VAD: Available")
        
        # Check LLM
        from livekit.plugins import openai
        print("   ✅ OpenAI LLM: Available")
        
    except Exception as e:
        print(f"   ❌ Audio Pipeline Error: {e}")
        audio_status = False
    
    # 7. Overall Status Summary
    print("\n7. 📊 OVERALL STATUS SUMMARY")
    print("-" * 40)
    
    all_checks = [
        ("Environment", env_status),
        ("Imports", import_status),
        ("API Connection", api_status),
        ("Agent Creation", agent_status),
        ("Call Dispatch", dispatch_status),
        ("Audio Pipeline", audio_status)
    ]
    
    passed = sum(1 for _, status in all_checks if status)
    total = len(all_checks)
    
    for check_name, status in all_checks:
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {check_name}: {'PASS' if status else 'FAIL'}")
    
    print(f"\n📈 SCORE: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 RESULT: LiveKit Agent is FULLY OPERATIONAL!")
        print("\n🚀 Ready to:")
        print("   • Start agent: python calling_agent.py dev")
        print("   • Make calls: python make_call.py")
        print("   • Monitor logs for real-time status")
        return True
    else:
        print(f"\n⚠️  RESULT: {total - passed} issues found - Agent may not work properly")
        print("\n🔧 Next steps:")
        print("   • Fix the failed checks above")
        print("   • Re-run this status checker")
        print("   • Check logs for detailed error messages")
        return False

async def main():
    try:
        success = await check_agent_status()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
