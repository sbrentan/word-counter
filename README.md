# Word Counter
## Architecture
The application uses the fog computing approach to manage text-generated data on multiple nodes and obtains the top most used words to be displayed in a central node.
To light the workloads of the nodes in case of a great number of text-genereted data, master nodes are used to mediate between edge nodes and central node.
The application architecture is further described in the file [Description.pdf](Description.pdf)

## Test the application on docker

For the application to work correctly on a single computer, a docker network connecting the containers is needed. Run the command to create the network:
```
docker network create word-counter-net
```
The containers we will use will be part of that network

### On Windows

Open the downloaded directory on cmd.exe and run
```
call monitor/start.bat 56700
call master/master-build.bat master 57700 56700
call node/client-build.bat node 57700
```

### On Linux
```
bash monitor/start.sh 56700
bash master/master-build.sh master 57700 56700
bash node/client-build.sh node 57700
```

## Application usage


These files will execute `docker build` and `docker run` with the respective parameters to start the 3 containers.
The `monitor` node needs as parameter the port it uses to expose the socket, `node` needs only the master port (master ip set as default "master") and `master` needs both.
There will be a container named `monitor` with a flask application installed on it that corresponds to the monitor on the centered application.
The `master` node will be connected through socket to the monitor and will communicate with `node` for the monitor.

Its web service is available on port 8080 at link [/top_words](http://localhost:8080/top_words).

At `node` startup, a document has already been generated. After a while the monitor should receive the data and show it on the page.
The data generated for now is a simple one with just few words.

Default data transmission mode is **passive**, that means that data will be uploaded to the master every 5 seconds(default), so to limit network usage.
Therefore after refreshing the *top_words* page in 5 seconds the word list will be updated, showing the top words and for each word its *references*, 
that is the files where the word has been found. Clicking on one of the names the document will be downloaded.

Now let's try with more masters and nodes. Run in order in the same directory as before:
### On Windows
```
call master/master-build.bat master2 58700 56700
call node/client2-build.bat node2 58700
call node/client3-build.bat node3 58700
```
### On Linux
```
bash master/master2-build.sh master2 58700 56700
bash node/client2-build.sh node2 58700
bash node/client3-build.sh node3 58700
```
This will create a new master named `master2` and two nodes connected to it named `node2` and `node3`.
As the nodes and masters need to use different ports between each other on the same machine, 
different script has been created to simplify the process of creation of the test.

This time some documents has already been generated at node startups, respectively doc2.txt and doc3.txt for `node2` and `node3`

Now after a while when `/top_words` is refreshed it's possible to see new documents in the *references* column and updated word counters.
After the nodes started, the documents were detected as generated data and sent passively to the master node( `master2` ).
The data, afterword, is sent to `monitor` updated.

The communication between the monitor and the masters so far has been `passive`, that means the data is uploaded automatically.

With [/accept_mode/active](http://localhost:8080/accept_mode/active) it can be changed to `active`,
so that the monitor actively asks and wait for the masters responses with the data updated. For this reason the page takes some more time to load.

With [/accept_mode/passive](http://localhost:8080/accept_mode/passive) it can be reversed to `passive`.
The only transmission mode it changes is the one between the monitor and the monitor children, so the say the masters.
Whereas between the masters and their children the mode remains unchanged as passive.






