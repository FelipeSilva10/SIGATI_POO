FROM python:3.13-slim

ENV TERM=xterm

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask

CMD ["python", "main.py"]
