FROM python:3.8.3-alpine
RUN apk --update add bash nano
RUN mkdir /documents
RUN mkdir /save
CMD tail -f /dev/null
WORKDIR /app