FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y ffmpeg wget && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    python3 -m pip install -r requirements.txt && \
    python3 -m pip install --upgrade yt-dlp

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]
