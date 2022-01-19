FROM python:3.10.2-alpine3.15 as builder

COPY setup.py /rainwave-tools/setup.py
COPY rainwave_tools /rainwave-tools/rainwave_tools

WORKDIR /rainwave-tools
RUN /usr/local/bin/python setup.py bdist_wheel

FROM python:3.10.2-alpine3.15

RUN /sbin/apk add --no-cache libpq libxslt
RUN /usr/sbin/adduser -g python -D python

USER python
RUN /usr/local/bin/python -m venv /home/python/venv

COPY --chown=python:python requirements.txt /home/python/rainwave-tools/requirements.txt
RUN /home/python/venv/bin/pip install --no-cache-dir --requirement /home/python/rainwave-tools/requirements.txt

ENV PATH="/home/python/venv/bin:${PATH}" \
    PYTHONUNBUFFERED="1" \
    RAINWAVE_TOOLS_VERSION="2021.4"

ENTRYPOINT ["/bin/sh"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.description="Tools for maintaining a local library of music for https://rainwave.cc/" \
      org.opencontainers.image.source="https://github.com/williamjacksn/rainwave-tools" \
      org.opencontainers.image.title="Rainwave Tools" \
      org.opencontainers.image.version="${RAINWAVE_TOOLS_VERSION}"

COPY --from=builder --chown=python:python /rainwave-tools/dist/*.whl /home/python/rainwave-tools/
RUN /home/python/venv/bin/pip install --no-cache-dir /home/python/rainwave-tools/*.whl
