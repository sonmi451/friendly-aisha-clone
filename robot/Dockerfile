FROM python:3.10

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]
CMD ["./robot.py"]
