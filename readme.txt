docker run -it --name=hivemq -p 1883:1883 -v docker run -it --restart always --name mqtt -p 1883:1883 -v /root/MQTT-Docker/hivemq-file-rbac-extension:/opt/hivemq-ce-2023.4/extensions/hivemq-file-rbac-extension hivemq/hivemq-ce
sudo lsof -i :1883
docker exec -it hivemq sh


docker build -t mqtt .
docker run -it --restart always --name mqtt -p 1883:1883 -v /root/MQTT-Docker/hivemq-file-rbac-extension:/opt/hivemq-ce-2023.4/extensions/hivemq-file-rbac-extension mqtt
docker run -it --restart always --name mqtt -p 1883:1883 -v /root/MQTT-Docker/hivemq-file-rbac-extension:/opt/hivemq-ce-2023.4/extensions/hivemq-file-rbac-extension -v /root/MQTT-Docker/log:/opt/hivemq-ce-2023.4/log mqtt
