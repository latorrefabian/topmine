class Node(object):
    def __init__(self, key=0, next_node=None, previous_node=None, **kwargs):
        self.key = key
        self.next_node = next_node
        self.previous_node = previous_node
        for name, value in kwargs.items():
            setattr(self, name, value)


