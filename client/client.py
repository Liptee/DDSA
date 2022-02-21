import socket
import os.path

filename = "console.jpg"
size = os.path.getsize(filename)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5001))
print(size)
client.send(f"{size}".encode('utf-8'))

file = open(filename, mode = "rb")
data = file.read(2048)
while data:
    client.send(data)
    data= file.read(2048)    
file.close()

file = open('res_image.jpg', mode = "wb")
data = client.recv(2048)
while data:
    file.write(data)
    data = client.recv(2048)
file.close()
  