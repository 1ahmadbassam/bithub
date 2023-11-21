class Pair:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"Key: {self.key}, Value: {self.value}"


# Function to return the position of 
# parent for the node currently 
# at pos
def _parent(pos):
    return pos // 2


# Function to return the position of 
# the left child for the node currently 
# at pos 
def _left_child(pos):
    return 2 * pos


# Function to return the position of
# the right child for the node currently
# at pos 
def _right_child(pos):
    return (2 * pos) + 1


class MinHeap:

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.heap = [None] * (self.maxsize + 1)
        self.front = 0

    # Function to swap two nodes of the heap
    def swap(self, fpos, spos):
        self.heap[fpos], self.heap[spos] = self.heap[spos], self.heap[fpos]

    # Function to heapify the node at pos
    def heapify(self, pos):

        # If the node is a non-leaf node and greater 
        # than any of its child 
        if not self.is_leaf(pos) and self.heap[pos]:
            if ((self.heap[_left_child(pos)] and self.heap[pos].key > self.heap[_left_child(pos)].key)
                    or (self.heap[_right_child(pos)].key and self.heap[pos].key > self.heap[_right_child(pos)].key)):

                # Swap with the left child and heapify 
                # the left child 
                if self.heap[_left_child(pos)].key < self.heap[_right_child(pos)].key:
                    self.swap(pos, _left_child(pos))
                    self.heapify(_left_child(pos))

                # Swap with the right child and heapify
                # the right child 
                else:
                    self.swap(pos, _right_child(pos))
                    self.heapify(_right_child(pos))

    # Function that returns true if the passed 
    # node is a leaf node 
    def is_leaf(self, pos):
        return pos * 2 > self.size

    # Function to insert a node into the heap
    def insert(self, element):
        if self.size >= self.maxsize:
            return
        self.size += 1
        self.heap[self.size] = element

        current = self.size

        while (self.heap[current] and self.heap[_parent(current)]
               and (self.heap[current].key < self.heap[_parent(current)].key)):
            self.swap(current, _parent(current))
            current = _parent(current)

    # Function to print the contents of the heap
    def print(self):
        for i in range(1, (self.size // 2) + 1):
            print(" PARENT : " + str(self.heap[i]) + " LEFT CHILD : " +
                  str(self.heap[2 * i]) + " RIGHT CHILD : " +
                  str(self.heap[2 * i + 1]))

    # Function to build the min heap using
    # the heapify function
    def to_min_heap(self):

        for pos in range(self.size // 2, 0, -1):
            self.heapify(pos)

            # Function to remove and return the minimum

    # element from the heap
    def extract(self):
        popped = self.heap[self.front]
        self.heap[self.front] = self.heap[self.size]
        self.size -= 1
        self.heapify(self.front)
        return popped
