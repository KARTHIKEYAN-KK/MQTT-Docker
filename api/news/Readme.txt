docker build -t news .
docker run -it --restart always --name=news -p 5009:5000 news