import argparse
import datetime
import twitch as tw
from messages import IRCClient


def get_datetime():
    return datetime.datetime.now().strftime('%Y%m%dT%H%M%S')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nickname', type=str, required=True, help='Nickname of my Twitch account.')
    parser.add_argument('-c', '--channel', type=str, required=True, help='Name of the Twitch channel you want to join.')
    return parser.parse_args()


def main():
    args = parse_args()
    acc = tw.Account(nickname=args.nickname)
    chn = tw.Channel(channel=args.channel)
    client = IRCClient(acc.nickname, acc.token, chn.channel)
    client.connect()
    client.join_channel()

    while True:
        with open(f"chat_msg_{chn.channel.strip('#')}_{get_datetime()}", "w") as f:
            response = client.receive_message()
            if response.startswith('PING'):
                client.send_message('PONG')
            elif len(response) > 0:
                f.write(response)
                print(response)


if __name__ == '__main__':
    main()
