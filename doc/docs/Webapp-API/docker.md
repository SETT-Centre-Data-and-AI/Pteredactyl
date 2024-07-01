The app can easily be deployed using docker with a bridge network binding to port 7860. The image can be built and deployed from source as follows:

```sh
docker build -t pteredactyl:latest .
docker run -d -p 7860:7860 --name pteredactyl-app pteredactyl:latest
```
####  Docker Hub

The webapp can also be deployed directly from [Docker Hub](https://registry.hub.docker.com/r/mattstammers/pteredactyl) to any cloud service container.
