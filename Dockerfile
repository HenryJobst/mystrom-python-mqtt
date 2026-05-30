FROM python:3.14.5-alpine

WORKDIR /mystrom

COPY requirements.txt ./

RUN apk upgrade --no-cache && \
    pip install --no-cache-dir --upgrade pip setuptools>=78.1.1 wheel>=0.46.2 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "-m", "main"]
