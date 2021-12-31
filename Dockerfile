FROM python:3.8.12

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app

RUN pip3 install -r requirements.txt

COPY . /usr/src/app

RUN python3 manage.py migrate


EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "localhost:8000"]