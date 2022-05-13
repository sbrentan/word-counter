import socket
import time
import os
import glob
import sys
from collections import Counter
from multiprocessing import Process


######### WORD COUNTER
docs_folder = "/documents/"
documents = []
occurrences = {}
counters = {}
doc = "doc"
new_document = False

def read_occurrences():
	global occurrences
	occ_file_r = open("/save/occurrences.txt", "r")
	lines = occ_file_r.readlines()
	occ_file_r.close()

	for line in lines:
		word, occ_txt = line.split(" ", 1)
		occurrences[word] = occ_txt.strip().split(" ")

def update_occurrences(counter, doc, node_id):
	global occurrences
	for c in counter:
		if c not in occurrences:
			occurrences[c] = [doc]
		else:
			if doc not in occurrences[c]:
				occurrences[c].append(doc)

def read_counters():
	global counters
	count_file_r = open("/save/counters.txt", "r")
	lines = count_file_r.readlines()
	count_file_r.close()

	for line in lines:
		word, count_txt = line.split(" ", 1)
		counters[word] = int(count_txt)

	counters = Counter(counters)

def get_new_document():
	global documents, docs_folder
	new_docs = []
	for filename in os.listdir(docs_folder):
		if filename not in documents:
			new_docs += [filename]
	return new_docs

def update_documents(node_id):

	global doc, occurrences, counters, documents, new_document

	new_docs = get_new_document()
	if(len(new_docs) == 0):
		return;

	new_document = True
	for new_doc in new_docs:

		doc = os.path.splitext(new_doc)[0]
		filename = docs_folder+doc+".txt"
		print("Found new document: " + filename + " -> " + node_id + "_" + doc)

		f = open(filename, "r")
		data = f.read()
		f.close()

		words = data.split(" ")
		word_counts = Counter(words)

		read_counters()
		read_occurrences()
		update_occurrences(word_counts, doc, node_id)
		counters += word_counts

		occ_file = open("/save/occurrences.txt", "w")
		for occ in occurrences.items():
			if(occ[0] != ''):
				occ_file.write(occ[0] + " " + ' '.join(occ[1]) + "\n")
		occ_file.close()

		count_file = open("/save/counters.txt", "w")
		for count in counters.most_common():
			if(count[0] != ''):
				count_file.write(count[0] + " " + str(count[1]) + "\n")
		count_file.close()

		documents += [new_doc]




############ NODE MAIN
is_master = True
node_id = "0"
last_cmd_code = 0
generator_on = False
# master_ip   = os.environ['MASTER_IP']
master_port = int(os.environ['MASTER_PORT'])
master_receive = 0
master_receive_doc = 0


def load():

	#TODO: load node id and documents, for now resetting every time
	f = open("/save/counters.txt", "w")
	f.close()
	f = open("/save/occurrences.txt", "w")
	f.close()

def send_file(s, filename):
	filesize = os.path.getsize(filename)
	s.send(filesize.to_bytes(4, byteorder='big'))

	filetosend = open(filename, "rb")
	data = filetosend.read(1024)
	while data:
		print("Sending "+filename+"...")
		s.send(data)
		data = filetosend.read(1024)
	filetosend.close()

	print("Done Sending.")

def send_document(filename, folder="/documents/"):
	global node_id, master_ip, master_port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((master_ip, master_port + 20))

	# print("Sending " + node_id)
	s.send(int(node_id).to_bytes(4, byteorder='big'))

	file_found = ""
	files = glob.glob(folder+'*')
	for f in files:
		doc = os.path.splitext(f)[0]
		# print("doc "+doc)
		if(folder+filename == doc):
			file_found = f
			break

	# print("File found: "+file_found)
	if(file_found):
		send_file(s, file_found)

	s.shutdown(2)
	s.close()

def send_command(command):
   file = open("/save/command.txt", "r")
   cmd_code, cmd_txt = file.readline().split(" ", 1)
   file.close()
   cmd_code = int(cmd_code) + 1

   file = open("/save/command.txt", "w")
   file.write(str(cmd_code) + " " + command)
   file.close()

