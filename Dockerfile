FROM python:3.12

WORKDIR /marketplace
COPY . /marketplace
EXPOSE 8000

RUN pip install -r requirements.txt

RUN adduser --disabled-password service-user

USER service-user
