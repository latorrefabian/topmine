from topmine import datastruct as ds
from topmine import phrase_mining as pm
import pdb
import random
import math

document = range(10)
tokens = [pm.Token(string=str(x)) for x in document]
linkedlist = ds.LinkedList(tokens)
for i, node in enumerate(linkedlist):
    node.key = random.randint(-100, 100)
heap = ds.Heap(tokens)
for i, node in enumerate(heap.heap):
    if node.index != i:
        print('wrong index')
    else:
        print('-', end='')

_max = math.inf
while heap.heap:
    for i, node in enumerate(heap.heap):
        if node.index != i:
            print('wrong index')
        else:
            print('-', end='')
    new_max = heap.pop_heap()
    if new_max.key > _max:
        print('error found better max')
    else:
        _max = new_max.key

