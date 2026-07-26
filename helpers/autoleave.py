from apscheduler.schedulers.asyncio import AsyncIOScheduler
from player.music_engine import call, music_queue
from database.mongo import is_247_on
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

async def check_idle_calls():
    """Har 5 minute mein inactive calls check karega"""
    try:
        # PyTgCalls active streams ki list return karta hai
        active_calls = await call.active_calls()
        
        for chat_call in active_calls:
            chat_id = chat_call.chat_id
            
            # Agar chat queue mein nahi hai ya khali hai
            if chat_id not in music_queue or len(music_queue[chat_id]) == 0:
                # Check agar 24/7 on hai
                if await is_247_on(chat_id):
                    continue
                    
                # Agar 24/7 off hai aur gaana nahi chal raha, toh leave VC
                await call.leave_call(chat_id)
                logger.info(f"Auto-left idle VC in chat {chat_id}")
    except Exception as e:
        logger.error(f"Auto-leave error: {e}")

# Scheduler ko har 5 minute par run karne ke liye set kiya
scheduler.add_job(check_idle_calls, "interval", minutes=5)
