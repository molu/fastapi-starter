####################
### BUILDER
####################
FROM python:3.10-alpine as builder

# install system dependencies
RUN apk update && \
    apk upgrade --available && \
    apk add --update --no-cache build-base curl \
        postgresql-dev gcc g++ python3-dev \
        musl-dev openssl-dev libffi-dev

# set environment variables
ENV APP_HOME /usr/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME /opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV PATH "${POETRY_HOME}/bin:${PATH}"

# change working directory 
WORKDIR ${APP_HOME}

# install dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project files
COPY . .

# install project
RUN if [ "${ENVIRONMENT}" = "prod" ]; then \
      poetry install --no-interaction --without dev ;\
    else \ 
      poetry install --no-interaction ;\
    fi

####################
### FINAL
####################
FROM python:3.10-alpine

# update the system and install bash 
RUN apk update && \
    apk upgrade --available && \
    apk add bash

# set environment variables
ENV APP_HOME /usr/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH ${APP_HOME}
ENV PATH "${PATH}:${APP_HOME}/.venv/bin"

# change the working directory
WORKDIR ${APP_HOME}
# make the entrypoint script executable
RUN addgroup -S fastapi && adduser -S fastapi -G fastapi -h ${APP_HOME}

# install Python dependencies
COPY --from=builder /usr/src ${APP_HOME}

# change context to the application user
USER fastapi

# run entrypoint.sh
CMD [ "/bin/bash", "-c", "${APP_HOME}/entrypoint.sh" ]
