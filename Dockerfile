FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONASYNCIODEBUG 1
WORKDIR /opt/app

ADD ./requirements.txt ./requirements_test.txt /opt/app/
RUN pip install -r requirements.txt -r requirements_test.txt \
  # https://github.com/PyCQA/pylint/issues/2241
  && pip install pylint astroid --pre -U

RUN mkdir /opt/log
VOLUME [ "/opt/app/data" ]
ADD . /opt/app
RUN python setup.py test && python setup.py install