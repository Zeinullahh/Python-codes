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
CHAT_ID = 123456789  # Replace with the actual chat ID
LANGUAGE_CHOICE = ""
NAME = ""
DESCRIPTION = ""
START_MESSAGE = ""

# Start command
async def start(update: Update, context: CallbackContext):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id  # Set CHAT_ID dynamically for testing
    buttons = [
        [InlineKeyboardButton("🇺🇸 English", callback_data='English')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='Russian')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Please choose your language:", reply_markup=reply_markup)
    return LANGUAGE

# Handle language selection
async def handle_language(update: Update, context: CallbackContext):
    global LANGUAGE_CHOICE
    query = update.callback_query
    await query.answer()
    LANGUAGE_CHOICE = query.data
    await context.bot.send_photo(chat_id=CHAT_ID, photo=open('aLC_name.jpg', 'rb'))
    await query.message.reply_text("Let's connect your website to aLiveChat!\nPlease, name it.")
    return NAME

# Handle the name input
async def handle_name(update: Update, context: CallbackContext):
    global NAME
    NAME = update.message.text
    await context.bot.send_photo(chat_id=CHAT_ID, photo=open('aLC_description.jpg', 'rb'))
    await update.message.reply_text("Please provide a description.")
    return DESCRIPTION

# Handle the description input
async def handle_description(update: Update, context: CallbackContext):
    global DESCRIPTION
    DESCRIPTION = update.message.text
    await context.bot.send_photo(chat_id=CHAT_ID, photo=open('aLC_message.jpg', 'rb'))
    await update.message.reply_text("Enter the start message for customers in chat.")
    return START_MESSAGE

# Handle the start message input
async def handle_start_message(update: Update, context: CallbackContext):
    global START_MESSAGE
    START_MESSAGE = update.message.text
    
    # JavaScript code to be embedded in the website
    script = f"""
    <script>
    window.liveChatSettings = {{
        name: '{NAME}',
        description: '{DESCRIPTION}',
        startMessage: '{START_MESSAGE}'
    }};
    </script>
    <script src="http://35.209.231.50/home/zikosh004/livechat.js"></script>
    """

    await update.message.reply_text("Chat has been created!")
    await update.message.reply_text("Here is your script to embed in your website:")
    await update.message.reply_text(script)
    return ConversationHandler.END

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
