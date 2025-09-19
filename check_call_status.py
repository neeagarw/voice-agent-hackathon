#!/usr/bin/env python3
"""
Check the status of the current call
"""

import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def check_call_status():
    """Check the current call status"""
    print("🔍 Checking Call Status")
    print("=" * 40)
    
    try:
        lkapi = api.LiveKitAPI()
        
        # Check active rooms
        rooms = await lkapi.room.list_rooms(api.ListRoomsRequest())
        print(f"📁 Active rooms: {len(rooms.rooms)}")
        
        for room in rooms.rooms:
            print(f"  📁 Room: {room.name}")
            print(f"     👥 Participants: {room.num_participants}")
            print(f"     🕐 Created: {room.creation_time}")
            
            # Get room participants
            participants = await lkapi.room.list_participants(
                api.ListParticipantsRequest(room=room.name)
            )
            print(f"     👤 Participant details:")
            for participant in participants.participants:
                print(f"       - {participant.identity} ({participant.state})")
        
        # Check if there are any SIP participants
        try:
            sip_participants = await lkapi.sip.list_sip_participants()
            print(f"\n📞 SIP Participants: {len(sip_participants.sip_participants)}")
            for sip in sip_participants.sip_participants:
                print(f"  📞 SIP Call: {sip.sip_call_id}")
                print(f"     📁 Room: {sip.room_name}")
                print(f"     👤 Identity: {sip.participant_identity}")
        except Exception as e:
            print(f"⚠️ Could not check SIP participants: {e}")
        
        await lkapi.aclose()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_call_status())
