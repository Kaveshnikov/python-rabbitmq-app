FROM python:3.7-slim

RUN apt-get update && apt-get install -y apt-utils gcc g++

WORKDIR /usr/src/app

ENV PYTHONPATH=:/usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY application/ ./

CMD ["python", "run.py"]
