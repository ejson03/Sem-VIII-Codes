
sudo rpcbind start || true
rpcgen rpcsquare.x
./server.sh
./server.out &
P1=$!
./client.sh
./client.out
kill -9 $P1