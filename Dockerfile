FROM python:3.12-alpine

WORKDIR /appbot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "appbot/bot.py"]
