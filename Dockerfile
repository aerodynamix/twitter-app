FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /
ADD . /

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python script.py

