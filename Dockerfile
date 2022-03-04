FROM debian:bullseye-slim

RUN mkdir -p /app/commands; mkdir /app/output

COPY commands /app/commands/

COPY cli.py /app/

RUN apt-get update && apt-get install -y python3-click python3-tabulate python3-termcolor python3-toml

WORKDIR /app/output

ENTRYPOINT ["python3", "/app/cli.py"]
