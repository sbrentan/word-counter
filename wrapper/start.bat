docker build -t monitor .
docker run -d -p 56700:80 -p 56710:56710 -p 56720:56720 --name=monitor --network=sample-net -v C:/Users/Simone/Documents/Workspace/word-wrapper/wrapper:/app monitor