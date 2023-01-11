from flask import Flask, request, url_for, render_template
from rucksack import BackgroundThread

app = Flask(__name__)
rucksack_thread = BackgroundThread()

rucksack_thread.start()
@app.route('/')
def index():
    return render_template('index.html')

@app.get('/status')
def status_get():
    return {
        "wanted_list" : list(rucksack_thread.wanted_list),
        "current_list" : list(rucksack_thread.current_list)
    }

@app.post('/reset')
def reset():
    rucksack_thread.reset()

if __name__ == "__main__":
    try:
        app.run()
    finally:
        rucksack_thread.stop()
        rucksack_thread.join()
