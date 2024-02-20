FROM python:3.10.13-alpine as base

ENV APP_NAME="metadata" \
    # ensures python output to be sent to the terminal without being buffered
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.2.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask interactive questions
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # where requirements + virtual environment will be
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# install required system dependencies
RUN apk update \
    && apk upgrade \
    && pip3 install --upgrade pip wheel


# `builder-base` stage is used to build deps + create virtual environment
FROM base as builder-base

RUN apk update \
    && apk upgrade \
    && apk add --update py3-pip \
    && apk --no-cache add \
    && pip3 install --ignore-installed distlib --disable-pip-version-check poetry==$POETRY_VERSION


# copy project requirement files to ensure they will be cached
WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./

# install runtime dependencies, internally uses $POETRY_VIRTUALENVS_IN_PROJECT
RUN poetry install --without dev


# `production` image used for runtime
FROM base as production

# app configuration
ARG USERNAME=appuser
ARG GROUP_NAME=$USERNAME
ARG UID=1000
ARG GID=$UID

# add a non-root user to run the app
RUN addgroup -g $UID $GROUP_NAME && \
    adduser -D -H -u $UID -G $GROUP_NAME $USERNAME
USER $USERNAME

# copy all required dependecies
COPY --from=builder-base --chown=$USERNAME:$USERNAME $PYSETUP_PATH $PYSETUP_PATH
COPY ./${APP_NAME} ./${APP_NAME}

# launch flask app with a WSGI
ENV PORT=5000 \
    APP_RUNNER=${APP_NAME}.server:app

ENTRYPOINT $VENV_PATH/bin/python -m gunicorn --bind :$PORT $APP_RUNNER