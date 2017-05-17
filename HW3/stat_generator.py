import os
import sys
import unicodedata
import numpy as np

import pickle


PUNCTUATION_TRANSLATE_TABLE = {i:None for i in range(sys.maxunicode)
    if unicodedata.category(unichr(i)).startswith('P') and unichr(i) != '.'}

def normalize_text(text):
    text = text.lower().translate(PUNCTUATION_TRANSLATE_TABLE)
    text = text.replace(u'.', u' . ')
    return text

class Corpus(object):


    def __init__(self):
        self.two_words_statistic = dict()
        self.one_word_statistic = dict()


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


    def save_statistics(self):
        print 'saving one_word statistics'
        f1 = open('data1.pickle', 'wb')
        pickle.dump(self.one_word_statistic, f1)
        print 'saving two_words statistics'
        f2 = open('data2.pickle', 'wb')
        pickle.dump(self.two_words_statistic, f2)



    def print_words_num(self):
        print 'Number of words = ', self.words_num

def main():
    assert len(sys.argv) == 2,  'Usage:  python {} directoryname'.format(sys.argv[0])
    directory = sys.argv[1]

    corpus = Corpus()
    for author_dir in os.listdir(directory):
        print "analising ", author_dir
        for doc in os.listdir(directory + '/' + author_dir):
            file_name = directory + '/' + author_dir + '/' + doc
            corpus.add_document(doc, open(file_name).read().decode('utf8'))
    corpus.generate_statistics()

    # corpus.print_two_words_statistic()
    # corpus.print_one_word_statistic()

    # corpus.save_statistics()

if __name__ == '__main__':
    main()
