docker build --build-arg MASTER_IP=master --build-arg MASTER_PORT=57710 -t %1 - < client.dockerfile
docker run -d --network=sample-net --name=%1 -v C:/Users/Simone/Documents/Workspace/word-wrapper/node:/node %1