docker build -t wrapper - < server.dockerfile
docker run -d -p 56733:56733 --name=wrapper --network=sample-net -v C:/Users/Simone/Documents/Workspace/word-wrapper/wrapper-node:/app wrapper