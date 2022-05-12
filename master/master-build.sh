docker build -t $1 master/
p1=$2
p2=$(( $2 + 10 ))
p3=$(( $2 + 20 ))
p4=$(( $2 + 30 ))
docker run -d -p $p1:$p1 -p $p2:$p2 -p $p3:$p3 -p $p4:$p4 -e EXP_PORT=$p1 -e SELF_NAME=$1 -e MASTER_PORT=$3 -e ACCEPT_MODE=passive --network=word-counter-net --name=$1 -v $PWD/node:/node -v $PWD/master:/master $1