from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

# Initialize Bot Client
bot = Client(
    "MusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

# Initialize Assistant (Userbot) Client
userbot = Client(
    "Assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Initialize PyTgCalls
call = PyTgCalls(userbot)
music_queue = {} # chat_id: [song_info_dicts]

async def play_audio(chat_id: int, audio_url: str):
    try:
        await call.play(
            chat_id,
            MediaStream(
                audio_url,
                audio_parameters=AudioQuality.HIGH
            )
        )
    except Exception as e:
        print(f"Play Error: {e}")
