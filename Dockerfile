FROM python:3.7.2-alpine3.9

COPY requirements.txt /rainwave-tools/requirements.txt

RUN /sbin/apk add --no-cache --virtual .deps gcc libxml2-dev libxslt-dev musl-dev postgresql-dev \
 && /sbin/apk add --no-cache libpq libxslt \
 && /usr/local/bin/pip install --no-cache-dir --requirement /rainwave-tools/requirements.txt \
 && /sbin/apk del --no-cache .deps

COPY . /rainwave-tools

RUN /usr/local/bin/pip install --no-cache-dir /rainwave-tools

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/bin/sh"]

LABEL maintainer=william@subtlecoolness.com \
      org.label-schema.schema-version=1.0 \
      org.label-schema.version=0.7.7
