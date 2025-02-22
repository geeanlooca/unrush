FROM python:3.11-slim-bullseye AS unrush-builder

RUN apt-get update && apt-get upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN mkdir /wheels
RUN pip install --no-cache-dir wheel setuptools

COPY . .
RUN pip install --no-cache-dir .
RUN pip wheel --no-cache-dir --wheel-dir=/wheels .

FROM python:3.11-slim-bullseye AS unrush-image
RUN apt-get update && apt-get upgrade -y --no-install-recommends && apt-get install -y --no-install-recommends mkvtoolnix && rm -rf /var/lib/apt/lists/*
COPY --from=unrush-builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels unrush && rm -rf /wheels


CMD ["unrush"]

