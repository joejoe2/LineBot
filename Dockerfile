FROM joejoe2/ub_py3:01

RUN apt-get update

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV LC_ALL C.UTF-8

ENTRYPOINT ["gunicorn"]

CMD ["app:app","-w","1","--threads","1"]