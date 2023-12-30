from enum import Enum


class AppConfig(Enum):
    BATCH_INTERVAL: int = 20
    BUCKET_EXTRACT: str = 'twitch-insights-extract-landing-eu-central-1'
    BUCKET_STAGING: str = 'twitch-insights-staging-eu-central-1'
    QUEUE_URL: str = 'https://sqs.eu-central-1.amazonaws.com/508997417107/staging-files-queue'