from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import add_to_playlist, get_playlist, clear_playlist
from helpers.downloader import get_audio_info
from player.music_engine import play_audio, music_queue
import asyncio

@Client.on_message(filters.command("saveplaylist"))
async def save_song(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `/saveplaylist <song name or youtube link>`")
    
    query = message.text.split(" ", 1)[1]
    wait_msg = await message.reply_text("⏳ **Finding and saving track...**")
    
    try:
        track_info = await get_audio_info(query)
        await add_to_playlist(
            message.from_user.id, 
            track_info["title"], 
            track_info["webpage_url"]
        )
        await wait_msg.edit_text(f"✅ **Saved to your playlist:**\n[{track_info['title']}]({track_info['webpage_url']})", disable_web_page_preview=True)
    except Exception as e:
        await wait_msg.edit_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command("playlist"))
async def show_playlist(client: Client, message: Message):
    tracks = await get_playlist(message.from_user.id)
    if not tracks:
        return await message.reply_text("❌ Aapki playlist khali hai.")
    
    text = f"**📂 {message.from_user.first_name}'s Playlist:**\n\n"
    for i, track in enumerate(tracks[:20]): # Showing max 20 for spam control
        text += f"**{i+1}.** {track['title']}\n"
        
    text += "\n▶️ Play using `/playplaylist`"
    await message.reply_text(text)

@Client.on_message(filters.command("playplaylist") & filters.group)
async def play_user_playlist(client: Client, message: Message):
    tracks = await get_playlist(message.from_user.id)
    if not tracks:
        return await message.reply_text("❌ Aapki playlist khali hai. Pehle `/saveplaylist` se gaane add karein.")
    
    chat_id = message.chat.id
    status_msg = await message.reply_text(f"⏳ **Loading {len(tracks)} tracks into queue...**")
    
    if chat_id not in music_queue:
        music_queue[chat_id] = []
        
    added = 0
    for track in tracks:
        try:
            # Re-fetch fresh streaming URL kyunki purane expire ho jate hain
            track_info = await get_audio_info(track['url'])
            music_queue[chat_id].append(track_info)
            added += 1
            
            # Agar queue mein pehla gaana hai toh turant play start kar do
            if len(music_queue[chat_id]) == 1:
                await play_audio(chat_id, track_info["stream_url"])
                await message.reply_text(f"▶️ **Started Playing Playlist:**\n{track_info['title']}")
                
        except Exception:
            continue # Agar koi ek gaana fail ho jaye toh skip karke next add karo
            
    await status_msg.edit_text(f"✅ **Successfully added {added} tracks to the queue!**")
