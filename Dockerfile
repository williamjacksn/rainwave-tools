FROM python:3.9.5-alpine3.13

COPY requirements.txt /rainwave-tools/requirements.txt

RUN /sbin/apk add --no-cache libpq libxslt
RUN /usr/local/bin/pip install --no-cache-dir --requirement /rainwave-tools/requirements.txt

COPY . /rainwave-tools

RUN /usr/local/bin/pip install --no-cache-dir /rainwave-tools

ENV PYTHONUNBUFFERED="1" \
    RAINWAVE_TOOLS_VERSION="2021.3"

ENTRYPOINT ["/bin/sh"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.description="Tools for maintaining a local library of music for https://rainwave.cc/" \
      org.opencontainers.image.source="https://github.com/williamjacksn/rainwave-tools" \
      org.opencontainers.image.title="Rainwave Tools" \
      org.opencontainers.image.version="${RAINWAVE_TOOLS_VERSION}"
