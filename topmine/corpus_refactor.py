from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import string


REMOVE_PUNCT_TABLE = str.maketrans(
            string.punctuation, ' ' * len(string.punctuation))


class Corpus(object):
    '''Memory Friendly Corpus Reader'''
    def __init__(self, files=None, documents=None):
        self.files = files
        self.documents = documents
        if files is not None and documents is not None:
            raise ValueError('Define corpus with files or documents but not both')
        if documents is not None:
            self.cached = True
        else:
            self.cached = False


    def __iter__(self):
        if not self.cached:
            for file in self.files:
                with open(file, 'r') as f:
                    yield f.read()
        else:
            for document in self.documents:
                yield document

    def __len__(self):
        if self.cached:
            return len(self.documents)
        else:
            return len(self.files)

    def transform(self, function, output_dir='', suffix='', overwrite=False):
        '''Transform a corpus with a function
        Args:
            function (callable): function with one parameter.
            output_dir (str): path to folder where the transformed files
                will be stored.
            suffix (str): will be appended to the filenames.
        Returns:
            Corpus: the transformed corpus
        '''
        if self.cached:
            return Corpus(documents=[function(x) for x in self])

        if output_dir == '' and suffix == '' and not overwrite:
            raise IOError('default output_dir and suffix parameters'
                    ' would overwrite files, use overwrite=True')
        transformed_files = []
        extension = '.txt'
        for file in self.files:
            with open(file, 'r') as f:
                text = function(f.read())
            name, old_extension = os.path.splitext(file)
            name = os.path.basename(name)
            transformed_file = os.path.join(
                        output_dir, name + suffix + extension)
            with open(transformed_file, 'w') as f:
                f.write(text)
            transformed_files.append(transformed_file)

        return Corpus(files=transformed_files)

    def cached(self):
        '''Return a new corpus with documents in memory'''
        if self.cached:
            return self
        return Corpus(documents=[x for x in self])

    def flushed(self, output_dir, suffix=''):
        '''Return a new corpus with documents in disk'''
        extension = '.txt'
        files = []
        for i, document in enumerate(self.documents):
            file = os.path.join(
                    output_dir, 'doc_' + str(i) + suffix + extension)
            with open(file, 'w') as f:
                f.write(document)
            files.append(file)
        return Corpus(files=files)

    def vocabulary(self, preprocessor):
        '''Extract the vocabulary from all documents'''
        n_tokens = 0
        vocabulary = set()
        for document in self:
            tokens = (preprocessor.preprocess(
                document.translate(REMOVE_PUNCT_TABLE))
                                  .split())
            n_tokens += len(tokens)
            vocabulary.update(tokens)
        return vocabulary, n_tokens

    @staticmethod
    def _vocabulary_map(vocabulary):
        '''Maps each element of the vocabulary to an integer
        also returns a list mapping integers to words
        '''
        vocabulary_map= {x: i for i, x in enumerate(vocabulary)}
        vocabulary_list = [''] * len(vocabulary_map)
        for x, i in vocabulary_map.items():
            vocabulary_list[i] = x
        return vocabulary_map, vocabulary_list

    def vocabulary_map(self, preprocessor):
        '''Maps each element of the vocabulary to an integer
        also returns a list mapping integers to words and a
        count of the total number of tokens in the corpus
        '''
        vocabulary, n_tokens = self.vocabulary(preprocessor)
        vocabulary_map, vocabulary_list = self._vocabulary_map(vocabulary)
        return vocabulary_map, vocabulary_list, n_tokens

