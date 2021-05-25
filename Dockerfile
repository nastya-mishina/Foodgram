FROM python:3.8.5

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code

RUN pip3 install -r /code/requirements.txt

COPY . /code

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

