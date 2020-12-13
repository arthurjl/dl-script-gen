from flask import render_template, request
from app import app


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    data = request.args
    # Generate some text with the data and the audio clip
    if data:
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer malesuada consequat massa nec ultrices. Vivamus tincidunt lacus ac nisl sodales, eget imperdiet lorem accumsan. Ut interdum purus nec ex vestibulum, ac bibendum nulla ultricies. In hac habitasse platea dictumst. Donec vel finibus mauris, sed porta nibh. Praesent non eros dapibus, sagittis quam eu, suscipit tellus. In aliquam, dui ut cursus maximus, risus risus ultricies velit, sit amet tempor ipsum sapien a nunc. Suspendisse imperdiet vel ipsum vitae finibus. Ut aliquet eros vitae arcu aliquam porttitor et vel mauris. In accumsan enim lacus, a viverra orci lacinia sed. Sed interdum, turpis sit amet tincidunt feugiat, libero lacus aliquam neque, at gravida nibh arcu vitae est. Phasellus sapien sapien, mattis at nibh quis, eleifend aliquam erat. Sed in nisi vehicula, congue dui quis, malesuada magna."
        audio = "app\static\out289.wav"
        return render_template('index.html', text=text, audio=audio)
    else:
        return render_template('index.html', text=None, audio=None)
    
