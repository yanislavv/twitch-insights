import json
import io
import uuid
from datetime import datetime
from aws import AWSServices


def lambda_handler(event, context):
    s3_key = event['Records'][0]['s3']['object']['key']
    body = AWSServices.read_s3('twitch-insights-extract-landing-eu-central-1', s3_key)
    rows = body.split('\r\n')
    out_buffer = io.BytesIO()
    messages = {}
    for row in rows:
        line = {}
        row = row.split(';')
        for col in row:
            col_value = col.split('=')
            try:
                line.update({col_value[0]: col_value[1]})
            except:
                print(f"Invalid record!\n>>{col_value}<<")
        if line:
            loading_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            if loading_time not in messages:
                messages[loading_time] = [line]
            else:
                messages[loading_time].append(line)

    messages = json.dumps(messages, indent=2)
    out_buffer.write(bytes(messages, encoding='utf-8'))
    out_buffer.seek(0)
    AWSServices.upload_s3(out_buffer, 'twitch-insights-staging-eu-central-1',
                          f'{datetime.now().strftime("%Y-%m-%d")}/{uuid.uuid4()}.json')

    return messages
