import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, CallbackContext, filters, ConversationHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation
LANGUAGE, NAME, DESCRIPTION, START_MESSAGE = range(4)

# Initialize global variables
user_data = {}

# Start command
async def start(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id] = {}  # Create a new user data entry
    buttons = [
        [InlineKeyboardButton("🇺🇸 English", callback_data='English')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='Russian')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Please choose your language:", reply_markup=reply_markup)
    return LANGUAGE

# Handle language selection
async def handle_language(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    user_data[query.message.chat.id]['language'] = query.data
    await context.bot.send_photo(chat_id=query.message.chat.id, photo=open('aLC_name.jpg', 'rb'))
    await query.message.reply_text("Let's connect your website to aLiveChat!\nPlease, name it.")
    return NAME

# Handle the name input
async def handle_name(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['name'] = update.message.text
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('aLC_description.jpg', 'rb'))
    await update.message.reply_text("Please provide a description.")
    return DESCRIPTION

# Handle the description input
async def handle_description(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['description'] = update.message.text
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('aLC_message.jpg', 'rb'))
    await update.message.reply_text("Enter the start message for customers in chat.")
    return START_MESSAGE

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
        chatWidget.style.bottom = '20px';
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

# Main function to start the bot
def main():
    TELEGRAM_TOKEN = '7637744571:AAH5dNLsd-kXReU7MSfEiy5W3nrqFecMazo'
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(handle_language)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description)],
            START_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_message)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
