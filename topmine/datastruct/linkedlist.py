class LinkedList(object):
    def __init__(self, nodes):
        last_node = nodes.pop() # use last node to initialize linked list
        self.first_node = last_node
        self.last_node = last_node
        for node in reversed(nodes):
            self.push(node)
        nodes.append(last_node) # put back last node

    def push(self, node):
        '''Pushes the node <node> at the "front" of the ll
        '''
        node.next_node = self.first_node
        node.previous_node = None
        self.first_node.previous_node = node
        self.first_node = node

    def pop(self):
        '''Pops the last node out of the list'''
        old_last_node = self.last_node
        to_be_last = self.last_node.previous_node
        to_be_last.next_node = None
        old_last_node.previous_node = None

        # Set the last node to the "to_be_last"
        self.previous_node = to_be_last

        return old_last_node

    def remove(self, node):
        '''Removes and returns node, and connects the previous and next
        nicely
        '''
        next_node = node.next_node
        previous_node = node.previous_node

        previous_node.next_node = next_node
        next_node.previous_node = previous_node

        # Make it "free"
        node.next_node = node.previous_node = None

        return node

    def __str__(self):
        next_node = self.first_node
        s = ''
        while next_node:
            if next_node.next_node:
                s += str(next_node) + ' | '
            else:
                s += str(next_node)
            next_node = next_node.next_node

        return s

    def __iter__(self):
        return ListIterator(self.first_node)


class ListIterator(object):
    def __init__(self, node):
        self.current = node

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration()
        node, self.current = self.current, self.current.next_node
        return node
