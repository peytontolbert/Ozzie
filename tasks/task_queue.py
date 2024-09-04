from collections import deque

class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task, *args, **kwargs):
        self.queue.append((task, args, kwargs))

    def get_next_task(self):
        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue.clear()