from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import time

bot_start_time = time.time()

@Client.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me to Your Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("📚 Help & Commands", callback_data="help_menu")]
        ])
        
        await message.reply_text(
            f"Hey {message.from_user.first_name}! 👋\n\n"
            f"Main ek **Advanced Music Bot** hoon. Main aapke group ke VC mein high-quality music aur video stream kar sakta hoon.\n\n"
            f"Kripya mujhe apne group mein add karein aur admin banayein taaki main proper function kar sakun.",
            reply_markup=markup
        )
    else:
        await message.reply_text("✅ **Bot zinda hai!** Music play karne ke liye `/play <song>` use karein.")


@Client.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    start = time.time()
    reply = await message.reply_text("🏓 Pong...")
    end = time.time()
    
    latency = round((end - start) * 1000, 2)
    uptime = round(time.time() - bot_start_time)
    
    # Uptime format (Seconds to HH:MM:SS)
    uptime_formatted = time.strftime("%H:%M:%S", time.gmtime(uptime))
    
    await reply.edit_text(
        f"🏓 **Pong!**\n\n"
        f"**Latency:** `{latency}ms`\n"
        f"**Uptime:** `{uptime_formatted}`"
    )
