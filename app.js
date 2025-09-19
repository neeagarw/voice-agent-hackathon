// Voice Chat App JavaScript
class VoiceChatApp {
    constructor() {
        this.ws = null;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.isProcessing = false;
        this.isMuted = false;
        this.currentLanguage = 'en';
        
        this.initializeElements();
        this.initializeSpeechRecognition();
        this.connectWebSocket();
        this.setupEventListeners();
    }

    initializeElements() {
        this.voiceButton = document.getElementById('voiceButton');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.statusText = document.getElementById('statusText');
        this.conversation = document.getElementById('conversation');
        this.resetButton = document.getElementById('resetButton');
        this.muteButton = document.getElementById('muteButton');
    }

    initializeSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
        } else if ('SpeechRecognition' in window) {
            this.recognition = new SpeechRecognition();
        } else {
            this.showError('Speech recognition not supported in this browser');
            return;
        }

        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI('listening');
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.handleUserSpeech(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateUI('ready');
            
            if (event.error === 'not-allowed') {
                this.showError('Microphone access denied. Please allow microphone access and refresh the page.');
            } else {
                this.showError('Speech recognition error. Please try again.');
            }
        };

        this.recognition.onend = () => {
            this.isListening = false;
            if (!this.isProcessing) {
                this.updateUI('ready');
            }
        };
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.updateUI('ready');
            this.voiceButton.disabled = false;
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleServerMessage(data);
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.updateUI('disconnected');
            this.voiceButton.disabled = true;
            
            // Attempt to reconnect after 3 seconds
            setTimeout(() => {
                this.connectWebSocket();
            }, 3000);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.showError('Connection error. Trying to reconnect...');
        };
    }

    setupEventListeners() {
        this.voiceButton.addEventListener('click', () => {
            if (this.isListening) {
                this.stopListening();
            } else {
                this.startListening();
            }
        });

        this.resetButton.addEventListener('click', () => {
            this.resetConversation();
        });

        this.muteButton.addEventListener('click', () => {
            this.toggleMute();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            if (event.code === 'Space' && !event.target.matches('input, textarea')) {
                event.preventDefault();
                if (!this.isListening && !this.isProcessing) {
                    this.startListening();
                }
            }
        });

        document.addEventListener('keyup', (event) => {
            if (event.code === 'Space' && this.isListening) {
                event.preventDefault();
                this.stopListening();
            }
        });
    }

    startListening() {
        if (!this.recognition || this.isListening || this.isProcessing) return;

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting speech recognition:', error);
            this.showError('Could not start listening. Please try again.');
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }

    handleUserSpeech(transcript) {
        console.log('User said:', transcript);
        
        // Add user message to conversation
        this.addMessage('user', transcript);
        
        // Send to server
        this.sendMessage({
            type: 'user_message',
            message: transcript
        });

        this.isProcessing = true;
        this.updateUI('processing');
    }

    handleServerMessage(data) {
        switch (data.type) {
            case 'agent_response':
                this.handleAgentResponse(data);
                break;
            case 'error':
                this.showError(data.message);
                this.isProcessing = false;
                this.updateUI('ready');
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    handleAgentResponse(data) {
        console.log('Agent response:', data.message);
        
        // Update language if changed
        if (data.language && data.language !== this.currentLanguage) {
            this.currentLanguage = data.language;
            this.recognition.lang = data.language === 'es' ? 'es-ES' : 'en-US';
        }

        // Add agent message to conversation
        this.addMessage('agent', data.message);

        // Speak the response if not muted
        if (!this.isMuted) {
            this.speakText(data.message, data.language);
        }

        this.isProcessing = false;
        this.updateUI('ready');
    }

    speakText(text, language = 'en') {
        if (!this.synthesis) return;

        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = language === 'es' ? 'es-ES' : 'en-US';
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;

        // Try to find a female voice
        const voices = this.synthesis.getVoices();
        const femaleVoice = voices.find(voice => 
            voice.lang.startsWith('en') && 
            (voice.name.includes('Female') || 
             voice.name.includes('Samantha') || 
             voice.name.includes('Victoria') || 
             voice.name.includes('Susan') || 
             voice.name.includes('Karen') || 
             voice.name.includes('Google US English Female') ||
             voice.name.includes('Microsoft Zira') ||
             voice.name.includes('Microsoft Hazel'))
        );
        
        if (femaleVoice) {
            utterance.voice = femaleVoice;
        } else {
            // Fallback: find any female-sounding voice
            const anyFemaleVoice = voices.find(voice => 
                voice.lang.startsWith('en') && 
                !voice.name.includes('Male') &&
                (voice.name.includes('a') || voice.name.includes('e'))
            );
            if (anyFemaleVoice) {
                utterance.voice = anyFemaleVoice;
            }
        }

        utterance.onstart = () => {
            this.updateUI('speaking');
        };

        utterance.onend = () => {
            this.updateUI('ready');
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            this.updateUI('ready');
        };

        this.synthesis.speak(utterance);
    }

    addMessage(sender, text) {
        const messageContainer = this.conversation.querySelector('.message-container');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'user' ? '👤' : '🤖';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        messageContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.conversation.scrollTop = this.conversation.scrollHeight;
    }

    sendMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            this.showError('Not connected to server');
        }
    }

    resetConversation() {
        // Clear conversation display
        const messageContainer = this.conversation.querySelector('.message-container');
        messageContainer.innerHTML = '';
        
        // Send reset message to server
        this.sendMessage({
            type: 'reset_conversation'
        });

        // Cancel any ongoing speech
        if (this.synthesis) {
            this.synthesis.cancel();
        }

        this.isProcessing = false;
        this.updateUI('ready');
    }

    toggleMute() {
        this.isMuted = !this.isMuted;
        this.muteButton.textContent = this.isMuted ? '🔊 Unmute Responses' : '🔇 Mute Responses';
        
        if (this.isMuted && this.synthesis) {
            this.synthesis.cancel();
        }
    }

    updateUI(state) {
        const button = this.voiceButton;
        const buttonIcon = button.querySelector('.button-icon');
        const buttonText = button.querySelector('.button-text');
        
        // Remove all state classes
        button.classList.remove('listening', 'processing');
        
        switch (state) {
            case 'ready':
                this.statusIndicator.textContent = '🤖';
                this.statusText.textContent = 'Ready to chat - Click to talk';
                buttonIcon.textContent = '🎤';
                buttonText.textContent = 'Start Talking';
                button.disabled = false;
                break;
                
            case 'listening':
                this.statusIndicator.textContent = '👂';
                this.statusText.textContent = 'Listening... Speak now';
                buttonIcon.textContent = '🛑';
                buttonText.textContent = 'Stop';
                button.classList.add('listening');
                button.disabled = false;
                break;
                
            case 'processing':
                this.statusIndicator.textContent = '🧠';
                this.statusText.textContent = 'Processing your message...';
                buttonIcon.textContent = '⏳';
                buttonText.textContent = 'Thinking...';
                button.classList.add('processing');
                button.disabled = true;
                break;
                
            case 'speaking':
                this.statusIndicator.textContent = '🗣️';
                this.statusText.textContent = 'AI is speaking...';
                buttonIcon.textContent = '🔊';
                buttonText.textContent = 'Speaking';
                button.disabled = true;
                break;
                
            case 'disconnected':
                this.statusIndicator.textContent = '❌';
                this.statusText.textContent = 'Disconnected - Reconnecting...';
                buttonIcon.textContent = '🔄';
                buttonText.textContent = 'Connecting...';
                button.disabled = true;
                break;
        }
    }

    showError(message) {
        console.error('Error:', message);
        
        // Show error in conversation
        this.addMessage('agent', `❌ Error: ${message}`);
        
        // Update status
        this.statusIndicator.textContent = '⚠️';
        this.statusText.textContent = message;
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Wait for voices to load
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = () => {
            new VoiceChatApp();
        };
    } else {
        new VoiceChatApp();
    }
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden && window.speechSynthesis) {
        window.speechSynthesis.cancel();
    }
});
