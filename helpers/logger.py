import logging
import traceback
from config import LOG_GROUP_ID
from player.music_engine import bot

# Console logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MusicBot")

async def send_log(message: str):
    """Sends log text to the Telegram Log Group"""
    try:
        if LOG_GROUP_ID:
            await bot.send_message(LOG_GROUP_ID, f"📝 **Bot Log:**\n`{message}`")
    except Exception as e:
        logger.error(f"Failed to send log to Telegram: {e}")

async def handle_exception(e: Exception):
    """Formats and sends exception tracebacks"""
    error_trace = traceback.format_exc()
    logger.error(error_trace)
    
    # Telegram message limit is 4096, truncate if necessary
    if len(error_trace) > 4000:
        error_trace = error_trace[-4000:]
        
    await send_log(f"❌ **CRITICAL ERROR:**\n\n`{error_trace}`")
