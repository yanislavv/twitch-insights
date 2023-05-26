import argparse
import datetime
import time
import io
from pathlib import PurePosixPath

from src.services.aws import AWSServices as aws
from src.extract.twitch import Account, Channel
from src.extract.messages import IRCClient
from . import ExtractVar


def get_datetime():
    return datetime.datetime.now()


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

        out_buffer = io.BytesIO()
        while elapsed_time < ExtractVar.BATCH_INTERVAL.value:

            response = client.receive_message()
            if response.startswith('PING'):
                client.send_message('PONG')
            elif len(response) > 0:
                out_buffer.write(bytes(response, encoding='utf8'))
            elapsed_time = time.time() - start_time

        out_buffer.seek(0)
        aws.upload_s3(out_buffer, ExtractVar.BUCKET_EXTRACT.value,
                      str(PurePosixPath(chn.channel.strip('#'), str(get_datetime().date()), get_datetime().strftime('%H%M%S')+'.txt')))


if __name__ == '__main__':
    main()
