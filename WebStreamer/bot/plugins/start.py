# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from pyrogram import filters
from pyrogram.types import Message

from WebStreamer.vars import Var 
from WebStreamer.bot import StreamBot

@StreamBot.on_message(filters.command(["start", "help"]) & filters.private)
async def start(_, m: Message):
    await m.reply(
        f'Hi {m.from_user.mention(style="md")}, Send me a file to get an instant stream link.'
        '\n'
        f'سلام {m.from_user.mention(style="md")}, من تبدیل کننده فایل تلگرام به لینک مستقیم دانلود هستم. برام فایلت رو بفرست تا لینک مستقیم رو بگیری'
    )

@StreamBot.on_message(filters.command("start") & filters.channel)
async def channel_id(_, m: Message):
    await m.reply(f"Channel ID: `{m.chat.id}`\nYou can use this ID in the CHANNEL_IDS environment variable.")
