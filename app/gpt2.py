from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import numpy as np

model_location = './app/models/output'
device = 'cpu'

tokenizer = GPT2Tokenizer.from_pretrained(model_location)
model = GPT2LMHeadModel.from_pretrained(model_location)
model = model.to(device)

def generate(input_str, length=250, n=5):
  cur_ids = torch.tensor(tokenizer.encode(input_str)).unsqueeze(0).long().to(device)
  model.eval()
  with torch.no_grad():
    for i in range(length):
      outputs = model(cur_ids[:, -1024:], labels=cur_ids[:, -1024:])
      loss, logits = outputs[:2]
      softmax_logits = torch.softmax(logits[0,-1], dim=0)
      next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=n)
      cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device) * next_token_id], dim=1)
    output_list = list(cur_ids.squeeze().to('cpu').numpy())
    output_text = tokenizer.decode(output_list)
    return output_text

def choose_from_top(probs, n=5):
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)

generated_text = generate("My office is in ")
print(generated_text)