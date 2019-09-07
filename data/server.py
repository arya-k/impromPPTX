import socketserver
from main_function import gen_element
import json


def line(s):
    ret = ""
    while True:
        c = s.recv(1).decode("UTF8")
        if c == "\n":
            break
        else:
            ret += c
    return ret


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        real_deets = line(self.request)
        json_deets = json.loads(real_deets)
        el = gen_element(json_deets['text'],
                         json_deets['event'] == "next_slide")
        self.request.sendall(json.dumps(el.json()).encode())
        self.request.send("\n".encode())
        self.request.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 1337

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
