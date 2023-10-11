from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
        return await m.reply("You are not <b>allowed to use</b> this <a href='https://github.com/EverythingSuckz/TG-FileStreamBot'>bot</a>.", quote=True)
    
    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")

    # Create an inline keyboard with a button that opens the file link
    inline_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Open File", url=stream_link)]]
    )

    # Send a message to the user with the file link and the "Open" button
    try:
        await m.reply_text(
            text="Short Url: <code>{}</code>\n\n Long Url: <code>{}</code>".format(
                short_link, stream_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=inline_keyboard,
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="Short Url: <code>{}</code>\n\n Long Url: <code>{}</code>".format(
                short_link, stream_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )

    # Send a separate message in the log channel with the file and the "Open" button
    await StreamBot.send_document(
        chat_id=Var.BIN_CHANNEL,
        document=log_msg.document.file_id,
        caption="File forwarded to the channel. You can access it using the link below:",
        reply_markup=inline_keyboard,
    )

    # You may also want to delete the original forwarded message from the log channel
    await log_msg.delete()
