#!/usr/bin/env python3
"""
Quick setup script to help configure environment variables for the voice agent.
"""

import os
from pathlib import Path

def create_env_file():
    """Create a .env file with the required variables"""
    
    print("🔧 Setting up Environment Variables for AI Voice Agent")
    print("=" * 60)
    
    # Get user input for required variables
    print("\n📋 Please provide the following information:")
    print("(Press Enter to skip optional fields)")
    
    # LiveKit Configuration
    print("\n🌐 LiveKit Configuration (REQUIRED for calls):")
    livekit_url = input("LiveKit URL (wss://your-project.livekit.cloud): ").strip()
    livekit_key = input("LiveKit API Key: ").strip()
    livekit_secret = input("LiveKit API Secret: ").strip()
    
    # SIP Configuration
    print("\n📞 SIP Configuration (REQUIRED for phone calls):")
    sip_trunk = input("SIP Trunk ID (ST_...): ").strip()
    phone_number = input("Phone number to call (+1234567890): ").strip()
    
    # AI Service Keys
    print("\n🤖 AI Service API Keys:")
    assemblyai_key = input("AssemblyAI API Key: ").strip()
    openai_key = input("OpenAI API Key: ").strip()
    rime_key = input("Rime API Key: ").strip()
    
    # Create .env content
    env_content = f"""# LiveKit Configuration (REQUIRED for calls)
LIVEKIT_URL={livekit_url or 'wss://your-project.livekit.cloud'}
LIVEKIT_API_KEY={livekit_key or 'your_api_key'}
LIVEKIT_API_SECRET={livekit_secret or 'your_api_secret'}

# SIP Configuration (REQUIRED for phone calls)
SIP_OUTBOUND_TRUNK_ID={sip_trunk or 'ST_your_trunk_id'}
DEMO_PHONE_NUMBER={phone_number or '+1234567890'}

# AI Service API Keys
ASSEMBLYAI_API_KEY={assemblyai_key or 'your_assemblyai_key'}
OPENAI_API_KEY={openai_key or 'your_openai_key'}
RIME_API_KEY={rime_key or 'your_rime_key'}

# Optional Configuration
LK_ROOM_NAME=care-room
LK_AGENT_NAME=voice-care-agent
DEFAULT_LANG_PREF=auto
ESCALATION_WEBHOOK_URL=
CALL_RESULT_WEBHOOK_URL=

# Rime TTS Configuration
RIME_MODEL=mist
RIME_SPEAKER=rainforest
RIME_SPEED=0.9

# LLM Configuration
LLM_MODEL=gpt-4o-mini
"""
    
    # Write .env file
    env_file = Path(".env")
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"\n✅ Created .env file with your configuration!")
    print(f"📁 Location: {env_file.absolute()}")
    
    # Show next steps
    print("\n🚀 Next Steps:")
    print("1. Get your API keys from the services listed above")
    print("2. Edit the .env file with your real credentials")
    print("3. Run: python make_call.py")
    
    # Check if we can run a test
    if livekit_url and livekit_key and livekit_secret:
        print("\n🧪 Test Configuration:")
        print("You can now test the system with:")
        print("  python make_call.py")
    else:
        print("\n⚠️  You still need to:")
        print("  - Get LiveKit credentials from https://livekit.io/")
        print("  - Set up a SIP trunk for phone calls")
        print("  - Get API keys for AI services")

def test_configuration():
    """Test the current configuration"""
    print("\n🔍 Testing Current Configuration...")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ No .env file found. Run setup first.")
        return
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check required variables
    required_vars = [
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY", 
        "LIVEKIT_API_SECRET",
        "SIP_OUTBOUND_TRUNK_ID",
        "DEMO_PHONE_NUMBER"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("your_") or value.startswith("wss://your-"):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete variables: {', '.join(missing_vars)}")
        print("Please edit your .env file with real values.")
    else:
        print("✅ Configuration looks good!")
        print("You can now run: python make_call.py")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Create .env file")
    print("2. Test current configuration")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_env_file()
    elif choice == "2":
        test_configuration()
    else:
        print("Invalid choice. Please run again and choose 1 or 2.")
