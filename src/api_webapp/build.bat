docker build -t pteredactyl:latest .
docker run -d -p 7800:7800 --name pteredactyl-container pteredactyl:latest
