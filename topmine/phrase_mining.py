import pdb
from collections import Counter
from itertools import chain
from copy import deepcopy

def phrase_mine(corpus, min_support):
    D = deepcopy(corpus)
    indices = [range(len(document)) for document in D]
    counter = Counter(chain(*D))
    n = 2
    while D:
        for i, document in enumerate(D):
            indices[i] = [
                x for x in indices[i]
                if counter(' '.join(document[i:i+n-1])) > min_support
            ]
            indices[i].pop()


if __name__ == '__main__':
    corpus = [x.split(' ') for x in
        ['hola soy danny',
        'el colmo el presidente de venezuela',
        'fuerza mi atletico bucaramanga',
        'teoria de la relatividad propuesta por einstein',
        'teoria de la gravedad propuesta por newton']]
    pdb.set_trace()
    phrase_mine(corpus, min_support=0)
