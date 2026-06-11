import telebot

TOKEN = "8928453138:AAFRnPv_HLOPQVscRnWURug9_onBFeASVFw"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "بات روی سرور روشن شد 😎")

@bot.message_handler(func=lambda m: True)
def chat(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
