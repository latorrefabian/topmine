import os
import pdb
import tempfile
from collections import Counter
import pickle


class Corpus(object):
    '''Memory Friendly Corpus Reader'''

    def __init__(self, name, files, type):
        if type != 'text' and type != 'bytes':
            raise ValueError('type not recognized')
        self.name = name
        self.files = files
        self.type = type
        if self.type == 'text':
            self.read_mode = 'r'
            self._read = lambda f: f.read()
        elif self.type == 'bytes':
            self.read_mode = 'rb'
            self._read = lambda f: pickle.load(f)

    def __iter__(self):
        for file in self.files:
            with open(file, self.read_mode) as f:
                yield self._read(f)

    def __len__(self):
        return len(self.files)

    def pop(self, k):
        self.files.pop(k)

    def transform(self, name, function, output_dir=None, suffix='_t', output_type='text', split=False):
        '''Transform a corpus with a function
        Args:
            function (callable): function with string as parameter.
            output_dir (str): path to folder where the transformed files
                will be stored.
            suffix (str): will be appended to the filenames.
            output_type (str): one of 'text' or 'bytes'.
            split (bool): If the function returns a list and split is True, each element in the list
                will be written to disk to a different file. Defaults to False.

        Returns:
            Corpus: the transformed corpus
        '''
        if output_type == 'text':
            extension = '.txt'
            write_mode = 'w'
            def _write(obj, file):
                file.write(obj)
        elif output_type == 'bytes':
            extension = '.pkl'
            write_mode = 'wb'
            def _write(obj, file):
                pickle.dump(obj, file)
        else:
            raise ValueError('output_type not recognized')

        transformed_files = []

        for file in self.files:
            with open(file, self.read_mode) as f:
                transformed_obj = function(self._read(f))
            if not isinstance(transformed_obj, list) or not split:
                transformed_obj = [transformed_obj]
            name, old_extension = os.path.splitext(file)
            if output_dir:
                name = os.path.basename(name)
            for i, obj in enumerate(transformed_obj):
                transformed_file = os.path.join(
                        output_dir, name + suffix + str(i) + extension)
                with open(transformed_file, write_mode) as tf:
                    _write(obj, tf)
                transformed_files.append(transformed_file)

        return Corpus(name=name, files=transformed_files, type=output_type)


def phrase_frequency(corpus, min_support):
    '''Calculates counter with frequent phrases
    Args:
        corpus (Corpus): preprocessed corpus, that is, it is assumed that
            tokens are whitespace separated.
    '''
    temp_dir = tempfile.TemporaryDirectory()
    corpus = corpus.transform(lambda x: x.split(' '), output_dir=temp_dir,
            output_type='bytes')
    indices = [range(len(document)) for document in corpus]
    counter = Counter(chain.from_iterable(corpus))
    n = 2
    while len(corpus) > 0:
        # traverse backwards
        # this allows to pop elements and still traverse
        # each index in the list
        for d, document in zip(range(len(corpus)-1, -1, -1), reversed(corpus)):
            indices[d] = [i for i in indices[d]
                          if counter[' '.join(document[i: i+n-1])] > min_support]
            if not indices[d]:
                indices.pop(d)
                corpus.pop(d)
                continue
            else:
                for i in indices[d]:
                    if i + 1 in indices[d]:
                        phrase = ' '.join(document[i: i+n])
                        counter.update([phrase])
            indices[d].pop()
        n = n + 1
    return counter
