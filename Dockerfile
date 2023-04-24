#syntax=docker/dockerfile:1.2
ARG PYTHON_VERSION=3.9.5
ARG APP_DIR=/srv/app

# I used to think using alpine linux for python was a good idea back in 2019,
# but it's not always the case.
# See: https://pythonspeed.com/articles/alpine-docker-python/
FROM python:${PYTHON_VERSION}-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV APP_DIR=${APP_DIR}


# create the app user
RUN groupadd -r app && useradd -r -g app app \
    # create the appropriate directories \
    && mkdir -p /srv/app \
    && chown -R app:app /srv/app \
    && chmod 755 /srv/app
#
WORKDIR /srv/app

# install dependencies \
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    ;
#
COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip \
    && pip install pipenv && pip install -r /tmp/requirements.txt \
    ;

FROM base AS dev

COPY --from=base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY install-watchman.sh /usr/local/bin/install-watchman.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/install-watchman.sh

ENTRYPOINT ["docker-entrypoint.sh"]

RUN /usr/local/bin/install-watchman.sh

COPY . /srv/app

EXPOSE 8000
