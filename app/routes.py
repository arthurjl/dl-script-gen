import requests
from flask import render_template, request, Markup
from app import app

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    data = request.args
    # Generate some text with the data and the audio clip
    if data:
        text_data = {"seedWords": data["seedWords"], "model": data["languageModel"]}
        res = requests.post("https://c709c4f714d4.ngrok.io/generateText", data=text_data)
        import sys
        print(res.text, file=sys.stderr)
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


