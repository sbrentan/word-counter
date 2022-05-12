FROM python:3.8.3-alpine
RUN apk --update add bash nano
RUN mkdir /documents
RUN mkdir /uploads
RUN mkdir -p /save/counters
RUN mkdir -p /save/occurrences
RUN touch /save/nodes.txt
RUN touch /save/command.txt
RUN touch /save/counters.txt
RUN touch /save/occurrences.txt
RUN echo 0 none > /save/command.txt
WORKDIR /master

ENV EXP_PORT=56710
ENV SELF_NAME=localhost
ENV ACCEPT_MODE=passive
ENV MASTER_IP=monitor
ENV MASTER_PORT=56710

ENTRYPOINT python monitor.py $ACCEPT_MODE