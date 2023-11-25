FROM python:3.9-alpine

WORKDIR /extract

COPY requirements.txt /extract/
COPY wheels/ /extract/wheels/

RUN pip install --no-cache-dir -r requirements.txt

CMD []