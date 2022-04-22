from modules_connector import Server
import time


class ModuleB:
    def __init__(self):
        self.data = None

    def main(self):
        filename = 'test.ovdump'
        server = Server(filename, self.callback)

        while True:
            server.read()
            print('data is: %s' % self.data)
            time.sleep(1)

    def callback(self, data):
        # print(data)
        self.data = data


ModuleB().main()
