FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir discord.py python-dotenv

CMD ["python", "bot.py"]
