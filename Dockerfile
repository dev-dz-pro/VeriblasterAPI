# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .


# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# Work on all accept heruko 
# EXPOSE 8000

# CMD [ "gunicorn", "--bind", ":8000", "--workers", "4", "veriblaster.wsgi:application" ]

# Work for heruko
CMD gunicorn veriblaster.wsgi:application --bind 0.0.0.0:$PORT 