from modules_connector import Server
from modules_connector import Client


def main():
    filename = 'test.ovdump'
    server = Server(filename, callback)
    client = Client(filename)
    client.write('zora koras')
    server.read()


def callback(data):
    print(data)


main()
