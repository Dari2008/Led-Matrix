import socket
import threading
import matrix.Variables as Variables
from matrix.KillableThread import KillableThread
import json

class CustomServer:

    def start_server(self):
        self.server_socket.bind((Variables.HOST, self.PORT))
        self.server_socket.listen()
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.client_socket = client_socket
            print("Connected: " + str(client_address))
            if hasattr(self, "tmpThread") and self.tmpThread is not None:
                self.tmpThread.kill()
            self.tmpThread = KillableThread(target=self.handle_client, name="runThread")
            self.tmpThread.start()

    def handle_client(self):
        try:
            while True:
                data = b''
                while True:
                    if not self.client_socket:
                        return
                    try:
                        chunk = self.client_socket.recv(20)
                        if not chunk:
                            break
                        if 14 in chunk:
                            break
                        data += chunk
                    except Exception as e:
                        return
                if not data:  # Überprüfen, ob Daten empfangen wurden
                    continue  # Beenden Sie die Schleife, wenn keine Daten empfangen wurden
                self.callback(json.loads(data.decode()))
        except ConnectionResetError:
            return
        except OSError:
            return

    def close(self):
        try:
            if hasattr(self, 'client_socket') and self.client_socket is not None:
                self.client_socket.close()  # Schließe die Client-Socket-Verbindung
            self.server_socket.close()
        except AttributeError:
            pass  # Wenn der Client-Socket bereits geschlossen ist

    def getClient(self):
        return self.client_socket if hasattr(self, 'client_socket') and self.client_socket is not None else None

    def getPort(self) -> int:
        return self.PORT
    
    def start(self):
        self.thread = KillableThread(target=self.start_server)
        self.thread.start()

    def stop(self):
        self.thread.kill()

    def dataReceived(self, data: json):
        pass

    def send(self, data: json):
        if not hasattr(self, 'client_socket') or self.client_socket is None:
            return
        self.client_socket.send((json.dumps(data) + "\n").encode())

    def sendString(self, data: str):
        if not hasattr(self, 'client_socket') or self.client_socket is None:
            return
        self.client_socket.send((data + "\n").encode())

    def __init__(self, port=Variables.MAIN_PORT):
        self.PORT = port
        self.callback = self.dataReceived
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None