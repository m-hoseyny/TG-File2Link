# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]
# Improving: m-hoseyny github

from pyrogram import filters
from pyrogram.types import Message
import time

from WebStreamer.vars import Var 
from WebStreamer.bot import StreamBot
from WebStreamer.utils.user_data import user_db

@StreamBot.on_message(filters.command(["start", "help"]) & filters.private)
async def start(_, m: Message):
    # Save user information
    user_data = {
        "user_id": m.from_user.id,
        "username": m.from_user.username,
        "first_name": m.from_user.first_name,
        "last_name": m.from_user.last_name,
        "language_code": m.from_user.language_code,
        "is_bot": m.from_user.is_bot,
        "is_premium": m.from_user.is_premium,
        "last_command": "start"
    }
    user_db.add_user(m.from_user.id, user_data)
    
    await m.reply(
        f'Hi {m.from_user.mention(style="md")}, Send me a file to get an instant stream link.'
        '\n'
        f'سلام {m.from_user.mention(style="md")}, من تبدیل کننده فایل تلگرام به لینک مستقیم دانلود هستم. برام فایلت رو بفرست تا لینک مستقیم رو بگیری'
    )

@StreamBot.on_message(filters.command("start") & filters.channel)
async def channel_id(_, m: Message):
    await m.reply(f"Channel ID: `{m.chat.id}`\nYou can use this ID in the CHANNEL_IDS environment variable.")

@StreamBot.on_message(filters.command("stats") & filters.private)
async def stats_command(_, m: Message):
    if str(m.from_user.id) not in Var.ALLOWED_USERS:
        return await m.reply("You are not authorized to use this command.")
    
    total_users = user_db.get_total_users()
    active_today = 0
    active_week = 0
    current_time = int(time.time())
    
    for user_data in user_db.get_all_users().values():
        last_seen = user_data.get("last_seen", 0)
        if current_time - last_seen < 86400:  # 24 hours
            active_today += 1
        if current_time - last_seen < 604800:  # 7 days
            active_week += 1
    
    stats_text = (
        "📊 **Bot Statistics**\n\n"
        f"👥 Total Users: `{total_users}`\n"
        f"📈 Active Today: `{active_today}`\n"
        f"📊 Active This Week: `{active_week}`\n"
        f"🔄 Last Updated: `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
    )
    
    await m.reply(stats_text)
