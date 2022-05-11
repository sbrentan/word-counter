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

ARG EXP_PORT=56710
ARG MASTER_IP=monitor
ARG MASTER_PORT=56710
ARG SELF_NAME=localhost
ENV EXP_PORT=$EXP_PORT
ENV MASTER_IP=$MASTER_IP
ENV MASTER_PORT=$MASTER_PORT
ENV SELF_NAME=$SELF_NAME

ENTRYPOINT ["python", "monitor.py", "passive"]