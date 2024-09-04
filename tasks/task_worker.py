import threading
import time

class TaskWorker(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue
        self.running = True

    def run(self):
        while self.running:
            if not self.task_queue.is_empty():
                task, args, kwargs = self.task_queue.get_next_task()
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    print(f"Error executing task: {e}")
            else:
                time.sleep(0.1)  # Sleep briefly to avoid busy-waiting

    def stop(self):
        self.running = False