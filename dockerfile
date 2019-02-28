FROM python

COPY ./src /app
WORKDIR /app

RUN apt-get update && \
	apt-get install git -y && \
	apt-get install python3 -y && \
	apt-get install python3-pip -y

RUN python3 -m pip install -U -r ./requirements.txt

EXPOSE 8080

CMD ["python3", "-u", "rufus.py"]
