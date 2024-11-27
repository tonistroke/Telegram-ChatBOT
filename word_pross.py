import nltk
import numpy as np
# nltk.download('punkt_tab') # pre trained tokenizer

import nltk.downloader
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stemmize(word):
    # print("stemmize used in: " , word)
    return stemmer.stem(word.lower())

def bag_of_word(tokenized_sentence, all_words):
        # stem each word
    sentence_words = [stemmize(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag



"""
a = "Hola como estas"
print(a)

a = tokenize(a)
print(a)

b = ["contingencia", "coneccion", "contra"]
print(b)
stemmed_b = [stemmize(i) for i in b]
print(stemmed_b)


sentence = ["hello", "how", "are", "you"]
words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
bog = bag_of_word(sentence, words)
print(bog) // [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
"""