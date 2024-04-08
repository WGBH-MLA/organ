###########################
# 'base' build stage, common to all build stages
###########################
FROM python as base
WORKDIR /app
RUN pip install -U pip
# Copy app code to container
COPY pyproject.toml pdm.lock ./

# add app directories
ADD organ/ organ/
ADD static/ static/
ADD templates/ templates/

# Install PDM dependency manager
RUN pip install pdm
RUN pdm config python.use_venv false
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages/pdm/pep582
ENV PATH=$PATH:/app/__pypackages__/3.11/bin/

RUN pdm install -v

# CMD gunicorn chowda:app -b 0.0.0.0:8000 -w 2 --worker-class uvicorn.workers.UvicornWorker
CMD uvicorn organ:main --host 0.0.0.0 --port 8000
