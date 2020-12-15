from flask import render_template, request, Markup
from app import app
from app.generate import generate_and_visualize
from app.vocab import Vocabulary
from app.models import ScriptGenModelNLayer

# Load pre-determined vocabs
office_vocab = Vocabulary("./app/static/vocabs/office_transcript_end_scene_linebreak_chars_train.pkl")
vocabs = {
    "office": office_vocab
}

# Load pre-trained models
office_model = ScriptGenModelNLayer(len(office_vocab), 512, 2)
office_model.load_last_model("./app/static/models/3.1.office/checkpoints")
models = {
    "office": office_model
}

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    data = request.args
    # Generate some text with the data and the audio clip
    if data:
        text, visualizations = generate_and_visualize(models[data["languageModel"]], vocabs[data["languageModel"]], data["seedWords"], None)
        text = text.split("\n")
        audio = "./static/out289.wav"
        return render_template('index.html', text=text, audio=audio, visualizations=visualizations)
    else:
        return render_template('index.html', text=None, audio=None, visualizations=None)

@app.route('/text-to-speech', methods=['GET'])  
def text_to_speech():
    return render_template('text_to_speech.html')
