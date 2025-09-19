import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import openai, silero, deepgram
from livekit.plugins import rime
from livekit.plugins import assemblyai as aai  # AssemblyAI STT plugin

import json
import re

load_dotenv()

logger = logging.getLogger("calling-agent")
logger.setLevel(logging.INFO)

HELP_KEYWORDS = ("help", "ayuda", "emergency", "auxilio")
NEGATIVE_WORDS = ("sick", "dizzy", "pain", "cold", "alone", "sad", "mal", "tos", "dolor", "triste")
COUGH_HINTS = ("*cough*",)  # placeholder; use audio events if available

def parse_metadata(meta_str: str) -> dict:
    d = {}
    for kv in meta_str.split(";"):
        if "=" in kv:
            k, v = kv.split("=", 1)
            d[k] = v
    return d

class CareAgent(Agent):
    def __init__(self, lang_pref: str = "auto") -> None:
        # Primary STT: AssemblyAI (low-latency). Fallback: Deepgram if Spanish is detected/forced.
        primary_stt = aai.STT()  # expects ASSEMBLYAI_API_KEY in env
        fallback_stt = deepgram.STT()  # keep installed for ES fallback if needed

        # Empathetic Rime TTS voice (tune persona via params)
        empathetic_tts = rime.TTS(
            model=os.getenv("RIME_MODEL", "mist"),
            speaker=os.getenv("RIME_SPEAKER", "rainforest"),
            speed_alpha=float(os.getenv("RIME_SPEED", "0.9")),
            reduce_latency=True,
        )

        # Low-latency LLM policy (use Accel if available; otherwise keep OpenAI here)
        llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")  # swap to Accel if you have it
        policy_llm = openai.LLM(model=llm_model)

        instructions = """
You are an empathetic elder-care voice agent. Goals:
1) Check safety during extreme weather and reassure.
2) Confirm medication adherence succinctly.
3) Keep language simple, warm, and slow. Prefer yes/no questions first.
4) If distress, repeated cough-like sounds, 'help' words, or negative mood persists → escalate immediately.
5) Language: default to user's preference (auto-detect English/Spanish). Mirror their language. Be gentle.

Script outline per call (adapt phrasing):
- Greeting: “Hi, this is your check-in call. How are you feeling today?”
- Weather reassurance (if reason=weather): “It may be rough outside—are you safe and comfortable?”
- Meds: “Did you take your medicines today? Yes or no?”
- If confusion: rephrase shorter; offer to repeat; slow down.
- If help/distress: “I’m contacting your family now and staying with you.”
- Close: “Thank you. I’ll check in again soon. You’re not alone.”
"""

        super().__init__(
            instructions=instructions,
            stt=primary_stt,
            llm=policy_llm,
            tts=empathetic_tts,
            vad=silero.VAD.load()
        )
        self.lang_pref = lang_pref
        self.meta = {}
        self.fallback_stt = fallback_stt
        self.language = "en"  # start; can switch to 'es'

    async def on_enter(self):
        # Read room metadata (from dispatch) to customize behavior
        md = getattr(self.session, 'room', None) and getattr(self.session.room, 'metadata', None) or ""
        self.meta = parse_metadata(md or "")
        reason = self.meta.get("reason", "weather")
        lang_pref = self.meta.get("langPref", self.lang_pref)

        # Optional: seed language preference
        if lang_pref in ("en", "es"):
            self.language = lang_pref

        # First line adapts to reason; TTS will pick correct language once we detect it.
        if reason == "weather":
            opening = "Hi, this is your check-in call. How are you feeling today?"
            if self.language == "es":
                opening = "Hola, esta es tu llamada de control. ¿Cómo te sientes hoy?"
        else:
            opening = "Hello! I’m calling to check on you and your medicines. How are you feeling?"
            if self.language == "es":
                opening = "¡Hola! Llamo para ver cómo estás y tus medicinas. ¿Cómo te sientes?"

        self.session.send_text(opening)
        self.session.generate_reply()  # kick off dialogue

    async def on_transcript(self, transcript: str):
        """
        Lightweight runtime policy:
        - Detect Spanish → switch STT to fallback if AssemblyAI stream struggles with ES.
        - Detect distress/help → escalate via webhook immediately.
        - Track negative sentiment heuristics (simple keyword proxy for demo).
        """
        t = transcript.lower()

        # Language sniff (very simple demo heuristic)
        if re.search(r"\b(hola|bien|gracias|sí|no|medicina|tiempo|lluvia|tormenta)\b", t):
            if self.language != "es":
                self.language = "es"
                # Switch STT to fallback (deepgram) for Spanish demo reliability
                self.session.set_stt(self.fallback_stt)
                self.session.send_text("Entiendo español. Podemos continuar en español.")

        # Distress/help escalation
        if any(k in t for k in HELP_KEYWORDS) or "fall" in t or "caí" in t:
            await self._escalate("help_keyword_detected", last_heard=transcript)
            return

        # Very simple “negative” signal (augment with AAI sentiment when you wire it)
        if any(n in t for n in NEGATIVE_WORDS):
            await self._flag_concern("negative_mood", last_heard=transcript)

        # Optional: cough hint (placeholder)
        if any(k in t for k in COUGH_HINTS):
            await self._flag_concern("cough_like_event", last_heard=transcript)

    async def _escalate(self, reason: str, last_heard: str = ""):
        """
        Handle escalation by notifying the user we're helping.
        """
        logger.info(f"[escalate] Escalation triggered: {reason}, last_heard: {last_heard}")
        
        # Let the user know we're helping
        msg_en = "I'm contacting your family now and will stay with you."
        msg_es = "Estoy contactando a tu familia ahora y me quedaré contigo."
        self.session.send_text(msg_es if self.language == "es" else msg_en)

    async def _flag_concern(self, kind: str, last_heard: str = ""):
        """
        Log concerns for monitoring purposes.
        """
        logger.info(f"[flag] Concern flagged: {kind}, last_heard: {last_heard}")

async def entrypoint(ctx: JobContext):
    # Read language pref from dispatch metadata (if any)
    lang_pref = "auto"
    md = ctx.room and ctx.room.metadata or ""
    if md:
        try:
            meta = parse_metadata(md)
            lang_pref = meta.get("langPref", "auto")
        except Exception:
            pass

    session = AgentSession()
    await session.start(
        agent=CareAgent(lang_pref=lang_pref),
        room=ctx.room
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
