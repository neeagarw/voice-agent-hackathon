#!/usr/bin/env python3
"""
Simple call test to verify the system is working
"""

import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def simple_call_test():
    """Simple test to verify calling works"""
    print("📞 Simple Call Test")
    print("=" * 30)
    
    phone_number = os.getenv("DEMO_PHONE_NUMBER")
    sip_trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")
    
    print(f"📱 Calling: {phone_number}")
    print(f"🔑 Using SIP trunk: {sip_trunk_id}")
    
    try:
        lkapi = api.LiveKitAPI()
        
        # Create a simple room
        room_name = "simple-call-test"
        print(f"\n📁 Creating room: {room_name}")
        
        # Create agent dispatch first
        print("🤖 Creating agent dispatch...")
        dispatch = await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name="voice-care-agent",
                room=room_name,
                metadata="phone=" + phone_number + ";reason=test;langPref=auto"
            )
        )
        print(f"✅ Agent dispatch created: {dispatch.id}")
        
        # Wait a moment for agent to join
        print("⏳ Waiting for agent to join...")
        await asyncio.sleep(3)
        
        # Create SIP participant
        print("📞 Creating SIP participant...")
        sip_participant = await lkapi.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=room_name,
                sip_trunk_id=sip_trunk_id,
                sip_call_to=phone_number,
                participant_identity="test_caller"
            )
        )
        print(f"✅ SIP participant created: {sip_participant.participant_id}")
        print(f"📞 SIP Call ID: {sip_participant.sip_call_id}")
        
        # Check room status
        print("\n🔍 Checking room status...")
        await asyncio.sleep(5)
        
        rooms = await lkapi.room.list_rooms(api.ListRoomsRequest())
        for room in rooms.rooms:
            if room.name == room_name:
                print(f"📁 Room: {room.name}")
                print(f"👥 Participants: {room.num_participants}")
                
                # Get detailed participant info
                participants = await lkapi.room.list_participants(
                    api.ListParticipantsRequest(room=room_name)
                )
                print(f"👤 Participants:")
                for participant in participants.participants:
                    print(f"   - {participant.identity} ({participant.state})")
                    if hasattr(participant, 'name'):
                        print(f"     Name: {participant.name}")
        
        print(f"\n🎉 Call test completed!")
        print(f"📞 Your phone should have received a call to {phone_number}")
        print(f"🔍 If no call was received, check:")
        print(f"   1. Phone number is correct and reachable")
        print(f"   2. Phone is not busy or in airplane mode")
        print(f"   3. SIP trunk configuration in LiveKit dashboard")
        
        await lkapi.aclose()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simple_call_test())
