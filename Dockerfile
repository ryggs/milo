FROM python:3.6.4

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt
RUN python manage.py migrate

RUN pip install gunicorn
ENV DJANGO_DEBUG False

CMD ["gunicorn", "milo.wsgi:application", "--bind", "0.0.0.0:8000"]