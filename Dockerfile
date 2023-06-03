FROM python:3.10-slim-buster
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install --yes --force-yes dnsutils
RUN python3.10 -m pip install -r /app/requirements.txt


COPY . /app


CMD [ "python", "-u", "/app/update-cloudflare.py" ]