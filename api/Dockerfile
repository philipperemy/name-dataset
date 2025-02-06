FROM python:3.10.12-bullseye
MAINTAINER Philippe Remy <premy.enseirb@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED 1

COPY . /app/

WORKDIR /app

RUN pip install -e . --upgrade

WORKDIR api
RUN pip install -r requirements.txt

EXPOSE 9999

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]