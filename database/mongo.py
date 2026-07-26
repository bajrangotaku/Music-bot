# Collections
playlists_col = db["playlists"]

# --- PLAYLIST FUNCTIONS ---
async def add_to_playlist(user_id: int, title: str, yt_url: str):
    """User ki playlist mein gaana add karta hai"""
    await playlists_col.update_one(
        {"user_id": user_id},
        {"$push": {"tracks": {"title": title, "url": yt_url}}},
        upsert=True
    )

async def get_playlist(user_id: int):
    """User ki saved playlist return karta hai"""
    data = await playlists_col.find_one({"user_id": user_id})
    return data["tracks"] if data and "tracks" in data else []

async def clear_playlist(user_id: int):
    """User ki puri playlist delete karta hai"""
    await playlists_col.delete_one({"user_id": user_id})


# --- 24/7 SETTINGS ---
async def set_247(chat_id: int, status: bool):
    """Group ke liye 24/7 mode toggle karta hai"""
    await chats_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"is_247": status}},
        upsert=True
    )

async def is_247_on(chat_id: int) -> bool:
    chat = await chats_col.find_one({"chat_id": chat_id})
    if chat and "is_247" in chat:
        return chat["is_247"]
    return False
