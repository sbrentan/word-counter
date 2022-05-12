docker build -t %1 node/
docker run -d --network=word-counter-net --name=%1 -e MASTER_IP=master -e MASTER_PORT=57710 -v %cd%\node:/node %1