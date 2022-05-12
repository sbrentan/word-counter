docker build -t %1 node/
docker run -d --network=word-counter-net -e MASTER_IP=master2 -e MASTER_PORT=58710 -e GENERATE=doc3.txt --name=%1 -v %cd%\node:/node %1