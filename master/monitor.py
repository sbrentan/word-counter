from collections import Counter
from multiprocessing import Process
import sys
import socket
import os
import glob

self_name = "monitor" #127.0.0.1
is_monitor = False
nodes = []
exp_port     = int(os.environ['EXP_PORT'])

def main(mode="active"):
   print("monitor main")

   global nodes, is_monitor, self_name, exp_port

   accept_mode = mode
   if(len(sys.argv) > 1): #is master node
      # master_node = sys.argv[1]
      accept_mode = sys.argv[1]
      master_node = os.environ['MASTER_IP']
   else:
      is_monitor = True
   f = open("/save/accept_mode.txt", "w")
   f.write(accept_mode)
   f.close()

   if not is_monitor:
      import node.updater as node
      self_name = os.environ['SELF_NAME']
      print("not is_monitor")
      p = Process(target=node.main, args=(master_node, receive, receive_document))
      p.start()
   # else:
   #    global monitor_port
   #    monitor_port = int(os.environ['MONITOR_PORT'])

   if(accept_mode == "passive"):
      p = Process(target=passive_receive, args=())
      p.start()

   print("Opening socket " + self_name + " " + str(exp_port))
   sys.stdout.flush()
   serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   serversocket.bind((self_name, exp_port))
   serversocket.listen()

   print("waiting connections")
   sys.stdout.flush()
   while True:
      connection, address = serversocket.accept()
      buf = connection.recv(100)
      if(len(buf) < 1):
         break
      msg = buf.decode()
      if(msg == "request"):
         file = open("/save/command.txt", "r")
         cmd = file.readline()
         file.close()
         connection.sendall(cmd.encode())
      elif(msg == "register"):
         nodes = read_nodes()
         new_node = len(nodes)+1
         nodes_file = open("/save/nodes.txt", "a")
         nodes_file.write(" "+str(new_node))
         nodes_file.close()
         nodes += [new_node]
         print("registered node id "+ str(new_node) + " with mode " + accept_mode)
         sys.stdout.flush()
         connection.sendall((str(new_node)+" "+accept_mode).encode())
      connection.shutdown(2)
      connection.close()
      sys.stdout.flush()


def send_command(command):
   file = open("/save/command.txt", "r")
   cmd_code, cmd_txt = file.readline().split(" ", 1)
   file.close()
   cmd_code = int(cmd_code) + 1

   file = open("/save/command.txt", "w")
   file.write(str(cmd_code) + " " + command)
   file.close()

def read_nodes():
   nodes_file = open("/save/nodes.txt", "r")
   nodes_txt = nodes_file.readline()
   nodes_file.close()
   nodes = filter(lambda x: bool(x.strip()), nodes_txt.split(" "))
   nodes = list(map(lambda x: int(x), nodes))
   print("Nodes are: " + nodes_txt)
   return nodes

def receive_file(node_id, conn, filename):
   filesize = int.from_bytes(conn.recv(4), byteorder='big')
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
   count_file_r = open("/save/counters.txt", "r")
   lines = count_file_r.readlines()
   count_file_r.close()

   for line in lines:
      word, count_txt = line.split(" ", 1)
      counters[word] = int(count_txt)

   counters = Counter(counters)
   return counters

def write_counters(counters):
   count_file = open("/save/counters.txt", "w")
   for count in counters.most_common():
      if(count[0] != ''):
         count_file.write(count[0] + " " + str(count[1]) + "\n")
   count_file.close()

def update_counters():
   
   counters = read_counters()
   for filename in os.listdir("/save/counters/"):
      with open(os.path.join("/save/counters/", filename), 'r') as f: # open in readonly mode
         lines = f.readlines()
         f.close()

         c = {}
         for line in lines:
            # print(line)
            if(len(line.split(" ")) < 2):
               continue
            word, count_txt = line.split(" ", 1)
            c[word] = int(count_txt)
         # print(c)
         counters += Counter(c)
   
   write_counters(counters)

   files = glob.glob('/save/counters/*')
   for f in files:
       os.remove(f)

def read_occurrences():
   occurrences = {}
   occ_file_r = open("/save/occurrences.txt", "r")
   lines = occ_file_r.readlines()
   occ_file_r.close()

   for line in lines:
      word, occ_txt = line.split(" ", 1)
      occurrences[word] = occ_txt.strip().split(" ")
   return occurrences

def write_occurrences(occurrences):
   occ_file = open("/save/occurrences.txt", "w")
   for occ in occurrences.items():
      if(occ[0] != ''):
         occ_file.write(occ[0] + " " + ' '.join(occ[1]) + "\n")
   occ_file.close()

def update_occurrences():

   occurrences = read_occurrences()
   print("occurrences: ")
   # print(occurrences)
   for filename in os.listdir("/save/occurrences/"):
      with open(os.path.join("/save/occurrences/", filename), 'r') as f: # open in readonly mode
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

   # print(occurrences)
   write_occurrences(occurrences)

   files = glob.glob('/save/occurrences/*')
   for f in files:
       os.remove(f)


def receive_document(filename, send_cmd = False):
   if(send_cmd):
      send_command("send_file " + filename)
   global self_name, exp_port
   print(self_name, exp_port + 20)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((self_name, exp_port + 20))
   s.listen()
   c,a = s.accept()
   node_id = str(int.from_bytes(c.recv(4), byteorder='big'))
   print("saved file as "+"/uploads/"+filename+".txt")
   receive_file(node_id, c, "/uploads/"+filename+".txt")
   c.shutdown(2)
   c.close()
   s.close()

def passive_receive():
   global self_name, exp_port

   print(self_name, exp_port + 30)

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((self_name, exp_port + 30))
   s.listen()
   print("Waiting passive connections")
   sys.stdout.flush()
   while(True):

      c,a = s.accept()
      node_id = str(int.from_bytes(c.recv(4), byteorder='big'))
      print("Received passive node id " + node_id)
      sys.stdout.flush()

      print("Receiving passive files")
      sys.stdout.flush()
      receive_file(node_id, c, "/save/counters/counter"+node_id+".txt")
      receive_file(node_id, c, "/save/occurrences/occurrences"+node_id+".txt")

      c.shutdown(2)
      c.close()

      update_counters()
      update_occurrences()

   s.close()


def receive(send_cmd = False):
   global self_name, exp_port
   nodes = read_nodes()
   data_is_updated = False

   print("Receiving from nodes: " + str(nodes))
   print(self_name, exp_port + 10)
   sys.stdout.flush()

   if(send_cmd):
      send_command("send_data")

   sys.stdout.flush()
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((self_name, exp_port + 10))
   s.listen()
   for i in range(len(nodes)):

      c,a = s.accept()
      print("Connection accepted")
      node_id = str(int.from_bytes(c.recv(4), byteorder='big'))
      print("Received node id " + node_id)

      msg = c.recv(4)
      print(msg.decode())
      if(msg.decode() == "send"):
         data_is_updated = True
         print("Receiving files")
         receive_file(node_id, c, "/save/counters/counter"+node_id+".txt")
         receive_file(node_id, c, "/save/occurrences/occurrences"+node_id+".txt")

      c.shutdown(2)
      c.close()

   s.close()
   print("received all node counters")

   update_counters()
   update_occurrences()

   return data_is_updated

if __name__ == '__main__':
   print(sys.argv)
   main()