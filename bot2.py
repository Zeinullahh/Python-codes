import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Global user data storage
user_data = {}

# Handle the start command
async def start(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id] = {}  # Create a new user data entry
    buttons = [[KeyboardButton("English"), KeyboardButton("Russian")]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text("Please choose your language:", reply_markup=reply_markup)

# Handle language selection
async def handle_language(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['language'] = update.message.text
    await update.message.reply_text("Let's connect your website to aLiveChat!\nPlease, name it.")

# Handle the name input
async def handle_name(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['name'] = update.message.text
    await update.message.reply_text("Please provide a description.")

# Handle the description input
async def handle_description(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['description'] = update.message.text
    await update.message.reply_text("Enter the start message for customers in chat.")

# Handle the start message input
async def handle_start_message(update: Update, context: CallbackContext):
    user_data[update.effective_chat.id]['start_message'] = update.message.text
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
    await update.message.reply_text(f"Chat has been created! Here is your script:\n{script}")

# Function to generate a unique chat ID
def generate_chat_id():
    import uuid
    return str(uuid.uuid4())

# Main function to start the bot
async def main():
    application = Application.builder().token("7637744571:AAH5dNLsd-kXReU7MSfEiy5W3nrqFecMazo").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_message))

    await application.run_polling()

if __name__ == '__main__':
  asyncio.run(main())