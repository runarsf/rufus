FROM python

RUN apt-get update && \
	apt-get install git -y && \
	apt-get install python3 -y && \
	apt-get install python3-pip -y

COPY ./src/requirements.txt /app/requirements.txt
RUN python3 -m pip install -U -r /app/requirements.txt

#COPY ./src /app
WORKDIR /app

#EXPOSE 8080

CMD ["python3", "-u", "rufus.py"]
#CMD ["python3", "-u", "-m", "trace", "--trace", "./rufus.py", "|", "grep", "rufus.py"]
