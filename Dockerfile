FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install --yes --force-yes dnsutils
RUN python3.13 -m pip install -r /app/requirements.txt


COPY . /app


CMD [ "python", "-u", "/app/update-cloudflare.py" ]