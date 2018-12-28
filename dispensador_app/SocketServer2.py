import socket
import threading
import socketserver
import sched, time
import schedule
import asyncio

def pass_response(a=None,**kwargs):
    print("Moviendo motor:",time.asctime())

async def run_scheduler():
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        print(data)
        print(time.asctime())
        #s = sched.scheduler(time.time, time.sleep)
        #s.enter(data,1,pass_response,kwargs={'a': data})
        cur_thread = threading.current_thread()
        hora={'a': data}
        schedule.every().day.at(data).do(pass_response,**hora)
        respuesta="Motor programado a las: "+data+"."
        response = bytes("{}: {}".format(cur_thread.name, respuesta), 'ascii')
        self.request.sendall(response)
        asyncio.run(run_scheduler())
        #s.run()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("{}".format(response))


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 9990
    PORT2,PORT3,PORT4=9991,9992,9993
    
    server2 = ThreadedTCPServer((HOST, PORT2), ThreadedTCPRequestHandler)


    with server2:
        ip, port = server2.server_address
        print("ip:",HOST," Puerto:",port,".")
        ipe=HOST
        puerto=9991

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server2.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server corriendo en:", server_thread.name)

server2.serve_forever()