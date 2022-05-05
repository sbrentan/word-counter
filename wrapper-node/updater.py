import socket
import time

node_id = "0"
last_cmd_code = 0

def send_counters():
	global node_id
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('monitor', 56720))

	# print("Sending " + node_id)
	s.send(node_id.encode())
	
	filetosend = open("counters.txt", "rb")
	data = filetosend.read(1024)
	while data:
	    print("Sending...")
	    s.send(data)
	    data = filetosend.read(1024)
	filetosend.close()
	s.send(b"DONE")
	print("Done Sending.")
	s.shutdown(2)
	s.close()

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
	print(cmd)

	cmd_code, cmd_txt = cmd.split(" ", 1)
	cmd_code = int(cmd_code)
	# print(cmd)
	# print(cmd_txt)

	serversocket.shutdown(2)
	serversocket.close()

	# print(cmd_code)
	if(cmd_code > last_cmd_code):
		print("Sending counters...")
		if(cmd_txt == "send_counters"):
			send_counters()

		last_cmd_code = cmd_code

	time.sleep(1)