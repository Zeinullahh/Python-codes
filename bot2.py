# Handle the start message input
async def handle_start_message(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['start_message'] = update.message.text
    chat_name = user_data[update.effective_chat.id]['name']
    chat_description = user_data[update.effective_chat.id]['description']
    start_message = user_data[update.effective_chat.id]['start_message']
    
    # Basic live chat JavaScript code to be embedded in the website
    script = f"""
    <script>
    window.liveChatSettings = {{
        name: '{chat_name}',
        description: '{chat_description}',
        startMessage: '{start_message}'
    }};
    (function() {{
        var chatWidget = document.createElement('div');
        chatWidget.id = 'liveChatWidget';
        chatWidget.style.position = 'fixed';
        chatWidget.style.bottom = '60px';  // Adjusted to be higher
        chatWidget.style.right = '20px';
        chatWidget.style.width = '300px';
        chatWidget.style.height = '400px';
        chatWidget.style.border = '1px solid #ccc';
        chatWidget.style.backgroundColor = '#fff';
        chatWidget.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
        chatWidget.style.zIndex = '1000';
        chatWidget.innerHTML = `
            <div style="padding: 10px; background-color: #007bff; color: #fff;">
                <strong>{chat_name}</strong>
                <p>{chat_description}</p>
            </div>
            <div id="chatMessages" style="padding: 10px; height: 300px; overflow-y: auto;">
                <div>{start_message}</div>
            </div>
            <div style="padding: 10px; border-top: 1px solid #ccc;">
                <input type="text" id="chatInput" style="width: 80%;" placeholder="Type a message...">
                <button id="sendButton" style="width: 18%;">Send</button>
            </div>
        `;
        document.body.appendChild(chatWidget);

        var sendButton = document.getElementById('sendButton');
        var chatInput = document.getElementById('chatInput');
        var chatMessages = document.getElementById('chatMessages');

        sendButton.addEventListener('click', function() {{
            var message = chatInput.value;
            if (message.trim() !== '') {{
                var messageElement = document.createElement('div');
                messageElement.textContent = message;
                chatMessages.appendChild(messageElement);
                chatInput.value = '';
                chatMessages.scrollTop = chatMessages.scrollHeight;

                // Send message to the server
                fetch('https://35.209.220.223:5000/webhook', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        chat_id: '{update.effective_chat.id}',
                        message: message
                    }})
                }})
                .then(response => response.json())
                .then(data => {{
                    console.log('Success:', data);
                }})
                .catch((error) => {{
                    console.error('Error:', error);
                }});
            }}
        }});
    }})();
    </script>
    """

    # Send the script to the user without HTML formatting
    await update.message.reply_text("Here is your live chat script. Embed it in your website's HTML:")
    await update.message.reply_text(script)
    return ConversationHandler.END
