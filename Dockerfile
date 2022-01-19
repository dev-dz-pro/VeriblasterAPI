FROM python:3.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# Work on all accept heruko 
# EXPOSE 8000

# CMD [ "gunicorn", "--bind", ":8000", "--workers", "4", "veriblaster.wsgi:application" ]

# Work for heruko
CMD gunicorn veriblaster.wsgi:application --bind 0.0.0.0:$PORT 