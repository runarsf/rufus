FROM python:3

#RUN apt-get update \
  # && apt-get install -y git python3 python3-pip

COPY ./src/requirements.txt /app/requirements.txt
RUN python3 -m pip install -U -r /app/requirements.txt

WORKDIR /app

CMD ["python3", "-u", "rufus.py"]
#CMD ["python3", "-u", "-m", "trace", "--trace", "./rufus.py", "|", "grep", "rufus.py"]
