#!/bin/bash
docker build -t $1 node/
docker run -d --network=word-counter-net --name=$1 -e MASTER_IP=master2 -e MASTER_PORT=$2 -e GENERATE=doc3.txt -v $PWD/node:/node $1