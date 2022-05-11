FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /monitor/app/static
COPY ./requirements.txt /monitor/requirements.txt
RUN pip install -r /monitor/requirements.txt

RUN mkdir /documents
RUN mkdir /uploads
RUN mkdir -p /save/counters
RUN mkdir -p /save/occurrences
RUN touch /save/nodes.txt
RUN touch /save/command.txt
RUN touch /save/counters.txt
RUN touch /save/occurrences.txt
RUN echo 0 none > /save/command.txt

ARG MONITOR_PORT=56700
ARG EXP_PORT=56710
ARG ACCEPT_MODE=active
ENV MONITOR_PORT=$MONITOR_PORT
ENV EXP_PORT=$EXP_PORT
ENV ACCEPT_MODE=$ACCEPT_MODE


WORKDIR /monitor