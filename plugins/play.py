from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.downloader import get_audio_info
from player.music_engine import play_audio, music_queue, call
from pytgcalls.exceptions import NotInCallError

@Client.on_message(filters.command(["play", "vplay"]) & filters.group)
async def play_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /play <song name or url>")

    query = message.text.split(" ", 1)[1]
    processing_msg = await message.reply_text("🔎 **Searching...**")

    try:
        # Extract audio info asynchronously
        track_info = await get_audio_info(query)
        chat_id = message.chat.id

        # Queue Management
        if chat_id not in music_queue:
            music_queue[chat_id] = []
        
        music_queue[chat_id].append(track_info)

        # UI Keyboard
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                InlineKeyboardButton("▶️ Resume", callback_data="resume"),
                InlineKeyboardButton("⏭ Skip", callback_data="skip")
            ],
            [InlineKeyboardButton("❌ Stop", callback_data="stop")]
        ])

        # If it's the first song, play it directly
        if len(music_queue[chat_id]) == 1:
            await play_audio(chat_id, track_info["stream_url"])
            await processing_msg.delete()
            await message.reply_photo(
                photo=track_info["thumbnail"],
                caption=f"🎵 **Now Playing:** [{track_info['title']}]({track_info['webpage_url']})\n⏱ **Duration:** {track_info['duration']}s\n👤 **Requested by:** {message.from_user.mention}",
                reply_markup=markup
            )
        else:
            await processing_msg.edit_text(
                f"📝 **Added to Queue at position #{len(music_queue[chat_id]) - 1}:**\n[{track_info['title']}]({track_info['webpage_url']})"
            )

    except Exception as e:
        await processing_msg.edit_text(f"❌ **Error:** {str(e)}")
