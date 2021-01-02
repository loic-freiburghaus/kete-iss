#Take python:3 as base image
FROM python:3

#Install the kafka library
RUN pip install kafka-python requests geopy

#Copy Python script
COPY producer.py .

#Configure command to execute at docker run
CMD [ "python", "producer.py" ]