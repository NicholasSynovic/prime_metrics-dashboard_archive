FROM python:3.9.1
RUN mkdir -p /dataCollected
COPY Data-Collection/ /app
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["python","dataCollection.py","-u","(URL)","-t","(GITHUB_TOKEN)","-o","(DATABASE.db)"]
ENTRYPOINT ["python","./dataCollection.py"]
# CMD ["-u","(URL)","-t","(GITHUB_TOKEN)","-o","(DATABASE.db)"]


