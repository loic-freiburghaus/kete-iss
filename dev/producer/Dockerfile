#Take ubuntu:20.04 as base image
#FROM ubuntu:20.04
FROM python:3

#Move to /tmp/app as current directory
#WORKDIR /tmp/app


#RUN apt update -y && apt install -y python3-pip

RUN pip install influxdb kafka-python

#Copy Python script
COPY producer.py .

#Configure executed command at docker run
CMD [ "python", "producer.py" ]