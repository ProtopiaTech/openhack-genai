document.addEventListener('DOMContentLoaded', async () => {
    const msalConfig = {
        auth: {
            clientId: clientId, // Use the injected client ID
            authority: `https://login.microsoftonline.com/${tenantId}`, // Use the injected tenant ID
            redirectUri: window.location.origin,
        },
        cache: {
            cacheLocation: "localStorage", // This configures where your cache will be stored
            storeAuthStateInCookie: false, // Set this to "true" if you're having issues on IE11 or Edge
        },
    };

    const msalInstance = new msal.PublicClientApplication(msalConfig);

    const loginRequest = {
        scopes: ["user.read", "api://" + clientId + "/chat"],
    };

    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const loginButton = document.getElementById('login-button');
    const userNameSpan = document.getElementById('user-name');
    const userLoginSpan = document.getElementById('user-login');
    const userRolesSpan = document.getElementById('user-roles');
    const errorMessage = document.getElementById('error-message');
    const decodedTokenDisplay = document.getElementById('decoded-token-display');
    const responseMetadataDisplay = document.getElementById('response-metadata-display');

    function logError(message, error = null) {
        errorMessage.textContent = message;
        if (error) {
            console.error(message, error);
        }
    }

    async function initializeMsal() {
        try {
            await msalInstance.initialize();
        } catch (error) {
            logError("MSAL initialization failed.", error);
        }
    }

    function decodeToken(token) {
        try {
            return jwt_decode(token);
        } catch (error) {
            logError("Failed to decode token.", error);
            return null;
        }
    }

    function handleResponse(response) {
        if (response !== null) {
            const account = response.account || response;
            userNameSpan.textContent = account.name;
            userLoginSpan.textContent = account.username;
            userRolesSpan.textContent = 'Public, Private, Personal Data'; // Replace with actual roles if needed
            sendButton.classList.remove('button-disabled', 'bg-gray-500');
            sendButton.classList.add('bg-blue-500');
            sendButton.removeAttribute('disabled');
            loginButton.textContent = "Logout";
            console.log(response);
            const decodedToken = decodeToken(response.idToken);
            if (decodedToken) {
                decodedTokenDisplay.textContent = JSON.stringify(decodedToken, null, 2);
            }
        }
    }

    function handleLogout() {
        // Clear application session state
        window.localStorage.clear();
        window.sessionStorage.clear();
        userNameSpan.textContent = "Guest";
        userLoginSpan.textContent = "Not logged in";
        userRolesSpan.textContent = "None";
        sendButton.classList.add('button-disabled', 'bg-gray-500');
        sendButton.classList.remove('bg-blue-500');
        sendButton.setAttribute('disabled', 'true');
        loginButton.textContent = "Login";
        decodedTokenDisplay.textContent = "";
        responseMetadataDisplay.textContent = "";
    }

    // Initialize MSAL instance
    await initializeMsal();

    // Handle the response from redirect
    try {
        const response = await msalInstance.handleRedirectPromise();
        if (response) {
            handleResponse(response);
        } else {
            // Check if a user is already logged in and set the account information
            const currentAccounts = msalInstance.getAllAccounts();
            if (currentAccounts.length > 0) {
                handleResponse(currentAccounts[0]);
            }
        }
    } catch (error) {
        logError("Error handling redirect promise.", error);
    }

    loginButton.addEventListener('click', async () => {
        if (loginButton.textContent === "Login") {
            try {
                const response = await msalInstance.loginPopup(loginRequest);
                handleResponse(response);
            } catch (error) {
                logError("Login failed.", error);
            }
        } else if (loginButton.textContent === "Logout") {
            handleLogout();
        }
    });

    sendButton.addEventListener('click', async () => {
        const userMessage = userInput.value.trim();
        if (userMessage) {
            appendMessage('User', userMessage);
            userInput.value = '';
            // Show typing indicator
            const typingIndicator = appendMessage('Chatbot', '');
            typingIndicator.classList.add('typing');

            try {
                const account = msalInstance.getAllAccounts()[0];
                const tokenRequest = {
                    //scopes: ["api://"+clientId+"/.default"],
                    scopes: ["api://" + clientId + "/chat"],
                    account: account
                };
                console.log(tokenRequest);
                const tokenResponse = await msalInstance.acquireTokenSilent(tokenRequest);
                const token = tokenResponse.accessToken;
                console.log("Access token:", token)
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
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