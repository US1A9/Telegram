import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5834476457:AAEotyDMhlyzUNL_z-b_UyfM7EVeLTWT16Q'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = InlineKeyboardMarkup()
    dev_button = InlineKeyboardButton(text='dev', url="https://t.me/z_0_g")
    markup.add(dev_button)
    bot.reply_to(message, "Hello, I'm a TikTok bot. Just send me your username and I will give you all the information", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    username = message.text
    user_info = TikTokInfo(username)
    bot.reply_to(message, f'''
user: @{user_info.get_usernames()}
Nick name: { user_info.get_name() }
User ID: { user_info.get_user_id() }
Is verified: { user_info.is_verified() }
Is private: { user_info.is_private() }
Followers: { user_info.followers() }
Following: { user_info.following() }
Video Count: { user_info.video_count() }
User Create Time: { user_info.user_create_time() }
Last Time Change Nickname: { user_info.last_change_name() }
Account Region: { user_info.region() }
secUid: { user_info.secUid() }
Language: { user_info.language() }
''')

def country_code_to_flag_emoji(country_code):
    country_code = country_code.upper()
    flag_emoji = ''.join(chr(127397 + ord(char)) for char in country_code)
    return flag_emoji

class TikTokInfo:
    def __init__(self, username: str):
        self.username = username.replace("@", "") if "@" in username else username
        self.json_data = None
        self.admin()

    def admin(self):
        self.send_request()

    def send_request(self):
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 GIVT"}
        r = requests.get(f"https://www.tiktok.com/@{self.username}", headers=headers)

        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            script_tag = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
            script_text = script_tag.text.strip()
            self.json_data = json.loads(script_text)["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
        except Exception:
            raise ValueError("Username not found")

    def profile(self):
        try:
            return str(self.json_data["user"]["avatarLarger"])
        except:
            return "Unknown"
            
    def get_user_id(self):
        try:
            return str(self.json_data["user"]["id"])
        except:
            return "Unknown"

    def get_usernames(self):
        try:
            return self.json_data["user"]["uniqueId"]
        except:
            return "Unknown"
            
    def get_name(self):
        try:
            return self.json_data["user"]["nickname"]
        except:
            return "Unknown"
            
    def is_verified(self):
        try:
            check = self.json_data["user"]["verified"]
            return "Yes✅" if check else "No❌"
        except:
            return "Unknown"

    def secUid(self):
        try:
            return self.json_data["user"]["secUid"]
        except:
            return "Unknown"

    def is_private(self):
        try:
            check = self.json_data["user"]["privateAccount"]
            return "Yes ✅" if check else "No ❌"
        except:
            return "Unknown"

    def followers(self):
        try:
            return self.json_data["stats"]["followerCount"]
        except:
            return "Unknown"

    def following(self):
        try:
            return self.json_data["stats"]["followingCount"]
        except:
            return "Unknown"

    def user_create_time(self):
        try:
            url_id = int(self.get_user_id())
            binary = "{0:b}".format(url_id)
            i = 0
            bits = ""
            while i < 31:
                bits += binary[i]
                i += 1
            timestamp = int(bits, 2)
            dt_object = datetime.fromtimestamp(timestamp)
            return dt_object
        except:
            return "Unknown"

    def last_change_name(self):
        try:
            time = self.json_data["user"]["nickNameModifyTime"]
            check = datetime.fromtimestamp(int(time))
            return check
        except:
            return "Unknown"

    def region(self):
        try:
            region_code = self.json_data["user"]["region"]
            flag_emoji = country_code_to_flag_emoji(region_code)
            return f"{region_code} {flag_emoji}"
        except:
            return "None"

    def video_count(self):
        try:
            return self.json_data["stats"]["videoCount"]
        except:
            return "Unknown"

    def open_favorite(self):
        try:
            check = self.json_data["user"]["openFavorite"]
            return "Yes" if check else "No"
        except:
            return "Unknown"

    def see_following(self):
        try:
            check = str(self.json_data["user"]["followingVisibility"])
            return "Yes" if check == "1" else "No"
        except:
            return "Unknown"

    def language(self):
        try:
            return str(self.json_data["user"]["language"])
        except:
            return "Unknown"

    def heart_count(self):
        try:
            return str(self.json_data["stats"]["heart"])
        except:
            return "Unknown"

print("Hi")            
bot.polling(True)
