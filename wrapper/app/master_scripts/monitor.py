from collections import Counter
from multiprocessing import Process
import socket
import os
import glob

nodes = []
no_data_nodes = 0

def main():
    global nodes
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
            file = open("app/master_scripts/save/command.txt", "r")
            cmd = file.readline()
            file.close()
            connection.sendall(cmd.encode())
        elif(msg == "register"):
            nodes = read_nodes()
            new_node = len(nodes)+1
            nodes_file = open("app/master_scripts/save/nodes.txt", "a")
            nodes_file.write(" "+str(new_node))
            nodes_file.close()
            nodes += [new_node]
            connection.sendall(str(new_node).encode())


def send_command(command):
   file = open("app/master_scripts/save/command.txt", "r")
   cmd_code, cmd_txt = file.readline().split(" ", 1)
   file.close()
   cmd_code = int(cmd_code) + 1

   file = open("app/master_scripts/save/command.txt", "w")
   file.write(str(cmd_code) + " " + command)
   file.close()

def read_nodes():
   nodes_file = open("app/master_scripts/save/nodes.txt", "r")
   nodes_txt = nodes_file.readline()
   nodes_file.close()
   nodes = filter(lambda x: bool(x.strip()), nodes_txt.split(" "))
   nodes = list(map(lambda x: int(x), nodes))
   print("Nodes are: ")
   print(nodes_txt)
   print(nodes)
   return nodes

def receive_file(node_id, conn, filename):
   filesize = int.from_bytes(conn.recv(16), byteorder='big')
   print("filesize " + str(filesize))

   filetodown = open(filename, "wb")

   l = conn.recv(filesize)
   # l = conn.recv(1024)
   # total = len(l)
   # while(l):
   #    print("Receiving...")

   #    filetodown.write(l) 
   #    if (total != filesize):
   #       print('trying to receive')
   #       l = conn.recv(1024)
   #       total = total + len(l)
   #    else:
   #       break
   filetodown.write(l) 

   filetodown.close()



   # total = 0
   # while True:
   #    print("Receiving....")
   #    data = conn.recv(1024)
   #    print(data.decode())
   #    if data == "DONE\n" or not data:
   #       print("Done Receiving.")
   #       break
   #    filetodown.write(data)
   # filetodown.close()

def read_counters():
   counters = {}
   count_file_r = open("app/master_scripts/save/counters.txt", "r")
   lines = count_file_r.readlines()
   count_file_r.close()

   for line in lines:
      word, count_txt = line.split(" ", 1)
      counters[word] = int(count_txt)

   counters = Counter(counters)
   return counters

def write_counters(counters):
   count_file = open("app/master_scripts/save/counters.txt", "w")
   for count in counters.most_common():
      if(count[0] != ''):
         count_file.write(count[0] + " " + str(count[1]) + "\n")
   count_file.close()

def update_counters():
   
   counters = read_counters()
   for filename in os.listdir("app/master_scripts/counters/"):
      with open(os.path.join("app/master_scripts/counters/", filename), 'r') as f: # open in readonly mode
         lines = f.readlines()
         f.close()

         c = {}
         for line in lines:
            print(line)
            if(len(line.split(" ")) < 2):
               continue
            word, count_txt = line.split(" ", 1)
            c[word] = int(count_txt)
         print(c)
         counters += Counter(c)
   
   write_counters(counters)

   files = glob.glob('app/master_scripts/counters/*')
   for f in files:
       os.remove(f)

def read_occurrences():
   occurrences = {}
   occ_file_r = open("app/master_scripts/save/occurrences.txt", "r")
   lines = occ_file_r.readlines()
   occ_file_r.close()

   for line in lines:
      word, occ_txt = line.split(" ", 1)
      occurrences[word] = occ_txt.strip().split(" ")
   return occurrences

def write_occurrences(occurrences):
   occ_file = open("app/master_scripts/save/occurrences.txt", "w")
   for occ in occurrences.items():
      if(occ[0] != ''):
         occ_file.write(occ[0] + " " + ' '.join(occ[1]) + "\n")
   occ_file.close()

def update_occurrences():

   occurrences = read_occurrences()
   print("occurrences: ")
   print(occurrences)
   for filename in os.listdir("app/master_scripts/occurrences/"):
      with open(os.path.join("app/master_scripts/occurrences/", filename), 'r') as f: # open in readonly mode
         lines = f.readlines()
         f.close()
         for line in lines:
            word, occ_txt = line.split(" ", 1)
            occs = occ_txt.strip().split(" ")
            if word not in occurrences:
               occurrences[word] = occs
            else:
               for occ in occs:
                  if occ not in occurrences[word]:
                     occurrences[word].append(occ)

   print(occurrences)
   write_occurrences(occurrences)

   files = glob.glob('app/master_scripts/occurrences/*')
   for f in files:
       os.remove(f)


def receive_document(filename):
   s = socket.socket()
   s.bind(("monitor", 56740))
   s.listen(1)
   c,a = s.accept()
   node_id = str(int.from_bytes(c.recv(16), byteorder='big'))
   receive_file(node_id, c, "app/master_scripts/documents/"+filename+".txt")
   c.shutdown(2)
   c.close()
   s.close()

def receive():
   nodes = read_nodes()

   s = socket.socket()
   s.bind(("monitor", 56720))
   s.listen(1)
   for i in range(len(nodes)):

      c,a = s.accept()
      print("Connection accepted")
      node_id = str(int.from_bytes(c.recv(16), byteorder='big'))
      print("Received node id " + node_id)

      msg = c.recv(4)
      print(msg.decode())
      if(msg.decode() == "send"):
         print("Receiving files")
         receive_file(node_id, c, "app/master_scripts/counters/counter"+node_id+".txt")
         receive_file(node_id, c, "app/master_scripts/occurrences/occurrences"+node_id+".txt")

      c.shutdown(2)
      c.close()

   s.close()
   print("received all node counters")

   update_counters()
   print("update")
   update_occurrences()


p = Process(target=main)
p.start()