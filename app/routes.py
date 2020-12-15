from flask import render_template, request
from app import app
from app.generate import generate
from app.vocab import Vocabulary
from app.models import ScriptGenModelNLayer

# Load pre-determined vocabs
office_vocab = Vocabulary("./app/vocab/office_transcript_end_scene_linebreak_chars_train.pkl")
vocabs = {
    "office": office_vocab
}

# Load pre-trained models
office_model = ScriptGenModelNLayer(len(office_vocab), 512, 2)
office_model.load_last_model("./models/3.1.office/checkpoints")
models = {
    "office": office_model
}

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    data = request.args
    # Generate some text with the data and the audio clip
    if data:
        text = generate(models[data["languageModel"]], vocabs[data["languageModel"]], None, data["seedWords"])
        # text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer malesuada consequat massa nec ultrices. Vivamus tincidunt lacus ac nisl sodales, eget imperdiet lorem accumsan. Ut interdum purus nec ex vestibulum, ac bibendum nulla ultricies. In hac habitasse platea dictumst. Donec vel finibus mauris, sed porta nibh. Praesent non eros dapibus, sagittis quam eu, suscipit tellus. In aliquam, dui ut cursus maximus, risus risus ultricies velit, sit amet tempor ipsum sapien a nunc. Suspendisse imperdiet vel ipsum vitae finibus. Ut aliquet eros vitae arcu aliquam porttitor et vel mauris. In accumsan enim lacus, a viverra orci lacinia sed. Sed interdum, turpis sit amet tincidunt feugiat, libero lacus aliquam neque, at gravida nibh arcu vitae est. Phasellus sapien sapien, mattis at nibh quis, eleifend aliquam erat. Sed in nisi vehicula, congue dui quis, malesuada magna."
        audio = "./static/out289.wav"
        return render_template('index.html', text=text, audio=audio)
    else:
        return render_template('index.html', text=None, audio=None)
    
