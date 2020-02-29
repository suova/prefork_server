import errno
import os
import socket

from request import Request
from response import Response


class Server:
    def __init__(self, host, port, queue, data_size, cpu_limit, document_root):
        self.port = port
        self.host = host
        self.cpu_limit = cpu_limit
        self.document_root = document_root
        self.queue = queue
        self.pid_forks = []
        self.data_size = data_size

    def launch(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, int(self.port)))
            sock.listen(self.queue)
            for fork in range(self.cpu_limit):
                pid = os.fork()
                if pid > 0:
                    self.pid_forks.append(pid)
                elif pid == 0:
                    while True:
                        try:
                            conn, _ = sock.accept()
                        except IOError as e:
                            if e.errno == errno.EINTR:
                                continue
                            raise
                        with conn:
                            request = conn.recv(self.data_size)
                            if len(request.strip()) == 0:
                                conn.close()
                                continue
                            request_processing = Request(request)
                            response = Response(request_processing,  self.document_root)
                            conn.sendall(response.send_response())
                            conn.close()
                else:
                    print("No more fork")
            sock.close()

            for pid in self.pid_forks:
                os.waitpid(pid, 0)

