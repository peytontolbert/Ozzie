import heapq

class TaskPrioritizer:
    def __init__(self):
        self.priority_queue = []

    def add_task(self, priority, task, *args, **kwargs):
        heapq.heappush(self.priority_queue, (priority, task, args, kwargs))

    def get_next_task(self):
        if not self.is_empty():
            _, task, args, kwargs = heapq.heappop(self.priority_queue)
            return task, args, kwargs
        return None

    def is_empty(self):
        return len(self.priority_queue) == 0

    def size(self):
        return len(self.priority_queue)

    def clear(self):
        self.priority_queue.clear()