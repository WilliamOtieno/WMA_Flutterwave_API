FROM python:3.10

# Install crontab binary to handle cron jobs
RUN apt-get update && apt-get install -y cron apt-utils

WORKDIR /usr/src/app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input --verbosity 0
RUN python manage.py create_demo_user
RUN python manage.py crontab add .
RUN rm -rf env
RUN rm -rf WMA/.env
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 8 --timeout 120 --preload WMA.wsgi
