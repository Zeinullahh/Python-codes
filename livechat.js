(function() {
    var chatWidget = document.createElement('div');
    chatWidget.id = 'liveChatWidget';
    chatWidget.style.position = 'fixed';
    chatWidget.style.bottom = '20px';
    chatWidget.style.right = '20px';
    chatWidget.style.width = '300px';
    chatWidget.style.height = '400px';
    chatWidget.style.border = '1px solid #ccc';
    chatWidget.style.backgroundColor = '#fff';
    chatWidget.style.zIndex = '10000';
    chatWidget.innerHTML = `
        <h2>${window.liveChatSettings.name}</h2>
        <p>${window.liveChatSettings.description}</p>
        <div id="chatMessages" style="height: 300px; overflow-y: auto;"></div>
        <textarea id="chatInput" placeholder="Type your message here..." style="width: 100%; height: 50px;"></textarea>
        <button id="sendMessage" style="width: 100%;">Send</button>
    `;
    document.body.appendChild(chatWidget);

    document.getElementById('sendMessage').addEventListener('click', function() {
        var message = document.getElementById('chatInput').value;
        if (message.trim() !== '') {
            sendMessage(message);
            document.getElementById('chatMessages').innerHTML += `<p>You: ${message}</p>`;
            document.getElementById('chatInput').value = '';
        }
    });

    function sendMessage(message) {
        fetch('http://localhost:5000/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
    }

    function receiveMessages() {
        fetch('http://localhost:5000/get_messages')
            .then(response => response.json())
            .then(data => {
                var chatMessages = document.getElementById('chatMessages');
                chatMessages.innerHTML = '';
                data.messages.forEach(msg => {
                    chatMessages.innerHTML += `<p>${msg}</p>`;
                });
            });
    }

    setInterval(receiveMessages, 1000); // Polling for new messages every second
})();
