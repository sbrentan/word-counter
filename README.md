# word-counter
## Architecture
The application uses the fog computing approach to manage text-generated data on multiple nodes and obtains the top most used words to be displayed in a central node.
To light the workloads of the nodes in case of a great number of text-genereted data, master nodes are used to mediate between edge nodes and central node.
The application architecture is further described on file [Architecture.pdf](docs/Architecture.pdf)

## Test the application on docker

For the application to work correctly on a single computer, a docker network connecting the containers is needed. Run the command to create the network:
```
docker network create word-counter-net
```
The containers we will use will be part of that network

### On Windows

Open the downloaded directory on cmd.exe and run
```
call monitor/start.bat
call master/master-build.bat master
call node/client-build.bat node
```

### On Linux
```
bash monitor/start.sh
bash master/master-build.sh master
bash node/client-build.sh node
```

## Application usage


These files will execute `docker build` and `docker run` with the respective parameters to start the 3 containers.
There will be a container named `monitor` with a flask application installed on it that corresponds to the monitor on the centered application.
The `master` node will be connected through socket to the monitor and will communicate with `node` for the monitor.

Its web service is available on port 56700 at link /top_words. Full link: [http://localhost:56700/top_words](http://localhost:56700/top_words).

Now the page will display an empty list, because no data has been generated yet.
To *generate* data on the node, open the node cli and run:
```
python /node/generator.py
```
This will generate a document named doc1.txt in folder /documents that will be read by the application and uploaded to master through socket connections.
The data generated for now is a simple one with just few words.

Default data transmission mode is **passive**, that means that data will be uploaded to the master every 5 seconds(default), so to limit network usage.
Therefore after refreshing the *top_words* page in 5 seconds the word list will be updated, showing the top words and for each word its *references*, 
that is the files where the word has been found. Clicking on one of the names the document will be downloaded.

Now let's try with more masters and nodes. Run in order in the same directory as before:
### On Windows
```
call master/master2-build.bat master2
call node/client2-build.bat node2
call node/client3-build.bat node3
```
### On Linux
```
bash master/master2-build.sh master2
bash node/client2-build.sh node2
bash node/client3-build.sh node3
```
This will create a new master named `master2` and two nodes connected to it named `node2` and `node3`.
As the nodes and masters need to use different ports between each other on the same machine, 
different script has been created to simplify the process of creation of the test.

This time some documents has already been generated at node startups, respectively doc2.txt and doc3.txt for `node2` and `node3`

Now after a while when `/top_words` is refreshed it's possible to see new documents in the *references* column and updated word counters.
After the nodes started the documents were detected as generated data and send passively to the master node( `master2` ).
The data, afterword, was sent to `monitor` and was updated





