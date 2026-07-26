import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("lyrics"))
async def get_lyrics(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Kiska lyrics chahiye? Usage: `/lyrics <song name>`")
    
    query = message.text.split(" ", 1)[1]
    wait_msg = await message.reply_text("🔎 **Searching for lyrics...**")
    
    try:
        # API request to fetch lyrics (Using Some Random API for free access)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.com/lyrics?title={query}") as response:
                if response.status == 200:
                    data = await response.json()
                    lyrics = data.get("lyrics")
                    title = data.get("title")
                    artist = data.get("author")
                    
                    if not lyrics:
                        return await wait_msg.edit_text("❌ Lyrics nahi mile.")
                    
                    # Telegram message limit is 4096, trimming if necessary
                    if len(lyrics) > 3500:
                        lyrics = lyrics[:3500] + "...\n\n(Lyrics too long)"
                        
                    text = f"**🎵 {title}** - *{artist}*\n\n{lyrics}"
                    await wait_msg.edit_text(text)
                else:
                    await wait_msg.edit_text("❌ Lyrics API down hai ya gaana nahi mila.")
    except Exception as e:
        await wait_msg.edit_text(f"❌ Error fetching lyrics: {str(e)}")
