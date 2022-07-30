FROM python:3.7-slim

WORKDIR /project

COPY requirements.txt /project

RUN pip3 install -r /project/requirements.txt --no-cache-dir

COPY . /project
 
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]