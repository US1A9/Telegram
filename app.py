from flask import Flask, request
import telebot

API_TOKEN = '5834476457:AAEotyDMhlyzUNL_z-b_UyfM7EVeLTWT16Q'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# Define a simple route to check if the Flask app is alive
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Set up a route to handle incoming messages from Telegram
@app.route('/' + API_TOKEN, methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

# Define a handler for the /start command in your Telegram bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your bot.")

# Define a handler for any text messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    # To run the Flask app
    app.run(host='0.0.0.0', port=5000)
  
