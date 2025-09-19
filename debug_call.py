#!/usr/bin/env python3
"""
Debug version of make_call.py to see what's happening during the call process
"""

import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from livekit import api
from datetime import datetime

# Load env
load_dotenv(dotenv_path=Path(__file__).parent / '.env')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("debug-call")

# Config
ROOM_NAME = os.getenv("LK_ROOM_NAME", "care-room")
AGENT_NAME = os.getenv("LK_AGENT_NAME", "voice-care-agent")
OUTBOUND_TRUNK_ID = os.getenv("SIP_OUTBOUND_TRUNK_ID")
DEMO_PHONE_NUMBER = os.getenv("DEMO_PHONE_NUMBER")
DEFAULT_LANG_PREF = os.getenv("DEFAULT_LANG_PREF", "auto")

async def debug_make_call(phone_number: str, reason: str = "weather", lang_pref: str = DEFAULT_LANG_PREF, person_id: str = "grandma-001"):
    """Debug version of make_call function"""
    logger.info(f"🚀 Starting call process...")
    logger.info(f"📞 Phone: {phone_number}")
    logger.info(f"🌐 LiveKit URL: {os.getenv('LIVEKIT_URL')}")
    logger.info(f"🔑 SIP Trunk: {OUTBOUND_TRUNK_ID}")
    
    try:
        # Initialize LiveKit API
        logger.info("🔧 Initializing LiveKit API...")
        lkapi = api.LiveKitAPI()
        logger.info("✅ LiveKit API initialized successfully")
        
        # Check SIP trunk
        if not OUTBOUND_TRUNK_ID or not OUTBOUND_TRUNK_ID.startswith("ST_"):
            logger.error(f"❌ SIP_OUTBOUND_TRUNK_ID is not set or invalid: {OUTBOUND_TRUNK_ID}")
            return
        
        logger.info(f"✅ SIP Trunk ID looks valid: {OUTBOUND_TRUNK_ID}")
        
        # Create call metadata
        call_metadata = f"phone={phone_number};reason={reason};langPref={lang_pref};personId={person_id};ts={datetime.utcnow().isoformat()}"
        logger.info(f"📋 Call metadata: {call_metadata}")
        
        # Create agent dispatch
        logger.info(f"🤖 Creating agent dispatch for agent={AGENT_NAME} room={ROOM_NAME}")
        dispatch = await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name=AGENT_NAME,
                room=ROOM_NAME,
                metadata=call_metadata
            )
        )
        logger.info(f"✅ Agent dispatch created: {dispatch}")
        
        # Create SIP participant
        logger.info(f"📞 Creating SIP participant for {phone_number} in room {ROOM_NAME}")
        sip_participant = await lkapi.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=ROOM_NAME,
                sip_trunk_id=OUTBOUND_TRUNK_ID,
                sip_call_to=phone_number,
                participant_identity=f"callee_{person_id}"
            )
        )
        logger.info(f"✅ SIP participant created: {sip_participant}")
        logger.info("🎉 Call initiated successfully! The AI agent should now be calling your phone.")
        
    except Exception as e:
        logger.error(f"❌ Error during call process: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await lkapi.aclose()

async def debug_main():
    """Debug main function"""
    logger.info("🏥 AI Voice Agent Call Debug")
    logger.info("=" * 50)
    
    phone_number = os.getenv("DEMO_PHONE_NUMBER")
    if not phone_number:
        logger.error("❌ DEMO_PHONE_NUMBER not set in environment")
        return
    
    logger.info(f"📱 Target phone number: {phone_number}")
    
    # Check if extreme weather (simulated)
    logger.info("🌤️ Checking for extreme weather...")
    extreme_weather = True  # Simulated
    logger.info(f"🌪️ Extreme weather detected: {extreme_weather}")
    
    if extreme_weather:
        logger.info("📞 Triggering call due to extreme weather...")
        await debug_make_call(phone_number, reason="weather", lang_pref="auto", person_id="grandma-001")
    else:
        logger.info("☀️ No extreme weather detected, no call needed.")

if __name__ == "__main__":
    asyncio.run(debug_main())
