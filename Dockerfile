FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY /Users/aviralchauhan/web-development/cosmocloud/cert.pem /Users/aviralchauhan/web-development/cosmocloud/key.pem /app/
COPY . /app

# debug command to check if the files are copied
RUN ls -la /app

EXPOSE 5000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--ssl-keyfile", "/app/key.pem", "--ssl-certfile", "/app/cert.pem"]