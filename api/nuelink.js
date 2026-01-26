const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const path = require('path');
const app = express();

app.use(cors());

app.get('/api/nuelink', (req, res) => {
    const videoUrl = req.query.url;

    console.log(`\n📥 Request: ${videoUrl}`);

    if (!videoUrl) {
        return res.status(400).json({ success: false, message: "URL missing!" });
    }

    // Path to your cookies file in the root
    const cookiePath = path.join(__dirname, '../cookies.txt');

    // Command with Cookies, User-Agent and Metadata Dump
    const command = `python3 -m yt_dlp --cookiefile "${cookiePath}" --dump-json --no-check-certificate --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" --format "best" "${videoUrl}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`❌ Error: ${stderr}`);
            return res.status(500).json({ 
                success: false, 
                message: "Instagram Blocked the request. Check your cookies.txt",
                error: stderr.split('\n')[0] 
            });
        }

        try {
            const data = JSON.parse(stdout);
            res.json({
                success: true,
                data: {
                    title: data.title || "Instagram Video",
                    thumbnail: data.thumbnail,
                    url: data.url,
                    uploader: data.uploader,
                    duration: data.duration_string
                }
            });
            console.log(`✅ Success: ${data.title}`);
        } catch (e) {
            res.status(500).json({ success: false, message: "Data parsing failed." });
        }
    });
});

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`🚀 API Live on Port ${PORT}`));
