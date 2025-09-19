# AI Voice Agent Hackathon - Elder Care Voice Agent

An empathetic AI voice agent designed for elder care, built with LiveKit, AssemblyAI, Rime TTS, and OpenAI. This system provides automated check-in calls, safety monitoring, and emergency escalation for elderly individuals.

## 🌟 Features

- **🤖 Empathetic AI Agent**: Warm, caring conversation in English and Spanish
- **📞 Real Phone Calls**: SIP telephony integration for actual phone calls
- **🌪️ Weather Safety**: Automated check-ins during extreme weather
- **💊 Medication Monitoring**: Daily medication adherence checking
- **🚨 Emergency Escalation**: Automatic family notification when help is needed
- **🌍 Bilingual Support**: Auto-detects and switches between English/Spanish
- **🛡️ Safety Monitoring**: Real-time detection of distress keywords and negative sentiment

## 🏗️ Architecture

### Core Components
- **`calling_agent.py`**: Main AI voice agent implementation
- **`make_call.py`**: SIP call dispatch and management system
- **`debug_call.py`**: Testing and debugging utilities
- **`check_agent.py`**: System health monitoring
- **`setup_env.py`**: Environment configuration helper

### AI Services Integration
- **AssemblyAI**: Speech-to-text with low latency
- **Rime TTS**: Empathetic voice synthesis
- **OpenAI GPT-4o-mini**: Conversational AI logic
- **LiveKit**: Real-time communication platform

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- LiveKit Cloud account
- API keys for AssemblyAI, OpenAI, and Rime

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/neeagarw/voice-agent-hackathon.git
cd voice-agent-hackathon

# Install dependencies
pip install livekit-agents livekit-plugins-openai livekit-plugins-silero livekit-plugins-deepgram livekit-plugins-rime livekit-plugins-assemblyai python-dotenv requests

# Configure environment
python setup_env.py
```

### 3. Environment Configuration
Create a `.env` file with your API credentials:
```env
# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# AI Service API Keys
ASSEMBLYAI_API_KEY=your_assemblyai_key
OPENAI_API_KEY=your_openai_key
RIME_API_KEY=your_rime_key

# SIP Configuration
SIP_OUTBOUND_TRUNK_ID=ST_your_trunk_id
DEMO_PHONE_NUMBER=+1234567890

# Optional
LK_ROOM_NAME=care-room
LK_AGENT_NAME=voice-care-agent
DEFAULT_LANG_PREF=auto
```

### 4. Run the System
```bash
# Start the agent worker
python calling_agent.py dev

# In another terminal, make a call
python debug_call.py
```

## 📞 How It Works

### Call Flow
1. **Trigger**: System detects extreme weather or scheduled check-in
2. **Dispatch**: Creates LiveKit room with AI agent
3. **Call**: Makes SIP call to elderly person's phone
4. **Conversation**: AI agent conducts empathetic conversation
5. **Monitoring**: Real-time safety and sentiment analysis
6. **Escalation**: Contacts family if help is needed

### Conversation Features
- **Greeting**: "Hi, this is your check-in call. How are you feeling today?"
- **Weather Check**: "It may be rough outside—are you safe and comfortable?"
- **Medication Check**: "Did you take your medicines today? Yes or no?"
- **Safety Monitoring**: Listens for distress signals
- **Emergency Response**: "I'm contacting your family now and staying with you."

## 🛠️ Development Tools

### Testing Scripts
- **`test_phone_number.py`**: Validate phone number format
- **`check_agent.py`**: Comprehensive system health check
- **`simple_call_test.py`**: Basic SIP connection testing
- **`debug_call.py`**: Full call flow testing with detailed logs

### Monitoring
- **Real-time logs**: Detailed conversation and system logs
- **LiveKit Dashboard**: Room sessions and participant monitoring
- **Webhook Integration**: External system notifications

## 🔧 Troubleshooting

### Common Issues
1. **"url must be set"**: Check LiveKit credentials in `.env`
2. **"SIP_OUTBOUND_TRUNK_ID is not set"**: Configure SIP trunk in LiveKit
3. **No phone calls**: Verify phone number format and SIP trunk setup
4. **Agent crashes**: Check API keys and dependencies

### Debug Commands
```bash
# Check system health
python check_agent.py

# Test phone number
python test_phone_number.py

# Test SIP connection
python test_sip_connection.py
```

## 📊 Dashboard Monitoring

The system provides real-time monitoring through:
- **LiveKit Dashboard**: Room sessions, participants, and call duration
- **Telephony Metrics**: Inbound/outbound call minutes and SIP sessions
- **Agent Logs**: Detailed conversation flow and error tracking

## 🌐 Integration Options

### Frontend Applications
- **Web**: React/Next.js voice chat interface
- **Mobile**: iOS, Android, React Native apps
- **Embedded**: Voice widget for existing websites

### Telephony Providers
- **LiveKit SIP**: Built-in SIP trunk support
- **Twilio**: Third-party telephony integration
- **Custom SIP**: Your own SIP provider configuration

## 📝 API Reference

### Agent Configuration
```python
agent = CareAgent(
    lang_pref="auto",  # "auto", "en", "es"
    empathetic_voice=True,
    safety_monitoring=True
)
```

### Call Dispatch
```python
await make_call(
    phone_number="+1234567890",
    reason="weather",  # "weather", "medication", "checkin"
    lang_pref="auto",
    person_id="grandma-001"
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LiveKit**: Real-time communication platform
- **AssemblyAI**: Speech-to-text technology
- **Rime**: Empathetic voice synthesis
- **OpenAI**: Conversational AI capabilities

## 📞 Support

For questions or support, please:
1. Check the troubleshooting section
2. Review the debug tools
3. Open an issue on GitHub
4. Contact the development team

---

**Built with ❤️ for elder care and voice AI innovation**
