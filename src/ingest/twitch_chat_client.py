import argparse
import datetime
import time

from .twitch import Account, Channel
from .messages import IRCClient
from . import ExtractVar


def get_datetime():
    return datetime.datetime.now().strftime('%Y%m%dT%H%M%S')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nickname', type=str, required=True, help='Nickname of my Twitch account.')
    parser.add_argument('-c', '--channel', type=str, required=True, help='Name of the Twitch channel to join.')
    return parser.parse_args()


def main():
    args = parse_args()
    acc = Account(nickname=args.nickname)
    chn = Channel(channel=args.channel)
    client = IRCClient(acc.nickname, acc.token, chn.channel)
    client.connect()
    client.join_channel()

    while True:
        # TODO: exit when stream ends

        start_time = time.time()
        elapsed_time = 0

        with open(f"chat_msg_{chn.channel.strip('#')}_{get_datetime()}", "w", encoding="utf-8", newline='') as f:

            while elapsed_time < ExtractVar.BATCH_INTERVAL.value:

                response = client.receive_message()
                if response.startswith('PING'):
                    client.send_message('PONG')
                elif len(response) > 0:
                    f.write(response)

                elapsed_time = time.time() - start_time


if __name__ == '__main__':
    main()
