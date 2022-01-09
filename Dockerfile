FROM python:3.8.12

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app

RUN pip3 install -r requirements.txt

COPY . /usr/src/app

RUN python3 manage.py migrate

ENV PYTHONUNBUFFERED=1



CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]