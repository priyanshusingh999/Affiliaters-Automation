import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is Running!'

def run_flask():
    app.run(host='0.0.0.0', port=8085)

threading.Thread(target=run_flask).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)