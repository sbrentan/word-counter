from app import app
from flask import render_template
from multiprocessing import Process
from collections import Counter
import os
import sys
import socket

# scriptpath = "app/scripts/monitor_receiver"
# print(os.getcwd())

# # Add the directory containing your module to the Python path (wants absolute paths)
# sys.path.append(os.path.abspath(scriptpath))

# Do the import
# import monitor_receiver

@app.route('/')
def home():
   return "hello world!"

@app.route('/top_words')
def template():
   # print("-=-----------------------ciao")
   # return str(os.listdir(os.getcwd()))


   send_command("send_counters")
   p = Process(target=receive)
   p.start()
   p.join()

   sc = sum_counters()
   print(sc)
   return render_template('top_words.html', counter=sc)

@app.route('/command/send')
def command():

   command = "send"
   file = open("scripts/save/command.txt", "r")
   cmd_code, cmd_txt = file.readline().split(" ", 1)
   file.close()
   cmd_code = int(cmd_code) + 1

   file = open("scripts/save/command.txt", "w")
   file.write(cmd_code + " " + command)
   file.close()

   return cmd_code + " " + command




def send_command(command):
   file = open("scripts/save/command.txt", "r")
   cmd_code, cmd_txt = file.readline().split(" ", 1)
   file.close()
   cmd_code = int(cmd_code) + 1

   file = open("scripts/save/command.txt", "w")
   file.write(str(cmd_code) + " " + command)
   file.close()

def sum_counters():
   c = Counter()
   for filename in os.listdir("/app/scripts/counters/"):
      with open(os.path.join("/app/scripts/counters/", filename), 'r') as f: # open in readonly mode
         lines = f.readlines()
         f.close()

         counters = {}
         for line in lines:
            print(line)
            if(len(line.split(" ")) < 2):
               continue
            word, count_txt = line.split(" ", 1)
            counters[word] = int(count_txt)
         print(counters)
         c += Counter(counters)
   return c

def read_nodes():
   nodes_file = open("scripts/save/nodes.txt", "r")
   nodes_txt = nodes_file.readline()
   nodes_file.close()
   nodes = filter(lambda x: bool(x.strip()), nodes_txt.split(" "))
   nodes = list(map(lambda x: int(x), nodes))
   print("Nodes are: ")
   print(nodes_txt)
   print(nodes)
   return nodes

def receive():
   nodes = read_nodes()

   s = socket.socket()
   s.bind(("monitor", 56720))
   s.listen(1)
   for i in range(len(nodes)):

      c,a = s.accept()
      print("Connection accepted")
      msg = c.recv(100)
      print("Message received")
      node_id = msg.decode()
      print("Received node id " + node_id)

      filetodown = open("scripts/counters/counter"+node_id+".txt", "wb")
      while True:
         print("Receiving....")
         data = c.recv(1024)
         print(data.decode())
         if data == b"DONE" or not data:
            print("Done Receiving.")
            break
         filetodown.write(data)
      filetodown.close()
      c.shutdown(2)
      c.close()

   s.close()
   print("received all node counters")