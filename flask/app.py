#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is up and running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50007, debug=True)
