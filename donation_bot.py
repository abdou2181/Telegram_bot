# donation_bot.py
import os, time
from dotenv import load_dotenv
import telebot
from telebot import types

# Load token from .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def start(msg):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("💎 10 Stars", callback_data="donate_10"),
        types.InlineKeyboardButton("💎 50 Stars", callback_data="donate_50"),
        types.InlineKeyboardButton("💎 100 Stars", callback_data="donate_100")
    )
    kb.add(types.InlineKeyboardButton("✍️ Custom amount", callback_data="donate_custom"))
    bot.send_message(msg.chat.id, "Support this bot with Telegram Stars 🌟", reply_markup=kb)

# Handle button clicks
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("donate_"))
def on_donate(call):
    data = call.data
    if data == "donate_custom":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "Type the number of Stars to donate:")
        bot.register_next_step_handler(msg, handle_custom_amount)
        return
    amount = int(data.split("_")[1])
    send_stars_invoice(call.message.chat.id, amount)

# Handle custom donation
def handle_custom_amount(message):
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            raise ValueError
    except:
        bot.reply_to(message, "Enter a positive number (e.g. 50).")
        return
    send_stars_invoice(message.chat.id, amount)

# Send invoice for Stars
def send_stars_invoice(chat_id, amount):
    payload = f"donation:{int(time.time())}"
    price = types.LabeledPrice(label=f"{amount} Stars", amount=amount)
    bot.send_invoice(
        chat_id=chat_id,
        title="Donation",
        description=f"Support with {amount} Stars",
        payload=payload,
        provider_token=None,  # Telegram will use Stars (XTR)
        currency="XTR",
        prices=[price],
        start_parameter="donate-start"
    )

# Pre-checkout
@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

# After successful payment
@bot.message_handler(content_types=['successful_payment'])
def got_payment(msg):
    amount = msg.successful_payment.total_amount
    bot.send_message(msg.chat.id, f"🎉 Thanks! You donated {amount} Stars 🌟")

# Run forever
bot.infinity_polling()
