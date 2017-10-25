from copy import deepcopy

class Queue:
    """
    Classe de fila.
    """
    def __init__(self, elements=None):
        if elements is not None and isinstance(elements, list):
            self._queue = elements
        else:
            self._queue = []

    def enqueue(self, element):
        """
        enqueue element
        """
        self._queue.append(element)

    def dequeue(self):
        """
        dequeue element
        """
        if self.size() == 0:
            return None
        __r = self._queue[0]
        del self._queue[0]
        return __r

    def peek(self):
        """
        peek next element
        """
        if self.size() == 0:
            return None
        return self._queue[0]

    def queue_list(self):
        """
        list elements
        """
        return deepcopy(self._queue)

    def remove_from_index(self, index):
        """
        remove element at index
        """
        if 0 <= index < self.size():
            del self._queue[index]

    def clear(self):
        """
        clear queue
        """
        self._queue = []

    def size(self):
        """
        get the queue size
        """
        return len(self._queue)

    def empty(self):
        """
        check if queue is empty
        """
        return self.size() == 0
