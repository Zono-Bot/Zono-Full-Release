from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return '<h1 style="text-align: center; font-weight: bold; background: linear-gradient(135deg, #FF70A6, #5A9EF8);">Hello, I\'m alive! "THIS VERSION OF ZONO IS NOT OFFICIAL, AND WAS DOWNLOADED FROM GITHUB. FOR THE OFFICIAL BOT, JOIN ZONO HUB SERVER."</h1>'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
