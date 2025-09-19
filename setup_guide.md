# 📞 How to Make the AI Voice Agent Call a Phone Number

## 🎯 Overview
This system makes actual phone calls using LiveKit's SIP integration. Here's exactly what you need to do:

## 🔧 Step 1: Get Required API Keys

### 1.1 LiveKit (Required for calls)
1. Go to https://livekit.io/
2. Sign up for a free account
3. Create a new project
4. Get your credentials:
   - **Server URL**: `wss://your-project.livekit.cloud`
   - **API Key**: `APIxxxxxxxxxxxx`
   - **API Secret**: `your-secret-key`

### 1.2 AssemblyAI (Speech-to-Text)
1. Go to https://www.assemblyai.com/
2. Sign up for free account
3. Get your API key from dashboard

### 1.3 OpenAI (Language Model)
1. Go to https://openai.com/
2. Sign up and get API key
3. Add some credits ($5-10 should be enough for testing)

### 1.4 Rime (Text-to-Speech)
1. Go to https://rime.ai/
2. Sign up for free account
3. Get your API key

## 🔧 Step 2: Set Up Environment Variables

Create a `.env` file in your project directory:

```env
# LiveKit Configuration (REQUIRED for calls)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=APIxxxxxxxxxxxx
LIVEKIT_API_SECRET=your-secret-key

# SIP Trunk (REQUIRED for phone calls)
SIP_OUTBOUND_TRUNK_ID=ST_your_trunk_id

# Phone Number to Call
DEMO_PHONE_NUMBER=+1234567890

# AI Service API Keys
ASSEMBLYAI_API_KEY=your_assemblyai_key
OPENAI_API_KEY=your_openai_key
RIME_API_KEY=your_rime_key

# Optional Configuration
LK_ROOM_NAME=care-room
LK_AGENT_NAME=voice-care-agent
DEFAULT_LANG_PREF=auto
```

## 🔧 Step 3: Set Up SIP Trunk (For Actual Phone Calls)

### Option A: Use LiveKit's SIP (Recommended)
1. In your LiveKit dashboard, go to "SIP" section
2. Create a new SIP trunk
3. Get the trunk ID (starts with "ST_")
4. Add it to your `.env` file

### Option B: Use Your Own SIP Provider
1. Get SIP credentials from providers like:
   - Twilio
   - Vonage
   - Your telecom provider
2. Configure in LiveKit dashboard

## 🚀 Step 4: Run the System

```bash
# Make sure you're in the project directory
cd "C:\Users\Ananta Verma\work\My projects\AI voice agents hackathon"

# Run the call dispatcher
python make_call.py
```

## 📱 What Happens When You Run It

1. **System checks for "extreme weather"** (currently simulated as True)
2. **Creates a LiveKit room** with the AI agent
3. **Makes a SIP call** to your phone number
4. **AI agent answers** and conducts conversation:
   - "Hi, this is your check-in call. How are you feeling today?"
   - Checks medication adherence
   - Monitors for safety concerns
   - Escalates if help is needed

## 🧪 Testing Without Real Phone Calls

If you want to test the agent logic without making actual calls:

```bash
# Set a test phone number
set DEMO_PHONE_NUMBER=+1234567890

# Run with mock SIP (will show what would happen)
python make_call.py
```

## 🔍 Troubleshooting

### Common Issues:
1. **"url must be set"** → Set LIVEKIT_URL in .env
2. **"SIP_OUTBOUND_TRUNK_ID is not set"** → Set up SIP trunk in LiveKit
3. **"AssemblyAI API key is required"** → Set ASSEMBLYAI_API_KEY
4. **Call doesn't connect** → Check phone number format (+1234567890)

### Phone Number Format:
- Use international format: `+1234567890`
- Include country code
- No spaces or dashes

## 💡 Quick Test Setup

For a quick test, you can use these mock values (won't make real calls):

```env
LIVEKIT_URL=wss://demo.livekit.io
LIVEKIT_API_KEY=demo_key
LIVEKIT_API_SECRET=demo_secret
SIP_OUTBOUND_TRUNK_ID=ST_demo_trunk
DEMO_PHONE_NUMBER=+1234567890
ASSEMBLYAI_API_KEY=your_real_key
OPENAI_API_KEY=your_real_key
RIME_API_KEY=your_real_key
```

This will show you the system flow without making actual calls.
