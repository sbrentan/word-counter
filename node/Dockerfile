FROM python:3.8.3-alpine
RUN apk --update add bash nano
RUN mkdir /documents
RUN mkdir /save
WORKDIR /node

ENV MASTER_IP=master
ENV MASTER_PORT=57710

ENTRYPOINT ["python", "updater.py"]