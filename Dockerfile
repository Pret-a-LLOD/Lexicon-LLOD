FROM python:3.9-slim-buster
WORKDIR /bnet

# create the app user
RUN addgroup --system bnet && adduser --system --group bnet

COPY api.py openapi.yaml requirements.txt /bnet

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chown -R bnet:bnet /bnet

# change to the app user
USER bnet

EXPOSE 8080
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "api:app", "--log-level=info", "--workers=4", "--log-file=/bnet/error.log", "--timeout=1200"]
