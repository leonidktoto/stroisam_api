FROM python:3.12.1

RUN mkdir /ssam

WORKDIR /ssam

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

