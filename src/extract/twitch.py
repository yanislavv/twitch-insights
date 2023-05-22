from dataclasses import dataclass


@dataclass
class TwitchConn:
    server: str = 'irc.chat.twitch.tv'
    port: int = 6667


@dataclass
class Account:
    nickname: str
    token: str = 'oauth:kou078uq5ea8aibboky96yt55jbu3p'


@dataclass
class Channel:
    channel: str
     