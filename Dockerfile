###########
# BUILDER #
###########
FROM python:3.10-alpine as builder

# install system dependencies
RUN apk update && \
    apk add --update --no-cache build-base curl \
        postgresql-dev gcc g++ python3-dev \
        musl-dev openssl-dev libffi-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -

# add poetry to PATH
ENV PATH "/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock ./
RUN if [[ ${ENVIRONMENT} == prod ]]; then \
      poetry export -f requirements.txt -o requirements.txt --without-hashes --without-urls ;\
    else \ 
      poetry export -f requirements.txt -o requirements.txt --without-hashes --without-urls --with=dev ;\
    fi
RUN pip install -U setuptools pip && \
    pip wheel --no-cache-dir --wheel-dir /tmp/wheels -r requirements.txt


#########
# FINAL #
#########
FROM python:3.10-alpine

# create the directory for the app
ENV APP_HOME /usr/src
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

# create the app user
RUN apk update && \
    apk upgrade --available && \
    apk add bash && \
    addgroup -S fastapi && adduser -S fastapi -G fastapi -h ${APP_HOME}

# set the environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${APP_HOME}

# install python dependencies
COPY --from=builder /tmp/wheels ${APP_HOME}/wheels
RUN pip install -U pip && \
    pip install --no-cache ${APP_HOME}/wheels/* && \
    rm -rf ${APP_HOME}/wheels

# add application sources
COPY ./app entrypoint.sh ./

# copy the start script and make it executable
RUN chmod +x entrypoint.sh && \
    chown -R fastapi:fastapi ${APP_HOME}

# change context to the app user
USER fastapi

# run entrypoint.sh
CMD [ "/bin/bash", "-c", "${APP_HOME}/entrypoint.sh" ]
