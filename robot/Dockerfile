FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3.10 python3-pip

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN playwright install \
    && playwright install-deps firefox

COPY . /app

ENTRYPOINT ["python3"]
CMD ["./robot.py"]
