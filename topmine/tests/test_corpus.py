import os, shutil
import pytest

from .. import Corpus, RomanPreprocessor

@pytest.fixture(scope='session')
def documents():
    return [
        'Hi everyone, this is the first document!',
        'This is the second document: the third is next',
        'As expected, this is the third document',
        'Lets hope this is the last one',]

@pytest.fixture(scope='session')
def files(documents, tmpdir_factory):
    files = []
    directory = tmpdir_factory.mktemp('corpus')
    for i, document in enumerate(documents):
        filename = directory.join('doc_' + str(i) + '.txt')
        with open(str(filename), 'w') as f:
            f.write(document)
        files.append(str(filename))
    return files

@pytest.fixture(scope='session')
def vocabulary():
    return set([
        'hi', 'everyone', 'this', 'is', 'the', 'first', 'document',
        'second', 'third', 'next', 'as', 'expected', 'third',
        'lets', 'hope', 'last', 'one'])

@pytest.fixture(scope='session')
def preprocessor():
    return RomanPreprocessor()

def test_init_corpus_files(files, documents):
    corpus = Corpus(files=files)
    assert not corpus.cached
    assert len(corpus) == len(documents)
    for i, document in enumerate(corpus):
        assert document == documents[i]

def test_init_corpus_docs(documents):
    corpus = Corpus(documents=documents)
    assert corpus.cached
    assert len(corpus) == len(documents)
    for i, document in enumerate(corpus):
        assert document == documents[i]

def test_transform_corpus(files, tmpdir):
    corpus = Corpus(files=files)
    transformed_corpus = corpus.transform(
            lambda x: x.lower(), output_dir=str(tmpdir))
    for document, transformed_document in zip(corpus, transformed_corpus):
        assert transformed_document == document.lower()

def test_vocabulary(documents, preprocessor, vocabulary):
    corpus = Corpus(documents=documents)
    t_vocabulary, n_tokens = corpus.vocabulary(preprocessor)
    assert t_vocabulary == vocabulary
    assert n_tokens == 30

def test_vocabulary_map(documents, vocabulary):
    corpus = Corpus(documents=documents)
    vocabulary_map, vocabulary_list = corpus._vocabulary_map(vocabulary)
    assert set(vocabulary_map.keys()) == vocabulary
    for word, index in vocabulary_map.items():
        assert vocabulary_list[index] == word
