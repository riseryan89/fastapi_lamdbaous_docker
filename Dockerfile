FROM python:3.8-slim AS base
WORKDIR /opt
COPY . /opt
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --no-deps -r requirements.txt
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
