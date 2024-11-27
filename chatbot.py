"""
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
"""

import random
import json

import torch

from model import neural_network
from word_pross import bag_of_word, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = neural_network(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def handle_response(sentence: str) -> str:
    sentence = tokenize(sentence)
    X = bag_of_word(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['respuestas'])
    else:
        return "Lo siento no entiendo..."


#Uso handle_response
dbg = handle_response("Estoy teniendo un gran día.")
print(dbg)


