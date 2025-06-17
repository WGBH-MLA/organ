###########################
# 'base' build stage, common to all build stages
###########################
FROM python:3.13-slim as base

# Set working dir to /app, where all code lives.
WORKDIR /app
RUN pip install -U pip

# Copy app code to container
COPY pyproject.toml README.md ./
COPY organ organ

# Copy migration files
# COPY alembic.ini ./
# COPY migrations migrations


###########################
# 'dev' build stage
###########################
FROM base as dev

# Install uv
RUN pip install uv

# Install dev dependencies
RUN uv sync --dev
# Start dev server.
CMD uvicorn organ.app:app --host 0.0.0.0 --reload --log-level debug


###########################
# 'production' final production image
############################
FROM python:3.13-slim as production
WORKDIR /app

# Copy the application code
COPY pyproject.toml README.md ./
COPY organ organ
COPY templates templates
COPY static static

# Install pip
RUN pip install -U pip

# Install the project in production mode
RUN pip install .[production]

# Clean up APT
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Set the production environment
ENV ENVIRONMENT=production

EXPOSE 8000

CMD gunicorn organ.main:main -b 0.0.0.0:8000 -w 2 --worker-class uvicorn.workers.UvicornWorker
