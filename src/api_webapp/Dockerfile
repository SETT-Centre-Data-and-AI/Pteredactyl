FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -e ../pteredactyl

RUN pip install -r requirements.txt

EXPOSE 7800

CMD ["python","app.py"]
