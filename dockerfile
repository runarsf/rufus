FROM python:alpine3.7
COPY . /src
WORKDIR /src
RUN pip install -r ./requirements.txt
EXPOSE 5000
CMD python ./rufus.py
