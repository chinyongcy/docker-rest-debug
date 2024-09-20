FROM python:3.12.6-alpine
EXPOSE 5000

LABEL MAINTAINER="Chin Yong"
LABEL GitHub="https://github.com/chinyongcy/docker-rest-debug"
LABEL version="0.1"
LABEL description="A Docker container to test debug api. Service is running on Port 5000"

WORKDIR /app

COPY requirements.txt app/main.py ./
RUN pip install --no-cache-dir -r requirements.txt && rm -f requirements.txt

CMD ["python", "main.py"]




