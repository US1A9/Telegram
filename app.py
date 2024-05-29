
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import pytz
import asyncio
import os

api_id = 25453504
api_hash = 'f5166e277a4ee215bd4acd6900067dcb'
session_name = 'm.txt.session'  # Use an absolute path

# Ensure the directory for the session file exists
os.makedirs(os.path.dirname(session_name), exist_ok=True)

egypt_timezone = pytz.timezone('Africa/Cairo')

def get_current_time_egypt():
    print(session_name)
    now_egypt = datetime.now(egypt_timezone)
    return now_egypt.strftime("%H:%M")

async def update_first_name(client):
    while True:
        current_time_egypt = get_current_time_egypt()
        new_first_name = f"🚴 EGYPT 🇪🇬 {current_time_egypt}"  
        await client(UpdateProfileRequest(first_name=new_first_name))
        print(f"Updated first name to: {new_first_name}")
        await asyncio.sleep(59)

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    
    print("Telegram client started")
   
    await update_first_name(client)

if __name__ == '__main__':
    asyncio.run(main())
