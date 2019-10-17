FROM python:3.7-slim-buster

WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD src .

EXPOSE 8080
ENTRYPOINT [ "python", "main.py" ]
