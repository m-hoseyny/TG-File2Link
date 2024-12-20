# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import logging
from pyrogram import filters, errors
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils import get_hash, get_name
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(_, m: Message):

    # Check if user has joined all required channels
    logger.info(Var.CHANNEL_IDS)
    if Var.CHANNEL_IDS:
        missing_channels = []
        for channel_id in Var.CHANNEL_IDS:
            try:
                if not str(channel_id).startswith("-100"):
                    channel_id = int('-100' + str(channel_id))
                member = await _.get_chat_member(channel_id, m.from_user.id)
                if member.status in ["left", "kicked", "banned"]:
                    chat = await _.get_chat(channel_id)
                    missing_channels.append((chat.title, chat.username or chat.invite_link))
            except errors.UserNotParticipant:
                chat = await _.get_chat(channel_id)
                missing_channels.append((chat.title, chat.username or chat.invite_link))
            except Exception as e:
                logger.error(f"Error checking channel membership: {e}")
                continue
        
        if missing_channels:
            buttons = []
            for title, link in missing_channels:
                if link:
                    buttons.append([InlineKeyboardButton(f"Join {title}", url=f"https://t.me/{link}" if not link.startswith("https://") else link)])
            
            return await m.reply(
                "To use this bot, you need to join our channel(s) first:\nبرای استفاده از بات نیاز است در کانال‌‌های زیر عضو شوید",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
    
    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    try:
        await m.reply_text(
            text="<code>{}</code>\n(<a href='{}'>shortened</a>)".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open", url=stream_link)]]
            ),
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="<code>{}</code>\n\nshortened: {})".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )
