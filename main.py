import asyncio
import os
from pyrogram import idle
from player.music_engine import bot, userbot, call
from database.mongo import mongo_client
from helpers.autoleave import scheduler
from helpers.logger import logger, send_log
import player.stream_handler  # Important: Register stream end events
import plugins  # Load all commands

# Create logs directory if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

async def start_bot():
    try:
        logger.info("Starting Assistant Client...")
        await userbot.start()
        
        logger.info("Starting Bot Client...")
        await bot.start()
        
        logger.info("Starting PyTgCalls Client...")
        await call.start()
        
        logger.info("Starting Auto-Leave Scheduler...")
        scheduler.start()
        
        success_msg = "✅ Music Bot is now alive and running!"
        logger.info(success_msg)
        await send_log(success_msg)
        
        # Keep the bot running
        await idle()
        
    except Exception as e:
        from helpers.logger import handle_exception
        await handle_exception(e)
        
    finally:
        logger.info("Stopping Clients...")
        await call.stop()
        await bot.stop()
        await userbot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
