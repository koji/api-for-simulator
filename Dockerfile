FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

# need to force reinstall because of dependeincies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn && \
    pip install --no-cache-dir  --force-reinstall opentrons

COPY ./app /app


