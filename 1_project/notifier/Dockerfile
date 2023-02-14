FROM python:latest

ADD requirements.txt /app/requirements.txt

COPY . .

RUN chmod +x /scripts/run_periodic_celery.sh

WORKDIR /app/

RUN pip install -r requirements.txt

RUN pip install Pillow

RUN adduser --disabled-password --gecos '' app  

