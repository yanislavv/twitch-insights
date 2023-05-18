import twitch as tw
from messages import IRCClient


def main():

    client = IRCClient(tw.Account.nickname, tw.Account.token, tw.Channel.channel)
    client.connect()
    client.join_channel()

    while True:
        response = client.receive_message()
        if response.startswith('PING'):
            client.send_message('PONG')
        elif len(response) > 0:
            print(response)


if __name__ == '__main__':
    main()
