FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y git python3-click python3-tabulate python3-termcolor python3-toml

RUN git clone --recurse-submodules https://github.com/martinvrba/xpnss.git /app

RUN mkdir /app/output

WORKDIR /app/output

ENTRYPOINT ["python3", "/app/cli.py"]
