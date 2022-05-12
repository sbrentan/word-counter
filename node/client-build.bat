docker build -t %1 node/
docker run -d --network=word-counter-net --name=%1 -e MASTER_IP=master -e MASTER_PORT=%2 -e GENERATE=doc1.txt -v %cd%\node:/node %1