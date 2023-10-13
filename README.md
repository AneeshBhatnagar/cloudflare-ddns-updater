# Cloudflare DDNS Updater

![Docker size](https://badgen.net/docker/size/aneeshbhatnagar/cloudflare-ddns-updater)

The Cloudflare DDNS Updater is a simple Python utility offered as a Docker image that you can use to update the Dynamic DNS on your Cloudflare account. It is particularly popular with people who want to host a website on a home server, where your IP Address is typically updating every now and then by your ISP.

## Pre-Requisites

In order to use this project, you'll need to have:

1. A domain name set up with [Cloudflare DNS](https://www.cloudflare.com/application-services/products/dns/)
1. A [Docker](https://docs.docker.com/) setup running locally, preferably with [Docker compose](https://docs.docker.com/compose/).


## Sample Setup Guide
You can use the following as a sample `docker-compose.yaml`. 

```yaml
version: '3'
services:
  app:
    image: 'aneeshbhatnagar/cloudflare-ddns-updater:latest'
    # init is optional
    init: true
    restart: unless-stopped
    environment:
      - CLOUDFLARE_API_KEY=<KEY_HERE>
      - CLOUDFLARE_ZONE_ID=<ZONE_ID_HERE>
      - CLOUDFLARE_DOMAIN=<DOMAIN_NAME_HERE>
      - CLOUDFLARE_SUBDOMAINS=<space_separated_subdomains/A-records_HERE>
      # Optional variables
      - CLOUDFLARE_PROXIED=<0 or 1 if the record should be proxied> #Default 0
```

1. If you saved the above file as `docker-compose.yaml`, then you can use `docker compose up -d` or `docker-compose up -d` to run this in a detached mode in the background with all your env config
1. If you prefer to run this using just the `docker` CLI, you can do so by passing each of the required environment variable and setup option via the command line. It would look something like this:

`docker run -d --restart unless-stopped -e CLOUDFLARE_API_KEY=<key> -e CLOUDFLARE_ZONE_ID=<> -e CLOUDFLARE_DOMAIN=<> -e CLOUDFLARE_SUBDOMAINS=<> aneeshbhatnagar/cloudflare-ddns-updater:latest`

## Contributing

Do you think something's broken and you can help fix it? Do you think there's a missing feature that this would benefit from? In either of these two cases, please feel free to create an [issue](/../../issues/new) in the repository so we can discuss about it. I'm more than happy to accept contributions to this repository.
