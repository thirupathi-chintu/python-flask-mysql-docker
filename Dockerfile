FROM python:3.7
MAINTAINER Thirupathi Peraboina <thirupathiperaboina@gmail.com>

## Update apt-get sources AND install Python-dve
RUN apt-get update && apt-get install -y build-essential python3-dev 
RUN apt-get install -y python3-setuptools gcc python3-dev musl-dev py3-mysqlclient
ADD ./app /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3","app.py"]
