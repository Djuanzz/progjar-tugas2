import socket
import logging

CRLF = '\r\n'

def main():
    logging.basicConfig(level=logging.WARNING)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 45000))

    try:
        while True:
            req = input("Select command (TIME | QUIT): ").strip().upper()
            
            if req == "TIME":
                request = f"TIME{CRLF}"
                sock.sendall(request.encode())

                response = sock.recv(1024).decode()
                logging.warning(f"Received: {response.strip()}")

            elif req == "QUIT":
                quit_command = f"QUIT{CRLF}"
                sock.sendall(quit_command.encode())
                logging.warning("Exiting...")
                break

            else:
                logging.warning("Invalid request. Select command (TIME | QUIT)")

    finally:
        sock.close()

if __name__ == "__main__":
    main()
