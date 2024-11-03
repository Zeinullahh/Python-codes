import os
import logging
from flask import Flask, request, jsonify 
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, CallbackContext, filters, ConversationHandler

app = Flask(__name__)
# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation
LANGUAGE, NAME, DESCRIPTION, START_MESSAGE = range(4)

# Initialize global variables
user_data = {}

messages = []

@app.route('/send_message', methods=['POST']) 
def send_message(): 
    data = request.get_json() 
    messages.append(f"Visitor: {data['message']}") 
    return jsonify({"status": "success"})

@app.route('/get_messages', methods=['GET']) 
def get_messages(): 
    return jsonify({"messages": messages})

def run_flask_app(): app.run(port=5000)
    
# Start Flask app in a separate thread
threading.Thread(target=run_flask_app).start()
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
    
    # Basic live chat JavaScript code to be embedded in the website
    script = f"""
    <script>
    window.liveChatSettings = {{
        name: '{chat_name}',
        description: '{chat_description}',
        startMessage: '{user_data[update.effective_chat.id]['start_message']}'
    }};
    (function(u) {{
        var s = document.createElement('script');
        s.async = true;
        s.src = u;
        var x = document.getElementsByTagName('script')[0];
        x.parentNode.insertBefore(s, x);
    }})('http://35.209.220.223/home/zikosh004/tech_enterp/Python-codes/livechat.js');
    </script>
    """

    await update.message.reply_text("Chat has been created!")
    await update.message.reply_text("Here is your script to embed in your website:")
    await update.message.reply_text(script)
    return ConversationHandler.END


# Function to send messages from the website to Telegram
async def send_website_messages_to_telegram(context: CallbackContext):
    while True:
        if messages:
            msg = messages.pop(0)
            await context.bot.send_message(chat_id=<YOUR_TELEGRAM_CHAT_ID>, text=msg)
        await asyncio.sleep(1)

# Function to generate a unique chat ID
def generate_chat_id():
    import uuid
    return str(uuid.uuid4())

# Main function to start the bot
def main():
    application = Application.builder().token("7637744571:AAH5dNLsd-kXReU7MSfEiy5W3nrqFecMazo").build()

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
    application.run(async_func=send_website_messages_to_telegram)
