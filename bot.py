import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize global variables
user_data = {}

# Start command
def start(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id] = {}  # Create a new user data entry
    buttons = [[KeyboardButton("English"), KeyboardButton("Russian")]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    update.message.reply_text("Please choose your language:", reply_markup=reply_markup)

# Handle language selection
def handle_language(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['language'] = update.message.text
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='URL_TO_YOUR_IMAGE')  # Add your image URL here
    update.message.reply_text("Let's connect your website to aLiveChat!\nPlease, name it.")

# Handle the name input
def handle_name(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['name'] = update.message.text
    update.message.reply_text("Please provide a description.")

# Handle the description input
def handle_description(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['description'] = update.message.text
    update.message.reply_text("Enter the start message for customers in chat.")

# Handle the start message input
def handle_start_message(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['start_message'] = update.message.text
    # Create a unique chat ID or script ID here (e.g., UUID)
    chat_id = generate_chat_id()  # Implement this function to generate unique IDs
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
    update.message.reply_text(f"Chat has been created! Here is your script:\n{script}")

# Function to generate a unique chat ID
def generate_chat_id():
    import uuid
    return str(uuid.uuid4())

# Main function to start the bot
def main():
    application = Application.builder().token("7637744571:AAH5dNLsd-kXReU7MSfEiy5W3nrqFecMazo").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_message))

    application.run_polling()

if __name__ == '__main__':
    main()
