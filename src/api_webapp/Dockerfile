FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --extra-index-url https://pypi.rds.uhs.nhs.uk/simple/ --trusted-host pypi.rds.uhs.nhs.uk -r requirements.txt

EXPOSE 7800

ENTRYPOINT ["tail", "-f", "/dev/null"]
