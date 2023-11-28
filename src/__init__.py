from enum import Enum


class ExtractVar(Enum):
    BATCH_INTERVAL: int = 20
    BUCKET_EXTRACT: str = 'twitch-insights-extract-landing-eu-central-1'
    QUEUE_URL: str = 'https://sqs.eu-central-1.amazonaws.com/508997417107/test'