def send_data(mode):
	global node_id, master_ip, is_master, master_port, master_receive, new_document, transmission_mode

	# print("is_master " + str(is_master))
	# print("Receiving child nodes")
	data_updated = False
	if(is_master):
		f = open("/save/accept_mode.txt", "r")
		accept_mode = f.readline().strip()
		f.close()
		if(accept_mode == "active"):
			print("Receiving child nodes")
			sys.stdout.flush()
			data_updated = master_receive(True)
		elif(accept_mode == "passive"):
			file_size = os.path.getsize("/save/counters.txt")
			print("File size: "+str(file_size))
			if(file_size > 0):
				data_updated = True

	if(mode == "active" or new_document or data_updated):
		port = master_port + 10
		if(mode == "passive"):
			port = master_port + 30

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((master_ip, port))

		# print("Sending " + node_id)
		s.send(int(node_id).to_bytes(4, byteorder='big'))

		if(mode == "active"):
			send = False
			if(new_document or data_updated):
				s.sendall(b"send")
				send = True
			else:
				s.sendall(b"none")
				print("No data to send")
		else:
			send=True
		
		if(send):
			new_document = False

			occs = {}
			occ_file_r = open("/save/occurrences.txt", "r")
			lines = occ_file_r.readlines()
			occ_file_r.close()

			for line in lines:
				word, occ_txt = line.split(" ", 1)
				occs[word] = occ_txt.strip().split(" ")
			occ_file = open("/save/occurrences.txt", "w")
			for occ in occs.items():
				if(occ[0] != ''):
					occ_file.write(occ[0] + " " + ' '.join(map(lambda x: node_id + "_" + x, occ[1])) + "\n")
			occ_file.close()

			print("Sending data...")
			send_file(s, "/save/counters.txt")
			send_file(s, "/save/occurrences.txt")
			f = open("/save/counters.txt", "w")
			f.close()
			f = open("/save/occurrences.txt", "w")
			f.close()
			occurrences = {}
			counters = {}

		s.shutdown(2)
		s.close()

def main_terminal():#run from terminal: is node
	global is_master
	is_master = False
	main(os.environ['MASTER_IP'])

def main(master, master_receive_fn=0, master_receive_doc_fn=0):

	global node_id, last_cmd_code, master_ip, master_port, master_receive, master_receive_doc
	load()

	if("GENERATE" in os.environ):
		print("Generating " + os.environ["GENERATE"])
		import generator as gen
		gen.generate(os.environ["GENERATE"])
		print("file generated")

	master_ip = master
	master_receive = master_receive_fn
	master_receive_doc = master_receive_doc_fn

	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.connect((master_ip, master_port))
	serversocket.sendall(b"register")

	msg = serversocket.recv(100)
	node_id, transmission_mode = msg.decode().split(" ")
	print("I am node " + node_id + ", with transmission_mode " + transmission_mode)
	f = open("/save/transmission_mode", "w")
	f.write(transmission_mode)
	f.close()

	serversocket.shutdown(2)
	serversocket.close()

	cmd_code_assigned = False

	passive_count = 0

	print("Master: " + master_ip + " " + str(master_port))
	while True:

		time.sleep(0.5)
		if(transmission_mode == "passive"):
			passive_count += 1 #seconds passed after last update


		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.connect((master_ip, master_port))
		serversocket.sendall(b"request")

		buf = serversocket.recv(512)
		cmd = buf.decode()

		# print(cmd)
		sys.stdout.flush()
		cmd_code, cmd_txt = cmd.split(" ", 1)
		cmd_code = int(cmd_code)

		# print("cmd: " + str(cmd_code) + " " + cmd_txt + ", " + str(last_cmd_code))
		sys.stdout.flush()
		
		send = False
		if(not cmd_code_assigned):
			cmd_code_assigned = True
			# print("cmd_code_assigned")
			sys.stdout.flush()
			last_cmd_code = cmd_code
		elif(cmd_code > last_cmd_code):
			print("New command " + str(cmd_code)+": "+cmd_txt)
			sys.stdout.flush()
			cmd = cmd_txt.split(" ")
			if(cmd[0] == "send_data"):
				send = True
			elif(cmd[0] == "send_file"):# 1 send_file 1_1_doc1.txt
				nodeid, filename = map(lambda x: x.strip(), cmd[1].split("_", 1))#  1, 1_doc1.txt
				if(nodeid == node_id):
					file_strip = list(map(lambda x: x.strip(), filename.split("_")))#  1, doc1.txt
					if(len(file_strip) > 1):
						print("Sending request to children...")
						print(filename)#    1_doc1.txt
						master_receive_doc(filename, True)
						send_document(filename, folder="/uploads/")
					else:
						print("Sending document...")
						send_document(filename)
			elif(cmd[0] == "chng_mode"):
				print("Changing transmission_mode from " + transmission_mode + " to " + cmd[1])
				transmission_mode = cmd[1]
				if(transmission_mode == "active"):
					passive_count = 0
				f = open("/save/transmission_mode.txt", "w")
				f.write(transmission_mode)
				f.close()
			elif(cmd[0] == "generate"):
				global doc_generator, generator_on
				if(cmd[1] == "on" and not generator_on):
					generator_on = True
					import generator as gen
					doc_generator = Process(target=gen.generate, args=("", True))
					doc_generator.start()
				elif(cmd[1] == "off" and generator_on):
					generator_on = False
					doc_generator.terminate()
					doc_generator.join()
				global is_master
				if(is_master):
					send_command(cmd_txt)

			last_cmd_code = cmd_code

		serversocket.shutdown(2)
		serversocket.close()

		if(send or passive_count == 3):
			passive_count = 0
			if(send):
				send_data("active")
			else:
				send_data("passive")

		update_documents(node_id)


if __name__ == '__main__':
	main_terminal()