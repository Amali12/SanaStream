# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import logging
from pyrogram import Client
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
    if Var.ALLOWED_USERS and not ((str(m.from_user.id) in Var.ALLOWED_USERS) or (m.from_user.username in Var.ALLOWED_USERS)):
        return await m.reply("Sorry you are not <b>allowed to use</b> this bot.", quote=True)
    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    short_hash = f"{file_hash}{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    try:
        await log_msg.reply_text(
            text=f"**⚡Short Url:-**\n{short_link}\n\n**⚡Short Hash:-**\n`{short_hash}`\n\n**⚡Long Url:-**\n{stream_link}",
            quote=True,
            parse_mode=ParseMode.MARKDOWN
        )
        await m.reply_text(
            text="<b>⚡Short Url:-</b>\n<code>{}</code>\n\n<b>⚡Short Hash:-</b>\n<code>{}</code>\n\n <b>⚡Long Url:-</b>\n<code>{}</code>".format(
                short_link, short_hash, stream_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Link", url=short_link)]]
            ),
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="<b>⚡Short Url:-</b>\n<code>{}</code>\n\n<b>⚡Short Hash:-</b>\n<code>{}</code>\n\n <b>⚡Long Url:-</b>\n<code>{}</code>".format(
                short_link, short_hash, stream_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )
