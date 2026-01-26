from http.server import BaseHTTPRequestHandler
import json
import yt_dlp
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. URL se query parameters nikalna
        query = urlparse(self.path).query
        params = parse_qs(query)
        video_url = params.get('url', [None])[0]

        if not video_url:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "message": "URL missing!"}).encode())
            return

        # 2. yt-dlp ki settings
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 3. Scraping logic
                info = ydl.extract_info(video_url, download=False)
                
                response_data = {
                    "success": True,
                    "data": {
                        "title": info.get('title'),
                        "thumbnail": info.get('thumbnail'),
                        "url": info.get('url'),
                        "uploader": info.get('uploader'),
                        "duration": info.get('duration_string')
                    }
                }

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*') # CORS allow
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
