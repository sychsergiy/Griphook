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
WORKDIR /etc/grip/griphook/tasks 
RUN pip install -e /etc/grip