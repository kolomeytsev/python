import os
import sys
import unicodedata
import numpy as np

import random

import pickle


PUNCTUATION_TRANSLATE_TABLE = {i:None for i in range(sys.maxunicode)
    if unicodedata.category(unichr(i)).startswith('P') and unichr(i) != '.'}


def normalize_text(text):
    text = text.lower().translate(PUNCTUATION_TRANSLATE_TABLE)
    text = text.replace(u'.', u' . ')
    return text


class TextGenerator(object):

    def __init__(self):
        self.two_words_statistic = dict()
        self.one_word_statistic = dict()
        self.text = []
        self.new_line_counter = 0


    def add_two_words(self, two_words, next_word):
        if two_words in self.two_words_statistic:
            val = self.two_words_statistic[two_words].get(next_word)
            if val == None:
                self.two_words_statistic[two_words][next_word] = 1
            else:
                self.two_words_statistic[two_words][next_word] += 1
        else:
            self.two_words_statistic.setdefault(two_words, {})
            self.two_words_statistic[two_words][next_word] = 1

    def add_one_word(self, word, next_word):
        if word in self.one_word_statistic:
            val = self.one_word_statistic[word].get(next_word)
            if val == None:
                self.one_word_statistic[word][next_word] = 1
            else:
                self.one_word_statistic[word][next_word] += 1
        else:
            self.one_word_statistic.setdefault(word, {})
            self.one_word_statistic[word][next_word] = 1


    def add_document(self, name, content):
        text = normalize_text(content).split()
        print "adding ", name

        self.words_num += len(text)

        for it in range(len(text)-2):
            self.add_two_words(text[it] + ' ' + text[it + 1], text[it + 2])
            self.add_one_word(text[it], text[it + 1])
        self.add_one_word(text[-2], text[-1])


    def generate_one_word_statistics(self):
        print "generating one word statistics"
        for one_word in self.one_word_statistic:
            new_words = []
            stats = []
            for word in self.one_word_statistic[one_word]:
                stats.append(self.one_word_statistic[one_word][word])
                new_words.append(word)
            key_sum = sum(stats)
            stats = np.array(stats) / float(key_sum)
            array = np.cumsum(np.array(stats))
            self.one_word_statistic[one_word] = [new_words, array.tolist()]


    def generate_two_words_statistics(self):
        print "generating two words statistics"
        for two_words in self.two_words_statistic:
            new_words = []
            stats = []
            for word in self.two_words_statistic[two_words]:
                stats.append(self.two_words_statistic[two_words][word])
                new_words.append(word)
            key_sum = sum(stats)
            stats = np.array(stats) / float(key_sum)
            array = np.cumsum(np.array(stats))
            self.two_words_statistic[two_words] = [new_words, array.tolist()]


    def generate_statistics(self):
        self.generate_one_word_statistics()
        self.generate_two_words_statistics()


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
                stats = self.one_word_statistic['.']
            else:
                stats = self.one_word_statistic[self.text[-1]]
        else:
            stats = self.two_words_statistic[self.text[-2] + ' ' + self.text[-1]]

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
    assert len(sys.argv) == 2,  'Usage:  python {} directoryname'.format(sys.argv[0])
    directory = sys.argv[1]

    generator = TextGenerator()
    for author_dir in os.listdir(directory):
        print "analising ", author_dir
        for doc in os.listdir(directory + '/' + author_dir):
            file_name = directory + '/' + author_dir + '/' + doc
            generator.add_document(doc, open(file_name).read().decode('utf8'))
    generator.generate_statistics()

    text_length = 13000

    text = generator.generate_text(text_length)
    f = open('generated_text.txt', 'w')
    f.write(text.encode('utf8'))

    # generator.print_two_words_statistic()
    # generator.print_one_word_statistic()

if __name__ == '__main__':
    main()