FROM python:3.10-slim-buster

LABEL maintainer="mattstammers"

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry lock

RUN poetry install

# Expose MkDocs development server port
EXPOSE 8000

# Start development server by default
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
