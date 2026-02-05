from fastapi import FastAPI, HTTPException, Query
import yt_dlp
import uvicorn

app = FastAPI()

def get_instagram_data(url: str):
    # Configure yt-dlp to extract data without downloading
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',  # Select best quality
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "success": True,
                "data": {
                    "title": info.get('title', 'Instagram Reel'),
                    "uploader": info.get('uploader', 'Unknown'),
                    "duration": info.get('duration', 0),
                    "thumbnail": info.get('thumbnail'),
                    "url": info.get('url'),  # Direct video stream link
                    "webpage_url": info.get('webpage_url')
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

@app.get("/")
def home():
    return {"message": "Instagram API is running. Use /api/download?url=YOUR_LINK"}

@app.get("/api/download")
def download_video(url: str = Query(..., description="The Instagram URL")):
    if "instagram.com" not in url:
        return {"success": False, "error": "Invalid URL. Must be an Instagram link."}
    
    result = get_instagram_data(url)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
