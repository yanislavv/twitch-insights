import time

from services.aws import AWSServices as aws
from configs.variables import AppConfig


def main():
    while True:

        response = aws.get_message(AppConfig.QUEUE_URL.value)

        print(response)

        time.sleep(10)


if __name__ == '__main__':
    main()
