FROM python:3.10.12-slim-bullseye
WORKDIR /app
COPY requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","polybot/bot.py"]