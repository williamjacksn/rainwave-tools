FROM python:3.7.0-alpine3.8

COPY requirements-docker.txt /rainwave-tools/requirements-docker.txt

RUN /sbin/apk --no-cache add --virtual .deps gcc libxml2-dev libxslt-dev musl-dev postgresql-dev \
 && /sbin/apk --no-cache add libpq \
 && /usr/local/bin/pip install --no-cache-dir --requirement /rainwave-tools/requirements-docker.txt \
 && /sbin/apk del .deps

COPY . /rainwave-tools

RUN /usr/local/bin/pip install /rainwave-tools

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/bin/sh"]

LABEL maintainer=william@subtlecoolness.com \
      org.label-schema.schema-version=1.0 \
      org.label-schema.version=0.7.2
