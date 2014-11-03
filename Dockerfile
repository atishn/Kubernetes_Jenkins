FROM ubuntu:14.04
MAINTAINER SysOps "sysops@hugeinc.com"

RUN apt-get update && apt-get install git python python python-dev python-distribute python-pip redis-server -y

RUN mkdir stormy-flask

ADD ./app/ stormy-flask/
ADD ./stormy_app.py stormy-flask/
ADD ./requirements.txt stormy-flask/

RUN pip install -r stormy-flask/requirements.txt

EXPOSE 5000

ENTRYPOINT "python stormy-flask/stormy_app.py"