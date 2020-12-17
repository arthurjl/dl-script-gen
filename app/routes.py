import requests
import sys
from flask import render_template, request, Markup, redirect, url_for
from app import app

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    data = request.args
    # Generate some text with the data and the audio clip
    if data and data["seedWords"]:
        text_data = {"seedWords": data["seedWords"], "model": data["languageModel"]}
<<<<<<< HEAD
        res = requests.post("https://c709c4f714d4.ngrok.io/generateText", data=text_data)
        import sys
=======
        res = requests.post("https://63332a7ef8f3.ngrok.io/generateText", data=text_data)
>>>>>>> b07017925762b7b809298d73a3649e33183996a3
        print(res.text, file=sys.stderr)
        if (res.status_code != 200):
            return render_template('index.html', error_message="Unable to retrieve successful request from backend")
        print(res.json(), file=sys.stderr)

        text_raw = res.json()["text"]
        text = text_raw.split("\n")

        vis_data = {"text": text_raw, "model": data["languageModel"]}
        res = requests.post("https://c709c4f714d4.ngrok.io/generateCellVis", data=vis_data)
        visualizations = res.json()["cell_vis"]

        audio = "./static/out289.wav"
        return render_template('index.html', text=text, audio=audio, visualizations=visualizations)
    else:
        return render_template('index.html', text=None, audio=None, visualizations=None)


