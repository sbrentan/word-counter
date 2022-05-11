import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('wrapper', 56733))
clientsocket.sendall('hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello'.encode("UTF-8"))


# import socket
# s = socket.socket()
# s.connect(("localhost", 5000))
# filetosend = open("img.png", "rb")
# data = filetosend.read(1024)
# while data:
#     print("Sending...")
#     s.send(data)
#     data = filetosend.read(1024)
# filetosend.close()
# s.send(b"DONE")
# print("Done Sending.")
# print(s.recv(1024))
# s.shutdown(2)
# s.close()