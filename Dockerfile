FROM node:18-slim

# System setup
RUN apt-get update && \
    apt-get install -y python3 python3-pip ffmpeg && \
    ln -s /usr/bin/python3 /usr/bin/python

# Force update yt-dlp to latest
RUN pip3 install -U yt-dlp --break-system-packages

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Permissions fix for cookies
RUN chmod 644 cookies.txt

EXPOSE 8000
CMD ["node", "api/nuelink.js"]
