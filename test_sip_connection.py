#!/usr/bin/env python3
"""
Test SIP connection and troubleshoot call issues
"""

import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def test_sip_connection():
    """Test SIP connection and call setup"""
    print("🔍 Testing SIP Connection")
    print("=" * 50)
    
    # Check environment variables
    sip_trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")
    phone_number = os.getenv("DEMO_PHONE_NUMBER")
    livekit_url = os.getenv("LIVEKIT_URL")
    
    print(f"📞 Phone Number: {phone_number}")
    print(f"🔑 SIP Trunk ID: {sip_trunk_id}")
    print(f"🌐 LiveKit URL: {livekit_url}")
    
    if not sip_trunk_id or not sip_trunk_id.startswith("ST_"):
        print("❌ Invalid SIP Trunk ID")
        return
    
    try:
        lkapi = api.LiveKitAPI()
        print("✅ LiveKit API connected")
        
        # Test creating a room first
        room_name = "test-room"
        print(f"\n📁 Creating test room: {room_name}")
        
        try:
            # Try to create a room
            room = await lkapi.room.create_room(api.CreateRoomRequest(name=room_name))
            print(f"✅ Room created: {room.name}")
        except Exception as e:
            print(f"⚠️ Room creation failed: {e}")
            # Room might already exist, that's okay
        
        # Test SIP participant creation
        print(f"\n📞 Testing SIP participant creation...")
        try:
            sip_participant = await lkapi.sip.create_sip_participant(
                api.CreateSIPParticipantRequest(
                    room_name=room_name,
                    sip_trunk_id=sip_trunk_id,
                    sip_call_to=phone_number,
                    participant_identity="test_caller"
                )
            )
            print(f"✅ SIP participant created successfully!")
            print(f"   Participant ID: {sip_participant.participant_id}")
            print(f"   SIP Call ID: {sip_participant.sip_call_id}")
            print(f"   Room: {sip_participant.room_name}")
            
            # Wait a moment to see if connection is established
            print("\n⏳ Waiting 10 seconds to check connection...")
            await asyncio.sleep(10)
            
            # Check room status
            rooms = await lkapi.room.list_rooms(api.ListRoomsRequest())
            active_room = None
            for room in rooms.rooms:
                if room.name == room_name:
                    active_room = room
                    break
            
            if active_room:
                print(f"✅ Room is active with {active_room.num_participants} participants")
                
                # Get participants
                participants = await lkapi.room.list_participants(
                    api.ListParticipantsRequest(room=room_name)
                )
                print(f"👥 Participants in room:")
                for participant in participants.participants:
                    print(f"   - {participant.identity} ({participant.state})")
            else:
                print("⚠️ Room not found or not active")
                
        except Exception as e:
            print(f"❌ SIP participant creation failed: {e}")
            print("\n🔧 Troubleshooting suggestions:")
            print("1. Check if SIP trunk ID is correct")
            print("2. Verify phone number format (+1234567890)")
            print("3. Check if SIP trunk is active in LiveKit dashboard")
            print("4. Ensure you have sufficient credits/balance")
        
        await lkapi.aclose()
        
    except Exception as e:
        print(f"❌ LiveKit API error: {e}")

if __name__ == "__main__":
    asyncio.run(test_sip_connection())
