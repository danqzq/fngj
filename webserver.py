from flask import Flask
from threading import Thread
import random

app = Flask('')



@app.route('/')
def home():
    return "Don't even try to hack our bot you scumbag"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()