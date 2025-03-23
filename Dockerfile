#Base Docker Image

FROM python:3-10-slim

#Install Dependecies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
#Set working directory
WORKDIR /productscout


#Copy application code
COPY requirements.txt /productscout//
RUN pip install --no-cache-dir -r requirements.txt
COPY . /productscout//





