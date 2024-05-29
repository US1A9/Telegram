import telebot

bot = telebot.TeleBot('5834476457:AAEotyDMhlyzUNL_z-b_UyfM7EVeLTWT16Q')

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hello")

bot.polling()
