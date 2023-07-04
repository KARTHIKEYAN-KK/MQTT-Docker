docker run -it --name=hivemq -p 1883:1883 -v /home/ubuntu/mqtt/hivemq-file-rbac-extension:/opt/hivemq-ce-2023.4/extensions/hivemq-file-rbac-extension hivemq/hivemq-ce
sudo lsof -i :1883
docker exec -it hivemq sh


docker build -t mqtt .
docker run -it --name mqtt -p 1883:1883 -v /home/mqtt/ubuntu/hivemq-file-rbac-extension:/opt/hivemq-ce-2023.4/extensions/hivemq-file-rbac-extension mqtt