docker build -t fuel-api .
docker run -it --restart always --name FUEL-API -p 5005:5000 fuel-api