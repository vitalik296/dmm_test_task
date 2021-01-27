FROM python:3.10.0a4-buster

WORKDIR /usr/src/flask

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./etc/requirment.txt /usr/src/flask/etc/requirment.txt
RUN pip install -r etc/requirment.txt

COPY . /usr/src/flask

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["main.py"]