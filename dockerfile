# docker build --tag rufus-py .
FROM python:alpine3.6
COPY ./src /app
WORKDIR /app
RUN pip install -r ./requirements.txt
EXPOSE 8080
CMD python ./rufus.py
