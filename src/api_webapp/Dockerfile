FROM python:3.11-slim

COPY . .

RUN pip install --extra-index-url https://pypi.rds.uhs.nhs.uk/simple/ --trusted-host pypi.rds.uhs.nhs.uk -r requirements.txt

EXPOSE 7800

CMD ["poetry", "run", "python", "app.py"]
