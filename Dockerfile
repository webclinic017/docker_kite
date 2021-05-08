FROM python:3.8-alpine

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk -U upgrade

RUN apk add --update \
  build-base \
  cairo \
  cairo-dev \
  cargo \
  freetype-dev \
  gcc \
  gdk-pixbuf-dev \
  gettext \
  jpeg-dev \
  lcms2-dev \
  libffi-dev \
  musl-dev \
  openjpeg-dev \
  openssl-dev \
  pango-dev \
  poppler-utils \
  postgresql-client \
  postgresql-dev \
  py-cffi \
  python3-dev \
  rust \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev

RUN pip install cryptography

RUN pip install -r /requirements.txt

RUN mkdir /app

COPY ./app /app

WORKDIR /app

