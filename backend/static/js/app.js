let currentUserId = 1;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    // chatData is now available from the template
    displayMessages(chatData[currentUserId] || []);
    setupChatSwitching();
});

function setupChatSwitching() {
    const chatItems = document.querySelectorAll('.chat-item');
    chatItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            chatItems.forEach(i => i.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
            
            const userId = parseInt(this.getAttribute('data-user-id'));
            const chatName = this.getAttribute('data-chat-name');
            const avatar = this.getAttribute('data-avatar');
            
            currentUserId = userId;
            
            // Update header
            document.getElementById('current-chat-name').textContent = chatName;
            document.getElementById('current-avatar').textContent = avatar;
            
            // Display messages for this chat
            displayMessages(chatData[userId] || []);
            
            // Reset AI panel to analyzing state for new chat
            resetAIPanel();
        });
    });
}

function displayMessages(messages) {
    const container = document.getElementById('messages-container');
    container.innerHTML = '';

    if (!messages || messages.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #666; padding: 40px;">No messages in this chat</div>';
        return;
    }

    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.sender === 'user' ? 'sent' : 'received'}`;
        
        messageDiv.innerHTML = `
            <div class="message-bubble">
                <div class="message-sender">${message.sender}</div>
                <div class="message-text">${message.message}</div>
                <div class="message-time">${getCurrentTime()}</div>
            </div>
        `;
        
        container.appendChild(messageDiv);
    });

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    });
}

function analyzeChat() {
    const btn = document.getElementById('schedule-btn');
    btn.disabled = true;
    btn.textContent = '⏳ Analyzing...';

    // Open AI panel and show analyzing state immediately
    const aiPanel = document.getElementById('ai-panel');
    const aiContent = document.getElementById('ai-content');
    
    aiPanel.classList.add('open');
    
    // Show analyzing state immediately
    aiContent.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Analyzing chat for meeting details...</p>
        </div>
    `;

    // Make API call
    fetch('/schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: currentUserId }),
    })
    .then(response => response.json())
    .then(data => {
        displayAIResults(data);
        btn.disabled = false;
        btn.textContent = '📅 Schedule Meeting';
    })
    .catch(error => {
        console.error('Error:', error);
        displayAIError(error.message);
        btn.disabled = false;
        btn.textContent = '📅 Schedule Meeting';
    });
}

function displayAIResults(result) {
    const content = document.getElementById('ai-content');
    
    if (result.error) {
        content.innerHTML = `
            <div class="error">
                <strong>Error:</strong> ${result.error}
            </div>
        `;
        return;
    }

    const participants = result.participants ? result.participants.join(', ') : 'Not specified';
    const emails = result.emails ? Object.entries(result.emails).map(([name, email]) => `${name}: ${email}`).join(', ') : 'Not found';
    const meetingTitle = result.meeting_title || 'Team Meeting';
    const location = result.location || 'Not specified';

    content.innerHTML = `
        <div class="ai-result">
            <h3>🎯 Meeting Analysis Results</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>📋 Meeting Title</strong>
                    <span>${meetingTitle}</span>
                </div>
                <div class="info-item">
                    <strong>📅 Date</strong>
                    <span>${result.date || 'Not specified'}</span>
                </div>
                <div class="info-item">
                    <strong>⏰ Time</strong>
                    <span>${result.time || 'Not specified'}</span>
                </div>
                <div class="info-item">
                    <strong>📍 Location</strong>
                    <span>${location}</span>
                </div>
                <div class="info-item">
                    <strong>👥 Participants</strong>
                    <span>${participants}</span>
                </div>
                <div class="info-item">
                    <strong>📧 Email Addresses</strong>
                    <span>${emails}</span>
                </div>
                <div class="info-item">
                    <strong>🎯 Meeting Intent</strong>
                    <span>${result.intent_detected ? '✅ Detected' : '❌ Not detected'}</span>
                </div>
            </div>
            ${result.intent_detected && result.emails ? `
                <div class="action-buttons">
                    <button class="send-email-btn" onclick="sendConfirmationEmails(${JSON.stringify(result).replace(/"/g, '&quot;')})">
                        📧 Send Confirmation Emails
                    </button>
                </div>
            ` : ''}
        </div>
    `;
}

function sendConfirmationEmails(meetingData) {
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = '⏳ Sending...';

    fetch('/send-confirmation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            meeting_details: meetingData,
            participant_emails: meetingData.emails
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the button to show success and disable it
            btn.textContent = '✅ Emails Sent Successfully!';
            btn.style.background = '#4caf50';
            btn.disabled = true;
            
            // Show success message
            const successMessage = document.createElement('div');
            successMessage.className = 'email-confirmation success';
            successMessage.innerHTML = `
                <h4>📧 Email Confirmation Sent</h4>
                <p>✅ Confirmation emails sent to ${data.total_participants} participants</p>
                <p><strong>Sent to:</strong> ${data.sent_emails.join(', ')}</p>
            `;
            
            // Insert the success message before the action buttons
            const actionButtons = btn.closest('.action-buttons');
            actionButtons.parentNode.insertBefore(successMessage, actionButtons);
        } else {
            alert(`❌ Failed to send confirmation emails: ${data.error}`);
            btn.disabled = false;
            btn.textContent = '📧 Send Confirmation Emails';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error sending confirmation emails');
        btn.disabled = false;
        btn.textContent = '📧 Send Confirmation Emails';
    });
}

function displayAIError(error) {
    const content = document.getElementById('ai-content');
    content.innerHTML = `
        <div class="error">
            <strong>Analysis Error:</strong> ${error}
        </div>
    `;
}

function resetAIPanel() {
    const aiPanel = document.getElementById('ai-panel');
    const aiContent = document.getElementById('ai-content');
    
    // Reset the AI panel content to analyzing state
    aiContent.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Analyzing chat for meeting details...</p>
        </div>
    `;
    
    // Close the AI panel if it's open
    aiPanel.classList.remove('open');
}

function closeAIPanel() {
    document.getElementById('ai-panel').classList.remove('open');
} 