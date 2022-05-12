docker build -t monitor monitor/
p1=$1
p2=$(( $1 + 10 ))
p3=$(( $1 + 20 ))
p4=$(( $1 + 30 ))
docker run -d -p 8080:80 -p $p1:$p1 -p $p2:$p2 -p $p3:$p3 -p $p4:$p4 -e EXP_PORT=$p1 -e ACCEPT_MODE=passive --name=monitor --network=word-counter-net -v $PWD/monitor:/monitor -v $PWD/master:/master monitor