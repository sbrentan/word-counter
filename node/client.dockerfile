FROM python:3.8.3-alpine
RUN apk --update add bash nano
RUN mkdir /documents
RUN mkdir /save
WORKDIR /node

ARG MASTER_IP=master
ARG MASTER_PORT=56710
ENV MASTER_IP=$MASTER_IP
ENV MASTER_PORT=$MASTER_PORT

ENTRYPOINT ["python", "updater.py"]