docker build -t news .
docker run -it --name=news -p 5009:5000 news