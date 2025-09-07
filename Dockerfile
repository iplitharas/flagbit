###########################################################################
######################### BASE STAGE #####################################
###########################################################################

# pull official base image
FROM python:3.11-slim as base
LABEL maintainer="johnplitharas@gmail.com"

ARG POETRY_VERSION="1.8.3"

# set environment variables
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    WORKDIR="/flagship"

# Set working directory
WORKDIR $WORKDIR

# Ugrade pip and istall poetry in the same layer
# hadolint ignore=DL3013
RUN pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION"

# Copy poetry files
COPY poetry.lock pyproject.toml ./

# Remove any temp build files
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Create a non-root user and group
RUN addgroup --system app && adduser --system --group app

# Set file permissions to allow the non-root user to write to it
RUN chown -R app:app $WORKDIR

###########################################################################
######################### END OF BASE STAGE ###############################
###########################################################################

FROM base as test

# install python dependencies and remove temp files
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf /root/.cache/pip /tmp/poetry_cache

# Switch to the non-root user
USER app
# Copy only project files to avoid cache invalidation
COPY --chown=app:app ./src ./src

# Uncomment the line below, and specify your entrypoint
#CMD ["python", "-u", "src/main.py"]

###########################################################################
######################### END OF TEST STAGE ###############################
###########################################################################


FROM base as prod

# install python dependencies and remove temp files
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --without dev \
    && rm -rf /root/.cache/pip /tmp/poetry_cache

# Switch to the non-root user
USER app
# Copy only project files to avoid cache invalidation
COPY --chown=app:app ./src ./src

# Uncomment the line below, and specify your entrypoint
#CMD ["python", "-u", "src/main.py"]

###########################################################################
######################### END OF PROD STAGE ###############################
###########################################################################