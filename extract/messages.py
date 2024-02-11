import socket
from .twitch import TwitchConn


class IRCClient:

    SERVER = TwitchConn.server
    PORT = TwitchConn.port

    def __init__(self, nickname: str, token: str, channel: str):
        self.nickname = nickname
        self.token = token
        self.channel = channel
        self.sock = socket.socket()

    def __str__(self):
        return f'Server: {IRCClient.SERVER}, Port: {IRCClient.PORT}, Nickname: {self.nickname}, Token: {self.token}, Channel: {self.channel}'

    def connect(self):
        try:
            self.sock.connect((self.SERVER, self.PORT))
        except OSError as e:
            raise e

    def join_channel(self):
        try:
            self.sock.send(f"CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands\n".encode('utf-8'))
            self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
            self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
            self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))
            response = self.sock.recv(2048).decode('utf-8')
            if 'Login authentication failed' in response:
                raise Exception('Invalid Token')
        except socket.error as e:
            raise e

    def receive_message(self):
        return self.sock.recv(2048).decode('utf-8', 'ignore')

    def send_message(self, command: str, message: str = ''):
        self.sock.send(f"{command} {self.channel} :{message}\n".encode('utf-8'))

    def disconnect(self):
        self.sock.close()
