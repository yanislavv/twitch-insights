from dataclasses import dataclass


@dataclass
class TwitchConn:
    server: str = 'irc.chat.twitch.tv'
    port: int = 6667


@dataclass
class Account:
    token: str
    nickname: str


@dataclass
class Channel:
    channel: str
     