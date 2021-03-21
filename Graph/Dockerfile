FROM python:3-buster
RUN mkdir -p /metrics
COPY code/ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./flaskr.py"]
