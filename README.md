# rss-funny-fetcher
 Fetches RSS feeds from reddit and sends them as a discord webhook in a channel

## installation

```docker-compose
version: "3.6"
services:
  nsfw-webhook:
    container_name: "rss-funny-fetcher"
    environment:
      - "WEBHOOK=WEBHOOK_URL_HERE"
    image: "dockeriousername/dockeriocontainerrepo"
    network_mode: "bridge"
    restart: "on-failure"
```