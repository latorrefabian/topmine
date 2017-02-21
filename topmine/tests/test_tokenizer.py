import pytest
import math

from collections import Counter
from .. import TopmineTokenizer, RomanPreprocessor, Corpus
from .. import enumerate_backwards

@pytest.fixture
def corpus():
    return Corpus(documents=[
        'Hi everyone, this is the first document!',
        'This is the second document: the third is next',
        'As expected, this is the third document',
        'Lets hope this is the last one',])

@pytest.fixture
def simple_corpus():
    return Corpus(documents=[
        'machine learning. support vector machines',
        'This is irrelevant: this is Support'])

@pytest.fixture
def tokenizer():
    tokenizer = TopmineTokenizer()
    tokenizer.counter = Counter({
        (0,): 4, (1,): 3, (0, 1,): 3, (2,): 5,
        (3,): 7, (4,): 4, (2, 3,): 4, (2, 3, 4,): 4,
        (5,): 8, (6,): 12, (7,): 3,
        })
    tokenizer.vocabulary_map = {
        'machine': 0, 'learning': 1, 'support': 2, 'vector': 3,
        'machines': 4, 'this': 5, 'is': 6, 'irrelevant': 7,}
    tokenizer.vocabulary = [
        'machine', 'learning', 'support', 'vector',
        'machines', 'this', 'is', 'irrelevant',]
    tokenizer.n_tokens = 38
    preprocessor = object()
    return tokenizer


def test_init_tokenizer():
    tokenizer = TopmineTokenizer()
    assert hasattr(tokenizer, 'threshold')
    assert hasattr(tokenizer, 'min_support')

def test_fit(corpus):
    tokenizer = TopmineTokenizer()
    tokenizer.fit(corpus)
    assert isinstance(tokenizer.counter, Counter)

def test_transform_document(tokenizer):
    phrases = tokenizer.transform_document(
            'machine. learning support vector Machines: this is iRrelevant')
    assert isinstance(phrases, list)
    assert phrases == ['machine', 'learning', 'support vector machines',
            'this', 'is', 'irrelevant']

def test_transform_sentence(tokenizer):
    phrases = tokenizer.transform_sentence(
            [0, 1, 2, 3, 4, 5, 6, 7])
    assert isinstance(phrases, list)
    assert phrases == ['machine learning', 'support vector machines',
            'this', 'is', 'irrelevant']

def test_corpus_to_list(tokenizer, simple_corpus):
    sentences = tokenizer.corpus_to_list(simple_corpus)
    assert sentences == [[0, 1], [2, 3, 4], [5, 6, 7], [5, 6, 2]]

def test_doc_to_list(tokenizer):
    document = 'machine learning: support vector machines. This is irrelevant'
    assert tokenizer.doc_to_list(document) == [
            [0, 1], [2, 3, 4], [5, 6, 7]]

def test_decode_phrases(tokenizer):
    encoded_phrases = [(0, 1,), (2, 3, 4), (5,), (6,), (7,)]
    assert tokenizer.decode_phrases(encoded_phrases) == (
            ['machine learning', 'support vector machines',
             'this', 'is', 'irrelevant'])

def test_cost(tokenizer):
    cost = tokenizer.cost((2, 3), (4,))
    assert isinstance(cost, float)
    assert cost == -(4 - (4 * 4) / 38) / math.sqrt(4)
    cost = tokenizer.cost((2, 3), (11,))
    assert cost == math.inf


def test_phrase_frequency():
    # TO DO
    pass

def test_enumerate_backwards():
    items = ['a', 'b', 'c']
    for i, item in enumerate_backwards(items):
        if item == 'c':
            assert i == 2
        elif item == 'b':
            assert i == 1
        elif item == 'a':
            assert i == 0
