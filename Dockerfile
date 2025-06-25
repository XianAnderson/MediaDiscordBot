FROM python:3.12-slim

WORKDIR /app

# Install required packages including Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
