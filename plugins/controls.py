from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from player.music_engine import call, music_queue, play_audio
from pytgcalls.exceptions import NotInCallError

@Client.on_callback_query(filters.regex("^(pause|resume|skip|stop)$"))
async def control_cb(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    action = query.data

    try:
        if action == "pause":
            await call.pause_stream(chat_id)
            await query.answer("Stream Paused.")
        
        elif action == "resume":
            await call.resume_stream(chat_id)
            await query.answer("Stream Resumed.")
            
        elif action == "stop":
            await call.leave_call(chat_id)
            music_queue[chat_id].clear()
            await query.answer("Stream Stopped and Queue Cleared.")
            await query.message.reply_text("⏹ **Music stopped and bot left VC.**")
            
        elif action == "skip":
            if chat_id in music_queue and len(music_queue[chat_id]) > 1:
                music_queue[chat_id].pop(0) # Remove current song
                next_track = music_queue[chat_id][0]
                await play_audio(chat_id, next_track["stream_url"])
                await query.answer("Skipped to next track.")
                await query.message.reply_text(f"⏭ **Skipped! Now Playing:** {next_track['title']}")
            else:
                await call.leave_call(chat_id)
                if chat_id in music_queue:
                    music_queue[chat_id].clear()
                await query.answer("Queue empty, leaving VC.")
                await query.message.reply_text("Queue is empty. Leaving voice chat.")

    except NotInCallError:
        await query.answer("Bot is not in a voice call!", show_alert=True)
    except Exception as e:
        await query.answer(f"Error: {str(e)}", show_alert=True)
