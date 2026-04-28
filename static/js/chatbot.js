// LinguaAI - Chatbot JavaScript

class Chatbot {
    constructor(options = {}) {
        this.messages = [];
        this.language = options.language || 'Spanish';
        this.apiEndpoint = options.apiEndpoint || '/api/chat/';
        this.maxMessages = options.maxMessages || 50;
        this.typingSpeed = options.typingSpeed || 30;
        
        this.init();
    }
    
    init() {
        this.loadHistory();
        this.setupEventListeners();
    }
    
    loadHistory() {
        const history = storage.get('chat_history_' + this.language);
        if (history) {
            this.messages = history;
        }
    }
    
    saveHistory() {
        if (this.messages.length > this.maxMessages) {
            this.messages = this.messages.slice(-this.maxMessages);
        }
        storage.set('chat_history_' + this.language, this.messages);
    }
    
    setupEventListeners() {
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.querySelector('.send-btn');
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.send();
                }
            });
        }
        
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.send());
        }
    }
    
    async send() {
        const chatInput = document.getElementById('chatInput');
        if (!chatInput) return;
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        chatInput.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            const response = await this.getAIResponse(message);
            this.hideTyping();
            this.addMessage(response, 'ai');
        } catch (error) {
            this.hideTyping();
            this.addMessage("Sorry, I encountered an error. Please try again.", 'ai');
            console.error('Chat error:', error);
        }
    }
    
    async getAIResponse(message) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value 
            || '{{ csrf_token }}';
        
        const response = await fetch(this.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                message: message,
                language: this.language
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        return data.response;
    }
    
    addMessage(text, type) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatarIcon = type === 'ai' ? 'fa-robot' : 'fa-user';
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <p>${this.escapeHtml(text)}</p>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Save to history
        this.messages.push({ text, type, time: new Date().toISOString() });
        this.saveHistory();
    }
    
    showTyping() {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        const indicator = document.createElement('div');
        indicator.className = 'message ai typing-indicator';
        indicator.id = 'typingIndicator';
        indicator.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    hideTyping() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    setLanguage(language) {
        this.language = language;
        this.loadHistory();
    }
    
    clearHistory() {
        this.messages = [];
        storage.remove('chat_history_' + this.language);
        
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.innerHTML = '';
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Quick Phrases
function sendPhrase(phrase) {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.value = phrase;
        
        // Trigger the chatbot send
        const chatbot = window.chatbot;
        if (chatbot) {
            chatbot.send();
        }
    }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('languageSelector');
    
    if (languageSelector) {
        window.chatbot = new Chatbot({
            language: languageSelector.value,
            apiEndpoint: '/api/chat/'
        });
        
        languageSelector.addEventListener('change', function() {
            window.chatbot.setLanguage(this.value);
        });
    }
});

// Export for use
window.Chatbot = Chatbot;
window.sendPhrase = sendPhrase;