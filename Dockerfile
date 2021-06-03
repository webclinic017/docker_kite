FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev && \
    apt-get -y install vim && \
    apt-get -y install git &&\
    apt-get -y install python3-setuptools


ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apt-get -y install build-essential libssl-dev libffi-dev \
    python3-dev cargo

#RUN apt-get update && apt-get install -y \
#  build-base \
#  cairo \
#  cairo-dev \
#  cargo \
#  freetype-dev \
#  gcc \
#  gdk-pixbuf-dev \
#  gettext \
#  jpeg-dev \
#  lcms2-dev \
#  libffi-dev \
#  musl-dev \
#  openjpeg-dev \
#  openssl-dev \
#  pango-dev \
#  poppler-utils \
#  postgresql-client \
#  postgresql-dev \
#  py-cffi \
#  python3-dev \
#  rust \
#  tcl-dev \
#  tiff-dev \
#  tk-dev \
#  zlib-dev

RUN pip3 install setuptools_rust

RUN pip3 install cryptography

RUN pip3 install -r /requirements.txt

RUN mkdir /app

COPY ./app /app

WORKDIR /app

