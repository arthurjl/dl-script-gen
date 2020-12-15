import os
import torch
import app.models

DEVICE = "cpu"
SEQUENCE_LENGTH = 512

def max_sampling_strategy(sequence_length, model, output, hidden, vocab, temperature=0.5):
    outputs = []
    for ii in range(sequence_length):
        sample = torch.argmax(output)
        outputs.append(sample)
        output, hidden = model.inference(sample, hidden, temperature)
    return outputs
    
def sample_sampling_strategy(sequence_length, model, output, hidden, vocab, temperature=0.5):
    outputs = []
    for ii in range(sequence_length):
        sample = torch.multinomial(output, 1)
        outputs.append(sample)
        output, hidden = model.inference(sample, hidden, temperature)
    return outputs

def beam_sampling_strategy(sequence_length, beam_width, model, output, hidden, vocab, temperature=0.5):
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


def generate_language(model, device, seed_words, sequence_length, vocab, sampling_strategy='max', beam_width=10, temperature=0.5):
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

def generate(language_model, vocab, speech_model, seed_words):
    return generate_language(language_model, DEVICE, seed_words, SEQUENCE_LENGTH, vocab, sampling_strategy="sampling")