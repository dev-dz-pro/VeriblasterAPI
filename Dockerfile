FROM python:3.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "--bind", ":8000", "--workers", "4", "veriblaster.wsgi:application" ]