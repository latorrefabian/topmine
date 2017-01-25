from topmine import corpus
import pdb
import os

mini_corpus = [
    'this is the first document in the corpus',
    'we are trying to check if the corpus is created',
    'finally another document in the corpus']


def test_create_corpus(tmpdir):
    '''Test if corpus is created correctly'''
    files = _files(tmpdir)
    corp = corpus.Corpus(files, type='text')
    assert len(corp) == 3
    for i, document in enumerate(corp):
        print(document)
        assert document == mini_corpus[i]


def test_transform_corpus(tmpdir):
    '''Test if corpus is transformed correctly'''
    corp = corpus.Corpus(_files(tmpdir), type='text')
    corp = corp.transform(_append, output_dir=str(tmpdir))
    transformed = [_append(x) for x in mini_corpus]
    for i, document in enumerate(corp):
        assert document == transformed[i]


def test_tranform_corpus_bytes(tmpdir):
    '''Test if corpus is transformed correctly using
       a bytes output_type
    '''
    corp = corpus.Corpus(_files(tmpdir), type='text')
    corp = corp.transform(_tokenize, output_dir=str(tmpdir),
                          output_type='bytes')
    transformed = [_tokenize(x) for x in mini_corpus]
    for i, document in enumerate(corp):
        assert document == transformed[i]


def _files(tmpdir):
    '''Generates the files from the mini_corpus'''
    files = []
    for i, document in enumerate(mini_corpus):
        file = tmpdir.join('doc_' + str(i) + '.txt')
        with file.open('w') as f:
            f.write(document)
        files.append(str(file))
    return files

def _append(text):
    '''Appends something to a string'''
    return text + ' x'

def _tokenize(text):
    '''Splits on whitespace'''
    return text.split(' ')
