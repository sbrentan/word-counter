import socket

nodes = []

def read_nodes():
    global nodes
    nodes_file = open("save/nodes.txt", "r")
    nodes_txt = nodes_file.readline()
    nodes_file.close()
    nodes = map(lambda x: int(x), split(nodes_txt, " "))

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('monitor', 56710))
serversocket.listen(5) # become a server socket, maximum 5 connections

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(512)
    if(len(buf) < 1):
        break
    msg = buf.decode()
    if(msg == "request"):
        file = open("save/command.txt", "r")
        cmd = file.readline()
        file.close()
        connection.sendall(cmd.encode())
    elif(msg == "register"):
        new_node = len(nodes)+1
        nodes_file = open("save/nodes.txt", "a")
        nodes_file.write(" "+str(new_node))
        nodes_file.close()
        nodes += [new_node]
        connection.sendall(str(new_node).encode())