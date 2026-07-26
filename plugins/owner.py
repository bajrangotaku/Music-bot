import sys
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID
from database.mongo import users_col, chats_col

# Restart Bot
@Client.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def restart_bot(client: Client, message: Message):
    await message.reply_text("🔄 **Bot is restarting...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Broadcast Message to all groups
@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_msg(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Ek message ka reply karo jise broadcast karna hai.")
    
    wait_msg = await message.reply_text("⏳ **Broadcasting started...**")
    success = 0
    failed = 0
    
    # Fetch all chats from DB
    async for chat in chats_col.find():
        try:
            await message.reply_to_message.copy(chat["chat_id"])
            success += 1
        except Exception:
            failed += 1
            
    await wait_msg.edit_text(f"✅ **Broadcast Complete!**\n\n📩 Success: `{success}` groups\n❌ Failed: `{failed}` groups")

# Eval command for running python code directly (Debugging)
@Client.on_message(filters.command("eval") & filters.user(OWNER_ID))
async def eval_code(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Code likho evaluate karne ke liye.")
        
    code = message.text.split(" ", 1)[1]
    
    try:
        # Caution: Very dangerous if misused, only for OWNER
        result = eval(code)
        await message.reply_text(f"💻 **Code Executed!**\n\n**Result:**\n`{result}`")
    except Exception as e:
        await message.reply_text(f"❌ **Error:**\n`{e}`")
