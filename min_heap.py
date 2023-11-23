class Pair:

    def __init__(self, key: int, value: str) -> None:
        self.key = key
        self.value = value

    def __str__(self) -> str:
        return f"Key: {self.key}, Value: {self.value}"


# Function to return the position of parent for the node currently at pos
def _parent(pos: int) -> int:
    return pos // 2


# Function to return the position of the left child for the node currently at pos
def _left_child(pos: int) -> int:
    return 2 * pos


# Function to return the position of the right child for the node currently at pos
def _right_child(pos: int) -> int:
    return (2 * pos) + 1


class MinHeap:

    def __init__(self, maxsize: int) -> None:
        self.maxsize = maxsize
        self.size = 0
        self.heap = [None] * (self.maxsize + 1)

    # Function to swap two nodes of the heap
    def swap(self, fpos: int, spos: int) -> None:
        self.heap[fpos], self.heap[spos] = self.heap[spos], self.heap[fpos]

    # Function to heapify the node at pos
    def heapify(self, pos: int) -> int:

        # If the node is a non-leaf node and greater than any of its child 
        if not self.is_leaf(pos) and self.heap[pos]:
            if ((self.heap[_left_child(pos)] and self.heap[pos].key > self.heap[_left_child(pos)].key)
                    or (self.heap[_right_child(pos)].key and self.heap[pos].key > self.heap[_right_child(pos)].key)):

                # Swap with the left child and heapify the left child 
                if (self.heap[_left_child(pos)]
                        and self.heap[_right_child(pos)]
                        and self.heap[_left_child(pos)].key < self.heap[_right_child(pos)].key):
                    self.swap(pos, _left_child(pos))
                    return self.heapify(_left_child(pos))

                # Swap with the right child and heapify the right child 
                else:
                    self.swap(pos, _right_child(pos))
                    return self.heapify(_right_child(pos))
        return pos

    # Function that returns true if the passed node is a leaf node 
    def is_leaf(self, pos: int) -> bool:
        return pos * 2 > self.size

    # Function to insert a node into the heap
    def insert(self, element: Pair) -> int:
        if self.size >= self.maxsize:
            raise ValueError("[ERR] Heap is full.")
        self.size += 1
        self.heap[self.size] = element

        current = self.size

        while (self.heap[current] and self.heap[_parent(current)]
               and (self.heap[current].key < self.heap[_parent(current)].key)):
            self.swap(current, _parent(current))
            current = _parent(current)
        return current

    # Function to print the contents of the heap
    def print(self) -> None:
        for i in range(1, (self.size // 2) + 1):
            print(" PARENT : " + str(self.heap[i]) + " LEFT CHILD : " +
                  str(self.heap[2 * i]) + " RIGHT CHILD : " +
                  str(self.heap[2 * i + 1]))

    # Function to build the min heap using the heapify function
    def to_min_heap(self) -> None:
        for pos in range(self.size // 2, 0, -1):
            self.heapify(pos)

    # Function to remove and return the minimum element from the heap
    def extract(self) -> Pair:
        if not self.heap[0]:
            raise ValueError("[ERR] Access on an empty heap.")
        popped = self.heap[0]
        self.heap[0] = self.heap[self.size]
        self.size -= 1
        self.heapify(0)
        return popped

    def increase_key(self, pos: int, key: int) -> int:
        if pos <= self.size:
            self.heap[pos].key = key
            return self.heapify(pos)
        else:
            raise ValueError("[ERR] Access on heap with an invalid position.")
