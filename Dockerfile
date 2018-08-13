FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONASYNCIODEBUG 1
WORKDIR /opt/app

ADD ./requirements.txt ./requirements_test.txt /opt/app/
RUN pip install -r requirements.txt -r requirements_test.txt

RUN mkdir /opt/log
VOLUME [ "/opt/app/data" ]
ADD . /opt/app
RUN python setup.py install