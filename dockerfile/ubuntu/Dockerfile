FROM ubuntu:14.04.5
  
MAINTAINER Toshiki Tsuboi <t.tsubo2000@gmail.com>

RUN apt-get update \
 && apt-get install -y git python-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install pip
WORKDIR /
ADD tools tools
ADD https://bootstrap.pypa.io/get-pip.py /
RUN python get-pip.py

# Install oslo_messaging
RUN pip install oslo_messaging==1.4.2

# Install eventlet
RUN pip install eventlet==0.15.2

WORKDIR /tools
