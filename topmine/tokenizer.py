from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import tempfile
import string
import math
import re
import unicodedata

import pdb
from collections import Counter
from itertools import chain
from heapq import heappush, heappop, heapify

NORMALIZE_PUNCT_TABLE = str.maketrans(
        string.punctuation, '.' * len(string.punctuation))

REMOVE_PUNCT_TABLE = str.maketrans(
            string.punctuation, ' ' * len(string.punctuation))


def to_ascii(s):
    '''Adapted from sklearn.feature_extraction.text'''
    nkfd_form = unicodedata.normalize('NFKD', s)
    only_ascii = nkfd_form.encode('ASCII', 'ignore').decode('ASCII')
    return only_ascii


def strip_tags(s):
    '''Taken from sklearn.feature_extraction.text'''
    return re.compile(r'<([^>]+)>', flags=re.UNICODE).sub('', s)


class RomanPreprocessor(object):
    '''Taken from sklearn.feature_extraction.text'''
    def preprocess(self, unicode_text):
        '''Preprocess strings'''
        return to_ascii(strip_tags(unicode_text.lower()))

    def __repr__(self):
        return 'RomanPreprocessor()'


DEFAULT_PREPROCESSOR = RomanPreprocessor()


class TopmineTokenizer(object):
    def __init__(self, preprocessor=DEFAULT_PREPROCESSOR,
                 threshold=1, min_support=1):
        self.preprocessor = preprocessor
        self.counter = None
        self.threshold = threshold
        self.min_support = min_support
        self.vocabulary_map = None
        self.vocabulary = None
        self.n_tokens = None

    def fit(self, corpus):
        '''Fits the vocabulary and vocabulary_map to a given corpus.
        Calculates the counter of phrases given the min_support
        '''
        self.vocabulary_map, self.vocabulary, self.n_tokens = (
                corpus.vocabulary_map(self.preprocessor))
        sentences = self.corpus_to_list(corpus)
        self.counter = phrase_frequency(sentences, self.min_support)

    def transform_document(self, document):
        '''Splits a document into sentences, transform the sentences
        and return the results in a list
        '''
        return [x for sentence in self.doc_to_list(document)
                for x in self.transform_sentence(sentence)]


    def transform_sentence(self, sentence):
        '''Given a sentence, encoded as a list of integers using
        the vocabulary_map, return it as a sequence of
        significant phrases.
        '''
        phrases = [(x,) for x in sentence]
        phrase_start = [x for x in range(len(phrases))]
        phrase_end = [x for x in range(len(phrases))]

        costs = [(self.cost(phrases[i], phrases[i + 1]), i, i + 1, 2)
                for i in range(len(phrases) - 1)]
        heapify(costs)

        while True and len(costs) > 0:
            # a = phrase a, b = phrase b
            # i_a = phrase a index, i_b = phrase b index
            # phrase_start[x] = x means that a phrase starts at that position
            cost, i_a, i_b, length = heappop(costs)

            if cost > -self.threshold:
                break
            if phrase_start[i_a] != i_a:
                continue
            if phrase_start[i_b] != i_b:
                continue
            if length != len(phrases[i_a] + phrases[i_b]):
                continue

            phrase_start[i_b] = i_a
            phrase_end[i_a] = phrase_end[i_b]
            merged_phrase = phrases[i_a] + phrases[i_b]
            phrases[i_a] = merged_phrase
            phrases[i_b] = None

            if i_a > 0:
                prev_phrase_start = phrase_start[i_a - 1]
                prev_phrase = phrases[prev_phrase_start]
                heappush(costs, (
                    self.cost(prev_phrase, merged_phrase),
                    prev_phrase_start, i_a,
                    len(prev_phrase) + len(merged_phrase)))

            if phrase_end[i_b] < len(phrases) - 1:
                next_phrase_start = phrase_end[i_b] + 1
                next_phrase = phrases[next_phrase_start]
                heappush(costs, (
                    self.cost(merged_phrase, next_phrase),
                    i_a, next_phrase_start,
                    len(merged_phrase) + len(next_phrase)))

        encoded_phrases = [x for x in phrases if x is not None]
        return self.decode_phrases(encoded_phrases)

    def corpus_to_list(self, corpus):
        '''Transforms a corpus into a list of lists, one list
        per sentence in the corpus, encoded using the vocabulary_map
        '''
        sentences = []
        for document in corpus:
            for sentence in self.doc_to_list(document):
                sentences.append(sentence)
        return sentences

    def doc_to_list(self, document):
        '''Splits a document on punctuation and returns a list
        of indices using the vocabulary_map, one list per sentence
        '''
        document = self.preprocessor.preprocess(
                       document.translate(NORMALIZE_PUNCT_TABLE))
        sentences = document.split('.')
        return [[self.vocabulary_map[x] for x in y.split()] for y in sentences]

    def decode_phrases(self, encoded_phrases):
        '''Takes a list of tuples of indices, and translate each tuple
        to a phrase, using the word given by such index in the vocabulary
        '''
        return [' '.join([self.vocabulary[i] for i in phrase])
                for phrase in encoded_phrases]

    def cost(self, a, b):
        '''Calculates the cost of merging two phrases. Cost is
        defined as the negative of significance. This way we can
        use the python min-heap implementation
        '''
        # flatten the tuples a, b
        ab = self.counter[tuple([x for x in chain(*(a, b))])]
        if ab > 0:
            return (-(ab - (self.counter[a] * self.counter[b]) / self.n_tokens )
                    / math.sqrt(ab))
        else:
            return math.inf


def phrase_frequency(sentences, min_support):
    '''Calculates counter with frequent phrases
    Args:
        sentences (list): each sentence is a list of words
    '''
    indices = [range(len(sentence)) for sentence in sentences]
    counter = Counter(((x,) for x in chain(*sentences)))
    n = 1
    while len(sentences) > 0:
        for i, sentence in enumerate_backwards(sentences):
            indices[i] = [
                    j for j in indices[i]
                    if counter[tuple(sentence[j: j+n])] >= min_support]
            if len(indices[i]) == 0:
                indices.pop(i)
                sentences.pop(i)
                continue
            for j in indices[i]:
                if j + 1 in indices[i]:
                    counter.update([tuple(sentence[i: i+n+1])])
            indices[i].pop()
        n = n + 1
    return counter


def enumerate_backwards(array):
    '''Generate indices and elements of an array from last to first
    this allows to pop elements and still traverse each index in the list
    '''
    for i, x in zip(range(len(array)-1, -1, -1), reversed(array)):
        yield i, x

