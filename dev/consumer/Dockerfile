#Take python:3 as base image
FROM python:3

#Install the influxdb and kafka libraries
RUN pip install influxdb kafka-python

#Copy Python script
COPY consumer.py .

#Configure command to execute at docker run
CMD [ "python", "consumer.py" ]