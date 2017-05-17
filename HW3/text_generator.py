import os
import sys
import unicodedata
import numpy as np
import random

import pickle

class TextGenerator(object):

    def __init__(self):
        self.data1 = dict()
        self.data2 = dict()
        self.text = []
        self.new_line_counter = 0


    def initialize_data(self):
        print "reading one"
        f1 = open('data1.pickle', 'rb')
        self.data1 = pickle.load(f1)
        print "reading two"
        f2 = open('data2.pickle', 'rb')
        self.data2 = pickle.load(f2)


    def generate_two_words(self):
        position = -1
        word1 = self.text[position]
        if word1 == '\n':
            position -= 1
            word1 = self.text[position]
        position -= 1
        word2 = self.text[position]
        if word1 == '\n':
            position -= 1
            word2 = self.text[position]
        return word2 + ' ' + word1


    def generate_one_word(self):
        position = -1
        word = self.text[position]
        if word == '\n':
            position -= 1
            word = self.text[position]
        return word.lower()


    def make_lines_and_upper(self):
        new_line_counter = 0
        positions = []
        i = 0
        while i < len(self.text):
            if i != 0:
                if self.text[i - 1] == '.':
                    self.text[i] = self.text[i][0].upper() + self.text[i][1:]

            new_line_counter += len(self.text[i])
            if new_line_counter > 70:
                self.text.insert(i, '\n')
                i += 1
                new_line_counter = 0
            i += 1

        self.text[0] = self.text[0][0].upper() + self.text[0][1:]
        if self.text[-1] != '.':
            self.text.append('.')


    def get_word(self, words_in_statement):
        num = random.random()
        if (words_in_statement == 0) or (words_in_statement == 1):
            if (words_in_statement == 0):
                stats = self.data1['.']
            else:
                stats = self.data1[self.text[-1]]
        else:
            stats = self.data2[self.text[-2] + ' ' + self.text[-1]]

        for j, stat in enumerate(stats[1]):
            if num < stat:
                word_number = j
                break
        return stats[0][word_number]


    def generate_text(self, lenght):
        print "generating text"
        words_in_statement = 0
        statement_lenght = random.randint(5, 30)
        for it in range(lenght):

            word = self.get_word(words_in_statement)
            self.text.append(word)
            words_in_statement += 1
            if word == '.':
                words_in_statement = 0
            if words_in_statement > statement_lenght:
                self.text.append('.')
                words_in_statement = 0
                statement_lenght = random.randint(5, 30)

        self.make_lines_and_upper()
        txt = ' '.join(self.text)
        txt = txt.replace('\n .', '.\n')
        txt = txt.replace('\n ', '\n')
        return txt.replace(' .', '.')


def main():
    text_length = 13000
    text_generator = TextGenerator()
    text_generator.initialize_data()
    text = text_generator.generate_text(text_length)
    f = open('generated_text.txt', 'w')
    f.write(text.encode('utf8'))


if __name__ == '__main__':
    main()
