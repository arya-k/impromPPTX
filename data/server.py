import socketserver
from main_function import gen_element
import json


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        deets = []
        data = self.request.recv(1024).decode().strip()
        while data:
            deets.append(data)
            data = self.request.recv(1024).decode().strip()
        real_deets = ''.join(deets)
        json_deets = json.loads(real_deets)
        el = gen_element(json_deets['text'],
                         json_deets['event'] == "new_slide")
        self.request.sendall(json.dumps(el.json()).encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
