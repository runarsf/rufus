FROM python:alpine3.6

COPY ./src /app
WORKDIR /app

RUN pip install -r ./requirements.txt
RUN python ./run.py

EXPOSE 8080

CMD ["python", "rufus.py"]
