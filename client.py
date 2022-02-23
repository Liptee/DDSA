from tools.Client import Client

client = Client()

while True:
    filename = input("Print your file: ")
    client.send_img(filename)
    client.get_img(filename)
