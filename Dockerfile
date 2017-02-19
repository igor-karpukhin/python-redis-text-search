FROM python:2.7.13-slim

MAINTAINER IgorKarpukhin

# Setting up python dependencies
RUN pip install requests
RUN pip install flask
RUN pip install redis
RUN mkdir -p /home/igor/

COPY app/ /home/igor/app/
WORKDIR /home/igor/app/

CMD ["python2"]

