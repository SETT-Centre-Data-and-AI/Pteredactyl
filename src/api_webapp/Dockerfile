FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry lock

RUN poetry install

EXPOSE 7800

CMD ["poetry", "run", "python", "app.py"]
