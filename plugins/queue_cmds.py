from pyrogram import Client, filters
from pyrogram.types import Message
from player.music_engine import music_queue
import random

@Client.on_message(filters.command("queue") & filters.group)
async def show_queue(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id not in music_queue or not music_queue[chat_id]:
        return await message.reply_text("❌ Queue bilkul khali hai. Kuch play toh karo!")
    
    text = "**🎵 Current Queue:**\n\n"
    for i, track in enumerate(music_queue[chat_id]):
        if i == 0:
            text += f"▶️ **Now Playing:** {track['title']} ({track['duration']}s)\n\n"
        else:
            text += f"**{i}.** {track['title']}\n"
        
        # Spam se bachne ke liye sirf top 10 gaane dikhayenge
        if i >= 10: 
            text += f"\n*...aur {len(music_queue[chat_id]) - 11} gaane.*"
            break
    
    await message.reply_text(text, disable_web_page_preview=True)


@Client.on_message(filters.command("clearqueue") & filters.group)
async def clear_queue(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id in music_queue and len(music_queue[chat_id]) > 1:
        # Current playing gaana save rakho, baaki sab hata do
        current_song = music_queue[chat_id][0]
        music_queue[chat_id] = [current_song]
        await message.reply_text("✅ Queue clear kar di gayi hai (Current gaana chalta rahega).")
    else:
        await message.reply_text("❌ Queue pehle se hi khali hai.")


@Client.on_message(filters.command("shuffle") & filters.group)
async def shuffle_queue(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id in music_queue and len(music_queue[chat_id]) > 2:
        current_song = music_queue[chat_id][0]
        upcoming = music_queue[chat_id][1:]
        
        # Upcoming gaano ko mix karo
        random.shuffle(upcoming)
        music_queue[chat_id] = [current_song] + upcoming
        
        await message.reply_text("🔀 **Queue shuffle kar di gayi hai!**")
    else:
        await message.reply_text("❌ Shuffle karne ke liye queue mein kam se kam 2 gaane hone chahiye.")
