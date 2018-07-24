FROM python:3.6
MAINTAINER Dockerfiles

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	apt-utils \
	libboost-all-dev &&\
	rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/grip
COPY . /etc/grip
WORKDIR /etc/grip
ENV PYTHONPATH=/etc/grip
RUN pip install -r requirements.txt