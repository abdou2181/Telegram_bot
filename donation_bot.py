import os
import logging
import telebot
from dotenv import load_dotenv

# Configure proper logging for Render
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Load token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Log bot start
logger.info("✅ Bot started and listening for messages...")

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"💬 {message.from_user.username or message.from_user.first_name} started the bot.")
    markup = telebot.types.InlineKeyboardMarkup()

    buttons = [
        telebot.types.InlineKeyboardButton("💫 Donate 1 Star", callback_data="donate_1"),
        telebot.types.InlineKeyboardButton("🌟 Donate 10 Stars", callback_data="donate_10"),
        telebot.types.InlineKeyboardButton("🚀 Donate 100 Stars", callback_data="donate_100"),
        telebot.types.InlineKeyboardButton("✨ Custom Amount", callback_data="donate_custom"),
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Choose how many stars you want to donate 🌟:", reply_markup=markup)

# Handle button presses
@bot.callback_query_handler(func=lambda call: True)
def handle_donation(call):
    user = call.from_user.username or call.from_user.first_name
    if call.data.startswith("donate_"):
        amount = call.data.split("_")[1]
        if amount == "custom":
            bot.send_message(call.message.chat.id, "💰 Please type the custom amount of stars you want to donate:")
            logger.info(f"🟡 {user} selected custom amount donation")
        else:
            bot.answer_callback_query(call.id, f"Thank you for donating {amount} ⭐!")
            bot.send_message(call.message.chat.id, f"🎉 Thank you for donating {amount} stars!")
            logger.info(f"💸 {user} donated {amount} stars")

# Run the bot forever
bot.polling(none_stop=True)
