FROM python:3.9.16-buster
WORKDIR /blaze
RUN apt-get update && apt-get -y upgrade 
RUN apt-get install -y python3-pip 
RUN apt-get install -y python3-dev build-essential
COPY . .
RUN pip install -r requirements.txt
SHELL ["python", "run_backend.py", " yaml/04_summary_custom.yaml"]
