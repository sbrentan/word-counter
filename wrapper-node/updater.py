import socket
import time
import word_counter as wc
import os
import glob

node_id = "0"
last_cmd_code = 0


def load():

	#TODO: load node id and documents, for now resetting every time
	f = open("/save/counters.txt", "w")
	f.close()
	f = open("/save/occurrences.txt", "w")
	f.close()

def send_file(s, filename):
	filesize = os.path.getsize(filename)
	s.send(filesize.to_bytes(16, byteorder='big'))

	filetosend = open(filename, "rb")
	data = filetosend.read(1024)
	while data:
		print("Sending "+filename+"...")
		s.send(data)
		data = filetosend.read(1024)
	filetosend.close()

	print("Done Sending.")

def send_document(filename):
	global node_id
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('monitor', 56740))

	# print("Sending " + node_id)
	s.send(int(node_id).to_bytes(16, byteorder='big'))

	file_found = ""
	files = glob.glob('/documents/*')
	for f in files:
		doc = os.path.splitext(f)[0]
		print("doc "+doc)
		if("/documents/"+filename == doc):
			file_found = f
			break

	print("File found: "+file_found)
	if(file_found):
		send_file(s, file_found)

	s.shutdown(2)
	s.close()


def send_data():
	global node_id
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('monitor', 56720))

	# print("Sending " + node_id)
	s.send(int(node_id).to_bytes(16, byteorder='big'))

	send = False
	if(wc.new_document):
		s.sendall(b"send")
		send = True
	else:
		s.sendall(b"none")
		print("No data to send")
	
	if(send):
		wc.new_document = False
		print("Sending data...")
		send_file(s, "/save/counters.txt")
		send_file(s, "/save/occurrences.txt")
		f = open("/save/counters.txt", "w")
		f.close()
		f = open("/save/occurrences.txt", "w")
		f.close()
		wc.occurrences = {}
		wc.counters = {}

	s.shutdown(2)
	s.close()


load()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.connect(('monitor', 56710))
serversocket.sendall(b"register")

msg = serversocket.recv(100)
node_id = msg.decode()
print("I am node " + node_id)

serversocket.shutdown(2)
serversocket.close()
time.sleep(1)

while True:

	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.connect(('monitor', 56710))
	serversocket.sendall(b"request")

	buf = serversocket.recv(512)
	cmd = buf.decode()
	# print(cmd)

	cmd_code, cmd_txt = cmd.split(" ", 1)
	cmd_code = int(cmd_code)
	# print(cmd)
	# print(cmd_txt)

	
	send = False
	# print(cmd_code)
	if(cmd_code > last_cmd_code):
		print("New command " + str(cmd_code)+": "+cmd_txt)
		cmd = cmd_txt.split(" ")
		if(cmd[0] == "send_data"):
			send = True
		elif(cmd[0] == "send_file"):
			nodeid, filename = map(lambda x: x.strip(), cmd[1].split("_"))
			if(nodeid == node_id):
				print("Sending document...")
				send_document(filename)

		last_cmd_code = cmd_code

	serversocket.shutdown(2)
	serversocket.close()

	if(send):
		send_data()
		

	wc.update_documents(node_id)

	time.sleep(1)