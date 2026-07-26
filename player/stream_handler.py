from pytgcalls.types import Update
from pytgcalls import filters as ptc_filters
from player.music_engine import call, play_audio, music_queue
import logging

logger = logging.getLogger(__name__)

# Yeh function tab trigger hoga jab current stream khatam hogi
@call.on_stream_end()
async def on_stream_end_handler(client, update: Update):
    chat_id = update.chat_id
    
    if chat_id in music_queue and len(music_queue[chat_id]) > 1:
        # Puraana gaana list se hatao
        music_queue[chat_id].pop(0)
        next_track = music_queue[chat_id][0]
        
        try:
            # Next gaana stream karo
            await play_audio(chat_id, next_track["stream_url"])
            logger.info(f"Auto-playing next track in {chat_id}")
        except Exception as e:
            logger.error(f"Error playing next track in {chat_id}: {e}")
    else:
        # Agar queue khali hai toh VC se exit karo
        if chat_id in music_queue:
            music_queue[chat_id].clear()
        
        await call.leave_call(chat_id)
        logger.info(f"Queue empty, left VC in {chat_id}")
