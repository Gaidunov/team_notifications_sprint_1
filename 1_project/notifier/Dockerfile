FROM python:latest

ADD requirements.txt /app/requirements.txt

COPY . .

WORKDIR /app/

RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' app  

