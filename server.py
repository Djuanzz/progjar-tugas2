import socket
import threading
import logging
import datetime

CRLF = '\r\n'

class ProcessClientThread(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
        logging.warning(f"Connected with {self.address}")
        try:
            while True:
                data = self.connection.recv(1024).decode('utf-8')
                if not data:
                    break

                logging.warning(f"Received: {data.strip()} from {self.address}")

                if data.startswith("TIME") and data.endswith(CRLF):
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    response = f"JAM {now}{CRLF}"
                    self.connection.sendall(response.encode('utf-8'))
                    logging.warning(f"Sent: {response.strip()} to {self.address}")
                elif data.strip() == "QUIT":
                    logging.warning(f"QUIT received. Closing connection {self.address}")
                    break
                else:
                    logging.warning(f"Invalid request: {data.strip()}")
        except Exception as e:
            logging.error(f"Error with {self.address}: {e}")
        finally:
            self.connection.close()

class TimeServer(threading.Thread):
    def __init__(self, host='0.0.0.0', port=45000):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        logging.warning(f"Time Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.sock.accept()
            client_thread = ProcessClientThread(conn, addr)
            client_thread.start()

def main():
    logging.basicConfig(level=logging.WARNING)
    server = TimeServer()
    server.start()

if __name__ == "__main__":
    main()
