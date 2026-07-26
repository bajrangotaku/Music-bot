from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import set_247, is_247_on

@Client.on_message(filters.command("247") & filters.group)
async def toggle_247(client: Client, message: Message):
    # Ideal logic check for Group Admins can be added here
    chat_id = message.chat.id
    current_status = await is_247_on(chat_id)
    
    if current_status:
        await set_247(chat_id, False)
        await message.reply_text("❌ **24/7 Mode Disabled.**\nAb bot gaane khatam hone par VC se chala jayega.")
    else:
        await set_247(chat_id, True)
        await message.reply_text("✅ **24/7 Mode Enabled!**\nBot hamesha VC mein rahega, chahe queue khali ho.")
