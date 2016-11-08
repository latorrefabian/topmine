import pdb
from collections import Counter
from itertools import chain
from copy import deepcopy
from heapq import heappush, heappop
import math

def phrase_frequency(corpus, min_support):
    D = deepcopy(corpus)
    indices = [range(len(document)) for document in D]
    counter = Counter(chain(*D))
    n = 2
    while D:
        for d, document in zip(range(len(D)-1, -1, -1), reversed(D)):
            indices[d] = [
                i for i in indices[d]
                if counter[' '.join(document[i: i+n-1])] > min_support
                ]
            if not indices[d]:
                indices.pop(d)
                D.pop(d)
                continue
            else:
                for i in indices[d]:
                    if i + 1 in indices[d]:
                        phrase = ' '.join(document[i: i+n])
                        counter.update([phrase])
            indices[d].pop()
        n = n + 1
    return counter


def _significance(a, b, ab, l):
    return (ab - (a * b) / l) / math.sqrt(ab)


def phrase_merge(document, counter, threshold):
    l = len(document)
    colloc = [(a, b) for a, b in zip(document[:-1], document[1:])]
    score_position = [(_score(x, counter, l), i) for i, x in enumerate(colloc)]
    while True:
        max_score, index = max(score_position)
        if max_score < threshold:
            break
        colloc = _merge(colloc, i)
        score_position[i-1] = (i-1, _score(colloc[i-1], counter, l))
        if i < len(score_position) - 1:
            score_position[i] = (i, _score(colloc[i], counter, l))
            score_position[i+1:] = score_position[i+2:]
        else:
            score_position.pop()
    last = colloc.pop()
    return [a for a, b in colloc] + list(last)


def _score(colloc, counter, l):
    return _significance(counter[colloc[0]], counter[colloc[1]],
                         counter[' '.join(colloc)], l)

def _merge(chain, i):
    new = ' '.join(chain[i])
    chain[i-1] = (chain[i-1][0], new)
    if i < len(chain) - 1:
        chain[i] = (new, chain[i+1][1])
        chain[i+1:] = chain[i+2:]
    else:
        chain.pop()
    return chain


if __name__ == '__main__':
    corpus = [x.split(' ') for x in
        ['hola soy danny',
         'hola soy edson',
         'hola soy johnson',
         'hola soy ronson',
         'hola soy jason',
         'hola soy randy'
        ]]
    counter = phrase_frequency(corpus, min_support=0)
    print(counter)
    print(phrase_merge(corpus[0], counter, 1))
