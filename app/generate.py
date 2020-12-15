import os
import torch
import app.models
import math
import random
from flask import Markup
from IPython.display import HTML as html_print

DEVICE = "cpu"
SEQUENCE_LENGTH = 512
TEMPERATURE = 0.5
BEAM_WIDTH = 10

def max_sampling_strategy(sequence_length, model, output, hidden, vocab, temperature=TEMPERATURE):
    outputs = []
    for ii in range(sequence_length):
        sample = torch.argmax(output)
        outputs.append(sample)
        output, hidden = model.inference(sample, hidden, temperature)
    return outputs
    
def sample_sampling_strategy(sequence_length, model, output, hidden, vocab, temperature=TEMPERATURE):
    outputs = []
    for ii in range(sequence_length):
        sample = torch.multinomial(output, 1)
        outputs.append(sample)
        output, hidden = model.inference(sample, hidden, temperature)
    return outputs

def beam_sampling_strategy(sequence_length, beam_width, model, output, hidden, vocab, temperature=TEMPERATURE):
    beams = [([], output, hidden, 0)]
    for ii in range(sequence_length):
        new_beams = []
        for b in beams:
            samples = b[0]
            output = b[1]
            hidden = b[2]
            likelihood = b[3]

            # compute probability distributions
            if ii != 0:
                output, hidden = model.inference(samples[-1], hidden, temperature)
            
            for _ in range(beam_width):
                sample = torch.multinomial(output, 1)[0]
                new_samples = list(samples)
                new_samples.append(sample)
                new_beam = (new_samples,
                            output,
                            hidden,
                            likelihood + torch.log(output[0][sample]))
                new_beams.append(new_beam)
            
        new_beams.sort(key = lambda b : b[3], reverse=True)
        beams = new_beams[:beam_width]

    outputs = beams[0][0]
    return outputs


def generate_language(model, vocab, seed_words, sequence_length,  device=DEVICE, sampling_strategy='max', beam_width=BEAM_WIDTH, temperature=TEMPERATURE):
    model.eval()
    with torch.no_grad():
        seed_words_arr = vocab.words_to_array(seed_words)

        # Computes the initial hidden state from the prompt (seed words).
        hidden = None
        for ind in seed_words_arr:
            data = ind.to(device)
            output, hidden = model.inference(data, hidden)

        if sampling_strategy == 'max':
            outputs = max_sampling_strategy(sequence_length, model, output, hidden, vocab)
        elif sampling_strategy == 'sample':
            outputs = sample_sampling_strategy(sequence_length, model, output, hidden, vocab)
        elif sampling_strategy == 'beam':
            outputs = beam_sampling_strategy(sequence_length, beam_width, model, output, hidden, vocab)
        return vocab.array_to_words(seed_words_arr.tolist() + outputs)

def generate_activations(model, vocab, text, temperature=TEMPERATURE):
    model.eval()
    with torch.no_grad():
        text_array = vocab.words_to_array(text)

        hidden = None
        activation_values = []
        for sample in text_array:
            output, hidden = model.inference(sample, hidden, temperature)
            activation_val = hidden[0].cpu().detach().numpy().flatten()
            activation_values.append(activation_val)
    return activation_values

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

def visualize(generated_sentence, activation_values, cell_no):
    text_colours = []

    for char, val in zip(generated_sentence, activation_values):
        text_clr = (char, get_clr(val[cell_no]))
        text_colours.append(text_clr)

    html_colors = html_print(''.join([cstr(ti, color=ci) for ti,ci in text_colours]))
    return html_colors

def construct_visualization(activation_values, text, n_visuals):
    result = []
    for cell_no in [625, 643, 652, 700]:
        print("Processing cell_no: " + str(cell_no))
        html_colors = visualize(text, activation_values, cell_no)
        cell_result = html_colors.data
        result.append((cell_no, Markup(cell_result)))
    return result

def generate_and_visualize(language_model, vocab, seed_words, speech_model, sequence_length=SEQUENCE_LENGTH, device="cpu", 
                        strategy="sample", beam_width=BEAM_WIDTH, temperature=TEMPERATURE, n_visuals=3):
    generated_sentence = generate_language(language_model, vocab, seed_words, sequence_length, sampling_strategy=strategy)
    activation_values = generate_activations(language_model, vocab, generated_sentence)
    visualization = construct_visualization(activation_values, generated_sentence, n_visuals)

    return generated_sentence, visualization