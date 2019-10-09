FROM python:3.7-slim-buster

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt


EXPOSE 8080

CMD python app.py