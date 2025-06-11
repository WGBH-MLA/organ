###########################
# 'base' build stage, common to all build stages
###########################
FROM python:3.11-slim as base

# Set working dir to /app, where all code lives.
WORKDIR /app
RUN pip install -U pip pdm

# Copy app code to container
COPY pyproject.toml pdm.lock README.md ./
COPY organ organ

# Copy migration files
# COPY alembic.ini ./
# COPY migrations migrations


###########################
# 'dev' build stage
###########################
FROM base as dev
# Configure pdm to instal dependencies into ./__pypyackages__/
RUN pdm config python.use_venv false
# Configure python to use pep582 with local __pypyackages__
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages/pdm/pep582
# Add local packages to $PATH
ENV PATH=/app/__pypackages__/3.11/bin/:$PATH

# Install dev dependencies with pdm
RUN pdm install -G dev
# Start dev server.
CMD uvicorn organ.app:app --host 0.0.0.0 --reload --log-level debug


###########################
# 'build' build stage for production
############################
FROM base as build
RUN apt update && apt install -y gcc libpq-dev git

RUN pdm config venv.with_pip True
RUN pdm install -G production -L pdm-locks/pdm.prod.lock

# Install pip into the virtual environment
RUN /app/.venv/bin/python -m ensurepip

###########################
# 'production' final production image
############################
FROM python:3.11-slim as production
WORKDIR /app

RUN apt update && apt install -y libpq-dev
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/ /app/
COPY templates templates
COPY static static

ENV organ_ENV=production
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD gunicorn organ.main:main -b 0.0.0.0:8000 -w 2 --worker-class uvicorn.workers.UvicornWorker
