class Heap(object):
    def __init__(self, nodes=[]):
        self.heap = nodes
        self.heapify()

    def push_heap(self, node):
        '''Pushes a value onto the heap `A` while keeping the heap property
        intact.  The heap size increases by 1.'''
        self.heap.append(node)
        node.index = len(self.heap) - 1
        self.__siftup(len(self.heap) - 1)   # furthest left node
        return


    def pop_heap(self):
        '''Returns the max value from the heap `A` while keeping the heap
        property intact.  The heap size decreases by 1.'''
        n = len(self.heap) - 1
        self.__swap(0, n)
        max = self.heap.pop(n)
        self.__siftdown(0)
        return max


    # runs in log(n) time
    def replace_key(self, index, new_value):
        '''Replace the node key at index `index` in the max-heap `A`
        with `newval`. The heap size does not change.'''
        current_value = self.heap[index].key
        self.heap[index].key = new_value
        # increase key
        if new_value > current_value:
            self.__siftup(index)
        # decrease key
        elif new_value < current_value:
            self.__siftdown(index)
        return


    # runs in log(n) time
    def __siftup(self, index):
        '''Traverse up an otherwise max-heap `A` starting at node `node`
        (which is the only node that breaks the heap property) and restore
        the heap structure.'''
        parent = (index - 1)//2
        if self.heap[parent].key < self.heap[index].key:
            self.__swap(index, parent)
        # base case; we've reached the top of the heap
        if parent <= 0:
            return
        else:
            self.__siftup(parent)


    # runs in log(n) time
    def __siftdown(self, index):
        '''Traverse down a binary tree `A` starting at index `index` and
        turn it into a max-heap'''
        child = 2 * index + 1
        # base case, stop recursing when we hit the end of the heap
        if child > len(self.heap) - 1:
            return
        # check that second child exists; if so find max
        if ((child + 1 <= len(self.heap) - 1) and
                (self.heap[child+1].key > self.heap[child].key)):
            child += 1
        # preserves heap structure
        if self.heap[index].key < self.heap[child].key:
            self.__swap(index, child)
            self.__siftdown(child)
        else:
            return

    def heapify(self):
        '''Turns a list `A` into a max-ordered binary heap.'''
        n = len(self.heap) - 1
        if n == -1:
            return
        # start at last parent and go left one node at a time
        for index in range(n//2, -1, -1):
            self.__siftdown(index)
        return


    def __swap(self, i, j):
        # the pythonic swap
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.heap[i].index = i
        self.heap[j].index = j
        return


    def __len__(self):
        return len(self.heap)
