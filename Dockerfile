FROM python:3.7.3-alpine3.9

COPY requirements.txt /rainwave-tools/requirements.txt

RUN /sbin/apk add --no-cache --virtual .deps gcc libxml2-dev libxslt-dev musl-dev postgresql-dev \
 && /sbin/apk add --no-cache libpq libxslt \
 && /usr/local/bin/pip install --no-cache-dir --requirement /rainwave-tools/requirements.txt \
 && /sbin/apk del --no-cache .deps

COPY . /rainwave-tools

RUN /usr/local/bin/pip install --no-cache-dir /rainwave-tools

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/bin/sh"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.description="Tools for maintaining a local library of music for https://rainwave.cc/" \
      org.opencontainers.image.source="https://github.com/williamjacksn/rainwave-tools" \
      org.opencontainers.image.title="Rainwave Tools" \
      org.opencontainers.image.version=0.8.2
