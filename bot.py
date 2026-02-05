import os
import random
import time
from fastapi import FastAPI, HTTPException, Query
import yt_dlp
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    # Check if cookies file exists
    if os.path.exists("cookies.txt"):
        return {"status": "active", "mode": "Authenticated (cookies.txt found)"}
    else:
        return {"status": "warning", "mode": "cookies.txt NOT found"}

@app.get("/api/download")
def download_video(url: str = Query(..., description="The Instagram URL")):
    if "instagram.com" not in url:
        return {"success": False, "error": "Invalid URL"}

    # 1. Check for cookies.txt
    cookie_path = "cookies.txt"
    if not os.path.exists(cookie_path):
        return {"success": False, "error": "cookies.txt file is missing on the server!"}

    # 2. Configure yt-dlp with the cookie file
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'cookiefile': cookie_path,  # <--- CRITICAL CHANGE
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info
            info = ydl.extract_info(url, download=False)
            
            return {
                "success": True,
                "data": {
                    "title": info.get('title', 'Instagram Reel'),
                    "uploader": info.get('uploader', 'Unknown'),
                    "duration": info.get('duration', 0),
                    "thumbnail": info.get('thumbnail'),
                    "url": info.get('url'),
                }
            }
    except Exception as e:
        error_msg = str(e)
        # Help debug specific login errors
        if "Sign in" in error_msg or "challenge" in error_msg:
             return {"success": False, "error": "Cookies are invalid or expired. Please update cookies.txt."}
        return {"success": False, "error": error_msg}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
