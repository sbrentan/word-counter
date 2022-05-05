import socket

def receive():
   nodes = []

   def read_nodes():
      global nodes
      nodes_file = open("save/nodes.txt", "r")
      nodes_txt = nodes_file.readline()
      nodes_file.close()
      nodes = filter(lambda x: bool(x.strip()), nodes_txt.split(" "))
      nodes = list(map(lambda x: int(x), nodes))

   read_nodes()

   s = socket.socket()
   s.bind(("monitor", 56720))
   s.listen(1)
   for i in range(len(nodes)):

      c,a = s.accept()
      msg = c.recv(100)
      node_id = msg.decode()

      filetodown = open("counters/counter"+node_id+".txt", "wb")
      while True:
         print("Receiving....")
         data = c.recv(1024)
         if data == b"DONE":
            print("Done Receiving.")
            break
         filetodown.write(data)
      filetodown.close()
      c.shutdown(2)
      c.close()

   s.close()
   print("received all node counters")

