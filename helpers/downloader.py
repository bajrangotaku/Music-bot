import asyncio
import yt_dlp

ydl_opts = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
}

def extract_info_sync(query: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if not query.startswith("http"):
            query = f"ytsearch:{query}"
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            return info["entries"][0]
        return info

async def get_audio_info(query: str):
    # Running blocking yt-dlp in a separate thread
    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, extract_info_sync, query)
    return {
        "title": info["title"],
        "duration": info["duration"],
        "stream_url": info["url"],
        "thumbnail": info.get("thumbnail"),
        "webpage_url": info["webpage_url"]
    }
