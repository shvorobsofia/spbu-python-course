import threading
import queue

class ThreadPool:
    def __init__(self, num_threads: int):
        self.num_threads = num_threads
        self.tasks = queue.Queue()
        self.threads = []
        self.shutdown_flag = threading.Event()

        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def _worker(self):
        while not self.shutdown_flag.is_set():
            try:
                task, callback = self.tasks.get(timeout=1)  # Таймаут для проверки shutdown_flag
                result = task()
                if callback:
                    callback(result)
                self.tasks.task_done()
            except queue.Empty:
                continue

    def enqueue(self, task, callback=None):
        if not self.shutdown_flag.is_set():
            self.tasks.put((task, callback))

    def dispose(self):
        self.shutdown_flag.set()
        for thread in self.threads:
            thread.join()