FROM python:3.12.6-alpine
EXPOSE 5022

LABEL version="0.1.1"

WORKDIR /app

COPY requirements.txt app/* ./
RUN pip install --no-cache-dir -r requirements.txt && rm -f requirements.txt


CMD ["python", "main.py"]

# docker buildx build \                                                                                                                              ─╯
# --push \
# --platform linux/amd64,linux/arm64 \
# --tag docker-rest-debug:latest \
# .