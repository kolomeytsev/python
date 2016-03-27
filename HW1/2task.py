import random
import sys


def split_text(text):
    words_and_punctuation = []
    word = []
    for symbol in text:
        if symbol.isalpha():
            word.append(symbol)
        else:
            if word:
                words_and_punctuation.append(''.join(word))
            words_and_punctuation.append(symbol)
            word = []
    if word:
        words_and_punctuation.append(''.join(word))
    return words_and_punctuation


def shuffle_letters(text):
    for i, element in enumerate(text):
        if len(element) > 3:
            half_word = list(element[1:len(element)-1])
            random.shuffle(half_word)
            text[i] = element[0] + ''.join(half_word) + element[-1]
    return text


def transform(text):
    text_splitted = split_text(text)
    shuffled_words = shuffle_letters(text_splitted)
    new_text = ''.join(shuffled_words)
    return new_text

text = sys.stdin.read()
if text:
    output_text = transform(text)
    print output_text
