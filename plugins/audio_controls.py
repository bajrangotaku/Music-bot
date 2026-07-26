from pyrogram import Client, filters
from pyrogram.types import Message
from player.music_engine import call, music_queue, play_audio
from pytgcalls.types import MediaStream, AudioQuality
from pytgcalls.exceptions import NotInCallError

# Volume Control
@Client.on_message(filters.command(["volume", "vol"]) & filters.group)
async def change_volume(client: Client, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `/volume <1-200>`")
    
    try:
        vol = int(message.command[1])
        if vol < 1 or vol > 200:
            return await message.reply_text("❌ Volume 1 se 200 ke beech honi chahiye.")
            
        await call.change_volume_call(chat_id, volume=vol)
        await message.reply_text(f"🔊 **Volume set to {vol}%**")
    except NotInCallError:
        await message.reply_text("❌ Bot kisi VC mein nahi hai.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# FFmpeg Effects (Speed/Nightcore)
@Client.on_message(filters.command(["speed", "nightcore"]) & filters.group)
async def apply_filter(client: Client, message: Message):
    chat_id = message.chat.id
    cmd = message.command[0]
    
    if chat_id not in music_queue or not music_queue[chat_id]:
        return await message.reply_text("❌ Queue khali hai. Filter kispar lagau?")

    current_track = music_queue[chat_id][0]
    stream_url = current_track["stream_url"]
    
    # Define FFmpeg parameters based on command
    ffmpeg_params = ""
    if cmd == "nightcore":
        ffmpeg_params = "-af asetrate=44100*1.25,atempo=1.25"
        text = "🌙 **Nightcore effect applied!**"
    elif cmd == "speed":
        if len(message.command) < 2:
            return await message.reply_text("❌ Usage: `/speed <0.5 to 2.0>`")
        speed = float(message.command[1])
        ffmpeg_params = f"-af atempo={speed}"
        text = f"⚡ **Speed changed to {speed}x!**"

    try:
        # Stream change karna padega naye FFmpeg filters ke sath
        await call.change_stream(
            chat_id,
            MediaStream(
                stream_url,
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=ffmpeg_params
            )
        )
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"❌ Failed to apply filter: {e}")
