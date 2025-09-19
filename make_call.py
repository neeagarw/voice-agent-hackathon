import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from livekit import api
from datetime import datetime, timezone

# Load env
load_dotenv()

logger = logging.getLogger("make-call")
logger.setLevel(logging.INFO)

# Config
ROOM_NAME = os.getenv("LK_ROOM_NAME", "care-room")
AGENT_NAME = os.getenv("LK_AGENT_NAME", "Agent care")
OUTBOUND_TRUNK_ID = os.getenv("SIP_OUTBOUND_TRUNK_ID")
DEFAULT_LANG_PREF = os.getenv("DEFAULT_LANG_PREF", "auto")  # "auto" | "en" | "es"
USE_CALENDAR = os.getenv("USE_CALENDAR", "false").lower() == "true"

async def make_call(phone_number: str, reason: str = "weather", lang_pref: str = DEFAULT_LANG_PREF, person_id: str = "grandma-001"):
    """
    Create a dispatch and add a SIP participant to call the phone number.
    `reason` helps the agent tailor tone/script (e.g., 'weather' vs 'medication').
    `lang_pref` can be 'auto', 'en', or 'es'.
    """
    lkapi = api.LiveKitAPI()
    if not OUTBOUND_TRUNK_ID or not OUTBOUND_TRUNK_ID.startswith("ST_"):
        logger.error("SIP_OUTBOUND_TRUNK_ID is not set or invalid")
        return

    # Metadata the agent can read on join (JSON string is common; here we keep it simple)
    call_metadata = f"phone={phone_number};reason={reason};langPref={lang_pref};personId={person_id};" \
                    f"ts={datetime.now(timezone.utc).isoformat()}"

    logger.info(f"[dispatch] creating for agent={AGENT_NAME} room={ROOM_NAME}, reason={reason}, lang={lang_pref}")
    dispatch = await lkapi.agent_dispatch.create_dispatch(
        api.CreateAgentDispatchRequest(
            agent_name=AGENT_NAME,
            room=ROOM_NAME,
            metadata=call_metadata
        )
    )
    logger.info(f"[dispatch] created: {dispatch}")

    logger.info(f"[sip] dialing {phone_number} to room {ROOM_NAME}")
    try:
        sip_participant = await lkapi.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=ROOM_NAME,
                sip_trunk_id=OUTBOUND_TRUNK_ID,
                sip_call_to=phone_number,
                participant_identity=f"callee_{person_id}"
            )
        )
        logger.info(f"[sip] participant created: {sip_participant}")
    except Exception as e:
        logger.error(f"[sip] Error creating SIP participant: {e}")
    finally:
        await lkapi.aclose()

# --- Optional scheduling (disabled for demo). Kept here for completeness.
async def schedule_medication_calls_if_enabled():
    if not USE_CALENDAR:
        logger.info("[schedule] Calendar scheduling disabled. Skipping.")
        return
    # TODO: Pull today's med times and call make_call(...) at those times.
    # Keep empty for demo, to avoid complexity.

# --- Weather trigger (primary demo path)
async def trigger_call_on_extreme_weather(phone_number: str, person_id: str = "grandma-001"):
    """
    Pseudo-check for 'extreme' weather and fire the call. In your worker,
    replace this with real alert ingestion (OpenWeather/NWS) and thresholds.
    """
    extreme = await is_extreme_weather(person_id)
    if extreme:
        await make_call(phone_number, reason="weather", lang_pref="auto", person_id=person_id)
    else:
        logger.info("[weather] No extreme weather detected, no call queued.")

async def is_extreme_weather(person_id: str) -> bool:
    # TODO: Replace with real API check for person's location (OpenWeather One Call alerts or NWS)
    # For demo, just return True to show flow, or wire to your actual worker.
    return True

async def main():
    phone_number = os.getenv("DEMO_PHONE_NUMBER")
    await trigger_call_on_extreme_weather(phone_number)

if __name__ == "__main__":
    asyncio.run(main())
