####################
### BUILDER
####################
FROM python:3.11-alpine as builder

# update the system and install dependencies
RUN apk update && \
    apk upgrade --available && \
    apk add --update --no-cache build-base curl \
        postgresql-dev gcc g++ python3-dev \
        musl-dev openssl-dev libffi-dev

# set the environment variables
ENV APP_HOME /usr/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME /opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV PATH "${PATH}:${POETRY_HOME}/bin"

# change the working directory 
WORKDIR ${APP_HOME}

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy the project files
COPY . .

# install the project
RUN if [ "${ENVIRONMENT}" = "prod" ]; then \
      poetry install --no-interaction --without dev ;\
    else \ 
      poetry install --no-interaction ;\
    fi

####################
### FINAL
####################
FROM python:3.11-alpine

# update the system and install bash 
RUN apk update && \
    apk upgrade --available && \
    apk add bash

# set the environment variables
ENV APP_USER fastapi
ENV APP_HOME /usr/src
ENV PYTHONPATH ${APP_HOME}
ENV PATH "${PATH}:${APP_HOME}/.venv/bin"

# copy the project files from the builder stage
COPY --from=builder /usr/src ${APP_HOME}

# change the working directory
WORKDIR ${APP_HOME}

# create the application user
RUN addgroup -S ${APP_USER} && \
    adduser -S ${APP_USER} -G ${APP_USER} -h ${APP_HOME} && \
    chown -R ${APP_USER}:${APP_USER} ${APP_HOME} && \
    chmod +x ${APP_HOME}/entrypoint.sh

# change context to the application user
USER ${APP_USER}

# run entrypoint.sh
CMD [ "/bin/bash", "-c", "${APP_HOME}/entrypoint.sh" ]
