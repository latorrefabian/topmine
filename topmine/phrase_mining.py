import pdb
from collections import Counter
from itertools import chain
import copy
import math
from . import datastruct


def phrase_frequency(corpus, min_support):
    D = copy.copy(corpus)
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


class Token(datastruct.Node):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def merge(self):
        '''
        merges one node with the next and pops such node.
        returns the popped node
        '''
        if self.next_node:
            pop_node, self.next_node = (
                self.next_node, self.next_node.next_node)
            self.string += ' ' + pop_node.string
        else:
            raise IndexError('impossible to merge the last node')
        return pop_node

    def calculate_key(self, counter, l):
        if self.next_node:
            return _significance(self.string, self.next_node.string, counter, l)
        else:
            return -math.inf

    def __str__(self):
        return self.string


def recalculate_keys(linkedlist, counter, l):
    node = linkedlist.first_node
    while node:
        node.key = node.calculate_key(counter, l)
        node = node.next_node
    return


def segment_document(document, threshold, counter, l):
    tokens = [Token(string=x) for x in document]
    linkedlist = datastruct.LinkedList(nodes=tokens)
    recalculate_keys(linkedlist, counter, l)
    heap = datastruct.Heap(nodes=tokens)
    while segment_once(heap, threshold, counter, l):
        pass
    return [x.string for x in linkedlist]


def segment_once(heap, threshold, counter, l):
    max_node = heap.pop_heap()
    if max_node.key >= threshold:
        merged_node = max_node.merge()
        max_node.key = max_node.calculate_key(counter, l)
        heap.replace_key(index=merged_node.index, new_value=-math.inf)
        previous_node = max_node.previous_node
        if previous_node:
            heap.replace_key(
                    index=previous_node.index,
                    new_value=previous_node.calculate_key(counter, l))
        heap.push_heap(max_node)
        return True
    else:
        return False

def topmine_tokenizer(corpus, threshold, min_support):
    '''
    corpus is a list of pre-tokenized strings
    '''
    l = sum([len(x) for x in corpus])
    counter = phrase_frequency(corpus, min_support)
    def tokenize(document):
        return segment_document(document, threshold, counter, l)
    return tokenize, [key for key in counter.keys()]


def _significance(a, b, counter, l):
    ab = counter[' '.join([a, b])]
    if ab > 0:
        return (ab - (counter[a] * counter[b]) / l) / math.sqrt(ab)
    else:
        return -math.inf
