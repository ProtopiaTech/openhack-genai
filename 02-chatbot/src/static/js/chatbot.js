document.addEventListener('DOMContentLoaded', async () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const errorMessage = document.getElementById('error-message');
    const responseMetadataDisplay = document.getElementById('response-metadata-display');

    function logError(message, error = null) {
        errorMessage.textContent = message;
        if (error) {
            console.error(message, error);
        }
    }

    sendButton.addEventListener('click', async () => {
        const userMessage = userInput.value.trim();
        if (userMessage) {
            appendMessage('User', userMessage);
            userInput.value = '';
            // Show typing indicator
            const typingIndicator = appendMessage('Chatbot', '');
            typingIndicator.classList.add('typing');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: userMessage })
                });
                // Remove typing indicator
                typingIndicator.remove();
                if (!response.ok) {
                    const data = await response.json();
                    logError("Error sending message to chatbot. " + JSON.stringify(data));
                    appendMessage('Chatbot', 'Failed to get response from chatbot.');
                } else {
                    const data = await response.json();
                    // Append chatbot response
                    appendMessage('Chatbot', data.content);
                    if (data.response_metadata) {
                        responseMetadataDisplay.textContent = JSON.stringify(data.response_metadata, null, 2);
                    }
                }
            } catch (error) {
                logError("Error sending message to chatbot.", error);
                typingIndicator.remove();
                appendMessage('Chatbot', 'Failed to get response from chatbot.');
            }
        }
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('mb-2', 'p-2', 'rounded-md', 'whitespace-pre-wrap');
        const senderClass = sender === 'User' ? 'bg-blue-100 self-end' : 'bg-gray-100';
        messageElement.classList.add(...senderClass.split(' '));

        const senderName = document.createElement('div');
        senderName.classList.add('text-sm', 'font-semibold', 'mb-1');
        senderName.textContent = sender;

        const messageContent = document.createElement('div');
        messageContent.textContent = message;

        messageElement.appendChild(senderName);
        messageElement.appendChild(messageContent);
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return messageElement;
    }
});