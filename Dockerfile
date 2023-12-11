FROM python:3.9-alpine

WORKDIR /extract

COPY . /extract/

RUN pip install --no-cache-dir -r requirements.txt

CMD []

# TODO create docker compose file with services - extract and import to db
