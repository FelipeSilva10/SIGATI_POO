FROM python:3.13-slim

ENV TERM=xterm

WORKDIR /app

COPY . .

CMD ["python", "main.py"]
