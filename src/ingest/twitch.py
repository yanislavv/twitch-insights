from dataclasses import dataclass


@dataclass
class TwitchConn:
    server: str
    port: int


@dataclass
class Account:
    token: str
    nickname: str


@dataclass
class Channel:
    channel: str
     