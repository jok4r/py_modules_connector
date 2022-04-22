from modules_connector import Client


def main():
    filename = 'test.ovdump'
    client = Client(filename)
    client.write('zora koras')


main()
