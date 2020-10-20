#Take ubuntu:20.04 as base image
FROM ubuntu:20.04

#Move to /tmp/app as current directory
WORKDIR /tmp/app


RUN apt update -y && apt install -y python3-pip

RUN pip3 install influxdb

#Copy Python script
COPY api_test_2.py .

#Configure executed command at docker run
CMD [ "python3", "api_test_2.py" ]