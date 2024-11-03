import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, ConversationHandler

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
    buttons = [[KeyboardButton("English"), KeyboardButton("Russian")]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text("Please choose your language:", reply_markup=reply_markup)
    return LANGUAGE

# Handle language selection
async def handle_language(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['language'] = update.message.text
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('aLC_name.jpg', 'rb'))
    await update.message.reply_text("Let's connect your website to aLiveChat!\nPlease, name it.")
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
    chat_id = generate_chat_id()  # Create a unique chat ID or script ID here (e.g., UUID)
    script = f"""
<script>
window.replainSettings = {{ id: '{chat_id}' }};
(function(u) {{
var s = document.createElement('script');
s.async = true;
s.src = u;
var x = document.getElementsByTagName('script')[0];
x.parentNode.insertBefore(s, x);
}})('https://widget.replain.cc/dist/client.js');
</script>
"""
    await update.message.reply_text(f"Chat has been created! Here is your script:\n{script}")
    return ConversationHandler.END

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
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language)],
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
