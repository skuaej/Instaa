const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const app = express();

app.use(cors());

// Ye endpoint ab aapke file name se match karega
app.get('/api/nuelink', (req, res) => {
    const videoUrl = req.query.url;

    console.log(`📥 Request Received for: ${videoUrl}`);

    if (!videoUrl) {
        return res.status(400).json({ success: false, message: "URL missing!" });
    }

    // Pro command to get high quality video
    const command = `python3 -m yt_dlp --dump-json --no-check-certificate --format "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" "${videoUrl}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`❌ Scraper Error: ${stderr}`);
            return res.status(500).json({ success: false, message: "Scraping failed." });
        }

        try {
            const metadata = JSON.parse(stdout);
            res.json({
                success: true,
                data: {
                    title: metadata.title,
                    thumbnail: metadata.thumbnail,
                    url: metadata.url, // Main Video URL
                    uploader: metadata.uploader,
                    duration: metadata.duration_string
                }
            });
            console.log(`✅ Done: ${metadata.title}`);
        } catch (e) {
            res.status(500).json({ success: false, message: "JSON parsing error." });
        }
    });
});

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`🚀 API is running on port ${PORT}`));
