FROM python:2.7
MAINTAINER jasmeet.kohli@digitalonus.com

RUN apt-get update \
 && apt-get install -y cmake

RUN wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz \
 && tar xzf v0.27.0.tar.gz \
 && cd libgit2-0.27.0/ \
 && cmake . \
 && make \
 && make install \
 && pip install pygit2 \
 && ldconfig

RUN pip install lxml