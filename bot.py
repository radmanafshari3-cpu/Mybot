import telebot
import time
from datetime import datetime, timedelta

TOKEN = "8928453138:AAFRnPv_HLOPQVscRnWURug9_onBFeASVFw"
CHANNEL_ID = "@sektorgodlybloodines"
bot = telebot.TeleBot(TOKEN)

# دیتابیس ساده (فعلاً داخل رم)
users = {}

# --- چک اشتراک ---
def is_active(user_id):
    if user_id not in users:
        return False
    return users[user_id] > datetime.now()

# --- دکمه‌ها ---
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def buy_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💳 خرید اشتراک", callback_data="buy"))
    return markup

# --- استارت ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if not is_active(user_id):
        bot.send_message(
            user_id,
            "❌ اشتراک نداری!\n۱ هفته تست رایگان بزن یا بخر 😏",
            reply_markup=buy_button()
        )
    else:
        bot.send_message(user_id, "✅ اشتراک فعاله 😎")

# --- خرید (شبیه‌سازی) ---
@bot.callback_query_handler(func=lambda call: call.data == "buy")
def buy(call):
    user_id = call.message.chat.id

    # فعال‌سازی تست 7 روزه
    users[user_id] = datetime.now() + timedelta(days=7)

    bot.answer_callback_query(call.id, "فعال شد 😎")
    bot.send_message(user_id, "🎉 اشتراک ۷ روزه فعال شد!")

# --- ارسال به کانال (فقط اگر فعال باشه) ---
@bot.message_handler(commands=['post'])
def post(message):
    user_id = message.chat.id

    if not is_active(user_id):
        bot.reply_to(message, "❌ اشتراک نداری برو خرید 😏")
        return

    text = message.text.replace("/post", "").strip()

    if text == "":
        bot.reply_to(message, "چی بفرستم؟")
        return

    bot.send_message(CHANNEL_ID, text)
    bot.reply_to(message, "فرستادم 😎")

bot.infinity_polling()
