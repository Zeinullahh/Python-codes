
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
        <textarea id="chatInput" placeholder="Type your message here..." style="width: 100%; height: 50px;"></textarea>
        <button id="sendMessage" style="width: 100%;">Send</button>
    `;
    document.body.appendChild(chatWidget);

    document.getElementById('sendMessage').addEventListener('click', function() {
        var message = document.getElementById('chatInput').value;
        alert('Message sent: ' + message); // Replace with actual message handling logic
        document.getElementById('chatInput').value = '';
    });
})();
