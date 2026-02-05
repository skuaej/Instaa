import os
import time
import random
from fastapi import FastAPI, HTTPException, Query
import yt_dlp
import uvicorn

app = FastAPI()

# List of real browser User-Agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
]

@app.get("/")
def home():
    return {"status": "active", "message": "API is running."}

@app.get("/api/download")
def download_video(url: str = Query(..., description="The Instagram URL")):
    if "instagram.com" not in url:
        return {"success": False, "error": "Invalid URL"}

    # 1. Add a random delay (1-3 seconds) to mimic human behavior
    # This slows down the bot but protects the IP
    time.sleep(random.uniform(1.0, 3.0))

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'user_agent': random.choice(USER_AGENTS), # Randomize User Agent
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'no_color': True,
        'geo_bypass': True,
        # 'cookies': 'cookies.txt',  <-- NEVER USE THIS WITH YOUR MAIN ACCOUNT
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Check if we actually got a URL
            if not info or 'url' not in info:
                return {"success": False, "error": "Instagram requires login for this reel."}

            return {
                "success": True,
                "data": {
                    "title": info.get('title', 'Instagram Reel'),
                    "uploader": info.get('uploader', 'Unknown'),
                    "duration": info.get('duration', 0),
                    "thumbnail": info.get('thumbnail'),
                    "url": info.get('url'),
                    "webpage_url": info.get('webpage_url')
                }
            }
    except Exception as e:
        # If Instagram blocks the IP, you will see HTTP 429 or 403 here
        return {"success": False, "error": f"Instagram blocked the request: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
