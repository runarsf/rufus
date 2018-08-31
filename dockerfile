# https://www.wintellect.com/containerize-python-app-5-minutes/
FROM python:alpine3.7
COPY ./src ./app
WORKDIR /app
RUN pip install -r ./requirements.txt
EXPOSE 5000
CMD python ./rufus.py
