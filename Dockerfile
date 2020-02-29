FROM ubuntu:16.04
RUN apt-get -y update
RUN apt-get install -y python3

ADD . ./server/
RUN ls ./server

EXPOSE 80

CMD python3 ./server/main.py