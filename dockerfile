FROM python:alpine3.8
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./rufus.py
