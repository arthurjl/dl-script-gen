import torch
import math
from app.generate import generate_language
from IPython.display import HTML as html_print


# get html element
def cstr(s, color='black'):
    if (s == ' '):
        return "<text style=color:#000;padding-left:10px;background-color:{}> </text>".format(color, s)
    elif (s == '\n'):
        return "<text style=color:#000;padding-left:10px;background-color:{}> <br></text>".format(color, s)
    else:
        return "<text style=color:#000;background-color:{}>{} </text>".format(color, s)

# get appropriate color for value
def get_clr(value):
    colors = ['#85c2e1', '#89c4e2', '#95cae5', '#99cce6', '#a1d0e8'
        '#b2d9ec', '#baddee', '#c2e1f0', '#eff7fb', '#f9e8e8',
        '#f9e8e8', '#f9d4d4', '#f9bdbd', '#f8a8a8', '#f68f8f',
        '#f47676', '#f45f5f', '#f34343', '#f33b3b', '#f42e2e']

    value_idx = math.floor(value * len(colors))
    if value_idx >= len(colors):
        value_idx = len(colors) - 1

    return colors[value_idx]


def generate_and_visualize_strategies(model, device, seed_words, sequence_length, vocab, strategy="sample", beam_width=10, temperature=0.4):
    generated_sentence = generate_language(model, device, seed_words, sequence_length, vocab, strategy, beam_width=beam_width)

    model.eval()
    with torch.no_grad():
        generated_sentence_array = vocab.words_to_array(generated_sentence)

        hidden = None

        activation_values = []
        for sample in generated_sentence_array:
            output, hidden = model.inference(sample, hidden, temperature)
            activation_val = hidden[0].cpu().detach().numpy().flatten()
            activation_values.append(activation_val)

    return generated_sentence, activation_values

def visualize(generated_sentence, activation_values, cell_no):
    text_colours = []

    for i in range(len(activation_values)):
        text = (generated_sentence[i], get_clr(activation_values[i][cell_no]))
        text_colours.append(text)

    html_colors = html_print(''.join([cstr(ti, color=ci) for ti,ci in text_colours]))
    return html_colors