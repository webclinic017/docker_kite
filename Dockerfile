#creating the base image
FROM python:3

#RUN apt-get update && \
#    apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev && \
#    apt-get -y install vim && \
#    apt-get -y install git &&\
#    apt-get -y install python3-setuptools


#RUN apt-get update \
#    && apt-get install -y --no-install-recommends gcc and-build-dependencies \
#    && rm -rf /var/lib/apt/lists/* \
#    && pip install cryptography \
#    && apt-get purge -y --auto-remove gcc and-build-dependencies

ENV PYTHONBUFFERED 1

#copying the requirements into the iimage
COPY ./requirements.txt /requirements.txt

#RUN apk update && apk upgrade
#RUN apk add --no-cache bash\
#                       python \
#                       pkgconfig \
#                       git \
#                       gcc \
#                       openldap \
#                       libcurl \
#                       python2-dev \
#                       gpgme-dev \
#                       libc-dev \
#    && rm -rf /var/cache/apk/*
#RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
#

#RUN pip install setuptools==30.1.0
RUN pip3 install setuptools_rust

RUN pip3 install pillow
RUN pip3 install Rust
RUN pip3 install cryptography


RUN pip install -r /requirements.txt
#RUN apk del .tmp-build-deps

#RUN apt-get -y install build-essential libssl-dev libffi-dev \
#    python3-dev cargo
#
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

#RUN pip3 install setuptools_rust

#RUN pip3 install cryptography

#RUN pip3 install -r /requirements.txt

RUN mkdir /app

COPY ./app /app

WORKDIR /app

