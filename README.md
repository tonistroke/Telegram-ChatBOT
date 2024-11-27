# ChatBOT
Los datos, como los `tags`, `patrones` y `respuestas`, pasan por un proceso de tokenización antes de ser utilizados en el entrenamiento del modelo, que posteriormente será empleado para darle vida a la IA.

#### pipeline tokenizacion creacion de datos de entrenamiento del modelo
tokenize --> lower and stemmize --> exclude puntuation chsrscters --> bag of words

##### Bag of words
```python
sentence = ["hello", "how", "are", "you"]
words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
bow = bag_of_word(sentence, words)
print(bow) // [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
```