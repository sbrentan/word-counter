import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('wrapper', 56733))
serversocket.listen(5) # become a server socket, maximum 5 connections

while True:
    connection, address = serversocket.accept()
    while True:
        buf = connection.recv(512)
        if (len(buf) < 1):
            break
        print(buf.decode())




# import socket
# s = socket.socket()
# s.bind(("localhost", 5000))
# s.listen(1)
# c,a = s.accept()
# filetodown = open("img.png", "wb")
# while True:
#    print("Receiving....")
#    data = c.recv(1024)
#    if data == b"DONE":
#            print("Done Receiving.")
#            break
#    filetodown.write(data)
# filetodown.close()
# c.send("Thank you for connecting.")
# c.shutdown(2)
# c.close()
# s.close()
