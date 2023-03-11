FROM mcr.microsoft.com/playwright/python:v1.30.0-focal

RUN apt update
RUN apt install -y python3

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN playwright install \
    && playwright install-deps firefox

COPY . /app

ENTRYPOINT ["python3"]
CMD ["./robot.py"]
