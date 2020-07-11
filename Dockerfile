FROM python:3

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
RUN python -m pip install -U -r requirements.txt

CMD [ "python", "-u", "rufus.py" ]