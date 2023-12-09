import argparse
import datetime
import time
import io
import sys
from pathlib import PurePosixPath

from services.aws import AWSServices as aws
from extract.twitch import Account, Channel
from extract.messages import IRCClient
from configs.variables import AppConfig


def get_datetime():
    return datetime.datetime.now()


def main():
    acc = Account(nickname=sys.argv[1])
    chn = Channel(channel=sys.argv[2])
    client = IRCClient(acc.nickname, acc.token, chn.channel)
    client.connect()
    client.join_channel()

    while True:
        # TODO: exit when stream ends

        start_time = time.time()
        elapsed_time = 0

        out_buffer = io.BytesIO()
        while elapsed_time < AppConfig.BATCH_INTERVAL.value:

            response = client.receive_message()
            if response.startswith('PING'):
                client.send_message('PONG')
            elif len(response) > 0:
                out_buffer.write(bytes(response, encoding='utf8'))
            elapsed_time = time.time() - start_time

        out_buffer.seek(0)
        aws.upload_s3(out_buffer, AppConfig.BUCKET_EXTRACT.value,
                      str(PurePosixPath(chn.channel.strip('#'), str(get_datetime().date()), get_datetime().strftime('%H%M%S')+'.txt')))


if __name__ == '__main__':
    main()
