def heapify(A):
    '''Turns a list `A` into a max-ordered binary heap.'''
    n = len(A) - 1
    # start at last parent and go left one node at a time
    for index in range(n/2, -1, -1):
        __siftdown(A, index)
    return


def __swap(A, i, j):
    # the pythonic swap
    A[i], A[j] = A[j], A[i]
    A[i].position = i
    A[j].position = j
    return


def push_heap(A, node):
    '''Pushes a value onto the heap `A` while keeping the heap property
    intact.  The heap size increases by 1.'''
    A.append(node)
    node.position = len(A) - 1
    __siftup(A, len(A) - 1)   # furthest left node
    return


def pop_heap(A):
    '''Returns the max value from the heap `A` while keeping the heap
    property intact.  The heap size decreases by 1.'''
    n = len(A) - 1
    __swap(A, 0, n)
    max = A.pop(n)
    __siftdown(A, 0)
    return max

# runs in log(n) time
def replace_key(A, index, new_value):
    '''Replace the node key at index `index` in the max-heap `A`
    with `newval`. The heap size does not change.'''
    current_value = A[index].key
    A[index].key = new_value
    # increase key
    if new_value > current_value:
        __siftup(A, index)
    # decrease key
    elif new_value < current_value:
        __siftdown(A, index)
    return

# runs in log(n) time
def __siftdown(A, index):
    '''Traverse down a binary tree `A` starting at index `index` and
    turn it into a max-heap'''
    child = 2 * index + 1
    # base case, stop recursing when we hit the end of the heap
    if child > len(A) - 1:
        return
    # check that second child exists; if so find max
    if (child + 1 <= len(A) - 1) and (A[child+1].key > A[child].key):
        child += 1
    # preserves heap structure
    if A[index].key < A[child].key:
        __swap(A, index, child)
        __siftdown(A, child)
    else:
        return

# runs in log(n) time
def __siftup(A, index):
    '''Traverse up an otherwise max-heap `A` starting at node `node`
    (which is the only node that breaks the heap property) and restore
    the heap structure.'''
    parent = (index - 1)/2
    if A[parent].key < A[node].key:
        __swap(A, index, parent)
    # base case; we've reached the top of the heap
    if parent <= 0:
        return
    else:
        __siftup(A, parent)

class Node(object):
    def __init__(self, key):
        self.key = key
        self.position = None

class LinkedHeap(object):
    def __init__(self):
        pass

